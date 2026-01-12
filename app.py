"""
Egyptian National ID Extractor - Main Entry Point

This application uses MVC architecture to extract information from Egyptian National ID cards.
It employs YOLO for object detection and EasyOCR for text extraction.

Architecture:
- Models: Data structures and ML model wrappers
- Views: Streamlit UI components
- Controllers: Business logic for ID extraction
- Utils: Helper functions for image processing and ID decoding
"""

from views.streamlit_app import run_app

if __name__ == "__main__":
    run_app()
