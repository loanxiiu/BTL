import os
import time
import tkinter as tk
from shutil import copyfile
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from view.chung.BaseManagementView import BaseManagementView
from controller.ChiTietPhieuNhapController import ChiTietPhieuNhapController
from controller.PhieuNhapController import PhieuNhapController
from controller.SanPhamController import SanPhamController


class SanPham(BaseManagementView):
    def __init__(self, root):
        super().__init__(root, "Sản Phẩm", "Quản Lý Sản Phẩm")

        # Constants
        self.IMAGE_SAVE_DIR = r"E:\Users\ploan\python_EAUT\BTL\BTL\assets\images"
        self.MAX_WIDTH, self.MAX_HEIGHT = 150, 180

        # Image-related attributes
        self.selected_image_path = None

        # Setup
        self.controller = SanPhamController()
        self.pn_controller = PhieuNhapController()
        self.ctpn_controller = ChiTietPhieuNhapController()
        self.create_main_content()
        self.load_data()
        self.list_view.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def create_main_content(self):
        main_content = tk.Frame(self.root, bg="white")
        main_content.pack(fill=tk.BOTH, expand=True)

        container_frame = tk.Frame(main_content, bg="white")
        container_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        fields = {
            "ten_sp": "Tên sản phẩm",
            "so_luong": "Số lượng",
            "don_gia": "Đơn giá",
            "mo_ta": "Mô tả",
            "ma_dm": "Mã danh mục"
        }

        form_frame = self.create_form_fields(container_frame, fields)
        form_frame.grid(row=0, column=1, padx=10, pady=10)

        # Image upload section
        image_frame = self._create_image_upload_section(container_frame)
        image_frame.grid(row=0, column=0, padx=10, pady=10)

        # Action buttons
        fields_button = {
            "Thêm": "add_product",
            "Sửa": "update_product",
            "Xóa": "delete_product",
            "Dự báo & Đề xuất": "forecast_and_suggest"
        }
        button_frame = self.create_action_buttons(container_frame, fields_button)
        button_frame.grid(row=0, column=2, padx=10, pady=10, sticky="s")

        # Search section
        search_frame = self.create_search_section(main_content, self.search_product)
        search_frame.grid(row=1, column=0, sticky="nw")

        # Product list (Treeview)
        columns = ("Mã", "Tên", "Số Lượng", "Đơn Giá", "Mã DM", "Mô Tả", "Ảnh")
        columns_config = [
            ("#0", "", 0, "center"),
            ("Mã", "Mã Sản Phẩm", 70, "center"),
            ("Tên", "Tên Sản Phẩm", 200, "center"),
            ("Số Lượng", "Số Lượng", 70, "center"),
            ("Đơn Giá", "Đơn Giá", 100, "w"),
            ("Mã DM", "Mã DM", 70, "center"),
            ("Mô Tả", "Mô Tả", 500, "w"),
            ("Ảnh", "Ảnh", 200, "center")
        ]
        self.list_view = self.create_list_view(main_content, columns_config, columns)

    def forecast_and_suggest(self):
        de_xuat = self.controller.tao_de_xuat_mua_hang()
        if de_xuat:
            message = "\n".join([f"{item['TenSP']}: Cần nhập {item['SoLuongCanNhap']}" for item in de_xuat])
            messagebox.showinfo("Đề xuất mua hàng", message)
        else:
            messagebox.showinfo("Thông báo", "Không cần nhập hàng thêm!")

    def tao_phieu_nhap_tu_de_xuat(self, de_xuat, ma_quan_ly, ma_ncc):
        from datetime import datetime
        ngay_nhap = datetime.now().strftime("%Y-%m-%d")
        self.pn_controller.them(ngay_nhap, ma_quan_ly, ma_ncc)
        # Thêm chi tiết phiếu nhập từ đề xuất
        # self.ctpn_controller.them(de_xuat.)

    def _create_image_upload_section(self, parent):
        image_frame = tk.Frame(parent, bg="white")
        self.image_label = tk.Label(image_frame, text="Chưa có ảnh", bg="gray", width=18, height=12)
        self.image_label.pack(pady=5)
        upload_button = tk.Button(image_frame, text="Tải ảnh", command=self.upload_image)
        upload_button.pack(pady=5)
        return image_frame

    def on_treeview_select(self, event):
        super().on_treeview_select(event, keys=["ten_sp", "so_luong", "don_gia", "ma_dm", "mo_ta"])

        selected_item = self.list_view.selection()
        if not selected_item:
            return

        values = self.list_view.item(selected_item)["values"]
        image_path = values[-1]

        if image_path and image_path != "Không có ảnh":
            try:
                full_path = os.path.join(self.IMAGE_SAVE_DIR, image_path)
                tk_image = self._resize_image(full_path)

                self.image_label.config(image=tk_image, width=self.MAX_WIDTH, height=self.MAX_HEIGHT)
                self.image_label.image = tk_image

                self.selected_image_path = full_path
            except Exception as e:
                print("Lỗi khi mở ảnh", e)
                self.image_label.config(text="Lỗi ảnh", image="")
                self.selected_image_path = None
        else:
            self.image_label.config(text="Không có ảnh", image="")
            self.selected_image_path = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.selected_image_path = file_path
            tk_image = self._resize_image(file_path)
            self.image_label.config(image=tk_image, text="", width=self.MAX_WIDTH, height=self.MAX_HEIGHT)
            self.image_label.image = tk_image

    def _resize_image(self, file_path, max_width=None, max_height=None):
        max_width = max_width or self.MAX_WIDTH
        max_height = max_height or self.MAX_HEIGHT

        pil_image = Image.open(file_path)
        width, height = pil_image.size
        ratio = min(max_width / width, max_height / height)

        new_width = int(width * ratio)
        new_height = int(height * ratio)

        resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    def _validate_and_get_form_values(self):
        values = {k: v.get() for k, v in self.entries.items()}
        if not all(values.values()):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return None
        return values

    def _handle_image_upload(self):
        if not os.path.exists(self.IMAGE_SAVE_DIR):
            os.makedirs(self.IMAGE_SAVE_DIR)

        if self.selected_image_path:
            ext = os.path.splitext(self.selected_image_path)[-1]
            new_filename = f"anh{int(time.time())}{ext}"
            save_path = os.path.join(self.IMAGE_SAVE_DIR, new_filename)
            copyfile(self.selected_image_path, save_path)
            return new_filename
        return "Không có ảnh"

    def add_product(self):
        values = self._validate_and_get_form_values()
        if not values:
            return

        values['anh'] = self._handle_image_upload()
        self.controller.them(**values)
        self.load_data()
        messagebox.showinfo("Thành công", "Đã thêm sản phẩm!")

    def update_product(self):
        selected_item = self.list_view.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm để sửa!")
            return

        values = self._validate_and_get_form_values()
        if not values:
            return

        ma_sp = self.list_view.item(selected_item, "values")[0]

        # Image handling
        if self.selected_image_path and not self.selected_image_path.startswith(self.IMAGE_SAVE_DIR):
            values['anh'] = self._handle_image_upload()
        else:
            values['anh'] = self.list_view.item(selected_item, "values")[-2]

        self.controller.sua(ma_sp=ma_sp, **values)
        self.load_data()
        messagebox.showinfo("Thành công", "Đã cập nhật sản phẩm!")

    def delete_product(self):
        selected_item = self.list_view.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm để xóa!")
            return

        ma_sp = self.list_view.item(selected_item, "values")[0]

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa sản phẩm này?"):
            self.controller.xoa(ma_sp)
            self.load_data()
            messagebox.showinfo("Thành công", "Đã xóa sản phẩm!")

    def load_data(self):
        self.list_view.delete(*self.list_view.get_children())
        for sp in self.controller.lay_tc():
            self.list_view.insert("", "end", values=sp)
        self.on_treeview_select(None)

    def search_product(self):
        search_term = self.entry_search.get()
        self.list_view.delete(*self.list_view.get_children())

        ds_sp = self.controller.lay_bang_ten(search_term)
        sp = self.controller.lay_bang_id(search_term)

        results = ds_sp if ds_sp else ([sp] if sp else [])

        if results:
            for item in results:
                self.list_view.insert("", "end", values=item)
        else:
            messagebox.showinfo("Lỗi", "Không có thông tin")

        self.on_treeview_select(None)


if __name__ == "__main__":
    root = tk.Tk()
    app = SanPham(root)
    root.mainloop()
