from model.dao.connect.DatabaseConnect import cur, conn
from model.PhieuNhap import PhieuNhap

class PhieuNhapDAO:
    def __init__(self):
        pass

    def lay_tat_ca(self):
        cur.execute("SELECT * FROM PhieuNhap")
        phieu_nhap = cur.fetchall()
        return [PhieuNhap(ma_pn=row[0], ngay_nhap=row[1], ma_quan_ly=row[2], ma_ncc=row[3]) for row in phieu_nhap]

    def lay_bang_id(self, ma_pn):
        cur.execute("SELECT * FROM PhieuNhap WHERE MaPN = ?", (ma_pn,))
        row = cur.fetchone()
        if row:
            return PhieuNhap(ma_pn=row[0], ngay_nhap=row[1], ma_quan_ly=row[2], ma_ncc=row[3])
        return None

    def dem(self):
        cur.execute("SELECT COUNT(*) FROM PhieuNhap")
        return cur.fetchone()[0]

    def tao(self, phieu_nhap: PhieuNhap):
        cur.execute("INSERT INTO PhieuNhap (NgayNhap, MaQL, MaNCC) VALUES (?, ?, ?)",
                    (phieu_nhap.ngay_nhap, phieu_nhap.ma_quan_ly, phieu_nhap.ma_ncc))
        conn.commit()

    def sua(self, phieu_nhap: PhieuNhap):
        cur.execute("UPDATE PhieuNhap SET NgayNhap=?, MaQL=?, MaNCC=? WHERE MaPN=?",
                    (phieu_nhap.ngay_nhap, phieu_nhap.ma_quan_ly, phieu_nhap.ma_ncc, phieu_nhap.ma_pn))
        conn.commit()

    def xoa(self, ma_pn):
        cur.execute("DELETE FROM PhieuNhap WHERE MaPN = ?", (ma_pn,))
        conn.commit()
