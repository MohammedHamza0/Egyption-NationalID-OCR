import streamlit as st
import numpy as np
import cv2
from PIL import Image
import json
from utils import detect_and_process_id_card

st.set_page_config(page_title="Egyptian ID Extractor", layout="wide")

st.title("🪪 Egyptian National ID Extractor")
st.markdown("Upload an image of an Egyptian National ID to extract data.")

uploaded_file = st.file_uploader("Choose an ID Card Image", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded ID Card', use_column_width=True)

    if st.button("Extract Data"):
        with st.spinner("Processing ID Card..."):
            try:
                # Convert PIL image to OpenCV format (BGR)
                image_np = np.array(image)
                image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

                # Process the image
                result = detect_and_process_id_card(image_bgr)

                # Display Results
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("Data Extracted Successfully!")
                    st.json(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
