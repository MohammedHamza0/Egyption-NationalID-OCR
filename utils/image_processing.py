"""
Image processing utilities.
"""

import cv2
import numpy as np
from typing import List, Tuple
from models.id_card_model import BoundingBox


def crop_image(image: np.ndarray, bbox: BoundingBox) -> np.ndarray:
    """
    Crop image using bounding box.
    
    Args:
        image: Input image
        bbox: Bounding box
        
    Returns:
        Cropped image
    """
    return image[bbox.y1:bbox.y2, bbox.x1:bbox.x2]


def annotate_image(
    image: np.ndarray, 
    bboxes: List[BoundingBox],
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2,
    show_labels: bool = True
) -> np.ndarray:
    """
    Annotate image with bounding boxes and labels.
    
    Args:
        image: Input image
        bboxes: List of bounding boxes
        color: Color for boxes (BGR format)
        thickness: Line thickness
        show_labels: Whether to show labels
        
    Returns:
        Annotated image
    """
    annotated = image.copy()
    
    for bbox in bboxes:
        # Draw rectangle
        cv2.rectangle(
            annotated, 
            (bbox.x1, bbox.y1), 
            (bbox.x2, bbox.y2), 
            color, 
            thickness
        )
        
        # Add label if requested
        if show_labels and bbox.class_name:
            label = f"{bbox.class_name}"
            if bbox.confidence > 0:
                label += f": {bbox.confidence:.2f}"
            
            # Calculate label size
            label_size, _ = cv2.getTextSize(
                label, 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, 
                2
            )
            
            # Draw label background
            cv2.rectangle(
                annotated, 
                (bbox.x1, bbox.y1 - label_size[1] - 10), 
                (bbox.x1 + label_size[0], bbox.y1), 
                color, 
                -1
            )
            
            # Draw label text
            cv2.putText(
                annotated, 
                label, 
                (bbox.x1, bbox.y1 - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, 
                (0, 0, 0), 
                2
            )
    
    return annotated
