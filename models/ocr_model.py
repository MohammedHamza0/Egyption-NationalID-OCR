"""
OCR Model wrapper for text extraction using EasyOCR.
"""

import easyocr
import cv2
import numpy as np
from typing import Optional


class OCRModel:
    """Wrapper for EasyOCR model."""
    
    def __init__(self, languages: list = None, gpu: bool = False):
        """
        Initialize OCR model.
        
        Args:
            languages: List of language codes (default: ['ar'] for Arabic)
            gpu: Whether to use GPU acceleration
        """
        if languages is None:
            languages = ['ar']
        
        self.reader = easyocr.Reader(languages, gpu=gpu)
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR results.
        
        Args:
            image: Input image (BGR or RGB)
            
        Returns:
            Preprocessed grayscale image
        """
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image
        
        return gray_image
    
    def extract_text(
        self, 
        image: np.ndarray, 
        bbox: Optional[tuple] = None,
        preprocess: bool = True,
        paragraph: bool = True
    ) -> str:
        """
        Extract text from image or image region.
        
        Args:
            image: Input image
            bbox: Optional bounding box (x1, y1, x2, y2) to crop region
            preprocess: Whether to preprocess the image
            paragraph: Whether to return text as paragraph
            
        Returns:
            Extracted text
        """
        # Crop if bounding box provided
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            cropped_image = image[y1:y2, x1:x2]
        else:
            cropped_image = image
        
        # Preprocess if requested
        if preprocess:
            processed_image = self.preprocess_image(cropped_image)
        else:
            processed_image = cropped_image
        
        # Extract text
        try:
            results = self.reader.readtext(
                processed_image, 
                detail=0, 
                paragraph=paragraph
            )
            text = ' '.join(results) if isinstance(results, list) else str(results)
            return text.strip()
        except Exception as e:
            print(f"OCR extraction error: {e}")
            return ""
