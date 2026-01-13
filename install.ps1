# Installation script for Egyptian National ID OCR
# This script installs dependencies in the correct order to avoid build issues

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Egyptian National ID OCR - Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "Found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host ""

# Install core dependencies
Write-Host "Installing core dependencies (numpy, pillow)..." -ForegroundColor Yellow
pip install numpy pillow
Write-Host ""

# Install PyTorch (CPU version for faster installation)
Write-Host "Installing PyTorch (CPU version)..." -ForegroundColor Yellow
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
Write-Host ""

# Install OpenCV
Write-Host "Installing OpenCV..." -ForegroundColor Yellow
pip install opencv-python --only-binary opencv-python
Write-Host ""

# Install EasyOCR
Write-Host "Installing EasyOCR..." -ForegroundColor Yellow
pip install easyocr
Write-Host ""

# Install Ultralytics (YOLO)
Write-Host "Installing Ultralytics..." -ForegroundColor Yellow
pip install ultralytics
Write-Host ""

# Install Streamlit
Write-Host "Installing Streamlit..." -ForegroundColor Yellow
pip install streamlit
Write-Host ""

# Verify installation
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verifying installation..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

python tests/test_mvc_structure.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Installation completed successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "To run the application:" -ForegroundColor Cyan
    Write-Host "  streamlit run app.py" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Installation verification failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check the errors above and try again." -ForegroundColor Yellow
    Write-Host "See SETUP.md for troubleshooting steps." -ForegroundColor Yellow
    Write-Host ""
}
