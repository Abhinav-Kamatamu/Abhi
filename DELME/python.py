import os
import json
from datetime import datetime
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import qrcode
from PIL import ImageTk, Image

class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fernet QR Generator")
        self.history_file = "qr_history.json"
        self.qr_dir = "qr_codes"
        self.history = []
        
        os.makedirs(self.qr_dir, exist_ok=True)
        self.load_history()
        self.create_main_ui()

    def create_main_ui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        btn_style = {'width': 20, 'padding': 10}
        ttk.Button(main_frame, text="Generate New QR", command=self.generate_new_qr, **btn_style).pack(pady=5)
        ttk.Button(main_frame, text="View Recent QR", command=self.view_recent, **btn_style).pack(pady=5)
        ttk.Button(main_frame, text="View History", command=self.show_history, **btn_style).pack(pady=5)
        
    def generate_fernet_key(self):
        return Fernet.generate_key().decode()
    
    def get_qr_name(self):
        name = simpledialog.askstring("QR Name", "Enter a name for this QR code:")
        return name.strip() if name else "Unnamed"
    
    def generate_qr_code(self, key, name):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(key)
        qr.make(fit=True)
        
        clean_name = "".join([c if c.isalnum() else "_" for c in name])[:30]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.qr_dir, f"{clean_name}_{timestamp}.png")
        qr.make_image(fill_color="black", back_color="white").save(filename)
        return filename
    
    def save_to_history(self, name, key, filename):
        self.history.insert(0, {
            'name': name,
            'key': key,
            'filename': filename,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'time': datetime.now().strftime("%H:%M:%S")
        })
        self.save_history()
    
    def generate_new_qr(self):
        name = self.get_qr_name()
        if name is None: 
            return
        key = self.generate_fernet_key()
        filename = self.generate_qr_code(key, name)
        self.save_to_history(name, key, filename)
        messagebox.showinfo("Success", "New QR code generated!")
        self.view_qr(filename)
    
    def view_recent(self):
        if not self.history:
            messagebox.showwarning("Warning", "No QR codes generated yet!")
            return
        self.view_qr(self.history[0]['filename'])
    
    def view_qr(self, filename):
        viewer = tk.Toplevel(self.root)
        viewer.title("QR Code Viewer")
        
        try:
            img = Image.open(filename).resize((400, 400), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            canvas = tk.Canvas(viewer, width=400, height=450)
            canvas.pack()
            canvas.create_image(0, 0, anchor='nw', image=photo)
            
            basename = os.path.basename(filename)
            canvas.create_text(200, 410, text=f"Name: {basename[:-4]}", anchor='center')
            
            key_info = next((item for item in self.history if item['filename'] == filename), None)
            if key_info:
                canvas.create_text(200, 430, text=f"Key: {key_info['key'][:10]}...", anchor='center')
            
            canvas.image = photo
            ttk.Button(viewer, text="Close", command=viewer.destroy).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display QR: {str(e)}")
    
    def show_history(self):
        history_win = tk.Toplevel(self.root)
        history_win.title("QR History")
        
        frame = ttk.Frame(history_win, padding=10)
        frame.pack(fill='both', expand=True)
        
        tree = ttk.Treeview(frame, columns=('name', 'date', 'time'), show='headings')
        tree.heading('name', text='Name')
        tree.heading('date', text='Date')
        tree.heading('time', text='Time')
        tree.column('name', width=150)
        tree.column('date', width=100)
        tree.column('time', width=80)
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        for entry in self.history:
            tree.insert('', 'end', values=(entry['name'], entry['date'], entry['time']), tags=(entry['filename'],))
        
        btn_frame = ttk.Frame(history_win)
        btn_frame.pack(fill='x', padx=10, pady=5)
        ttk.Button(btn_frame, text="View Selected", command=lambda: self.view_selected(tree)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=lambda: self.delete_entry(tree)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Close", command=history_win.destroy).pack(side='right', padx=5)
    
    def view_selected(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No item selected!")
            return
        self.view_qr(tree.item(selected[0], 'tags')[0])
    
    def delete_entry(self, tree):
        selected = tree.selection()
        if not selected:
            return
        filename = tree.item(selected[0], 'tags')[0]
        try:
            os.remove(filename)
            self.history = [entry for entry in self.history if entry['filename'] != filename]
            self.save_history()
            tree.delete(selected[0])
            messagebox.showinfo("Success", "Entry deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete: {str(e)}")
    
    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load history: {str(e)}")
    
    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()
