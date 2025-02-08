import os
import shutil
from collections import defaultdict

def get_subdirs(base_dir):
    return [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

def parse_folder_name(name):
    parts = name.split()
    if len(parts) < 3:
        return None, None  # Ignore folders that don't fit the pattern
    key = " ".join(parts[:2])  # "Vol.XX Ch.XXXXX"
    translator = None
    if "[" in name and "]" in name:
        translator = name[name.rfind("[") + 1:name.rfind("]")]
    return key, translator

def extract_chapter_number(name):
    parts = name.split()
    if len(parts) >= 3 and parts[1].startswith("Ch."):
        try:
            return float(parts[1][3:])  # Handle both integers and decimals
        except ValueError:
            return None
    return None

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    subdirs = get_subdirs(base_dir)
    
    chapter_groups = defaultdict(list)
    chapter_numbers = set()
    kept_chapters = {}
    delete_log = []
    
    for folder in subdirs:
        key, translator = parse_folder_name(folder)
        chapter_num = extract_chapter_number(folder)
        if chapter_num is not None:
            chapter_numbers.add(chapter_num)
        if key:
            folder_path = os.path.join(base_dir, folder)
            file_count = len(os.listdir(folder_path))
            chapter_groups[key].append((folder, file_count, translator))
    
    for key, folders in chapter_groups.items():
        if len(folders) > 1:
            # Sort folders by file count (descending), then name (to keep a consistent result)
            folders.sort(key=lambda x: (-x[1], x[0]))
            
            # Keep the one with the most files, remove the rest
            kept_folder, kept_file_count, kept_translator = folders[0]
            kept_chapters[key] = kept_translator
            
            for folder, file_count, translator in folders[1:]:
                delete_reason = "has less pages ({} < {})".format(file_count, kept_file_count)
                
                # If overlapping chapter numbers, check translator consistency
                if extract_chapter_number(folder) is not None:
                    base_chapter = int(extract_chapter_number(folder))
                    if base_chapter in kept_chapters and kept_chapters[base_chapter] != translator:
                        delete_reason = "it has a different translator than previously kept chapter ({})".format(translator)
                
                folder_path = os.path.join(base_dir, folder)
                shutil.rmtree(folder_path)
                delete_log.append(f"Deleting {folder}, {delete_reason}")
    
    # Check for missing numbers
    chapter_numbers = sorted(chapter_numbers)
    missing_numbers = []
    
    for num in range(int(chapter_numbers[0]), int(chapter_numbers[-1]) + 1):
        if num not in chapter_numbers and not any(str(num) in str(ch) for ch in chapter_numbers):
            missing_numbers.append(num)
    
    for num in range(int(chapter_numbers[0]), int(chapter_numbers[-1]) + 1):
        if num in missing_numbers:
            print(f"no. {num}")
        else:
            print(num)
    
    if missing_numbers:
        print("\nMissing chapters:")
        for num in missing_numbers:
            print(num)
    else:
        print("\nNo missing chapter numbers.")
    
    # Print deletion log at the end
    if delete_log:
        print("\nDeletion Log:")
        for log in delete_log:
            print(log)

if __name__ == "__main__":
    main()
