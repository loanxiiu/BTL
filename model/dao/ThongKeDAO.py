import sqlite3
import pandas as pd
import os

class ThongKeDAO:
    def __init__(self):
        # Chemin absolu vers la base de données
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.db_path = os.path.join(BASE_DIR, "model", "dao", "connect", "ITSHOP.db")

    def get_doanhthu_data(self, start_date, end_date, time_format):
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = f"""
                    SELECT strftime('{time_format}', NgayBan) AS ThoiGian, 
                           SUM(DonGia) AS DoanhThu
                    FROM DonHang
                    WHERE NgayBan BETWEEN ? AND ?
                    GROUP BY ThoiGian
                    ORDER BY ThoiGian
                """
                df = pd.read_sql(query, conn, params=(start_date, end_date))
                return df
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return pd.DataFrame()

    def get_sanpham_data(self, start_date, end_date):
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = """
                    SELECT sp.MaSPham, sp.TenSPham, 
                           COALESCE(SUM(ctdh.SoLuong), 0) AS SoLuongBan,
                           COALESCE(SUM(ctdh.SoLuong * ctdh.DonGia), 0) AS DoanhThu,
                           sp.SoLuong AS TonKho
                    FROM SanPham sp
                    LEFT JOIN ChiTietDonHang ctdh ON sp.MaSPham = ctdh.MaSP
                    LEFT JOIN DonHang dh ON ctdh.MaDH = dh.MaDH
                    WHERE (dh.NgayBan BETWEEN ? AND ?) OR dh.NgayBan IS NULL
                    GROUP BY sp.MaSPham, sp.TenSPham, sp.SoLuong
                    ORDER BY SoLuongBan DESC
                """
                df = pd.read_sql(query, conn, params=(start_date, end_date))
                return df
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return pd.DataFrame()

    def get_donhang_data(self, start_date, end_date, time_format):
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = f"""
                    SELECT strftime('{time_format}', NgayBan) AS ThoiGian,
                           COUNT(MaDH) AS SoDon,
                           AVG(DonGia) AS GiaTriTrungBinh
                    FROM DonHang
                    WHERE NgayBan BETWEEN ? AND ?
                    GROUP BY ThoiGian
                    ORDER BY ThoiGian
                """
                df = pd.read_sql(query, conn, params=(start_date, end_date))
                return df
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return pd.DataFrame()

    def get_doanhthu_summary(self, start_date, end_date):
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = "SELECT SUM(DonGia) AS DoanhThu FROM DonHang WHERE NgayBan BETWEEN ? AND ?"
                df = pd.read_sql(query, conn, params=(start_date, end_date))
                return df['DoanhThu'].iloc[0] if not df.empty and pd.notna(df['DoanhThu'].iloc[0]) else 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0

    def get_donhang_summary(self, start_date, end_date):
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = """
                    SELECT COUNT(MaDH) AS SoLuongDon, 
                           AVG(DonGia) AS GiaTriTrungBinh,
                           SUM(DonGia) AS TongGiaTri
                    FROM DonHang
                    WHERE NgayBan BETWEEN ? AND ?
                """
                df = pd.read_sql(query, conn, params=(start_date, end_date))
                return {
                    'SoLuongDon': df['SoLuongDon'].iloc[0] if not df.empty and pd.notna(df['SoLuongDon'].iloc[0]) else 0,
                    'GiaTriTrungBinh': df['GiaTriTrungBinh'].iloc[0] if not df.empty and pd.notna(df['GiaTriTrungBinh'].iloc[0]) else 0,
                    'TongGiaTri': df['TongGiaTri'].iloc[0] if not df.empty and pd.notna(df['TongGiaTri'].iloc[0]) else 0
                }
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {'SoLuongDon': 0, 'GiaTriTrungBinh': 0, 'TongGiaTri': 0}