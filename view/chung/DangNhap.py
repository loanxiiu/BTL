import tkinter as tk
from tkinter import messagebox, PhotoImage
import face_recognition

from controller.FaceController import FaceController
from utils.session import Session
import os
from controller.TaiKhoanController import TaiKhoanController
from view.chung.TrangChu import TrangChu


class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng Nhập - IT SHOP")
        self.root.geometry("1920x950")
        self.root.configure(bg="#1a3f66")

        tai_khoan = Session.get_user()
        print(tai_khoan)
        if tai_khoan:
            TrangChu(root)
            return

        # Controller và thiết lập ban đầu
        self.face_controller = FaceController()
        self.tai_khoan_controller = TaiKhoanController()
        self.known_face_encodings = []
        self.known_face_usernames = []

        # Tải khuôn mặt đã biết
        self.load_known_faces()

        # Tạo giao diện
        self.create_ui()

    def load_known_faces(self):
        """Tải và mã hóa các khuôn mặt đã đăng ký"""
        faces_directory = "known_faces"

        # Tạo thư mục nếu chưa tồn tại
        if not os.path.exists(faces_directory):
            os.makedirs(faces_directory)

        for filename in os.listdir(faces_directory):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(faces_directory, filename)
                image = face_recognition.load_image_file(image_path)

                # Lấy mã hóa khuôn mặt
                face_encodings = face_recognition.face_encodings(image)

                if face_encodings:
                    # Lấy mã hóa của khuôn mặt đầu tiên
                    face_encoding = face_encodings[0]

                    # Lưu mã hóa và username
                    self.known_face_encodings.append(face_encoding)
                    username = os.path.splitext(filename)[0]
                    self.known_face_usernames.append(username)

    def create_ui(self):
        main_frame = tk.Frame(self.root, bg="#1a3f66")
        main_frame.pack(expand=True, padx=50, pady=50)

        # Logo
        logo_frame = tk.Frame(main_frame, bg="#1a3f66")
        logo_frame.grid(row=0, column=0, padx=50, pady=20)

        try:
            self.logo = PhotoImage(file="E:\\Users\\ploan\\python_EAUT\\BTL\\assets\\logo.png")
            logo_label = tk.Label(logo_frame, image=self.logo, bg="#1a3f66")
            logo_label.pack()
        except Exception as e:
            print(f"Lỗi khi tải logo: {e}")
            tk.Label(logo_frame, text="LOGO", font=("Arial", 14, "bold"), bg="#1a3f66", fg="white").pack()

        # Form đăng nhập
        form_frame = tk.Frame(main_frame, bg="#1a3f66", bd=2, relief="solid")
        form_frame.grid(row=0, column=1, padx=50, pady=20)

        tk.Label(form_frame, text="ĐĂNG NHẬP", font=("Arial", 18, "bold"), bg="#1a3f66", fg="white").pack(pady=15)

        # Nhập username
        tk.Label(form_frame, text="Tên đăng nhập:", font=("Arial", 12), bg="#1a3f66", fg="white").pack(anchor="w",
                                                                                                       padx=20)
        self.username_entry = tk.Entry(form_frame, font=("Arial", 12), width=35)
        self.username_entry.pack(pady=5, padx=20)

        # Nhập mật khẩu
        tk.Label(form_frame, text="Mật khẩu:", font=("Arial", 12), bg="#1a3f66", fg="white").pack(anchor="w", padx=20)
        self.password_entry = tk.Entry(form_frame, font=("Arial", 12), width=35, show="*")
        self.password_entry.pack(pady=5, padx=20)

        # Nút đăng nhập
        login_btn = tk.Button(form_frame, text="Đăng Nhập", font=("Arial", 12, "bold"),
                              bg="#008cff", fg="white", width=25, height=1,
                              relief="flat", command=self.login)
        login_btn.pack(pady=10)

        # Nút đăng nhập Face ID
        faceid_btn = tk.Button(form_frame, text="Đăng Nhập bằng Face ID",
                               font=("Arial", 12, "bold"),
                               bg="#4CAF50", fg="white", width=25, height=1,
                               relief="flat", command=self.login_with_face)
        faceid_btn.pack(pady=10)

        self.root.bind('<Return>', lambda event: self.login())

    def login_with_face(self):
        user_id, message = self.face_controller.verify_face()
        print(message)
        if user_id:
            tai_khoan = self.tai_khoan_controller.lay_bang_user_id(user_id)
            print(tai_khoan)
            # Lưu tài khoản vào session
            Session.set_user({
                "id": tai_khoan.id,
                "username": tai_khoan.username,
                "quyen": tai_khoan.ma_quyen,
                "user_id": user_id
            })

            # messagebox.showinfo("Thành công", f"Chào mừng {tai_khoan.username}!")
            for widget in self.root.winfo_children():
                widget.destroy()
            if tai_khoan.ma_quyen == 1:
                TrangChu(self.root)
            elif tai_khoan.ma_quyen == 2:
                TrangChu(self.root)
        else:
            messagebox.showwarning("Cảnh báo", "Không thể xác minh")

    # Import session

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin đăng nhập!")
            return

        tai_khoan = self.tai_khoan_controller.kiem_tra_dang_nhap(username, password)
        if tai_khoan:
            # Lưu tài khoản vào session
            Session.set_user({
                "id": tai_khoan.id,
                "username": tai_khoan.username,
                "quyen": tai_khoan.ma_quyen,
                "user_id": tai_khoan.user_id
            })

            # messagebox.showinfo("Thành công", f"Chào mừng {tai_khoan.username}!")
            for widget in self.root.winfo_children():
                widget.destroy()
            if tai_khoan.ma_quyen == 1:
                TrangChu(self.root)
            elif tai_khoan.ma_quyen == 2:
                TrangChu(self.root)

    # Các phương thức khác giữ nguyên như ban đầu


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = LoginForm(root)
        root.mainloop()
    except Exception as e:
        print(f"Lỗi khởi động ứng dụng: {e}")