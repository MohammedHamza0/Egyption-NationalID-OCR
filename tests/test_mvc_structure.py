"""
Simple test script to verify MVC structure is working correctly.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from models.id_card_model import IDCardData, BoundingBox, DetectionResult
        print("[PASS] Models imported successfully")
    except Exception as e:
        print(f"[FAIL] Failed to import models: {e}")
        return False
    
    try:
        from models.ocr_model import OCRModel
        print("[PASS] OCR Model imported successfully")
    except Exception as e:
        print(f"[FAIL] Failed to import OCR Model: {e}")
        return False
    
    try:
        from models.detection_model import DetectionModel, IDCardDetector, FieldDetector, DigitDetector
        print("[PASS] Detection Models imported successfully")
    except Exception as e:
        print(f"[FAIL] Failed to import Detection Models: {e}")
        return False
    
    try:
        from controllers.id_extraction_controller import IDExtractionController
        print("[PASS] Controller imported successfully")
    except Exception as e:
        print(f"[FAIL] Failed to import Controller: {e}")
        return False
    
    try:
        from utils.id_decoder import decode_egyptian_id
        from utils.image_processing import crop_image, annotate_image
        print("[PASS] Utils imported successfully")
    except Exception as e:
        print(f"[FAIL] Failed to import Utils: {e}")
        return False
    
    return True


def test_data_models():
    """Test data model creation."""
    print("\nTesting data models...")
    
    try:
        from models.id_card_model import IDCardData, BoundingBox
        
        # Test BoundingBox
        bbox = BoundingBox(x1=10, y1=20, x2=100, y2=80, class_name="test", confidence=0.95)
        assert bbox.x1 == 10
        assert bbox.class_name == "test"
        print("[PASS] BoundingBox creation works")
        
        # Test IDCardData
        id_data = IDCardData(
            first_name="Mohammed",
            second_name="Hamza",
            national_id="12345678901234"
        )
        assert id_data.first_name == "Mohammed"
        assert len(id_data.national_id) == 14
        print("[PASS] IDCardData creation works")
        
        # Test to_dict
        data_dict = id_data.to_dict()
        assert isinstance(data_dict, dict)
        assert 'first_name' in data_dict
        print("[PASS] IDCardData to_dict works")
        
        return True
    except Exception as e:
        print(f"[FAIL] Data model test failed: {e}")
        return False


def test_id_decoder():
    """Test Egyptian ID decoder."""
    print("\nTesting ID decoder...")
    
    try:
        from utils.id_decoder import decode_egyptian_id
        
        # Test valid ID (example: born in 1995, Cairo, male)
        test_id = "29501011234567"  # 2 = 1900s, 95 = year, 01 = month, 01 = day, 01 = Cairo
        result = decode_egyptian_id(test_id)
        
        assert 'Birth Date' in result
        assert 'Governorate' in result
        assert 'Gender' in result
        assert result['Governorate'] == 'Cairo'
        print(f"[PASS] ID decoder works: {result}")
        
        # Test invalid ID
        invalid_result = decode_egyptian_id("123")
        assert invalid_result['Birth Date'] == ''
        print("[PASS] ID decoder handles invalid IDs")
        
        return True
    except Exception as e:
        print(f"[FAIL] ID decoder test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("MVC Structure Verification Tests")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Data Models Test", test_data_models),
        ("ID Decoder Test", test_id_decoder),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[FAIL] {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] All tests passed! MVC structure is working correctly.")
    else:
        print("[ERROR] Some tests failed. Please check the errors above.")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
