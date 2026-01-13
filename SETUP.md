# Setup Guide - Egyptian National ID OCR

## Quick Start

### Option 1: Using Pre-built Wheels (Recommended)

If you encounter SSL or build errors, install packages individually with pre-built wheels:

```bash
# Install core dependencies first
pip install numpy pillow

# Install PyTorch (CPU version for faster installation)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install computer vision libraries
pip install opencv-python

# Install OCR and detection libraries
pip install easyocr ultralytics

# Install Streamlit
pip install streamlit
```

### Option 2: Using requirements.txt

```bash
pip install -r requirements.txt --prefer-binary
```

### Option 3: If SSL Errors Occur

If you get SSL certificate errors, try:

```bash
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

---

## Running the Application

Once dependencies are installed:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## Testing the Installation

Run the test script to verify everything is working:

```bash
python tests/test_mvc_structure.py
```

You should see:
```
============================================================
MVC Structure Verification Tests
============================================================
Testing imports...
[PASS] Models imported successfully
[PASS] OCR Model imported successfully
[PASS] Detection Models imported successfully
[PASS] Controller imported successfully
[PASS] Utils imported successfully

Testing data models...
[PASS] BoundingBox creation works
[PASS] IDCardData creation works
[PASS] IDCardData to_dict works

Testing ID decoder...
[PASS] ID decoder works: {...}
[PASS] ID decoder handles invalid IDs

============================================================
Test Results Summary
============================================================
Import Test: [PASS]
Data Models Test: [PASS]
ID Decoder Test: [PASS]

============================================================
[SUCCESS] All tests passed! MVC structure is working correctly.
============================================================
```

---

## Troubleshooting

### Issue: "No module named 'streamlit'"

**Solution:** Dependencies not installed. Run one of the installation commands above.

### Issue: SSL Certificate Errors

**Solution:** Use the `--trusted-host` option:
```bash
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

### Issue: OpenCV build errors

**Solution:** We've switched from `opencv-python-headless` to `opencv-python` which has pre-built wheels. If still failing, install manually:
```bash
pip install opencv-python --only-binary opencv-python
```

### Issue: "streamlit: command not found"

**Solution:** Use Python module syntax:
```bash
python -m streamlit run app.py
```

### Issue: EasyOCR download errors

**Solution:** EasyOCR downloads models on first run. Ensure you have internet connection. Models are cached in `~/.EasyOCR/`

---

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended for faster processing)
- **Disk Space**: ~2GB for dependencies and models
- **Internet**: Required for first-time model downloads

---

## Project Structure

```
Egyption-NationalID-OCR/
├── models/                         # ML models and data structures
│   ├── __init__.py
│   ├── id_card_model.py           # IDCardData, BoundingBox, DetectionResult
│   ├── ocr_model.py               # EasyOCR wrapper
│   └── detection_model.py         # YOLO detection wrappers
│
├── controllers/                    # Business logic
│   ├── __init__.py
│   └── id_extraction_controller.py # Main extraction workflow
│
├── views/                          # User interface
│   ├── __init__.py
│   └── streamlit_app.py           # Enhanced Streamlit UI
│
├── utils/                          # Helper functions
│   ├── __init__.py
│   ├── image_processing.py        # Image utilities
│   └── id_decoder.py              # Egyptian ID decoder
│
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── tests/                          # Testing
│   └── test_mvc_structure.py      # Structure verification tests
├── README.md                       # Project documentation
│
└── weights/                        # Model weights
    ├── detect_id_card.pt          # ID card detection model
    ├── detect_odjects.pt          # Field detection model
    └── detect_id.pt               # Digit detection model
```

---

## Usage

### Web Interface

1. Start the app: `streamlit run app.py`
2. Upload an ID card image
3. Click "Extract Data"
4. View results:
   - Original uploaded image
   - Cropped ID card
   - Annotated image with bounding boxes
   - Extracted information in organized sections

### Programmatic Usage

```python
from controllers.id_extraction_controller import IDExtractionController
import cv2

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
print(f"Gender: {id_data.gender}")

# Get as dictionary
data_dict = id_data.to_dict()
print(data_dict)
```

---

## Features

- ✅ Automatic ID card detection
- ✅ Field detection (name, address, ID, serial)
- ✅ Arabic OCR with EasyOCR
- ✅ National ID decoding (birth date, gender, governorate)
- ✅ Modern Streamlit UI with side-by-side image comparison
- ✅ Annotated images with bounding boxes
- ✅ JSON export functionality
- ✅ MVC architecture for maintainability

---

## Next Steps

After successful installation:

1. **Test with sample images**: Upload various ID card images to test accuracy
2. **Customize UI**: Modify `views/streamlit_app.py` for your branding
3. **Add features**: Extend the controller for batch processing, API endpoints, etc.
4. **Deploy**: Use Streamlit Cloud, Docker, or your preferred hosting platform

---

## Support

For issues or questions:
1. Check this setup guide
2. Review the README.md
3. Check the walkthrough.md in the brain folder
4. Verify all YOLO model files (.pt) are present in the project root

---

## License

[Your License Here]
