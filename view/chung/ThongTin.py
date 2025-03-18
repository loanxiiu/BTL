import tkinter as tk
from tkinter import messagebox

from controller.FaceController import FaceController
from controller.UserController import UserController
from utils.session import Session

class ThongTin:
    def __init__(self,root):
        self.root = root
        self.root.title("Thông tin")
        self.root.geometry("1920x1080")

        from view.chung.Header import Header
        from view.chung.Sidebar import Sidebar

        self.sidebar = Sidebar(self.root)
        self.header = Header(self.root, "Thông tin cá nhân")
        self.tai_khoan = Session.get_user()
        self.user_controller= UserController()
        self.face_controller= FaceController()
        self.create_main_content()

    def create_main_content(self):
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        user = self.user_controller.lay_bang_id(self.tai_khoan['user_id'])
        print(user)

        tk.Label(self.main_frame, text="Mã:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.ma_entry = tk.Entry(self.main_frame, font=("Arial", 12), width=30)
        self.ma_entry.grid(row=0, column=1)
        self.ma_entry.insert(0, user.id)

        tk.Label(self.main_frame, text="Tên:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.ten_entry = tk.Entry(self.main_frame, font=("Arial", 12), width=30)
        self.ten_entry.grid(row=1, column=1)
        self.ten_entry.insert(0, user.ten)

        tk.Label(self.main_frame, text="Địa chỉ:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.dia_chi_entry = tk.Entry(self.main_frame, font=("Arial", 12), width=30)
        self.dia_chi_entry.grid(row=2, column=1)
        self.dia_chi_entry.insert(0, user.dia_chi)

        tk.Label(self.main_frame, text="Số điện thoại:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=5,
                                                                                  pady=5)
        self.sdt_entry = tk.Entry(self.main_frame, font=("Arial", 12), width=30)
        self.sdt_entry.grid(row=3, column=1)
        self.sdt_entry.insert(0, user.sdt)

        tk.Button(self.main_frame, text="Cập nhật", font=("Arial", 12), command=self.cap_nhat).grid(row=4, column=0,
                                                                                                    columnspan=2,
                                                                                                   pady=10)

        tk.Button(self.main_frame, text="Đăng ký khuôn mặt", font=("Arial", 12), bg="#1a3f66", fg="white",
                  command=self.dang_ky_khuon_mat).grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(self.main_frame, text="Xóa khuôn mặt", font=("Arial", 12), bg="red", fg="white",
                  command=self.xoa_khuon_mat).grid(row=5, column=0, columnspan=2, pady=10)

    def cap_nhat(self):
        # Lấy dữ liệu từ các ô nhập liệu
        user_id = self.ma_entry.get()
        ten = self.ten_entry.get()
        dia_chi = self.dia_chi_entry.get()
        sdt = self.sdt_entry.get()

        # Kiểm tra dữ liệu hợp lệ
        if not ten or not dia_chi or not sdt:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        # Cập nhật thông tin người dùng trong DB
        try:
            success = self.user_controller.sua(user_id=user_id, ten=ten, dia_chi=dia_chi, sdt=sdt)
            if success:
                messagebox.showinfo("Thành công", "Cập nhật thông tin thành công!")
            else:
                messagebox.showerror("Lỗi", "Cập nhật không thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật: {e}")

    def dang_ky_khuon_mat(self):
        user_id = self.ma_entry.get()
        if not user_id:
            messagebox.showerror("Lỗi", "Vui lòng nhập Mã người dùng!")
            return

        success, message = self.face_controller.register_face(user_id)
        if success:
            messagebox.showinfo("Thành công", message)
        else:
            messagebox.showerror("Lỗi", message)

    def xoa_khuon_mat(self):
        user_id = self.ma_entry.get()
        if not user_id:
            messagebox.showerror("Lỗi", "Vui lòng nhập Mã người dùng!")
            return

        try:
            self.face_controller.face_dao.xoa(user_id)
            messagebox.showinfo("Thành công", "Xóa khuôn mặt thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa khuôn mặt: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    ThongTin(root)
    root.mainloop()