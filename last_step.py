import shutil
import os
import re

move_operations = []

reserved_names = [
    "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
]

# Look-alike replacements for illegal characters
illegal_to_lookalike = {
    '?': '？',
    '*': '∗',
    '/': '∕',
    '\\': '⧵⧵',
    '<': '＜',
    '>': '＞',
    ':': '：',
    '"': '＂',
    '|': 'ǀ'
}

def move_and_delete(path_1, path_2):
    """Function to move contents and delete source directory."""
    try:
        if os.path.exists(path_1):
            # Copy contents from path_1 to path_2
            for item in os.listdir(path_1):
                s = os.path.join(path_1, item)
                d = os.path.join(path_2, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            # Now delete all contents of path_1 (including the folder itself)
            shutil.rmtree(path_1)
            print(f"Moved and deleted: {path_1}")
    except Exception as e:
        print(f"Error processing {path_1}: {e}")

def process_move_operations():
    """Process the move and delete operations once the program ends."""
    print("Processing move and delete operations...")
    try:
        for path_1, path_2 in move_operations:
            print(f"moving {path_1} to {path_2}")
            move_and_delete(path_1, path_2)
    except Exception as e:
        print(f"Error processing {path_1}: {e}")
    
    move_operations = []

def extract_volume(input_string):
    # Remove the "Vol." prefix
    stripped_string = input_string.replace("Vol.", "")

    # Check if it's a digit
    if stripped_string.isdigit():
        return int(stripped_string)
    else:
        return stripped_string
        
def sub(input_string):
    # Check if the string is empty or just spaces
    if not input_string.strip():
        # Return a default name if the string is empty or just spaces
        input_string = "N∕O"
    
    # Remove any illegal characters and replace with look-alikes
    input_string = ''.join(illegal_to_lookalike.get(char, char) for char in input_string)
    
    # Replace any trailing period (.) with a similar character '·'
    input_string = input_string.rstrip('.') + '․ ' if input_string.endswith('.') else input_string
    
    # Remove trailing spaces (if any)
    input_string = input_string.rstrip()
    
    # Modify reserved names by changing one letter (just for safety)
    for reserved_name in reserved_names:
        if input_string.upper() == reserved_name:
            input_string = input_string[0] + 'Z' + input_string[2:]  # Just an example: change 'C' to 'Z'
            break

    return input_string

def get_first_folder(directory):
    items = os.listdir(directory)
    folders = [item for item in items if os.path.isdir(os.path.join(directory, item))]
    return folders[0] if folders else None

def parse_title_with_vol(title):
    # Split the title into its components
    parts = title.split(' - ')

    # Initialize variables
    volume = chapter = chapter_part = chapter_name = 0

    if len(parts) == 2:
        # Extract volume and chapter
        vol_chap = parts[0].split(' ')
        
        # Handle missing volume
        volume = vol_chap[0].split('.')[1] if vol_chap[0].startswith('Vol.') else 0

        if len(vol_chap) > 1:
            chapter_info = vol_chap[1].split('Ch.')
            if len(chapter_info) > 1:
                chapter = int(chapter_info[1].split('.')[0])
                chapter_part = int(chapter_info[1].split('.')[1]) if '.' in chapter_info[1] else 0
            else:
                chapter = int(chapter_info[0].split('.')[0])
                chapter_part = 0  # Default chapter part
        else:
            chapter = 0  # Default chapter if missing

        # Extract chapter name and remove content after '(' or '['
        chapter_name = parts[1]
        if '(' in chapter_name:
            chapter_name = chapter_name.split('(')[0].strip()
        elif '[' in chapter_name:
            chapter_name = chapter_name.split('[')[0].strip()
    else:
        # Handle case where there's no dash (e.g., "Ch.0086 (en) [My Darling]")
        chapter_info = title.split('Ch.')
        if len(chapter_info) > 1:
            chapter_str = re.sub(r'[^\d.]', '', chapter_info[1])  # Remove non-numeric characters except dots
            chapter_parts = chapter_str.split('.')
            chapter = int(chapter_parts[0]) if chapter_parts[0] else 0
            chapter_part = int(chapter_parts[1]) if len(chapter_parts) > 1 else 0
        else:
            chapter = 0
            chapter_part = 0
            
        chapter_name = f"Chapter {chapter}"
        
    chapter_name = sub(chapter_name)

    return volume, chapter, chapter_part, chapter_name

def parse_title_with_wo_vol(title):
    # Split the title into its components
    parts = title.split(' - ')

    # Initialize variables
    chapter = chapter_part = chapter_name = None

    if len(parts) == 2:
        # Extract chapter and chapter part
        chapter_info = parts[0].split('Ch.')
        if len(chapter_info) > 1:
            chapter = int(chapter_info[1].split('.')[0])
            chapter_part = int(chapter_info[1].split('.')[1]) if '.' in chapter_info[1] else 0
        else:
            chapter = int(chapter_info[0].split('.')[0])
            chapter_part = 0  # Default chapter part

        # Extract chapter name (if present) and remove content after '(' or '['
        chapter_name = parts[1]
        if '(' in chapter_name:
            chapter_name = chapter_name.split('(')[0].strip()
        elif '[' in chapter_name:
            chapter_name = chapter_name.split('[')[0].strip()
    else:
        # Handle case where there's no dash (e.g., "Ch.0086 (en) [My Darling]")
        chapter_info = parts[0].split('Ch.')
        if len(chapter_info) > 1:
            chapter_str = re.sub(r'\D', '', chapter_info[1].split('(')[0])  # Remove non-numeric characters
            chapter = int(chapter_str.split('.')[0])  # Convert to integer
            chapter_part = int(chapter_info[1].split('.')[1]) if '.' in chapter_info[1] else 0
        else:
            chapter_str = re.sub(r'\D', '', chapter_info[0].split('(')[0])  # Remove non-numeric characters
            chapter = int(chapter_str.split('.')[0])  # Convert to integer
            chapter_part = 0  # Default chapter part

        # Default chapter name format
        chapter_name = f"Chapter {chapter}"
    chapter_name = sub(chapter_name)
    return "X", chapter, chapter_part, chapter_name
    
def parse_title(title):
    if title[0] == 'V':
        return parse_title_with_vol(title)
    else:
        return parse_title_with_wo_vol(title)
        
def copy_and_delete(path_1, path_2):
    # Ensure both paths exist
    if os.path.exists(path_1) and os.path.isdir(path_1):
        # Copy all contents of path_1 to path_2
        for item in os.listdir(path_1):
            s = os.path.join(path_1, item)
            d = os.path.join(path_2, item)
            
            if os.path.isdir(s):
                # If it's a directory, copy it recursively
                shutil.copytree(s, d)
            else:
                # If it's a file, copy it
                shutil.copy2(s, d)

def scan_series_folder(directory):
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return

    for series_folder in os.listdir(directory):
        series_path = os.path.join(directory, series_folder)
        
        if os.path.isdir(series_path):
            user_input = input(f"Scan this folder '{series_folder}'? (y/n): ").strip().lower()
            
            if user_input == 'y':
                width = input(f"length of chap string (eg. 2 = 01, 3 = 001): ")
                print(f"Contents of {series_folder}:")
                
                prev_chap_numb = -1
                prev_title = ""
                prev_title_numb = 2
                
                for subfolder in os.listdir(series_path):
                    subfolder_path = os.path.join(series_path, subfolder)
                    
                    
                    
                    
                    if os.path.isdir(subfolder_path):
                        print(f"  - {subfolder}")
                        
                    count = 1
                    for chap in os.listdir(subfolder_path):
                        chap_path = os.path.join(subfolder_path, chap)
                        current = parse_title(chap)
                        
                        
                        title_current = ""
                        
                        if not current[1] == prev_chap_numb:
                            count = 1
                        
                        title_current = current[3]
                        if prev_title == current[3]:
                            if prev_chap_numb != current[1]:
                                title_current = f"{current[3]} - {prev_title_numb}"
                                prev_title_numb+=1
                            else:
                                prev_title_numb=2
                        else:
                                prev_title_numb=2
                        
                        if prev_chap_numb == current[1]:
                            
                            if prev_title == f"Chapter {current[1]}":
                                print(f"Chapter {current[1]} == {prev_title}")
                                new_path = f"./manga/{series_folder}/{series_folder} {subfolder}/{str(current[1]).zfill(int(width))} - {title_current}/"
                                old_path = f"./manga/{series_folder}/{series_folder} {subfolder}/{str(current[1]).zfill(int(width))} - {prev_title}/"
                                move_operations.append((old_path, new_path))
                                prev_title = current[3]
                            else:
                                print(f"using {prev_title}")
                                new_path = f"./manga/{series_folder}/{series_folder} {subfolder}/{str(current[1]).zfill(int(width))} - {prev_title}/"
                        else:
                            prev_title = current[3]
                            prev_chap_numb = current[1] 
                            new_path = f"./manga/{series_folder}/{series_folder} {subfolder}/{str(current[1]).zfill(int(width))} - {title_current}/"
                        
                       
                        
                        print(f"      - {current[1]}: {title_current}")
                        
                        
                        if not os.path.exists(new_path):
                            os.makedirs(new_path)
                            
                        for file in os.listdir(chap_path):
                            page_path = os.path.join(chap_path, file)
                            
                            new_file_path = os.path.join(new_path, f"{str(count).zfill(3)}.jpg")
                            
                            shutil.copy(page_path, new_file_path)
                            
                            
                            # print(f"            - page {count} saved")
                            count+=1
                    volume_num = extract_volume(subfolder)
                    cover_path = f"./covers/{series_folder}/"
                    
                    if os.path.exists(f"{cover_path}{volume_num}.jpg"):
                        shutil.copy(f"{cover_path}{volume_num}.jpg", f"./manga/{series_folder}/{series_folder} {subfolder}/{get_first_folder(f"./manga/{series_folder}/{series_folder} {subfolder}/")}/{str("0").zfill(int(3))}.jpg")
                        print("cover copiumed")
                        print(f"from {cover_path}{volume_num}.jpg")
                        print(f"to ./manga/{series_folder}/{series_folder} {subfolder}/{get_first_folder(f"./manga/{series_folder}/{series_folder} {subfolder}/")}/{str("0").zfill(int(3))}.jpg")
                    else:
                        print(f"Cover for Vol.{volume_num} does not exist in .mange dir")
                
                remove = input("remove original dir? Y/N: ")
                
                if remove == "y":
                    shutil.rmtree(series_path)
                    print(f"{series_path} has been removed")
                else:
                    print(f"{series_path} has not been removed")
                    
                #process_move_operations()
            
            
            
            
            
            
            
            
            
            
            
            
            else:
                print(f"Skipped {series_folder}.")

# Set the path to your .output directory
output_dir = "./output"  # Change this to the appropriate path

# Run the function
scan_series_folder(output_dir)
