import streamlit as st
import os
import shutil
import subprocess

st.title("Image Folder Mover")

def open_folder_in_explorer(path):
    if os.path.exists(path):
        if os.name == 'nt':  # Windows
            subprocess.Popen(f'explorer "{path}"')
        else:
            st.warning("Auto-opening folders supported only on Windows")
    else:
        st.warning("Path does not exist")

source_folder = st.text_input(
    "Source folder path",
    value=r"C:\Users\pdvis\OneDrive\Desktop\SKU Packshots - 06-11-2024"
)
if st.button("Open Source Folder"):
    open_folder_in_explorer(source_folder)

destination_folder = st.text_input(
    "Destination folder path",
    value=r"C:\Users\pdvis\OneDrive\Desktop\Italy"
)
if st.button("Open Destination Folder"):
    open_folder_in_explorer(destination_folder)

def move_images(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    all_files = []
    for root, dirs, files in os.walk(src):
        for file_name in files:
            all_files.append(os.path.join(root, file_name))
    
    total_files = len(all_files)
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, file_path in enumerate(all_files):
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            destination_file_path = os.path.join(dest, file_name)

            if os.path.exists(destination_file_path):
                base_name, extension = os.path.splitext(file_name)
                counter = 1
                new_file_name = f"{base_name}_{counter}{extension}"
                new_file_path = os.path.join(dest, new_file_name)
                while os.path.exists(new_file_path):
                    counter += 1
                    new_file_name = f"{base_name}_{counter}{extension}"
                    new_file_path = os.path.join(dest, new_file_name)
                shutil.move(file_path, new_file_path)
            else:
                shutil.move(file_path, destination_file_path)

        progress_bar.progress((i + 1) / total_files)
        status_text.text(f"Moved {i + 1} of {total_files} files")

    st.success("All images have been moved!")

if st.button("Move Images"):
    if not os.path.exists(source_folder):
        st.error("Source folder does not exist!")
    else:
        move_images(source_folder, destination_folder)
