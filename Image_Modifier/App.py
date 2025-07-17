# main_app.py
import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import Image_Modifiers  # This is your existing Python script with def functions for image modification

st.set_page_config(page_title="Image Processor", layout="centered")
st.title("Image Processing Interface")

st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        padding: 0.75em;
        font-size: 16px;
        border-radius: 10px;
    }
    .stTextInput>div>input {
        padding: 0.75em;
        font-size: 16px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Step 1: Take the image URL from the server
image_url = st.text_input("Paste the image URL from the server:")

if image_url:
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        wand_image = Image_Modifiers.pil_to_wand(image)

        st.image(image, caption="Original Image", use_column_width=True)

        # Step 2: Select modifications
        st.subheader("Choose Modifications")
        mod_type = st.selectbox("Select a modification", ["None", "Sharpener", "Compressor", "Blur"])

        if mod_type == "Blur":
            blur_val = st.slider("Blur Percentage", min_value=0, max_value=10, value=0)
        elif mod_type == "Compressor":
            width = st.number_input("Width (px)", min_value=1, value=image.width)
            height = st.number_input("Height (px)", min_value=1, value=image.height)

        if st.button("Apply Modification"):
            # Call the corresponding function from Image_Modifiers.py
            if mod_type == "Sharpener":
                image = Image_Modifiers.Sharpener(wand_image)
            elif mod_type == "Compressor":
                image = Image_Modifiers.Compressor(wand_image, width, height)
            elif mod_type == "Blur":
                image = Image_Modifiers.Blur(wand_image, blur_val)

            # Display modified image
            st.image(image, caption="Modified Image", use_column_width=True)

            # Prepare image to return
            buf = BytesIO()
            image.save(buf, format='PNG')
            buf.seek(0)

            st.download_button(
                label="Download Modified Image",
                data=buf,
                file_name="modified_image.png",
                mime="image/png"
            )

    except Exception as e:
        st.error(f"Failed to fetch or process image: {e}")
