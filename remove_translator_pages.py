import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ChapterPageViewer:
    def __init__(self, root, folder):
        self.root = root
        self.folder = folder
        self.chapters = self.get_chapters()
        self.selected_pages = set()
        self.images = {}
        self.current_translator = None
        
        self.canvas = tk.Canvas(root)
        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas)
        
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)
        
        # Row 1: Select 1st to 5th from beginning and 1st to 5th from end
        row_1 = tk.Frame(self.button_frame)
        row_1.pack(fill="x")
        for i in range(5):
            tk.Button(row_1, text=f"Select {i+1}st Pages", command=lambda i=i: self.mass_select(i)).pack(side="left", padx=5)
        for i in range(5, 0, -1):  # Start at 5, decrement to 1
            tk.Button(row_1, text=f"Select {i} from End", command=lambda i=i: self.mass_select(-i)).pack(side="left", padx=5)

        
        # Row 2: Deselect 1st to 5th from beginning and 1st to 5th from end
        row_2 = tk.Frame(self.button_frame)
        row_2.pack(fill="x")
        for i in range(5):
            tk.Button(row_2, text=f"Deselect {i+1}st Pages", command=lambda i=i: self.mass_deselect(i)).pack(side="left", padx=5)
        for i in range(5, 0, -1):  # Start at 5, decrement to 1
            tk.Button(row_2, text=f"Deselect {i} from End", command=lambda i=i: self.mass_deselect(-i)).pack(side="left", padx=5)

        
        # Row 3: Translator buttons
        self.translator_buttons = tk.Frame(root)
        self.translator_buttons.pack(pady=5)
        
        # Row 4: Delete Selected button
        self.delete_button = tk.Button(root, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack(pady=5)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.load_translator_buttons()
    
    def get_chapters(self):
        chapters = {}
        pattern = re.compile(r"(Vol\.\d+ )?Ch\.(\d+(\.\d+)?)")
        
        for folder in sorted(os.listdir(self.folder)):
            match = pattern.search(folder)
            if match:
                chapter_path = os.path.join(self.folder, folder)
                if os.path.isdir(chapter_path):
                    images = sorted([f for f in os.listdir(chapter_path) if f.lower().endswith((".jpg", ".png", ".jpeg"))])
                    if images:
                        translator = re.search(r"\[(.*?)\]", folder)
                        translator = translator.group(1) if translator else "Unknown"
                        
                        # If translator has been processed before, get the count of their chapters
                        translator_parts = [key for key in chapters.keys() if key.startswith(translator)]
                        chapter_count = sum(len(chapters[part]) for part in translator_parts)
                        
                        # Calculate the part number based on the total number of chapters processed
                        part_number = (chapter_count // 80) + 1
                        new_translator_name = f"{translator} Part {part_number}"
                        
                        # Append the chapter to the corresponding translator part
                        if new_translator_name not in chapters:
                            chapters[new_translator_name] = []
                        chapters[new_translator_name].append((chapter_path, images[:5] + [None] + images[-5:]))
        
        return chapters


    
    def load_translator_buttons(self):
        for widget in self.translator_buttons.winfo_children():
            widget.destroy()
        
        for translator in self.chapters.keys():
            tk.Button(self.translator_buttons, text=f"{translator} ({len(self.chapters[translator])})", 
                      command=lambda t=translator: self.display_chapters(t)).pack(side="left", padx=5)
    
    def display_chapters(self, translator=None):
        self.current_translator = translator
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        if translator and translator in self.chapters:
            tk.Label(self.frame, text=translator, font=("Arial", 14, "bold")).pack(anchor="w", pady=10)
            for chapter, images in self.chapters[translator]:
                row_frame = tk.Frame(self.frame)
                row_frame.pack(fill="x", pady=5)
                for i, image in enumerate(images):
                    if image is None:
                        tk.Label(row_frame, text="...").pack(side="left", padx=10)
                    else:
                        self.add_image(chapter, image, row_frame, i)
    
    def add_image(self, chapter, image_name, parent, position):
        image_path = os.path.join(chapter, image_name)
        img = Image.open(image_path)
        img.thumbnail((200, 300))
        photo = ImageTk.PhotoImage(img)
        
        img_label = tk.Label(parent, image=photo, highlightbackground="black", highlightthickness=15)
        img_label.image = photo
        img_label.pack(side="left", padx=5 if position < 5 else 15)
        
        img_label.bind("<Button-1>", lambda e, path=image_path, lbl=img_label: self.toggle_selection(path, lbl))
        img_label.bind("<Button-3>", lambda e, path=image_path: self.preview_image(path))
        
        self.images[image_path] = img_label
    
    def toggle_selection(self, image_path, label):
        if image_path in self.selected_pages:
            self.selected_pages.remove(image_path)
            label.config(highlightbackground="black")
        else:
            self.selected_pages.add(image_path)
            label.config(highlightbackground="red")
        
        print(f"Toggled: {image_path}")
        print(f"Total selected: {len(self.selected_pages)}")
    
    def mass_select(self, index):
        if self.current_translator:
            for chapter, images in self.chapters[self.current_translator]:
                if abs(index) < len(images):
                    path = os.path.join(chapter, images[index])
                    self.selected_pages.add(path)
                    if path in self.images:
                        self.images[path].config(highlightbackground="red")
        print(f"Total selected: {len(self.selected_pages)}")
    
    def mass_deselect(self, index):
        if self.current_translator:
            for chapter, images in self.chapters[self.current_translator]:
                if abs(index) < len(images):
                    path = os.path.join(chapter, images[index])
                    self.selected_pages.discard(path)
                    if path in self.images:
                        self.images[path].config(highlightbackground="black")
        print(f"Total selected: {len(self.selected_pages)}")
    
    def delete_selected(self):
        if not self.selected_pages:
            messagebox.showinfo("No Selection", "No pages selected for deletion.")
            return
        
        confirm = messagebox.askyesno("Confirm Deletion", f"Delete {len(self.selected_pages)} selected pages?")
        if confirm:
            for page in self.selected_pages:
                os.remove(page)
            messagebox.showinfo("Deleted", "Selected pages have been deleted.")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chapter Page Viewer")
    
    folder_path = "."
    app = ChapterPageViewer(root, folder_path)
    root.mainloop()
