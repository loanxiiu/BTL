from model.dao.connect.DatabaseConnect import conn, cur
from model.DanhMuc import DanhMuc

class DanhMucDAO:
    def __init__(self):
        pass

    def lay_tc(self):
        cur.execute("SELECT * FROM DanhMuc")
        danh_muc = cur.fetchall()
        return [DanhMuc(ma_dm=row[0], ten_dm=row[1]) for row in danh_muc]

    def lay_bang_id(self, id):
        cur.execute("SELECT * FROM DanhMucs WHERE id = ?", (id))
        row = cur.fetchone()
        if row:
            return DanhMuc(row[0], row[1])
        return None

    def dem(self):
        cur.execute("SELECT COUNT(*) FROM DanhMuc")
        return cur.fetchone()[0]

    def tao(self, danh_muc: DanhMuc):
        cur.execute("INSERT INTO DanhMuc (MaDM, TenDM) VALUES (?, ?)", (danh_muc.ma_dm, danh_muc.ten_dm))
        conn.commit()

    def sua(self, danh_muc: DanhMuc):
        cur.execute("UPDATE DanhMuc SET TenDM = ? WHERE id = ?", (danh_muc.ten_dm, danh_muc.ma_dm))
        conn.commit()

    def xoa(self, id):
        cur.execute("DELETE FROM DanhMucs WHERE id = ?", (id))
        conn.commit()