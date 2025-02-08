# Manga Processing Scripts

A collection of Python scripts for organizing, renaming, and processing manga chapters downloaded using tools like **Mihon** or **HakuNeko**. These scripts help in preparing manga files with **MangaDex-compatible naming** and volume structuring.

## 📂 Folder Structure

```
📁 manga-parser
│--📁 input/           # Raw downloaded manga files
│--📁 output/          # Processed chapters
│--📁 covers/          # Cover images for volumes
│--📁 manga/           # Final structured manga files
│--📝 README.md
│--🐍 cbz_ren_mangaFire.py
│--🐍 cbz_ren_mangaPlus.py
│--🐍 cbz_unpack.py
│--🐍 clean_up_folders.py
│--🐍 check4missing_and_rm_overlapping_chapters.py
│--🐍 remove_translator_pages.py
│--🐍 initial_prepare.py
│--🐍 last_step.py
```
## 🛠 Requirements
1. **Python**  
	Download and install it from the official Python website:  
   [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Download Requirements**
	```pip install -r requirements.txt```
	
---

## 🚀 How to Use

1. **Download your manga chapters** using tools like **HakuNeko** or **Mihon**.

2. **In the `input/` folder**, create a new folder with the same name as your manga series, and place the individual chapter folders inside.

3. **Rename chapter files** to match the **MangaDex format**:
    - For **Mihon**-downloads:
      - **`Vol.XX Ch.XXXX - <title> (<lan>) [<translator>]`**
      - Example: `Vol.01 Ch.0001 - Naruto (en) [VIZ]`
    - For **MangaReader/MangaFire format**:
      - **`Chapter X_ <title>.cbz`**
      - Example: `Chapter 1_ Naruto.cbz`
    - For **MangaPlus format**:
      - **`MANGA Plus_#XXX - Chapter X_ <title>.cbz`**
      - Example: `MANGA Plus_#001 - Chapter 1_ Naruto.cbz`

    You can change the names using the **`cbz_ren_mangaFire.py`** or **`cbz_ren_mangaPlus.py`** scripts (for MangaReader, use the MangaFire script).

4. **Unpack `.cbz` files** using **`cbz_unpack.py`**.  
    The `.cbz` files will remain in place but can be deleted manually after extraction.

5. **(Optional)** Check for missing or overlapping chapters with **`check4missing_and_rm_overlapping_chapters.py`**.

6. **(Optional)** Use **`remove_translator_pages.py`** to delete translator-added pages:
    1. Open the app.
    2. Go to the translator sections and select the pages you wish to delete.
    3. Delete unwanted pages.

7. **(Optional)** Run **`clean_up_folders.py`** to remove non-image files and empty folders.

8. **(Optional)** Trim page margins with **`trimm_pages.py`** (advanced feature).

9. Run **`initial_prepare.py`** to:
    - Perform light margin removal.
    - The program will ask whether to process each series.
    - If a chapter is unassigned to a volume, specify the number of the first chapter with no volume. (this will not override volume info in folder names, so write "1" to put all chapter with no volume as vol X)
    - The program may ask for volume assignments for chapters it cannot automatically determine.

10. Run **`last_step.py`** to:
    - Wrap everything into volumes.
    - Rename chapters.
    - Add cover images from the `covers/` folder (if covers are available).
    - The program will ask if you'd like to process each series and confirm the number of chapters per volume (e.g., `2` for <99 chapters, `3` for <999 chapters, etc.).
    - The final output will be in the `manga/` folder.
    - You’ll also be asked whether to delete the original directory in `output/`.

---

(yes, i did use chat gpt here, but no, its not braindead copy paste from it.)



