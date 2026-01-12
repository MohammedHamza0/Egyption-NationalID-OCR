import utils
import cv2
import json

image_path = "WhatsApp Image 2024-10-26 at 19.50.18_0b725990.jpg"
print(f"Testing extraction on {image_path}...")

try:
    # Test with file path
    print("Testing with file path...")
    result_path = utils.detect_and_process_id_card(image_path)
    print("Result (Path):")
    print(json.dumps(result_path, indent=2, ensure_ascii=False))

    # Test with numpy array
    print("\nTesting with numpy array...")
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not read image for array test")
    else:
        result_array = utils.detect_and_process_id_card(img)
        print("Result (Array):")
        print(json.dumps(result_array, indent=2, ensure_ascii=False))

except Exception as e:
    print(f"Error during testing: {e}")
