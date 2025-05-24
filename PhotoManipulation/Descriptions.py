import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class ScrollableImage(tk.Frame):
    def __init__(self, master, text="", width=300, height=300):
        super().__init__(master)
        ttk.Label(self, text=text).pack(anchor=tk.W)
        self.canvas_width = width
        self.canvas_height = height
        self.canvas = tk.Canvas(self, width=width, height=height, bg='grey')
        hbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        vbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.image_id = None
        self.img = None

    def show_image(self, pil_image):
        # Scale to fit canvas while preserving aspect ratio
        iw, ih = pil_image.size
        cw, ch = self.canvas_width, self.canvas_height
        scale = min(cw/iw, ch/ih, 1.0)
        new_size = (int(iw*scale), int(ih*scale))
        disp_image = pil_image.resize(new_size, Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(disp_image)
        self.canvas.config(scrollregion=(0,0,new_size[0], new_size[1]))
        if self.image_id:
            self.canvas.delete(self.image_id)
        x = (cw - new_size[0]) // 2 if new_size[0] < cw else 0
        y = (ch - new_size[1]) // 2 if new_size[1] < ch else 0
        self.image_id = self.canvas.create_image(x, y, anchor='nw', image=self.img)

class ImageCombinerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Combiner")
        self.geometry("1000x700")

        cwd = os.getcwd()
        self.images_dir = os.path.join(cwd, "images")
        self.desc_dir = os.path.join(cwd, "descriptions")
        self.final_dir = os.path.join(cwd, "Final")
        os.makedirs(self.final_dir, exist_ok=True)

        self.selected_img = None
        self.selected_desc = None
        self.combined_img = None

        self._build_ui()
        self._load_lists()

    def _build_ui(self):
        left = ttk.Frame(self)
        left.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        right = ttk.Frame(self)
        right.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        ttk.Label(left, text="/images").pack(anchor='w')
        self.img_list = tk.Listbox(left)
        self.img_list.pack(fill='both', expand=True)
        self.img_list.bind('<<ListboxSelect>>', self._on_img_select)

        ttk.Label(left, text="/descriptions").pack(anchor='w', pady=(10,0))
        self.desc_list = tk.Listbox(left)
        self.desc_list.pack(fill='both', expand=True)
        self.desc_list.bind('<<ListboxSelect>>', self._on_desc_select)

        previews = ttk.Frame(right)
        previews.pack(fill='both', expand=True)
        self.img_preview = ScrollableImage(previews, text="Image preview")
        self.img_preview.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.desc_preview = ScrollableImage(previews, text="Description preview")
        self.desc_preview.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.combined_preview = ScrollableImage(previews, text="Combined preview")
        self.combined_preview.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky='nsew')
        previews.rowconfigure(0, weight=1)
        previews.rowconfigure(1, weight=1)
        previews.columnconfigure(1, weight=1)

        control = ttk.Frame(right)
        control.pack(fill='x', pady=10)
        self.orientation = tk.StringVar(value='LR')
        ttk.Radiobutton(control, text="Left-Right", variable=self.orientation, value='LR').pack(side='left', padx=5)
        ttk.Radiobutton(control, text="Top-Down", variable=self.orientation, value='TD').pack(side='left', padx=5)
        ttk.Button(control, text="Preview", command=self._preview).pack(side='right', padx=5)
        ttk.Button(control, text="Save", command=self._save).pack(side='right')

    def _load_lists(self):
        self.img_list.delete(0, 'end')
        self.desc_list.delete(0, 'end')
        for f in sorted(os.listdir(self.images_dir)):
            if f.lower().endswith('.png'):
                self.img_list.insert('end', f)
        for f in sorted(os.listdir(self.desc_dir)):
            if f.lower().endswith('.png'):
                self.desc_list.insert('end', f)

    def _on_img_select(self, _):
        sel = self.img_list.curselection()
        if not sel: return
        fn = self.img_list.get(sel[0])
        self.selected_img = os.path.join(self.images_dir, fn)
        im = Image.open(self.selected_img)
        self.img_preview.show_image(im)

    def _on_desc_select(self, _):
        sel = self.desc_list.curselection()
        if not sel: return
        fn = self.desc_list.get(sel[0])
        self.selected_desc = os.path.join(self.desc_dir, fn)
        im = Image.open(self.selected_desc)
        self.desc_preview.show_image(im)

    def _create(self):
        im1 = Image.open(self.selected_img)
        im2 = Image.open(self.selected_desc)
        # Scale description to match primary dimension
        if self.orientation.get() == 'LR':
            # match height
            target_h = im1.height
            scale = target_h / im2.height
            new_w = int(im2.width * scale)
            im2 = im2.resize((new_w, target_h), Image.ANTIALIAS)
            w, h = im1.width + im2.width, target_h
        else:
            # match width
            target_w = im1.width
            scale = target_w / im2.width
            new_h = int(im2.height * scale)
            im2 = im2.resize((target_w, new_h), Image.ANTIALIAS)
            w, h = target_w, im1.height + im2.height
        combined = Image.new('RGB', (w, h), (0, 0, 0))
        if self.orientation.get() == 'LR':
            combined.paste(im1, (0, 0))
            combined.paste(im2, (im1.width, 0))
        else:
            combined.paste(im1, (0, 0))
            combined.paste(im2, (0, im1.height))
        return combined

    def _preview(self):
        if not self.selected_img or not self.selected_desc:
            messagebox.showwarning("Missing", "Select both first.")
            return
        self.combined_img = self._create()
        self.combined_preview.show_image(self.combined_img)

    def _save(self):
        if self.combined_img is None:
            messagebox.showwarning("No preview", "Preview before save.")
            return
        name = os.path.basename(self.selected_img)
        path = os.path.join(self.final_dir, name)
        self.combined_img.save(path)
        messagebox.showinfo("Saved", f"Saved to {path}")
        self.combined_img = None
        self.combined_preview.canvas.delete('all')
        self._load_lists()

if __name__ == '__main__':
    ImageCombinerApp().mainloop()

