import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import uuid
import os

class ModernContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Contact Book")
        self.root.geometry("1200x800")
        self.current_theme = "light"
        self.avatar_cache = {}
        
        self.setup_db()
        self.create_styles()
        self.create_gui()
        self.populate_list()
        self.toggle_theme()

    def setup_db(self):
        self.conn = sqlite3.connect('contacts_v2.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS contacts
                         (id TEXT PRIMARY KEY,
                          name TEXT NOT NULL,
                          phone TEXT NOT NULL,
                          email TEXT,
                          address TEXT,
                          avatar_path TEXT,
                          notes TEXT,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def create_styles(self):
        style = ttk.Style()
        style.theme_create("modern", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 0, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [15, 5], "font": ('Helvetica', 10)},
                "map": {"background": [("selected", "#f0f0f0")]}
            },
            "TButton": {
                "configure": {"padding": 6, "font": ('Helvetica', 10)},
                "map": {"background": [("active", "#e0e0e0")]}
            }
        })
        style.theme_use("modern")

    def create_gui(self):
        # Main container
        main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left sidebar
        left_panel = ttk.Frame(main_frame, width=300)
        main_frame.add(left_panel)

        # Search bar
        search_frame = ttk.Frame(left_panel)
        search_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(search_frame, text="🔍", width=2, command=self.search_contacts).pack(side=tk.LEFT)

        # Contact list
        self.contact_list = tk.Canvas(left_panel)
        self.scrollbar = ttk.Scrollbar(left_panel, orient=tk.VERTICAL, command=self.contact_list.yview)
        self.scrollable_frame = ttk.Frame(self.contact_list)

        self.contact_list.configure(yscrollcommand=self.scrollbar.set)
        self.contact_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.contact_list.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.contact_list.configure(
            scrollregion=self.contact_list.bbox("all")
        ))

        # Right panel
        right_panel = ttk.Frame(main_frame)
        main_frame.add(right_panel)

        # Contact details
        self.detail_frame = ttk.Frame(right_panel)
        self.detail_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Avatar section
        self.avatar_label = ttk.Label(self.detail_frame)
        self.avatar_label.pack(pady=10)
        ttk.Button(self.detail_frame, text="Upload Avatar", command=self.upload_avatar).pack()

        # Details form
        form_frame = ttk.Frame(self.detail_frame)
        form_frame.pack(pady=20, fill=tk.X)
        
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.notes_var = tk.StringVar()

        fields = [
            ("Name", self.name_var),
            ("Phone", self.phone_var),
            ("Email", self.email_var),
            ("Address", self.address_var),
            ("Notes", self.notes_var)
        ]

        for text, var in fields:
            frame = ttk.Frame(form_frame)
            frame.pack(fill=tk.X, pady=5)
            ttk.Label(frame, text=text, width=8).pack(side=tk.LEFT)
            entry = ttk.Entry(frame, textvariable=var) if text != "Notes" else tk.Text(frame, height=4)
            if text != "Notes":
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            else:
                entry.pack(fill=tk.X, expand=True)
                self.notes_entry = entry

        # Action buttons
        btn_frame = ttk.Frame(self.detail_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Save", command=self.save_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="New", command=self.new_contact).pack(side=tk.LEFT, padx=5)

        # Theme toggle
        ttk.Button(right_panel, text="🌓", command=self.toggle_theme).pack(anchor=tk.NE, padx=10)

    def create_contact_card(self, contact):
        card = ttk.Frame(self.scrollable_frame)
        card.pack(fill=tk.X, pady=2, padx=5)

        # Avatar
        avatar = ttk.Label(card, text="👤", font=('Arial', 20))
        avatar.pack(side=tk.LEFT, padx=5)

        # Contact info
        info_frame = ttk.Frame(card)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(info_frame, text=contact[1], font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(info_frame, text=contact[2]).pack(anchor=tk.W)
        
        # Bind click event
        card.bind("<Button-1>", lambda e, c=contact: self.show_contact_details(c))
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e, c=contact: self.show_contact_details(c))

    def show_contact_details(self, contact):
        self.current_contact_id = contact[0]
        self.name_var.set(contact[1])
        self.phone_var.set(contact[2])
        self.email_var.set(contact[3])
        self.address_var.set(contact[4])
        self.notes_entry.delete("1.0", tk.END)
        self.notes_entry.insert(tk.END, contact[6] if contact[6] else "")
        
        if contact[5]:
            self.load_avatar(contact[5])
        else:
            self.avatar_label.config(image='')

    def upload_avatar(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.load_avatar(file_path)
            self.avatar_cache[self.current_contact_id] = file_path

    def load_avatar(self, path):
        try:
            image = Image.open(path)
            image = image.resize((80, 80), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.avatar_label.config(image=photo)
            self.avatar_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def save_contact(self):
        if not self.name_var.get() or not self.phone_var.get():
            messagebox.showerror("Error", "Name and Phone are required")
            return

        contact_id = self.current_contact_id if hasattr(self, 'current_contact_id') else str(uuid.uuid4())
        avatar_path = self.avatar_cache.get(contact_id, None)

        self.c.execute('''INSERT OR REPLACE INTO contacts 
                        (id, name, phone, email, address, avatar_path, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                     (contact_id,
                      self.name_var.get(),
                      self.phone_var.get(),
                      self.email_var.get(),
                      self.address_var.get(),
                      avatar_path,
                      self.notes_entry.get("1.0", tk.END)))
        self.conn.commit()
        self.populate_list()
        self.new_contact()

    def delete_contact(self):
        if hasattr(self, 'current_contact_id'):
            if messagebox.askyesno("Confirm Delete", "Delete this contact permanently?"):
                self.c.execute("DELETE FROM contacts WHERE id=?", (self.current_contact_id,))
                self.conn.commit()
                self.populate_list()
                self.new_contact()

    def new_contact(self):
        self.current_contact_id = None
        self.name_var.set('')
        self.phone_var.set('')
        self.email_var.set('')
        self.address_var.set('')
        self.notes_entry.delete("1.0", tk.END)
        self.avatar_label.config(image='')

    def populate_list(self, search_term=None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        query = "SELECT * FROM contacts"
        params = ()
        if self.search_var.get():
            query += " WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?"
            params = (f'%{self.search_var.get()}%', 
                     f'%{self.search_var.get()}%',
                     f'%{self.search_var.get()}%')
        
        self.c.execute(query, params)
        for contact in self.c.fetchall():
            self.create_contact_card(contact)

    def search_contacts(self):
        self.populate_list()

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        bg = "#2d2d2d" if self.current_theme == "dark" else "#ffffff"
        fg = "#ffffff" if self.current_theme == "dark" else "#000000"
        
        self.root.config(bg=bg)
        self.detail_frame.config(style="TFrame")
        style = ttk.Style()
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("TEntry", fieldbackground=bg, foreground=fg)
        style.configure("TButton", background=bg, foreground=fg)
        style.configure("TCanvas", background=bg)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernContactBook(root)
    root.mainloop()