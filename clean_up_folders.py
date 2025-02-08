import os
import shutil
from PIL import Image

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

def can_open_image(file_path):
    """Check if a file can be opened as an image."""
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verify the image without fully loading it
        return True
    except Exception:
        return False

# Iterate through all subdirectories
for folder in os.listdir(script_dir):
    folder_path = os.path.join(script_dir, folder)

    if os.path.isdir(folder_path):  # Check if it's a folder
        # Iterate over all files in the folder
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check if the file is an actual image
                if not can_open_image(file_path):
                    try:
                        os.remove(file_path)  # Delete the file
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")

        # Remove empty directories
        for root, dirs, _ in os.walk(folder_path, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):  # If empty
                    try:
                        os.rmdir(dir_path)  # Remove empty folder
                        print(f"Removed empty folder: {dir_path}")
                    except Exception as e:
                        print(f"Error removing {dir_path}: {e}")
