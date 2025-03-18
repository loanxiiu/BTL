from model.dao.connect.DatabaseConnect import conn, cur
from model.NhaCungCap import NhaCungCap

class NhaCungCapDAO:
    def __init__(self):
        pass

    def lay_tc(self):
        cur.execute("SELECT * FROM NhaCungCap")
        nha_cung_cap = cur.fetchall()
        return [NhaCungCap(ma_ncc=row[0], ten_ncc=row[1], dia_chi=row[2], sdt=row[3]) for row in nha_cung_cap]

    def lay_bang_id(self, ma_ncc):
        cur.execute("SELECT * FROM NhaCungCap WHERE MaNCC = ?", (ma_ncc))
        row = cur.fetchone()
        if row:
            return NhaCungCap(row[0], row[1], row[2], row[3])
        return None

    def dem(self):
        cur.execute("SELECT COUNT(*) FROM NhaCungCap")
        return cur.fetchone()[0]

    def tao(self, nha_cung_cap : NhaCungCap):
        cur.execute("INSERT INTO NhaCungCap(TenNCC, DiaChi, SDT) VALUES (?, ?, ?)", (nha_cung_cap.ten_ncc, nha_cung_cap.dia_chi, nha_cung_cap.sdt))
        conn.commit()

    def sua(self, nha_cung_cap : NhaCungCap):
        cur.execute("UPDATE NhaCungCap SET TenNCC = ?, DiaChi=?, SDT=? WHERE MaNCC = ?",(nha_cung_cap.ten_ncc, nha_cung_cap.dia_chi, nha_cung_cap.sdt, nha_cung_cap.ma_ncc))
        conn.commit()

    def xoa(self, ma_ncc):
        cur.execute("DELETE FROM NhaCungCap WHERE MaNCC = ?", (ma_ncc))
        conn.commit()
