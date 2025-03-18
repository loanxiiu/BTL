import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from view.chung.Sidebar import Sidebar
from view.chung.Header import Header
import os


class ThongKe:
    def __init__(self, root):
        self.root = root
        self.root.title("FieldCheck - Dashboard")
        self.root.geometry("1920x1080")

        self.sidebar = Sidebar(self.root)
        self.header = Header(self.root, "Thống kê")
        self.create_main_content()

    def create_main_content(self):
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        df_sanpham, df_khachhang, df_doanhthu = self.lay_du_lieu()

        self.ve_bieu_do_san_pham(main_frame, df_sanpham)
        self.ve_bieu_do_khach_hang(main_frame, df_khachhang)
        # self.ve_bieu_do_doanh_thu(main_frame, df_doanhthu)

    def lay_du_lieu(self):
        # Calculate the absolute path to ITSHOP.db
        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # E:\Users\ploan\python_EAUT\BTL
        db_path = os.path.join(BASE_DIR, "model", "dao", "connect", "ITSHOP.db")  # Full path to ITSHOP.db

        try:
            with sqlite3.connect(db_path) as conn:
                query_sanpham = """
                    SELECT SanPham.TenSPham, SUM(ChiTietDonHang.SoLuong) AS TongBan
                    FROM ChiTietDonHang
                    JOIN SanPham ON ChiTietDonHang.MaSP = SanPham.MaSPham
                    GROUP BY SanPham.TenSPham
                    ORDER BY TongBan DESC
                    LIMIT 5
                """
                df_sanpham = pd.read_sql(query_sanpham, conn)

                query_khachhang = """
                    SELECT Users.Ten, COUNT(DonHang.MaDH) AS SoDon
                    FROM DonHang
                    JOIN Users ON DonHang.MaKH = Users.id
                    GROUP BY Users.Ten
                    ORDER BY SoDon DESC
                    LIMIT 5
                """
                df_khachhang = pd.read_sql(query_khachhang, conn)

                query_doanhthu = """
                    SELECT strftime('%Y-%m', NgayBan) AS Thang, SUM(DonGia) AS DoanhThu
                    FROM DonHang
                    GROUP BY Thang
                    ORDER BY Thang DESC
                    LIMIT 12
                """
                df_doanhthu = pd.read_sql(query_doanhthu, conn)

            return df_sanpham, df_khachhang, df_doanhthu
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()  # Return empty DataFrames on error

    def ve_bieu_do_san_pham(self, parent, df):
        frame = tk.Frame(parent, bg="white")
        frame.pack(side="left", padx=10, pady=10)

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(df["TenSPham"], df["TongBan"], color="blue")
        ax.set_title("Top 5 sản phẩm bán chạy")
        ax.set_xlabel("Sản phẩm")
        ax.set_ylabel("Số lượng bán")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack()

    def ve_bieu_do_khach_hang(self, parent, df):
        frame = tk.Frame(parent, bg="white")
        frame.pack(side="left", padx=10, pady=10)

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(df["Ten"], df["SoDon"], color="green")
        ax.set_title("Top 5 khách hàng thân thiết")
        ax.set_xlabel("Khách hàng")
        ax.set_ylabel("Số đơn hàng")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack()
    #
    # def ve_bieu_do_doanh_thu(self, parent, df):
    #     frame = tk.Frame(parent, bg="white")
    #     frame.pack(side="left", padx=10, pady=10)
    #
    #     fig, ax = plt.subplots(figsize=(5, 3))
    #     ax.plot(df["Thang"], df["DoanhThu"], marker="o", linestyle="-", color="red")
    #     ax.set_title("Doanh thu theo tháng")
    #     ax.set_xlabel("Tháng")
    #     ax.set_ylabel("Doanh thu (VNĐ)")
    #
    #     canvas = FigureCanvasTkAgg(fig, master=frame)
    #     canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = ThongKe(root)
    root.mainloop()