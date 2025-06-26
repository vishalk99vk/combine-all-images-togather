import streamlit as st
import os
import shutil
from zipfile import ZipFile
from io import BytesIO

st.title("Upload Images and Download Processed Zip")

uploaded_files = st.file_uploader(
    "Upload multiple images",
    type=["png", "jpg", "jpeg", "gif", "bmp"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"Uploaded {len(uploaded_files)} files.")

    # Create a temp directory to store uploads
    temp_dir = "temp_uploads"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Save uploaded files to temp_dir
    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    if st.button("Process and Prepare Download"):
        # Here you can do your "processing" if needed
        # For demo, we just zip all uploaded files

        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                zip_file.write(file_path, arcname=file_name)

        zip_buffer.seek(0)

        st.success("Ready to download!")

        st.download_button(
            label="Download ZIP of uploaded images",
            data=zip_buffer,
            file_name="processed_images.zip",
            mime="application/zip"
        )

        # Clean up temp folder after download preparation
        shutil.rmtree(temp_dir)
