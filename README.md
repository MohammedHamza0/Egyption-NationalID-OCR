# Egyptian National ID OCR

An advanced OCR system for extracting information from Egyptian National ID cards using YOLO object detection and EasyOCR text recognition.

## Features

- 🎯 **Automatic ID Card Detection**: Detects and crops ID cards from images
- 🔍 **Field Detection**: Identifies specific fields (name, address, national ID, etc.)
- 📝 **Arabic OCR**: Extracts Arabic text using EasyOCR
- 🔢 **Digit Recognition**: Specialized detection for National ID numbers
- 🎨 **Modern UI**: Beautiful Streamlit interface with side-by-side image comparison
- 📊 **Structured Output**: Returns data in JSON format
- 🏗️ **MVC Architecture**: Clean, maintainable code structure

## Architecture

The project follows the Model-View-Controller (MVC) pattern:

```
Egyption-NationalID-OCR/
├── models/                      # Data models and ML wrappers
│   ├── id_card_model.py        # Data structures (IDCardData, BoundingBox)
│   ├── ocr_model.py            # EasyOCR wrapper
│   └── detection_model.py      # YOLO detection wrappers
├── views/                       # UI components
│   └── streamlit_app.py        # Enhanced Streamlit interface
├── controllers/                 # Business logic
│   └── id_extraction_controller.py  # Extraction workflow orchestration
├── utils/                       # Helper functions
│   ├── image_processing.py     # Image utilities
│   └── id_decoder.py           # Egyptian ID decoder
├── app.py                       # Main entry point
├── weights/                     # Model weights
│   ├── detect_id_card.pt       # YOLO model for ID card detection
│   ├── detect_odjects.pt       # YOLO model for field detection
│   └── detect_id.pt            # YOLO model for digit detection
├── tests/                       # Unit tests
│   └── test_mvc_structure.py   # Structure verification tests
└── requirements.txt            # Python dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Egyption-NationalID-OCR.git
cd Egyption-NationalID-OCR
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Streamlit App

```bash
streamlit run app.py
```

Then:
1. Upload an image of an Egyptian National ID card
2. Click "Extract Data"
3. View the extracted information and annotated images

### Using the Controller Programmatically

```python
import cv2
from controllers.id_extraction_controller import IDExtractionController

# Initialize controller
controller = IDExtractionController()

# Load image
image = cv2.imread('path/to/id_card.jpg')

# Extract information
id_data, cropped_card, annotated_card = controller.extract_from_image(image)

# Access extracted data
print(f"Name: {id_data.full_name}")
print(f"National ID: {id_data.national_id}")
print(f"Birth Date: {id_data.birth_date}")
print(f"Governorate: {id_data.governorate}")
```

## Extracted Information

The system extracts the following information:

- **Personal Information**:
  - First Name (Arabic)
  - Second Name (Arabic)
  - Full Name
  - Gender
  - Birth Date
  - Governorate

- **ID Information**:
  - National ID Number (14 digits)
  - Serial Number

- **Address**:
  - Full address (Arabic)

## Egyptian National ID Structure

The 14-digit National ID encodes:
- Digit 1: Century (2 = 1900s, 3 = 2000s)
- Digits 2-3: Year of birth
- Digits 4-5: Month of birth
- Digits 6-7: Day of birth
- Digits 8-9: Governorate code
- Digits 10-12: Unique sequence
- Digit 13: Gender (odd = male, even = female)
- Digit 14: Check digit

## Technologies Used

- **YOLO (Ultralytics)**: Object detection for ID cards and fields
- **EasyOCR**: Arabic text recognition
- **Streamlit**: Web interface
- **OpenCV**: Image processing
- **NumPy**: Array operations

## UI Features

- ✨ Modern gradient design
- 📱 Responsive layout
- 🖼️ Side-by-side image comparison
- 🎨 Annotated images with bounding boxes
- 📥 JSON export functionality
- ⚡ Real-time processing feedback
- 🎯 Clear error messages

## Requirements

- Python 3.8+
- See `requirements.txt` for full dependencies

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- YOLO by Ultralytics
- EasyOCR by JaidedAI
- Streamlit for the amazing framework