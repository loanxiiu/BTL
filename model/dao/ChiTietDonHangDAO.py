from model.dao.connect.DatabaseConnect import cur, conn
from model.ChiTietDonHang import ChiTietDonHang

class ChiTietDonHangDAO:
    def __init__(self):
        pass

    def lay_tat_ca(self):
        cur.execute("SELECT * FROM ChiTietDonHang")
        return cur.fetchall()

    def lay_bang_id(self, ma_ctdh):
        cur.execute("SELECT * FROM ChiTietDonHang WHERE MaCTDH = ?", (ma_ctdh,))
        return cur.fetchone()

    def tao(self, chi_tiet_dh: ChiTietDonHang):
        cur.execute("INSERT INTO ChiTietDonHang (MaDH, SoLuong, DonGia,MaSP) VALUES (?, ?, ?,?)",
                    (chi_tiet_dh.ma_dh, chi_tiet_dh.so_luong, chi_tiet_dh.don_gia, chi_tiet_dh.ma_sp))
        conn.commit()

    def sua(self, chi_tiet_dh: ChiTietDonHang):
        cur.execute("UPDATE ChiTietDonHang SET MaDH=?, SoLuong=?, DonGia=?, MaSP=? WHERE MaCTDH=?",
                    (chi_tiet_dh.ma_dh, chi_tiet_dh.so_luong, chi_tiet_dh.don_gia, chi_tiet_dh.ma_sp, chi_tiet_dh.ma_ctdh))
        conn.commit()

    def xoa(self, ma_ctdh):
        cur.execute("DELETE FROM ChiTietDonHang WHERE MaCTDH = ?", (ma_ctdh,))
        conn.commit()
