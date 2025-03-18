from model.dao.connect.DatabaseConnect import cur, conn
from model.DonHang import DonHang

class DonHangDAO:
    def __init__(self):
        pass

    def lay_tat_ca(self):
        cur.execute("SELECT * FROM DonHang")
        return cur.fetchall()

    def lay_bang_id(self, ma_don_hang):
        cur.execute("SELECT * FROM DonHang WHERE MaDH = ?", (ma_don_hang,))
        row = cur.fetchone()
        if row:
            return DonHang(ma_don_hang=row[0], ma_kh=row[1], ngay_ban=row[2], don_gia=row[3], ma_nv=row[4])
        return None

    def dem(self):
        cur.execute("SELECT COUNT(*) FROM DonHang")
        return cur.fetchone()[0]

    def tao(self, don_hang: DonHang):
        cur.execute("INSERT INTO DonHang (MaKH, NgayBan, DonGia, MaNV) VALUES (?, ?, ?, ?)",
                    (don_hang.ma_kh, don_hang.ngay_ban, don_hang.don_gia, don_hang.ma_nv))
        conn.commit()

    def sua(self, don_hang: DonHang):
        cur.execute("UPDATE DonHang SET MaKH=?, NgayBan=?, DonGia=?, MaNV=? WHERE MaDH=?",
                    (don_hang.ma_kh, don_hang.ngay_ban, don_hang.don_gia, don_hang.ma_nv, don_hang.ma_don_hang))
        conn.commit()

    def xoa(self, ma_don_hang):
        cur.execute("DELETE FROM DonHang WHERE MaDH = ?", (ma_don_hang,))
        conn.commit()
