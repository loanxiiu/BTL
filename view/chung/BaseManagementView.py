import tkinter as tk
from tkinter import messagebox, ttk


class BaseManagementView:
    def __init__(self, root, title, header_text):
        self.root = root
        self.root.title(title)
        self.root.geometry("1920x1080")

        from view.chung.Header import Header
        from view.chung.Sidebar import Sidebar

        self.sidebar = Sidebar(self.root)
        self.header = Header(self.root, header_text)

        self.entries = {}
        self.list_view = None
        self.entry_search = None
        self.controller = None

    def _validate_and_get_form_values(self):
        values = {k: v.get() for k, v in self.entries.items()}
        if not all(values.values()):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return None
        return values

    def create_form_fields(self, parent, fields, bg_color="white"):
        form_frame = tk.Frame(parent, bg=bg_color)
        for i, (key, label) in enumerate(fields.items()):
            tk.Label(form_frame, text=label + ":", bg=bg_color).grid(row=i, column=0)
            entry = tk.Entry(form_frame, width=50)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[key] = entry
        return form_frame

    def create_action_buttons(self, parent, fields_button, bg_color="white"):
        button_frame = tk.Frame(parent, bg=bg_color)
        for i, (label, command_name) in enumerate(fields_button.items()):
            btn = tk.Button(button_frame, text=label, width=12, command=getattr(self, command_name))
            btn.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        return button_frame

    def create_search_section(self, parent, command, bg_color="white"):
        search_frame = tk.Frame(parent, bg=bg_color)
        tk.Label(search_frame, text="Nhập dữ liệu cần tìm:", bg=bg_color).grid(row=0, column=0)
        self.entry_search = tk.Entry(search_frame, width=100)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(search_frame, text="🔍", bg="#5bc0de", fg="white", command=command).grid(row=0, column=2, padx=5,
                                                                                          pady=5)
        return search_frame

    def create_list_view(self, parent, columns_config, columns):
        list_view = ttk.Treeview(parent, columns=columns)
        list_view.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        parent.grid_rowconfigure(2, weight=5)

        for col, text, width, anchor in columns_config:
            list_view.heading(col, text=text)
            list_view.column(col, width=width, anchor=anchor, stretch=tk.NO)

        return list_view

    def on_treeview_select(self, event, keys):
        selected_item = self.list_view.selection()
        if not selected_item:
            return

        values = self.list_view.item(selected_item)["values"]

        for i, key in enumerate(keys):
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(tk.END, values[i + 1])