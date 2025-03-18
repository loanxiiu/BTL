from model.dao.connect.DatabaseConnect import cur, conn
from model.ChiTietPhieuNhap import ChiTietPhieuNhap

class ChiTietPhieuNhapDAO:
    def __init__(self):
        pass

    def lay_tat_ca(self):
        cur.execute("SELECT * FROM ChiTietPhieuNhap")
        rows = cur.fetchall()
        return [ChiTietPhieuNhap(ma_ctpn=row[0], ma_sp=row[1], so_luong=row[2], don_gia=row[3]) for row in rows]

    def lay_bang_id(self, ma_ctpn):
        cur.execute("SELECT * FROM ChiTietPhieuNhap WHERE MaCTPN = ?", (ma_ctpn,))
        row = cur.fetchone()
        if row:
            return ChiTietPhieuNhap(ma_ctpn=row[0], ma_sp=row[1], so_luong=row[2], don_gia=row[3])
        return None

    def tao(self, chi_tiet_pn: ChiTietPhieuNhap):
        cur.execute("INSERT INTO ChiTietPhieuNhap (MaSP, SoLuong, DonGia) VALUES (?, ?, ?)",
                    (chi_tiet_pn.ma_sp, chi_tiet_pn.so_luong, chi_tiet_pn.don_gia))
        conn.commit()

    def sua(self, chi_tiet_pn: ChiTietPhieuNhap):
        cur.execute("UPDATE ChiTietPhieuNhap SET MaSP=?, SoLuong=?, DonGia=? WHERE MaCTPN=?",
                    (chi_tiet_pn.ma_sp, chi_tiet_pn.so_luong, chi_tiet_pn.don_gia, chi_tiet_pn.ma_ctpn))
        conn.commit()

    def xoa(self, ma_ctpn):
        cur.execute("DELETE FROM ChiTietPhieuNhap WHERE MaCTPN = ?", (ma_ctpn,))
        conn.commit()
