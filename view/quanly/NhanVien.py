import tkinter as tk
from tkinter import messagebox

from view.chung.BaseManagementView import BaseManagementView
from controller.NhanVienController import NhanVienController


class NhanVien(BaseManagementView):
    def __init__(self, root):
        super().__init__(root, "Nhân Viên", "Quản Lý Nhân Viên")

        self.controller = NhanVienController()
        self.create_main_content()
        self.load_data()
        self.list_view.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def create_main_content(self):
        main_content = tk.Frame(self.root, bg="white")
        main_content.pack(fill=tk.BOTH, expand=True)

        container_frame = tk.Frame(main_content, bg="white")
        container_frame.grid(row=0, column=0, pady=10, sticky="ew")

        fields = {
            "ten": "Tên",
            "dia_chi": "Địa chỉ",
            "sdt": "Số điện thoại"
        }

        form_frame = self.create_form_fields(container_frame, fields)
        form_frame.grid(row=0, column=0, padx=10, pady=10)

        fields_button = {
            "Thêm": "add_user",
            "Sửa": "update_user",
            "Xóa": "delete_user"
        }
        button_frame = self.create_action_buttons(container_frame, fields_button)
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="s")

        # Search section
        search_frame = self.create_search_section(container_frame, self.search_user)
        search_frame.grid(row=1, column=0, sticky="nw")

        # User list (Treeview)
        columns = ("Mã", "Tên", "Địa chỉ", "Số điện thoại")
        columns_config = [
            ('#0', "", 0, "center"),
            ("Mã", "Mã", 70, "center"),
            ("Tên", "Tên Nhân Viên", 300, "center"),
            ("Địa chỉ", "Địa Chỉ", 300, "center"),
            ("Số điện thoại", "SĐT", 200, "center"),
        ]
        self.list_view = self.create_list_view(main_content, columns_config, columns)

    def on_treeview_select(self, event):
        super().on_treeview_select(event, keys=["ten", "dia_chi", "sdt"])
    def add_user(self):
        values = self._validate_and_get_form_values()
        if not values:return
        self.controller.them(**values)
        self.load_data()
        messagebox.showinfo("Thành công", "Đã thêm nhân viên!")

    def update_user(self):
        select_item = self.list_view.selection()
        if not select_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm để sửa")
            return

        values = self._validate_and_get_form_values()
        if not values:return

        ma_nv = self.list_view.item(select_item, "values")[0]

        self.controller.sua(ma_nv=ma_nv, **values)
        self.load_data()
        messagebox.showinfo("Thành công", "Đã cập nhật sản phẩm!")

    def delete_user(self):
        selected_item = self.list_view.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để xóa!")
            return
        ma_nv = self.list_view.item(selected_item, 'values')[0]
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa nhân viên này?"):
            self.controller.xoa(ma_nv)
            self.load_data()
            messagebox.showinfo("Thành công", "Đã xóa nhân viên!")

    def search_user(self):
        search_term = self.entry_search.get()
        print(search_term)
        self.list_view.delete(*self.list_view.get_children())
        ds_nv=self.controller.lay_bang_ten(search_term)
        nv=self.controller.lay_bang_id(search_term)
        results = ds_nv if ds_nv else ([nv] if nv else [])

        print(ds_nv)
        if results:
            for nv in results:
                self.list_view.insert('', 'end', values=nv)
        else:
            messagebox.showinfo("Lỗi", "Không có thông tin")
        self.on_treeview_select(None)

    def load_data(self):
        self.list_view.delete(*self.list_view.get_children())
        for user in self.controller.lay_tc():
            self.list_view.insert("", "end", values=user)
        self.on_treeview_select(None)

if __name__ == "__main__":
    root = tk.Tk()
    app = NhanVien(root)
    root.mainloop()
