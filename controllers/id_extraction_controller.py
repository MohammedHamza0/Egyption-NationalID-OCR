"""
ID Extraction Controller - Orchestrates the ID card extraction workflow.
"""

import cv2
import numpy as np
from typing import Dict, Any, Tuple, Optional

from models.id_card_model import IDCardData, BoundingBox, DetectionResult
from models.ocr_model import OCRModel
from models.detection_model import IDCardDetector, FieldDetector, DigitDetector
from utils.id_decoder import decode_egyptian_id
from utils.image_processing import crop_image, annotate_image


class IDExtractionController:
    """Controller for Egyptian National ID extraction workflow."""
    
    def __init__(self):
        """Initialize the controller with required models."""
        self.ocr_model = OCRModel(languages=['ar'], gpu=False)
        self.id_card_detector = IDCardDetector()
        self.field_detector = FieldDetector()
        self.digit_detector = DigitDetector()
    
    def extract_from_image(
        self, 
        image: np.ndarray,
        return_annotated: bool = True
    ) -> Tuple[IDCardData, Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Extract ID card information from image.
        
        Args:
            image: Input image (BGR format)
            return_annotated: Whether to return annotated images
            
        Returns:
            Tuple of (IDCardData, cropped_id_card, annotated_id_card)
        """
        # Step 1: Detect ID card in the image
        id_card_bbox = self.id_card_detector.detect_first(image)
        
        if id_card_bbox is None:
            # Return error result
            error_data = IDCardData()
            return error_data, None, None
        
        # Step 2: Crop the ID card
        cropped_id_card = crop_image(image, id_card_bbox)
        
        # Step 3: Detect fields in the cropped ID card
        field_detection = self.field_detector.detect(
            cropped_id_card, 
            annotate=return_annotated
        )
        
        # Step 4: Extract information from each field
        id_data = self._extract_fields(cropped_id_card, field_detection.bounding_boxes)
        
        # Step 5: Store detection results
        id_data.detection_result = field_detection
        id_data.cropped_id_card = cropped_id_card
        
        # Return data and images
        annotated_card = field_detection.annotated_image if return_annotated else None
        
        return id_data, cropped_id_card, annotated_card
    
    def _extract_fields(
        self, 
        cropped_id_card: np.ndarray, 
        bboxes: list
    ) -> IDCardData:
        """
        Extract information from detected fields.
        
        Args:
            cropped_id_card: Cropped ID card image
            bboxes: List of detected bounding boxes
            
        Returns:
            IDCardData with extracted information
        """
        id_data = IDCardData()
        
        for bbox in bboxes:
            class_name = bbox.class_name
            
            if class_name == 'firstName':
                id_data.first_name = self.ocr_model.extract_text(
                    cropped_id_card,
                    (bbox.x1, bbox.y1, bbox.x2, bbox.y2)
                )
            
            elif class_name == 'lastName':
                id_data.second_name = self.ocr_model.extract_text(
                    cropped_id_card,
                    (bbox.x1, bbox.y1, bbox.x2, bbox.y2)
                )
            
            elif class_name == 'serial':
                id_data.serial = self.ocr_model.extract_text(
                    cropped_id_card,
                    (bbox.x1, bbox.y1, bbox.x2, bbox.y2)
                )
            
            elif class_name == 'address':
                id_data.address = self.ocr_model.extract_text(
                    cropped_id_card,
                    (bbox.x1, bbox.y1, bbox.x2, bbox.y2)
                )
            
            elif class_name == 'nid':
                # Expand bounding box for better digit detection
                expanded_bbox = bbox.expand_height(
                    scale=1.5, 
                    image_height=cropped_id_card.shape[0]
                )
                
                # Crop the NID region
                nid_region = crop_image(cropped_id_card, expanded_bbox)
                
                # Detect digits
                id_data.national_id = self.digit_detector.detect_digits(nid_region)
        
        # Merge names
        id_data.full_name = f"{id_data.first_name} {id_data.second_name}".strip()
        
        # Decode National ID if valid
        if id_data.national_id and len(id_data.national_id) == 14:
            decoded_info = decode_egyptian_id(id_data.national_id)
            id_data.birth_date = decoded_info.get('Birth Date', '')
            id_data.governorate = decoded_info.get('Governorate', '')
            id_data.gender = decoded_info.get('Gender', '')
        
        return id_data
    
    def process_uploaded_file(
        self, 
        uploaded_file
    ) -> Dict[str, Any]:
        """
        Process uploaded file from Streamlit.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Dictionary with extraction results and images
        """
        try:
            # Read image from uploaded file
            from PIL import Image
            image = Image.open(uploaded_file)
            image_np = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            if len(image_np.shape) == 3 and image_np.shape[2] == 3:
                image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            else:
                image_bgr = image_np
            
            # Extract information
            id_data, cropped_card, annotated_card = self.extract_from_image(
                image_bgr, 
                return_annotated=True
            )
            
            # Check if ID card was detected
            if cropped_card is None:
                return {
                    'success': False,
                    'error': 'No ID card detected in the image. Please ensure the ID card is clearly visible.',
                    'data': None,
                    'cropped_card': None,
                    'annotated_card': None
                }
            
            # Convert images back to RGB for display
            cropped_card_rgb = cv2.cvtColor(cropped_card, cv2.COLOR_BGR2RGB)
            annotated_card_rgb = cv2.cvtColor(annotated_card, cv2.COLOR_BGR2RGB) if annotated_card is not None else None
            
            return {
                'success': True,
                'error': None,
                'data': id_data.to_dict(),
                'cropped_card': cropped_card_rgb,
                'annotated_card': annotated_card_rgb
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'An error occurred during processing: {str(e)}',
                'data': None,
                'cropped_card': None,
                'annotated_card': None
            }
