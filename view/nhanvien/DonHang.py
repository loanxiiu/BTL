import tkinter as tk
from tkinter import messagebox
from view.chung.BaseManagementView import BaseManagementView
from controller.DonHangController import DonHangController

class DonHang(BaseManagementView):
    def __init__(self, root):
        super().__init__(root, "Đơn Hàng", "Quản Lý Đơn Hàng")

        self.controller = DonHangController()
        self.create_main_content()
        self.load_data()
        self.list_view.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def create_main_content(self):
        main_content = tk.Frame(self.root, bg="white")
        main_content.pack(fill=tk.BOTH, expand=True)

        container_frame = tk.Frame(main_content, bg="white")
        container_frame.grid(row=0, column=0, pady=10, sticky="ew")

        # Form fields for DonHang
        fields = {
            "ma_kh": "Mã khách hàng",
            "ngay_ban": "Ngày bán",
            "don_gia": "Đơn giá",
            "ma_nv": "Mã nhân viên"
        }
        form_frame = self.create_form_fields(container_frame, fields)
        form_frame.grid(row=0, column=0, padx=10, pady=10)

        # Action buttons
        fields_button = {
            "Thêm": "add_order",
            "Sửa": "update_order",
            "Xóa": "delete_order"
        }
        button_frame = self.create_action_buttons(container_frame, fields_button)
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="s")

        # Search section
        search_frame = self.create_search_section(container_frame, self.search_order)
        search_frame.grid(row=1, column=0, sticky="nw")

        # Order list (Treeview)
        columns = ("Mã ĐH", "Mã KH", "Ngày Bán", "Đơn Giá", "Mã NV")
        columns_config = [
            ('#0', "", 0, "center"),
            ("Mã ĐH", "Mã Đơn Hàng", 70, "center"),
            ("Mã KH", "Mã Khách Hàng", 100, "center"),
            ("Ngày Bán", "Ngày Bán", 150, "center"),
            ("Đơn Giá", "Đơn Giá", 150, "center"),
            ("Mã NV", "Mã Nhân Viên", 100, "center"),
        ]
        self.list_view = self.create_list_view(main_content, columns_config, columns)

    def on_treeview_select(self, event):
        super().on_treeview_select(event, keys=["ma_kh", "ngay_ban", "don_gia", "ma_nv"])

    def add_order(self):
        values = self._validate_and_get_form_values()
        if not values: return
        self.controller.them(**values)
        self.load_data()
        messagebox.showinfo("Thành công", "Đã thêm đơn hàng!")

    def update_order(self):
        select_item = self.list_view.selection()
        if not select_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn đơn hàng để sửa")
            return

        values = self._validate_and_get_form_values()
        if not values: return

        ma_dh = self.list_view.item(select_item, "values")[0]
        self.controller.sua(ma_dh=ma_dh, **values)
        self.load_data()
        messagebox.showinfo("Thành công", "Đã cập nhật đơn hàng!")

    def delete_order(self):
        selected_item = self.list_view.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn đơn hàng để xóa!")
            return

        ma_dh = self.list_view.item(selected_item, 'values')[0]
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa đơn hàng này?"):
            self.controller.xoa(ma_dh)
            self.load_data()
            messagebox.showinfo("Thành công", "Đã xóa đơn hàng!")

    def search_order(self):
        search_term = self.entry_search.get()
        self.list_view.delete(*self.list_view.get_children())
        dh = self.controller.lay_bang_id(search_term)
        results = [dh] if dh else []

        if not results:
            messagebox.showinfo("Thông báo", "Không tìm thấy đơn hàng!")
        else:
            for order in results:
                self.list_view.insert('', 'end', values=(
                    order.ma_don_hang,
                    order.ma_kh,
                    order.ngay_ban,
                    order.don_gia,
                    order.ma_nv
                ))
        self.on_treeview_select(None)

    def load_data(self):
        self.list_view.delete(*self.list_view.get_children())
        orders = self.controller.lay_tc()
        if orders:
            for order in orders:
                self.list_view.insert("", "end", values=order)
        self.on_treeview_select(None)

if __name__ == "__main__":
    root = tk.Tk()
    app = DonHang(root)
    root.mainloop()