import os
from PIL import Image
from collections import Counter

def within_tolerance(pixel, margin_color, tolerance):
    return sum((p - mc)**2 for p, mc in zip(pixel, margin_color)) <= tolerance**2

def get_margin_color(image, margin_color):
    if margin_color:
        # If margin_color is provided, convert hex to RGB
        return tuple(int(margin_color[i:i+2], 16) for i in (1, 3, 5))
    
    # Get image dimensions
    width, height = image.size
    
    # Sample colors from all four corners
    corners = [
        image.getpixel((0, 0))[:3],          # Top-left
        image.getpixel((width - 1, 0))[:3],  # Top-right
        image.getpixel((0, height - 1))[:3], # Bottom-left
        image.getpixel((width - 1, height - 1))[:3]  # Bottom-right
    ]
    
    # Find the most frequent corner color
    color_counter = Counter(corners)
    most_common_color, most_common_count = color_counter.most_common(1)[0]
    
    if most_common_count >= 2:
        # If at least two corners have the same color, use that as the margin color
        return most_common_color
    else:
        # If all corners are different, calculate the average color
        avg_color = tuple(
            sum(channel) // len(corners) for channel in zip(*corners)
        )
        
        # Determine if the average color is closer to white or black
        avg_brightness = sum(avg_color) / 3
        is_closer_to_white = avg_brightness > 127.5
        
        # Find the corner color closest to white or black based on the average
        target_color = (255, 255, 255) if is_closer_to_white else (0, 0, 0)
        closest_corner = min(
            corners,
            key=lambda color: sum((c - tc) ** 2 for c, tc in zip(color, target_color))
        )
        
        return closest_corner

def find_crop_bounds(image, margin_color, tolerance):
    width, height = image.size
    pixels = image.load()
    
    # Top
    top = 0
    for y in range(height):
        row = [pixels[x, y] for x in range(width)]
        if any(not within_tolerance(pixel, margin_color, tolerance) for pixel in row):
            top = y
            break
    
    # Bottom
    bottom = height - 1
    for y in range(height-1, -1, -1):
        row = [pixels[x, y] for x in range(width)]
        if any(not within_tolerance(pixel, margin_color, tolerance) for pixel in row):
            bottom = y
            break
    
    # Left
    left = 0
    for x in range(width):
        col = [pixels[x, y] for y in range(height)]
        if any(not within_tolerance(pixel, margin_color, tolerance) for pixel in col):
            left = x
            break
    
    # Right
    right = width - 1
    for x in range(width-1, -1, -1):
        col = [pixels[x, y] for y in range(height)]
        if any(not within_tolerance(pixel, margin_color, tolerance) for pixel in col):
            right = x
            break
    
    return (left, top, right + 1, bottom + 1)

def process_image(image_path, margin_color, tolerance):
    try:
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            margin_rgb = get_margin_color(img, margin_color)
            crop_box = find_crop_bounds(img, margin_rgb, tolerance)
            
            cropped_img = img.crop(crop_box)
            
            # Overwrite the original image with the trimmed version
            cropped_img.save(image_path)
            print(f"Processed and overwritten: {image_path}")
            
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")

def find_images(directory):
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')
    image_paths = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                image_paths.append(os.path.join(root, file))
    
    return image_paths

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Trim margins from images in current directory and subdirectories')
    parser.add_argument('--margin-color', type=str, help='Hex color code for margins (e.g., #FFFFFF)')
    parser.add_argument('--tolerance', type=int, default=10,
                       help='Color tolerance (0-255, default: 10)')
    
    args = parser.parse_args()
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all images in the script directory and subdirectories
    image_paths = find_images(script_dir)
    
    if not image_paths:
        print("No images found in the current directory or subdirectories.")
        return
    
    print(f"Found {len(image_paths)} images to process.")
    
    # Process each image
    for image_path in image_paths:
        process_image(image_path, args.margin_color, 150)
    
    print("Processing complete.")

if __name__ == "__main__":
    main()