from model.dao.connect.DatabaseConnect import conn, cur
from model.KhachHang import KhachHang

class KhachHangDAO:
    def __init__(self):
        pass

    def lay_tc(self):
        cur.execute("SELECT * FROM Users WHERE id NOT IN (SELECT MaTK FROM TaiKhoan)")
        return cur.fetchall()

    def lay_bang_id(self, id):
        cur.execute("SELECT * FROM Users WHERE id = ? AND id NOT IN (SELECT MaTK FROM TaiKhoan)", (id,))
        return cur.fetchone()

    def dem(self):
        cur.execute("""
               SELECT COUNT(*) FROM Users 
               WHERE id NOT IN (SELECT MaTK FROM TaiKhoan)
           """)
        count = cur.fetchone()[0]
        return count

    def tao(self, khach_hang: KhachHang):
        cur.execute("INSERT INTO Users (Ten, DiaChi, SDT) VALUES (?, ?, ?)", (khach_hang.ten, khach_hang.dia_chi, khach_hang.sdt))
        conn.commit()

    def sua(self, khach_hang: KhachHang):
        cur.execute("UPDATE Users SET Ten = ?, DiaChi = ?, SDT = ? WHERE id = ?", 
                    (khach_hang.ten, khach_hang.dia_chi, khach_hang.sdt, khach_hang.id))
        conn.commit()

    def xoa(self, id):
        cur.execute("DELETE FROM Users WHERE id = ?", (id,))
        conn.commit()
