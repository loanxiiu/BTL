import tkinter as tk
from tkinter import PhotoImage, messagebox
from utils.session import Session

class Sidebar:
    def __init__(self, root):
        self.root = root
        self.current_view = None

        # Sidebar Frame
        self.sidebar = tk.Frame(root, bg="#1a3f66", width=300)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Logo Frame
        self._create_logo()

        # Menu items based on user role
        self._create_menu()

    def _create_logo(self):
        logo_frame = tk.Frame(self.sidebar, bg="#1a3f66")
        logo_frame.pack(fill=tk.X, pady=2)

        try:
            image = PhotoImage(file="E:\\Users\\ploan\\python_EAUT\\BTL\\assets\\logo.png")
            logo_label = tk.Label(logo_frame, image=image, bg="#1a3f66", relief=tk.FLAT, height=270)
            logo_label.pack(pady=10)
            logo_label.image = image  # Keep reference to avoid garbage collection
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo_label = tk.Label(logo_frame, text="IT STORE\nFashion Store", bg="#1a3f66", fg="white",
                                  font=("Arial", 14, "bold"))
            logo_label.pack(pady=10)

    def _create_menu(self):
        # Menu items for different roles
        quan_ly_menu = [
            ("🏠", "Trang Chủ", "trang_chu"),
            ("👚", "Sản Phẩm", "san_pham"),
            ("🛒", "Đơn Hàng", "don_hang"),
            ("👥", "Nhân Viên", "nhan_vien"),
            ("🛍", "Nhập Hàng", "nhap_hang"),
            ("📊", "Thống Kê", "thong_ke"),
            ("🚪", "Đăng xuất", "logout")
        ]
        nhan_vien_menu = [
            ("🏠", "Trang Chủ", "trang_chu"),
            ("👚", "Sản Phẩm", "san_pham"),
            ("🛍", "Danh Mục", "danh_muc"),
            ("👥", "Khách Hàng", "khach_hang"),
            ("🛒", "Đơn Hàng", "don_hang"),
            ("🚪", "Đăng xuất", "logout")
        ]

        # Select menu based on user role
        user_role = Session.get_user()
        if user_role:
            print("user_role:", user_role)  # Debugging output
            # Check 'quyen' key for role (1 = Quản lý, else = Nhân viên)
            menu_items = quan_ly_menu if user_role.get('quyen') == 1 else nhan_vien_menu
        else:
            print("No user logged in, defaulting to nhan_vien_menu")
            menu_items = nhan_vien_menu  # Default if no session

        # Create menu buttons
        self.menu_buttons = []
        for i, (icon, text, action) in enumerate(menu_items):
            menu_frame = tk.Frame(self.sidebar, bg="#1a3f66", height=40)
            menu_frame.pack(fill=tk.X, pady=0, ipady=1)

            btn = tk.Button(menu_frame, text=icon, bg="#1a3f66", fg="white",
                            font=("Arial", 14), relief=tk.FLAT, bd=0, width=5, height=2,
                            anchor="center",
                            command=lambda a=action: self.menu_click(a))  # Simplified lambda
            btn.pack(side=tk.LEFT, padx=5, pady=2)

            label = tk.Label(menu_frame, text=text, bg="#1a3f66", fg="white",
                             font=("Arial", 12), anchor="center")
            label.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.X)

            self.menu_buttons.append((btn, label, menu_frame, action))  # Store action directly

        # Highlight default item (Trang Chủ)
        self._highlight_menu(0)

    def _highlight_menu(self, index):
        for i, (btn, label, frame, _) in enumerate(self.menu_buttons):
            bg_color = "#14355a" if i == index else "#1a3f66"
            frame.configure(bg=bg_color)
            btn.configure(bg=bg_color)
            label.configure(bg=bg_color)

    def menu_click(self, action):
        # Highlight the clicked menu item
        for i, (_, _, _, stored_action) in enumerate(self.menu_buttons):
            if stored_action == action:
                self._highlight_menu(i)
                break

        # Handle the action
        if action == "logout":
            self.logout()
        else:
            self.change_view(action)

    def logout(self):
        confirm = messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất?")
        if confirm:
            for widget in self.root.winfo_children():
                widget.destroy()
            Session.clear()
            from view.chung.DangNhap import LoginForm
            LoginForm(self.root)

    def change_view(self, view_name):
        # Remove current view
        for widget in self.root.winfo_children():
            # if widget != self.sidebar:  # Keep sidebar
            widget.destroy()

        # Create new view
        view_mapping = {
            "trang_chu": ("view.chung.TrangChu", "TrangChu"),
            "san_pham": ("view.nhanvien.SanPham", "SanPham"),
            "danh_muc": ("view.nhanvien.DanhMuc", "DanhMuc"),
            "don_hang": ("view.nhanvien.DonHang", "DonHang"),
            "nhan_vien": ("view.quanly.NhanVien", "NhanVien"),
            "thong_ke": ("view.quanly.ThongKe", "ThongKe"),
            "khach_hang": ("view.quanly.KhachHang", "KhachHang"),
            "nhap_hang": ("view.quanly.NhapHang", "NhapHang"),
        }

        if view_name in view_mapping:
            module_path, class_name = view_mapping[view_name]
            module = __import__(module_path, fromlist=[class_name])
            view_class = getattr(module, class_name)
            self.current_view = view_class(self.root)
            self.current_view.pack(fill=tk.BOTH, expand=True)
        else:
            view_frame = tk.Frame(self.root, bg="white")
            view_frame.pack(fill=tk.BOTH, expand=True)
            tk.Label(view_frame, text=f"View '{view_name}' is not implemented yet",
                     font=("Arial", 16), bg="white", fg="black").pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    # Simulate a session for testing
    Session.set_user({"id": 1, "username": "user1", "quyen": 1, "user_id": "1"})
    app = Sidebar(root)
    root.mainloop()