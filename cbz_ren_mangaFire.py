import os

# Get the directory of the script
folder_path = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder_path):
    if filename.endswith(".cbz"):
        try:
            # Split the filename into base and extension
            base, ext = os.path.splitext(filename)
            parts = base.split("_", 1)  # Split into chapter and title
            chapter_part = parts[0].strip()
            title_part = parts[1].strip() if len(parts) > 1 else ""

            # Extract chapter number
            if chapter_part.lower().startswith("chapter"):
                chapter_number = chapter_part.split(" ", 1)[1]
                # Format chapter number to 4 digits, including decimal
                if "." in chapter_number:
                    integer_part, decimal_part = chapter_number.split(".")
                    formatted_chapter = f"Ch.{int(integer_part):04d}.{decimal_part}"
                else:
                    formatted_chapter = f"Ch.{int(chapter_number):04d}"
                
                # Construct the new filename
                new_filename = f"{formatted_chapter} - {title_part} (en){ext}"

                # Rename the file
                os.rename(os.path.join(folder_path, filename),
                          os.path.join(folder_path, new_filename))
                print(f"Renamed: {filename} -> {new_filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
