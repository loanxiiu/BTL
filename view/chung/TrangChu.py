import tkinter as tk
from PIL import Image, ImageTk
from view.chung.Sidebar import Sidebar
from view.chung.Header import Header
from controller.SanPhamController import SanPhamController
from controller.DanhMucController import DanhMucController
from controller.DonHangController import DonHangController
from controller.NhanVienController import NhanVienController

class TrangChu:
    def __init__(self, root):
        self.san_pham_controller = SanPhamController()
        self.danh_muc_controller = DanhMucController()
        self.don_hang_controller = DonHangController()
        self.nhan_vien_controller = NhanVienController()
        self.root = root
        self.root.title("IT SHOP")
        self.root.geometry("1920x950")
        self.sidebar = Sidebar(self.root)
        self.header = Header(self.root, "Trang chủ")
        self.create_main_content()

    def create_main_content(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(main_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.content_frame = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.bind_mousewheel()

        cards_frame = tk.Frame(self.content_frame, bg="white")
        cards_frame.pack(fill=tk.X, padx=10, pady=10)

        card_data = [
            ("Sản Phẩm", f"{self.san_pham_controller.dem()}", "#e6a23c", "👚"),
            ("Danh Mục", f"{self.danh_muc_controller.dem()}", "#f79a98", "🛅"),
            ("Đơn Hàng", f"{self.don_hang_controller.dem()}", "#d0d0d0", "🛒"),
            ("Nhân Viên", f"{self.nhan_vien_controller.dem()}", "#4caf50", "👩"),
        ]

        for i, data in enumerate(card_data):
            title, count, color, icon = data
            row = i // 4
            col = i % 4
            self.create_card(cards_frame, title, count, color, icon, row, col)

        products_frame = tk.Frame(self.content_frame, bg="white")
        products_frame.pack(fill=tk.X, padx=20, pady=10)

        products = self.san_pham_controller.lay_tc()
        for i, data in enumerate(products):
            id, name, quantity, price, id_category, mo_ta, image = data
            row = i // 4
            col = i % 4
            self.create_product_card(products_frame, name, price, quantity, image, row, col)

    def bind_mousewheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux_up)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux_down)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_horizontal_scroll)

    def _on_mousewheel_windows(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def _on_mousewheel_linux_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def _on_horizontal_scroll(self, event):
        if self.canvas.xscrollcommand:
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_card(self, parent, title, count, color, icon, row, col):
        card = tk.Frame(parent, bg=color, width=250, height=120, padx=10, pady=10, relief=tk.RAISED, bd=0)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.grid_propagate(False)

        count_label = tk.Label(card, text=count, font=("Arial", 40, "bold"), bg=color, fg="white")
        count_label.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.NW)

        icon_label = tk.Label(card, text=icon, font=("Arial", 30), bg=color, fg="white")
        icon_label.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.NE)

        title_label = tk.Label(card, text=title, font=("Arial", 16), bg=color, fg="white")
        title_label.pack(side=tk.BOTTOM, pady=10, anchor=tk.SW)

    def create_product_card(self, parent, name, price, quantity, image_placeholder, row, col):
        card = tk.Frame(parent, bg="white", width=250, height=400, padx=10, pady=10, relief=tk.GROOVE, bd=1)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.grid_propagate(False)

        image_frame = tk.Frame(card, bg="#f5f5f5", width=230, height=270)
        image_frame.pack(fill=tk.X, pady=(0, 10))
        image_frame.pack_propagate(False)

        original_image = Image.open(image_placeholder)
        original_width, original_height = original_image.size
        frame_width = 230
        new_height = int(frame_width * original_height / original_width)
        image = original_image.resize((frame_width, new_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(image_frame, image=photo, bg="#f5f5f5")
        image_label.pack(expand=True)
        image_label.image = photo

        name_label = tk.Label(card, text=name, font=("Arial", 12, "bold"), bg="white", anchor="w")
        name_label.pack(fill=tk.X)

        price_label = tk.Label(card, text=f"{price} VND", font=("Arial", 14, "bold"), fg="#e74c3c", bg="white", anchor="w")
        price_label.pack(fill=tk.X, pady=(5, 0))

        quantity_label = tk.Label(card, text=f"Còn {quantity}", font=("Arial", 10), fg="gray", bg="white", anchor="w")
        quantity_label.pack(fill=tk.X)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrangChu(root)
    root.mainloop()