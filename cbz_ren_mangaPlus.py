import os

# Get the directory of the script
folder_path = os.path.dirname(os.path.abspath(__file__))

# Keep track of the previous chapter number
previous_chapter = None

for filename in sorted(os.listdir(folder_path)):  # Sort to process files in order
    if filename.startswith("MANGA Plus") and filename.endswith(".cbz"):
        try:
            # Split the filename into base and extension
            base, ext = os.path.splitext(filename)
            parts = base.split("_", 2)  # Split into prefix, chapter info, and title (if available)
            chapter_info = parts[1].strip()  # Example: "#007 - Chapter 7"
            title_part = parts[2].strip() if len(parts) > 2 else "N⁄A"  # Use "N/A" if no title exists

            # Extract the chapter number
            if chapter_info.startswith("#"):
                chapter_number = chapter_info[1:].split(" -")[0].strip()  # Extract numeric part after '#'
                
                # Handle "ex" chapters
                if chapter_number.lower() == "ex":
                    if previous_chapter is not None:
                        # Increment the previous chapter by 0.1
                        chapter_number = f"{previous_chapter + 0.1:.1f}"
                    else:
                        # If there's no previous chapter, skip this file
                        print(f"Skipping {filename}: No previous chapter found for 'ex'.")
                        continue
                else:
                    # Convert to integer for regular chapters
                    chapter_number = int(chapter_number)
                
                # Format chapter number
                if isinstance(chapter_number, float):
                    formatted_chapter = f"Ch.{int(chapter_number):04d}.{str(chapter_number).split('.')[1]}"
                else:
                    formatted_chapter = f"Ch.{int(chapter_number):04d}"
                
                # Update the previous chapter tracker
                previous_chapter = float(chapter_number)

                # Construct the new filename
                new_filename = f"{formatted_chapter} - {title_part} (en){ext}"

                # Build the full file paths
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_filename)

                # Rename the file
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    else:
        print(f"Skipping {filename}: Does not start with 'MANGA Plus'.")
