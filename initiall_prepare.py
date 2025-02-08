import os
import shutil
from PIL import Image, ImageOps, ImageChops

def get_user_input(prompt, allowed_values=None):
    while True:
        response = input(prompt).strip()
        if allowed_values is None or response in allowed_values:
            return response
        print("Invalid input. Please try again.")

def crop_borders(img):
    # Detect border color dynamically
    img = img.convert('RGB')
    border_color = get_border_color(img)
    
    # Create a background with the detected border color
    bg = Image.new(img.mode, img.size, border_color)

    # Find bounding box where the image differs from the border color
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    # Crop or return the original image
    cropped_img = img.crop(bbox)
    return cropped_img, border_color

def get_border_color(img):
    # Ensure the image is in RGB mode

    width, height = img.size
    top_border = img.crop((0, 0, width, 1)).getdata()
    bottom_border = img.crop((0, height - 1, width, height)).getdata()
    left_border = img.crop((0, 0, 1, height)).getdata()
    right_border = img.crop((width - 1, 0, width, height)).getdata()

    # Combine all border pixels and find the most common color
    border_pixels = list(top_border) + list(bottom_border) + list(left_border) + list(right_border)
    most_common_color = max(set(border_pixels), key=border_pixels.count)
    return most_common_color

def adjust_ratio(img, target_ratio, border_color):
    target_width, target_height = target_ratio
    width, height = img.size
    current_ratio = width / height

    if current_ratio < target_width / target_height:
        # Add border to width
        new_width = int(height * (target_width / target_height))
        new_img = Image.new("RGB", (new_width, height), border_color)
        new_img.paste(img, ((new_width - width) // 2, 0))
    else:
        # Add border to height
        new_height = int(width / (target_width / target_height))
        new_img = Image.new("RGB", (width, new_height), border_color)
        new_img.paste(img, (0, (new_height - height) // 2))

    return new_img

def process_chapter(input_dir, output_dir, chapter_name, volume_name, page_start, target_ratio):
    chapter_path = os.path.join(output_dir, volume_name, chapter_name)
    os.makedirs(chapter_path, exist_ok=True)
    adjust_ratio_bool = bool
    chapter_parts = sorted([d for d in os.listdir(input_dir) if d.startswith(chapter_name)])
    page_number = page_start

    for part in chapter_parts:
        part_path = os.path.join(input_dir, part)
        if not os.path.isdir(part_path):
            continue

        for file in sorted(os.listdir(part_path)):
            if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue

            img_path = os.path.join(part_path, file)
            
            try:
                img = Image.open(img_path)
                img, border_color = crop_borders(img)
                # img = adjust_ratio(img, target_ratio, border_color)

                output_file = os.path.join(chapter_path, f"{str(page_number).zfill(3)}.jpg")
                img.save(output_file)
                print(f"Processed {volume_name} {chapter_name[0]}{chapter_name[1]}{chapter_name[2]}{chapter_name[3]}{chapter_name[4]}{chapter_name[5]}{chapter_name[6]} Page {page_number}")
                page_number += 1
                
            except Exception as e:
                print(f"Error processing {img_path}: {e}")

    return page_number

def assign_volumes(chapters):
    volume_assignments = {}
    unassigned_volume_start = None

    # Function to detect and return the volume format
    def detect_volume_format(chapters):
        # Try to detect volume format by checking existing volume numbers
        volume_format = None
        for chapter in chapters:
            if "Vol." in chapter:
                vol_number = chapter.split("Vol.")[1].split()[0]
                # Check if the volume number has leading zeros
                if vol_number.isdigit():
                    # Store the number of digits in the volume number
                    if volume_format is None:
                        volume_format = len(vol_number)  # Detect the length of digits
                    elif volume_format != len(vol_number):
                        raise ValueError("Volume number format is inconsistent.")
        return volume_format or 1  # Default to no leading zeros if not found

    # Step 1: Ask when unassigned chapters start
    while True:
        unassigned_start = get_user_input("Enter chapter number where unassigned volume starts (e.g., 123): ")
        if unassigned_start.isdigit():
            unassigned_volume_start = int(unassigned_start)
            break
        else:
            print("Invalid input. Please enter a valid chapter number.")

    # Step 2: Automatically assign chapters based on folder names
    volume_format = detect_volume_format(chapters)  # Get the volume format
    for chapter in chapters:
        if "Vol." in chapter:
            vol_number = chapter.split("Vol.")[1].split()[0]
            volume_assignments[chapter] = f"Vol.{vol_number.zfill(volume_format)}"  # Ensure the format matches
        else:
            # Extract chapter number, ignoring decimals
            try:
                chapter_number = int(chapter.split("Ch.")[1].split()[0].split('.')[0])
                if chapter_number >= unassigned_volume_start:
                    volume_assignments[chapter] = f"Vol.X"  # Assign default value for unassigned
            except ValueError:
                print(f"Skipping invalid chapter format: {chapter}")

    # Step 3: Prompt user to assign missing chapters
    for chapter in chapters:
        if chapter not in volume_assignments:
            while True:
                vol = get_user_input(f"Assign volume for chapter {chapter} (e.g., 1, 2, etc.): ")
                if vol.isdigit():
                    volume_assignments[chapter] = f"Vol.{vol.zfill(volume_format)}"  # Adjust user input to match format
                    break
                else:
                    print("Invalid input. Please enter a valid volume number.")

    return volume_assignments


def process_series(series_name, input_dir, output_dir, target_ratio):
    print(f"Processing series: {series_name}")
    series_input_dir = os.path.join(input_dir, series_name)
    series_output_dir = os.path.join(output_dir, series_name)
    os.makedirs(series_output_dir, exist_ok=True)
    ### 
    chapters = sorted([d for d in os.listdir(series_input_dir) if os.path.isdir(os.path.join(series_input_dir, d))])
    volume_assignments = assign_volumes(chapters)
    
    for chapter, volume in volume_assignments.items():
        volume_path = os.path.join(series_output_dir, volume)
        os.makedirs(volume_path, exist_ok=True)
        process_chapter(series_input_dir, series_output_dir, chapter, volume, 1, target_ratio)
    
    

if __name__ == "__main__":
    input_dir = "./input"
    output_dir = "./output"
    covers_dir = "./covers"

    target_ratio = (1836, 2448)

    series_list = sorted([d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))])
    
    
    for series in series_list:
        process = get_user_input(f"Process series {series}? (y/n): ", ["y", "n"])
        if process == "y":
            process_series(series, input_dir, output_dir, target_ratio)
