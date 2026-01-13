"""
Data models for Egyptian National ID card information.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import numpy as np


@dataclass
class BoundingBox:
    """Represents a bounding box for detected objects."""
    x1: int
    y1: int
    x2: int
    y2: int
    class_name: str = ""
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2,
            'class_name': self.class_name,
            'confidence': self.confidence
        }
    
    def expand_height(self, scale: float = 1.2, image_height: int = None) -> 'BoundingBox':
        """Expand bounding box height only."""
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        center_x = self.x1 + width // 2
        center_y = self.y1 + height // 2
        new_height = int(height * scale)
        new_y1 = max(center_y - new_height // 2, 0)
        new_y2 = center_y + new_height // 2
        
        if image_height is not None:
            new_y2 = min(new_y2, image_height)
        
        return BoundingBox(
            x1=self.x1,
            y1=new_y1,
            x2=self.x2,
            y2=new_y2,
            class_name=self.class_name,
            confidence=self.confidence
        )


@dataclass
class DetectionResult:
    """Represents detection results with bounding boxes."""
    bounding_boxes: List[BoundingBox] = field(default_factory=list)
    annotated_image: Optional[np.ndarray] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'bounding_boxes': [bbox.to_dict() for bbox in self.bounding_boxes],
            'has_annotated_image': self.annotated_image is not None
        }


@dataclass
class IDCardData:
    """Represents extracted Egyptian National ID card data."""
    first_name: str = ""
    second_name: str = ""
    full_name: str = ""
    national_id: str = ""
    address: str = ""
    serial: str = ""
    birth_date: str = ""
    governorate: str = ""
    gender: str = ""
    
    # Additional metadata
    detection_result: Optional[DetectionResult] = None
    cropped_id_card: Optional[np.ndarray] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'first_name': self.first_name,
            'second_name': self.second_name,
            'full_name': self.full_name,
            'national_id': self.national_id,
            'address': self.address,
            'serial': self.serial,
            'birth_date': self.birth_date,
            'governorate': self.governorate,
            'gender': self.gender
        }
    
    def is_valid(self) -> bool:
        """Check if the extracted data is valid."""
        return bool(self.national_id and len(self.national_id) == 14)
