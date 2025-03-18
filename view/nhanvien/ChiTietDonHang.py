import tkinter as tk
from tkinter import messagebox
from view.chung.BaseManagementView import BaseManagementView
from controller.ChiTietDonHangController import ChiTietDonHangController


class ChiTietDonHang(BaseManagementView):
    def __init__(self, root):
        super().__init__(root, "Chi Tiết Đơn Hàng", "Quản Lý Chi Tiết Đơn Hàng")

        self.controller = ChiTietDonHangController()
        self.create_main_content()
        self.load_data()
        self.list_view.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def create_main_content(self):
        main_content = tk.Frame(self.root, bg="white")
        main_content.pack(fill=tk.BOTH, expand=True)

        container_frame = tk.Frame(main_content, bg="white")
        container_frame.grid(row=0, column=0, pady=10, sticky="ew")

        fields = {
            "ma_dh": "Mã Đơn Hàng",
            "so_luong": "Số Lượng",
            "don_gia": "Đơn Giá",
            "ma_sp": "Mã Sản Phẩm"
        }

        form_frame = self.create_form_fields(container_frame, fields)
        form_frame.grid(row=0, column=0, padx=10, pady=10)

        fields_button = {
            "Thêm": "add_order_detail",
            "Sửa": "update_order_detail",
            "Xóa": "delete_order_detail"
        }
        button_frame = self.create_action_buttons(container_frame, fields_button)
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="s")

        search_frame = self.create_search_section(container_frame, self.search_order_detail)
        search_frame.grid(row=1, column=0, sticky="nw")

        columns = ("Mã CTĐH", "Mã Đơn Hàng", "Số Lượng", "Đơn Giá", "Mã SP")

        columns_config = [
            ('#0', "", 0, "center"),
            ("Mã CTĐH", "Mã Chi Tiết Đơn Hàng", 100, "center"),
            ("Mã Đơn Hàng", "Mã Đơn Hàng", 100, "center"),
            ("Số Lượng", "Số Lượng", 100, "center"),
            ("Đơn Giá", "Đơn Giá", 100, "center"),
            ("Mã SP", "Mã Sản Phẩm", 100, "center")
        ]
        self.list_view = self.create_list_view(main_content, columns_config, columns)

    def on_treeview_select(self, event):
        super().on_treeview_select(event, keys=["ma_dh", "so_luong", "don_gia", "ma_sp"])

    def add_order_detail(self):
        values = self._validate_and_get_form_values()
        if not values:
            return
        self.controller.them(**values)
        self.load_data()
        messagebox.showinfo("Thành công", "Đã thêm chi tiết đơn hàng!")

    def update_order_detail(self):
        selected_item = self.list_view.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn chi tiết đơn hàng để sửa!")
            return

        values = self._validate_and_get_form_values()
        if not values:
            return

        ma_ctdh = self.list_view.item(selected_item, "values")[0]
        self.controller.sua(ma_ctdh=ma_ctdh, **values)
        self.load_data()
        messagebox.showinfo("Thành công", "Đã cập nhật chi tiết đơn hàng!")

    def delete_order_detail(self):
        selected_item = self.list_view.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn chi tiết đơn hàng để xóa!")
            return

        ma_ctdh = self.list_view.item(selected_item, 'values')[0]
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa chi tiết đơn hàng này?"):
            self.controller.xoa(ma_ctdh)
            self.load_data()
            messagebox.showinfo("Thành công", "Đã xóa chi tiết đơn hàng!")

    def search_order_detail(self):
        search_term = self.entry_search.get()
        self.list_view.delete(*self.list_view.get_children())

        ds_ctdh = self.controller.lay_tc()
        ctdh = self.controller.lay_bang_id(search_term)
        results = ds_ctdh if ds_ctdh else ([ctdh] if ctdh else [])

        if results:
            for item in results:
                self.list_view.insert('', 'end', values=item)
        else:
            messagebox.showinfo("Thông báo", "Không có thông tin phù hợp")
        self.on_treeview_select(None)

    def load_data(self):
        self.list_view.delete(*self.list_view.get_children())
        for item in self.controller.lay_tc():
            self.list_view.insert("", "end", values=item)
        self.on_treeview_select(None)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChiTietDonHang(root)
    root.mainloop()
