"""
Models package for Egyptian National ID OCR.
Contains data models and ML model wrappers.
"""

from .id_card_model import IDCardData, BoundingBox, DetectionResult
from .ocr_model import OCRModel
from .detection_model import DetectionModel

__all__ = [
    'IDCardData',
    'BoundingBox',
    'DetectionResult',
    'OCRModel',
    'DetectionModel'
]
