"""
Enhanced Streamlit UI for Egyptian National ID Extractor.
"""

import streamlit as st
from controllers.id_extraction_controller import IDExtractionController


def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown("""
        <style>
        /* Main container styling */
        .main {
            padding: 2rem;
        }
        
        /* Header styling */
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        
        .header-title {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .header-subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        /* Card styling */
        .info-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin: 1rem 0;
        }
        
        .info-label {
            font-weight: 600;
            color: #667eea;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .info-value {
            font-size: 1.1rem;
            color: #2c3e50;
            margin-top: 0.3rem;
        }
        
        /* Image container */
        .image-container {
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 1rem;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Success/Error messages */
        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #28a745;
        }
        
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
        }
        
        /* Upload section */
        .upload-section {
            background: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            border: 2px dashed #667eea;
            text-align: center;
            margin: 2rem 0;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            padding: 0.75rem 2rem;
            border-radius: 5px;
            border: none;
            width: 100%;
            font-size: 1.1rem;
            transition: transform 0.2s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background: #f8f9fa;
            border-radius: 5px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the application header."""
    st.markdown("""
        <div class="header-container">
            <div class="header-title">🪪 Egyptian National ID Extractor</div>
            <div class="header-subtitle">
                Advanced OCR system powered by YOLO and EasyOCR
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_info_card(label: str, value: str):
    """Render an information card."""
    if value:
        st.markdown(f"""
            <div class="info-card">
                <div class="info-label">{label}</div>
                <div class="info-value">{value}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="info-card">
                <div class="info-label">{label}</div>
                <div class="info-value" style="color: #999;">Not detected</div>
            </div>
        """, unsafe_allow_html=True)


def render_extracted_data(data: dict):
    """Render extracted ID card data in a structured format."""
    st.markdown("### 📋 Extracted Information")
    
    # Personal Information
    with st.expander("👤 Personal Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            render_info_card("First Name", data.get('first_name', ''))
            render_info_card("Full Name", data.get('full_name', ''))
            render_info_card("Gender", data.get('gender', ''))
        with col2:
            render_info_card("Second Name", data.get('second_name', ''))
            render_info_card("Birth Date", data.get('birth_date', ''))
            render_info_card("Governorate", data.get('governorate', ''))
    
    # ID Information
    with st.expander("🆔 ID Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            render_info_card("National ID", data.get('national_id', ''))
        with col2:
            render_info_card("Serial Number", data.get('serial', ''))
    
    # Address
    with st.expander("📍 Address Information", expanded=True):
        render_info_card("Address", data.get('address', ''))
    
    # Raw JSON
    with st.expander("🔍 View Raw JSON Data"):
        st.json(data)


def run_app():
    """Main application function."""
    # Page configuration
    st.set_page_config(
        page_title="Egyptian ID Extractor",
        page_icon="🪪",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply custom styling
    apply_custom_css()
    
    # Render header
    render_header()
    
    # Instructions
    st.markdown("""
        <div style="background: #e3f2fd; padding: 1rem; border-radius: 5px; margin-bottom: 2rem; color: #2c3e50;">
            <strong>📌 Instructions:</strong>
            <ol style="margin: 0.5rem 0 0 1rem;">
                <li>Upload a clear image of an Egyptian National ID card</li>
                <li>Click "Extract Data" to process the image</li>
                <li>View the extracted information and annotated image</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an ID Card Image",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear photo of the Egyptian National ID card"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        st.markdown("### 📤 Uploaded Image")
        st.image(
            uploaded_file,
            caption='Original Uploaded Image',
            use_container_width=True
        )
        
        # Extract button
        if st.button("🚀 Extract Data", type="primary"):
            with st.spinner("🔄 Processing ID Card... Please wait..."):
                # Initialize controller
                controller = IDExtractionController()
                
                # Process the image
                result = controller.process_uploaded_file(uploaded_file)
                
                # Display results
                if result['success']:
                    st.success("✅ Data Extracted Successfully!")
                    
                    # Create two columns for images
                    st.markdown("### 🖼️ Processed Images")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Cropped ID Card**")
                        if result['cropped_card'] is not None:
                            st.image(
                                result['cropped_card'],
                                caption='Detected and Cropped ID Card',
                                use_container_width=True
                            )
                    
                    with col2:
                        st.markdown("**Detected Fields**")
                        if result['annotated_card'] is not None:
                            st.image(
                                result['annotated_card'],
                                caption='ID Card with Detected Bounding Boxes',
                                use_container_width=True
                            )
                    
                    # Display extracted data
                    st.markdown("---")
                    render_extracted_data(result['data'])
                    
                    # Download button for JSON
                    st.markdown("---")
                    st.download_button(
                        label="📥 Download Extracted Data (JSON)",
                        data=str(result['data']),
                        file_name="extracted_id_data.json",
                        mime="application/json"
                    )
                else:
                    st.error(f"❌ {result['error']}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            <p>Built with ❤️ using Streamlit, YOLO, and EasyOCR</p>
            <p style="font-size: 0.9rem;">For best results, ensure the ID card is well-lit and clearly visible</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    run_app()
