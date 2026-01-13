"""
Detection Model wrapper for YOLO-based object detection.
"""

import os
import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Tuple, Optional
from models.id_card_model import BoundingBox, DetectionResult


class DetectionModel:
    """Wrapper for YOLO detection models."""
    
    def __init__(self, model_path: str):
        """
        Initialize detection model.
        
        Args:
            model_path: Path to YOLO model weights
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        self.model = YOLO(model_path)
        self.model_path = model_path
    
    def detect(
        self, 
        image: np.ndarray,
        conf_threshold: float = 0.25,
        annotate: bool = False
    ) -> DetectionResult:
        """
        Perform object detection on image.
        
        Args:
            image: Input image (BGR format)
            conf_threshold: Confidence threshold for detections
            annotate: Whether to create annotated image
            
        Returns:
            DetectionResult with bounding boxes and optional annotated image
        """
        results = self.model(image, conf=conf_threshold)
        bounding_boxes = []
        annotated_image = image.copy() if annotate else None
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0].item())
                class_name = result.names[class_id]
                confidence = float(box.conf[0].item())
                
                bbox = BoundingBox(
                    x1=x1, y1=y1, x2=x2, y2=y2,
                    class_name=class_name,
                    confidence=confidence
                )
                bounding_boxes.append(bbox)
                
                # Annotate image if requested
                if annotate:
                    # Draw rectangle
                    cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # Add label
                    label = f"{class_name}: {confidence:.2f}"
                    label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                    cv2.rectangle(
                        annotated_image, 
                        (x1, y1 - label_size[1] - 10), 
                        (x1 + label_size[0], y1), 
                        (0, 255, 0), 
                        -1
                    )
                    cv2.putText(
                        annotated_image, 
                        label, 
                        (x1, y1 - 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, 
                        (0, 0, 0), 
                        2
                    )
        
        return DetectionResult(
            bounding_boxes=bounding_boxes,
            annotated_image=annotated_image
        )
    
    def detect_first(
        self, 
        image: np.ndarray,
        conf_threshold: float = 0.25
    ) -> Optional[BoundingBox]:
        """
        Detect and return only the first (highest confidence) detection.
        
        Args:
            image: Input image
            conf_threshold: Confidence threshold
            
        Returns:
            First bounding box or None
        """
        detection_result = self.detect(image, conf_threshold, annotate=False)
        
        if detection_result.bounding_boxes:
            # Sort by confidence and return highest
            sorted_boxes = sorted(
                detection_result.bounding_boxes, 
                key=lambda x: x.confidence, 
                reverse=True
            )
            return sorted_boxes[0]
        
        return None


class IDCardDetector(DetectionModel):
    """Specialized detector for ID cards."""
    
    def __init__(self, base_dir: str = None):
        """Initialize ID card detector."""
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        model_path = os.path.join(base_dir, 'weights', 'detect_id_card.pt')
        super().__init__(model_path)


class FieldDetector(DetectionModel):
    """Specialized detector for ID card fields."""
    
    def __init__(self, base_dir: str = None):
        """Initialize field detector."""
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        model_path = os.path.join(base_dir, 'weights', 'detect_odjects.pt')
        super().__init__(model_path)


class DigitDetector(DetectionModel):
    """Specialized detector for National ID digits."""
    
    def __init__(self, base_dir: str = None):
        """Initialize digit detector."""
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        model_path = os.path.join(base_dir, 'weights', 'detect_id.pt')
        super().__init__(model_path)
    
    def detect_digits(self, image: np.ndarray) -> str:
        """
        Detect and extract digits from National ID.
        
        Args:
            image: Cropped National ID region
            
        Returns:
            Detected ID number as string
        """
        detection_result = self.detect(image, annotate=False)
        
        # Sort detections by x-coordinate (left to right)
        detected_info = [
            (int(bbox.class_name) if bbox.class_name.isdigit() else bbox.class_name, bbox.x1)
            for bbox in detection_result.bounding_boxes
        ]
        detected_info.sort(key=lambda x: x[1])
        
        # Concatenate digits
        id_number = ''.join([str(cls) for cls, _ in detected_info])
        
        return id_number
