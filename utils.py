from ultralytics import YOLO
import cv2
import re
import easyocr
import os
import numpy as np

# Get the directory where utils.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize EasyOCR reader (this should be done once for efficiency)
reader = easyocr.Reader(['ar'], gpu=False)

# Function to preprocess the cropped image
def preprocess_image(cropped_image):
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    return  gray_image

# Functions for specific fields with custom OCR configurations
def extract_text(image, bbox, lang='ara'):
    x1, y1, x2, y2 = bbox
    cropped_image = image[y1:y2, x1:x2]
    preprocessed_image = preprocess_image(cropped_image)
    results = reader.readtext(preprocessed_image, detail=0, paragraph=True)
    text = ' '.join(results)
    return text.strip()

# Function to detect national ID numbers in a cropped image
def detect_national_id(cropped_image):
    model_path = os.path.join(BASE_DIR, 'detect_id.pt')
    model = YOLO(model_path)  # Load the model directly in the function
    results = model(cropped_image)
    detected_info = []

    for result in results:
        for box in result.boxes:
            cls = int(box.cls)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detected_info.append((cls, x1))
            # Visualization can be kept or removed; keeping it for now but checking if it affects performance/display
            # cv2.rectangle(cropped_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.putText(cropped_image, str(cls), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    detected_info.sort(key=lambda x: x[1])
    id_number = ''.join([str(cls) for cls, _ in detected_info])
    
    return id_number

# Function to remove numbers from a string
def remove_numbers(text):
    return re.sub(r'\d+', '', text)

# Function to expand bounding box height only
def expand_bbox_height(bbox, scale=1.2, image_shape=None):
    x1, y1, x2, y2 = bbox
    width = x2 - x1
    height = y2 - y1
    center_x = x1 + width // 2
    center_y = y1 + height // 2
    new_height = int(height * scale)
    new_y1 = max(center_y - new_height // 2, 0)
    new_y2 = min(center_y + new_height // 2, image_shape[0])
    return [x1, new_y1, x2, new_y2]

# Function to process the cropped image
def process_image(cropped_image):
    # Load the trained YOLO model for objects (fields) detection
    model_path = os.path.join(BASE_DIR, 'detect_odjects.pt')
    model = YOLO(model_path)
    results = model(cropped_image)

    # Variables to store extracted values
    first_name = ''
    second_name = ''
    merged_name = ''
    nid = ''
    address = ''
    serial = ''

    # Loop through the results
    for result in results:
        # Saving debug image might not be needed for web app, or can be optional. 
        # Commenting out for cleaner web app execution, or we can save to a temp path.
        # output_path = r'WhatsApp Image 2024-10-26 at 19.50.28_0694d61d.jpg'
        # result.save(output_path)

        for box in result.boxes:
            bbox = box.xyxy[0].tolist()
            class_id = int(box.cls[0].item())
            class_name = result.names[class_id]
            bbox = [int(coord) for coord in bbox]

            if class_name == 'firstName':
                first_name = extract_text(cropped_image, bbox, lang='ara')
            elif class_name == 'lastName':
                second_name = extract_text(cropped_image, bbox, lang='ara')
            elif class_name == 'serial':
                serial = extract_text(cropped_image, bbox, lang='eng')
            elif class_name == 'address':
                address = extract_text(cropped_image, bbox, lang='ara')
            elif class_name == 'nid':
                expanded_bbox = expand_bbox_height(bbox, scale=1.5, image_shape=cropped_image.shape)
                cropped_nid = cropped_image[expanded_bbox[1]:expanded_bbox[3], expanded_bbox[0]:expanded_bbox[2]]
                nid = detect_national_id(cropped_nid)

    merged_name = f"{first_name} {second_name}"
    
    # Check if NID was detected to avoid errors in decoding
    decoded_info = {}
    if nid and len(nid) == 14:
        try:
            decoded_info = decode_egyptian_id(nid)
        except Exception as e:
            print(f"Error decoding ID: {e}")
            decoded_info = {"Birth Date": "", "Governorate": "", "Gender": ""}
    else:
        decoded_info = {"Birth Date": "", "Governorate": "", "Gender": ""}

    return {
        "first_name": first_name,
        "second_name": second_name,
        "full_name": merged_name,
        "national_id": nid,
        "address": address,
        "serial": serial,
        "birth_date": decoded_info.get("Birth Date", ""),
        "governorate": decoded_info.get("Governorate", ""),
        "gender": decoded_info.get("Gender", "")
    }

# Function to decode the Egyptian ID number
def decode_egyptian_id(id_number):
    governorates = {
        '01': 'Cairo',
        '02': 'Alexandria',
        '03': 'Port Said',
        '04': 'Suez',
        '11': 'Damietta',
        '12': 'Dakahlia',
        '13': 'Ash Sharqia',
        '14': 'Kaliobeya',
        '15': 'Kafr El - Sheikh',
        '16': 'Gharbia',
        '17': 'Monoufia',
        '18': 'El Beheira',
        '19': 'Ismailia',
        '21': 'Giza',
        '22': 'Beni Suef',
        '23': 'Fayoum',
        '24': 'El Menia',
        '25': 'Assiut',
        '26': 'Sohag',
        '27': 'Qena',
        '28': 'Aswan',
        '29': 'Luxor',
        '31': 'Red Sea',
        '32': 'New Valley',
        '33': 'Matrouh',
        '34': 'North Sinai',
        '35': 'South Sinai',
        '88': 'Foreign'
    }

    century_digit = int(id_number[0])
    year = int(id_number[1:3])
    month = int(id_number[3:5])
    day = int(id_number[5:7])
    governorate_code = id_number[7:9]
    gender_code = int(id_number[12:13])

    if century_digit == 2:
        century = "1900-1999"
        full_year = 1900 + year
    elif century_digit == 3:
        century = "2000-2099"
        full_year = 2000 + year
    else:
        raise ValueError("Invalid century digit")

    gender = "Male" if gender_code % 2 != 0 else "Female"
    governorate = governorates.get(governorate_code, "Unknown")
    birth_date = f"{full_year:04d}-{month:02d}-{day:02d}"

    return {
        'Birth Date': birth_date,
        'Governorate': governorate,
        'Gender': gender
    }

# Function to detect the ID card and pass it to the existing code
def detect_and_process_id_card(image_input):
    # Load the ID card detection model
    model_path = os.path.join(BASE_DIR, 'detect_id_card.pt')
    id_card_model = YOLO(model_path)

    # Perform inference to detect the ID card
    id_card_results = id_card_model(image_input)

    # Load image if it's a path
    if isinstance(image_input, str):
        image = cv2.imread(image_input)
    else:
        # Assuming image_input is already a numpy array (BGR)
        image = image_input

    # Crop the ID card from the image
    cropped_image = None
    for result in id_card_results:
        if len(result.boxes) > 0:
            box = result.boxes[0] # Take the first detected card
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
            cropped_image = image[y1:y2, x1:x2]
            break # Process first detected card
    
    if cropped_image is None:
        return {"error": "No ID card detected"}

    # Pass the cropped image to the existing processing function
    return process_image(cropped_image)

















# import os
#
# # Set the environment variable to avoid OpenMP conflicts
# os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
#
# from ultralytics import YOLO
# import cv2
# import re
# import easyocr
#
# # Initialize EasyOCR reader
# reader = easyocr.Reader(['ar'], gpu=False)
#
# # Preprocessing function
# def preprocess_image(cropped_image):
#     gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
#     return gray_image
#
# # Function to extract text using EasyOCR
# def extract_text(image, bbox, lang='ara'):
#     x1, y1, x2, y2 = bbox
#     cropped_image = image[y1:y2, x1:x2]
#     preprocessed_image = preprocess_image(cropped_image)
#     results = reader.readtext(preprocessed_image, detail=0, paragraph=True)
#     text = ' '.join(results)
#     return text.strip()
#
# # Function to detect national ID numbers
# def detect_national_id(cropped_image):
#     model = YOLO('detect_id.pt')  # Load YOLO model
#     results = model(cropped_image)
#     detected_info = []
#
#     for result in results:
#         for box in result.boxes:
#             cls = int(box.cls)
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             detected_info.append((cls, x1))
#             cv2.rectangle(cropped_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.putText(cropped_image, str(cls), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
#
#     detected_info.sort(key=lambda x: x[1])
#     id_number = ''.join([str(cls) for cls, _ in detected_info])
#     return id_number
#
# # Function to decode the Egyptian ID number
# def decode_egyptian_id(id_number):
#     governorates = {
#         '01': 'Cairo', '02': 'Alexandria', '03': 'Port Said', '04': 'Suez',
#         '11': 'Damietta', '12': 'Dakahlia', '13': 'Ash Sharqia', '14': 'Kaliobeya',
#         '15': 'Kafr El-Sheikh', '16': 'Gharbia', '17': 'Monoufia', '18': 'El Beheira',
#         '19': 'Ismailia', '21': 'Giza', '22': 'Beni Suef', '23': 'Fayoum',
#         '24': 'El Menia', '25': 'Assiut', '26': 'Sohag', '27': 'Qena',
#         '28': 'Aswan', '29': 'Luxor', '31': 'Red Sea', '32': 'New Valley',
#         '33': 'Matrouh', '34': 'North Sinai', '35': 'South Sinai', '88': 'Foreign'
#     }
#
#     century_digit = int(id_number[0])
#     year = int(id_number[1:3])
#     month = int(id_number[3:5])
#     day = int(id_number[5:7])
#     governorate_code = id_number[7:9]
#     gender_code = int(id_number[12:13])
#
#     full_year = 1900 + year if century_digit == 2 else 2000 + year
#     gender = "Male" if gender_code % 2 != 0 else "Female"
#     governorate = governorates.get(governorate_code, "Unknown")
#     birth_date = f"{full_year:04d}-{month:02d}-{day:02d}"
#
#     return {'Birth Date': birth_date, 'Governorate': governorate, 'Gender': gender}
#
# # Function to process cropped ID card image
# def process_image(cropped_image):
#     model = YOLO('detect_odjects.pt')  # Load YOLO model for fields
#     results = model(cropped_image)
#
#     first_name, second_name, merged_name, nid, address, serial = '', '', '', '', '', ''
#     for result in results:
#         for box in result.boxes:
#             bbox = [int(coord) for coord in box.xyxy[0].tolist()]
#             class_name = result.names[int(box.cls[0].item())]
#
#             if class_name == 'firstName':
#                 first_name = extract_text(cropped_image, bbox, lang='ara')
#             elif class_name == 'lastName':
#                 second_name = extract_text(cropped_image, bbox, lang='ara')
#             elif class_name == 'serial':
#                 serial = extract_text(cropped_image, bbox, lang='eng')
#             elif class_name == 'address':
#                 address = extract_text(cropped_image, bbox, lang='ara')
#             elif class_name == 'nid':
#                 nid = detect_national_id(cropped_image[bbox[1]:bbox[3], bbox[0]:bbox[2]])
#
#     merged_name = f"{first_name} {second_name}"
#     decoded_info = decode_egyptian_id(nid)
#
#     return {
#         'First Name': first_name, 'Second Name': second_name, 'Full Name': merged_name,
#         'National ID': nid, 'Address': address, 'Serial': serial,
#         'Birth Date': decoded_info['Birth Date'],
#         'Governorate': decoded_info['Governorate'],
#         'Gender': decoded_info['Gender']
#     }
#
# # Function to detect and process ID card
# def detect_and_process_id_card(image_path):
#     model = YOLO('detect_id_card.pt')  # Load YOLO model for ID card detection
#     results = model(image_path)
#
#     image = cv2.imread(image_path)
#     for result in results:
#         for box in result.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             cropped_image = image[y1:y2, x1:x2]
#             return process_image(cropped_image)
#
# # Example usage
# result = detect_and_process_id_card("font_ID.jpg")
# print(result)
