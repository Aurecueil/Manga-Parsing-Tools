import os
import zipfile
import shutil

def extract_cbz_to_folders(directory):
    """
    Extracts all .cbz files in the given directory into folders with the same name
    and removes non-image files and empty directories from those folders.
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}

    for file in os.listdir(directory):
        if file.endswith('.cbz'):
            cbz_path = os.path.join(directory, file)
            folder_name = os.path.splitext(file)[0]
            extract_path = os.path.join(directory, folder_name)
            
            # Create a folder for extraction
            os.makedirs(extract_path, exist_ok=True)
            
            # Extract the .cbz file (it's essentially a .zip file)
            with zipfile.ZipFile(cbz_path, 'r') as cbz_file:
                cbz_file.extractall(extract_path)
            
            print(f"Extracted '{file}' to folder '{folder_name}'")
            
            # Clean up the extracted folder
            clean_extracted_folder(extract_path, image_extensions)

    print("Extraction and cleanup complete.")

def clean_extracted_folder(folder, image_extensions):
    """
    Removes all non-image files and empty directories in the given folder.
    """
    for root, dirs, files in os.walk(folder, topdown=False):
        # Remove non-image files
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.splitext(file)[1].lower() in image_extensions:
                os.remove(file_path)
                print(f"Removed non-image file: {file_path}")
        
        # Remove empty directories
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Check if directory is empty
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")

if __name__ == "__main__":
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Extract and clean all .cbz files in the same directory as the script
    extract_cbz_to_folders(script_dir)
