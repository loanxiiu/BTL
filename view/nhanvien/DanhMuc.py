import tkinter as tk
from tkinter import messagebox

from view.chung.BaseManagementView import BaseManagementView
from controller.DanhMucController import DanhMucController

class DanhMuc(BaseManagementView):
    def __init__(self, root):
        super().__init__(root, "Danh Mục", "Quản Lý Danh Mục")

        self.controller = DanhMucController()
        self.create_main_content()
        self.load_data()
        self.list_view.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def create_main_content(self):
        main_content = tk.Frame(self.root, bg="white")
        main_content.pack(fill=tk.BOTH, expand=True)

        container_frame = tk.Frame(main_content, bg="white")
        container_frame.grid(row=0, column=0, pady=10, sticky="ew")

        fields = {
            "ten_dm": "Tên Danh Mục"
        }

        form_frame = self.create_form_fields(container_frame, fields)
        form_frame.grid(row=0, column=0, padx=10, pady=10)

        fields_button = {
            "Thêm": "add_category",
            "Sửa": "update_category",
            "Xóa": "delete_category"
        }
        button_frame = self.create_action_buttons(container_frame, fields_button)
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="s")

        # Search section
        search_frame = self.create_search_section(container_frame, self.search_category)
        search_frame.grid(row=1, column=0, sticky="nw")

        # Category list (Treeview)
        columns = ("Mã Danh Mục", "Tên Danh Mục")
        columns_config = [
            ('#0', "", 0, "center"),
            ("Mã Danh Mục", "Mã Danh Mục", 150, "center"),
            ("Tên Danh Mục", "Tên Danh Mục", 300, "center"),
        ]
        self.list_view = self.create_list_view(main_content, columns_config, columns)

    def on_treeview_select(self, event):
        super().on_treeview_select(event, keys=["ten_dm"])

    def add_category(self):
        values = self._validate_and_get_form_values()
        if not values: return
        self.controller.them(**values)
        self.load_data()
        messagebox.showinfo("Thành công", "Đã thêm danh mục!")

    def update_category(self):
        select_item = self.list_view.selection()
        if not select_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn danh mục để sửa")
            return

        values = self._validate_and_get_form_values()
        if not values: return

        ma_dm = self.list_view.item(select_item, "values")[0]

        self.controller.sua(ma_dm=ma_dm, **values)
        self.load_data()
        messagebox.showinfo("Thành công", "Đã cập nhật danh mục!")

    def delete_category(self):
        selected_item = self.list_view.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn danh mục để xóa!")
            return
        ma_dm = self.list_view.item(selected_item, 'values')[0]
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa danh mục này?"):
            self.controller.xoa(ma_dm)
            self.load_data()
            messagebox.showinfo("Thành công", "Đã xóa danh mục!")

    def search_category(self):
        search_term = self.entry_search.get()
        self.list_view.delete(*self.list_view.get_children())
        danh_muc = self.controller.lay_bang_id(search_term)

        if danh_muc:
            self.list_view.insert('', 'end', values=(danh_muc.ma_dm, danh_muc.ten_dm))
        else:
            messagebox.showinfo("Lỗi", "Không có thông tin danh mục")
        self.on_treeview_select(None)

    def load_data(self):
        self.list_view.delete(*self.list_view.get_children())
        for danh_muc in self.controller.lay_tc():
            self.list_view.insert("", "end", values=(danh_muc.ma_dm, danh_muc.ten_dm))
        self.on_treeview_select(None)

if __name__ == "__main__":
    root = tk.Tk()
    app = DanhMuc(root)
    root.mainloop()
