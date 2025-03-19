import os
import sqlite3

from model.dao.SanPhamDAO import SanPhamDAO
from model.SanPham import SanPham

class SanPhamController:
    def __init__(self):
        self.san_pham_dao = SanPhamDAO()

    def lay_tc(self):
        try:
            return self.san_pham_dao.lay_tat_ca()
        except Exception as e:
            print(e)

    def lay_bang_id(self, ma_sp):
        try:
            return self.san_pham_dao.lay_bang_id(int(ma_sp))
        except Exception as e:
            print(e)

    def dem(self):
        try:
            return self.san_pham_dao.dem()
        except Exception as e:
            print(e)

    def them(self, ten_sp=None, so_luong=None, don_gia=None, mo_ta=None, ma_dm=None, anh=None):
        try:
            san_pham = SanPham(ten_sp=ten_sp, so_luong=so_luong, don_gia=don_gia, mo_ta=mo_ta, ma_dm=ma_dm, anh=anh)
            self.san_pham_dao.tao(san_pham)
        except Exception as e:
            print(e)

    def sua(self, ma_sp, ten_sp=None, so_luong=None, don_gia=None, mo_ta=None, ma_dm=None, anh=None):
        try:
            san_pham = self.san_pham_dao.lay_bang_id(int(ma_sp))
            print(san_pham)
            if san_pham:
                ten_sp = ten_sp or san_pham[1]  # Chỉ mục 1 là tên sản phẩm
                so_luong = so_luong or san_pham[2]
                don_gia = don_gia or san_pham[3]
                mo_ta = mo_ta or san_pham[6]
                ma_dm = ma_dm or san_pham[4]
                anh = anh or san_pham[5]
                san_pham = SanPham(ma_sp=ma_sp, ten_sp=ten_sp, so_luong=so_luong, don_gia=don_gia, mo_ta=mo_ta, ma_dm=ma_dm, anh=anh)
                self.san_pham_dao.sua(san_pham)
        except Exception as e:
            print(e)

    def xoa(self, ma_sp):
        try:
            self.san_pham_dao.xoa(int(ma_sp))
        except Exception as e:
            print(e)

    def lay_bang_ten(self, ten_sp):
        try:
            return self.san_pham_dao.lay_bang_ten(ten_sp)
        except Exception as e:
            print(e)

    def tao_de_xuat_mua_hang(self):
        ds_san_pham = self.lay_tc()
        du_bao = self.du_bao_nhu_cau()  # Hàm dự báo giả định
        de_xuat = []
        for sp, nhu_cau in zip(ds_san_pham, du_bao):
            so_luong_hien_tai = sp[2]  # Chỉ mục 2 là SoLuong
            if nhu_cau > so_luong_hien_tai:
                de_xuat.append({
                    "MaSP": sp[0],
                    "SoLuongCanNhap": nhu_cau - so_luong_hien_tai,
                    "TenSP": sp[1]
                })
        print(de_xuat)
        return de_xuat

    def du_bao_nhu_cau(self):
        import pandas as pd
        from sklearn.ensemble import RandomForestRegressor

        # Xác định thư mục gốc của dự án
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Lấy thư mục chứa file đang chạy
        DB_PATH = os.path.join(BASE_DIR, "..", "model", "dao", "connect", "ITSHOP.db")
        # Lấy dữ liệu lịch sử
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query("SELECT SanPham.MaSPham, SanPham.TenSPham, SUM(ChiTietDonHang.SoLuong) AS TongBan, strftime('%Y-%m', DonHang.NgayBan) AS Thang FROM ChiTietDonHang JOIN SanPham ON ChiTietDonHang.MaSP = SanPham.MaSPham JOIN DonHang ON ChiTietDonHang.MaDH = DonHang.MaDH GROUP BY SanPham.MaSPham, SanPham.TenSPham, Thang", conn)

        # Chuẩn bị dữ liệu cho mô hình
        df["Thang"] = pd.to_datetime(df["Thang"])
        X = df[["MaSPham", "Thang"]].pivot(index="Thang", columns="MaSPham", values="MaSPham").fillna(0)
        y = df.groupby("MaSPham")["TongBan"].sum()

        # Huấn luyện mô hình
        model = RandomForestRegressor(n_estimators=100)
        model.fit(X, y)

        # Dự báo (giả định tháng tiếp theo)
        thang_tiep_theo = pd.to_datetime("2024-11")
        X_new = pd.DataFrame(columns=X.columns, index=[thang_tiep_theo]).fillna(0)
        du_bao = model.predict(X_new)
        return du_bao