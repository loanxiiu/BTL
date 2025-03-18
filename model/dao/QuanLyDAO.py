from model.dao.connect.DatabaseConnect import conn, cur
from model.QuanLy import QuanLy

class QuanLyDAO:
    def __init__(self):
        pass

    def lay_tc(self):
        cur.execute("""
            SELECT u.id, u.Ten, u.DiaChi, u.SDT FROM Users u
            JOIN TaiKhoan t ON u.id = t.MaTK WHERE t.MaQuyen = 1
        """)
        quan_ly = cur.fetchall()
        return [QuanLy(id=row[0], ten=row[1], dia_chi=row[2], sdt=row[3]) for row in quan_ly]

    def lay_bang_id(self, id):
        cur.execute("""
            SELECT u.id, u.Ten, u.DiaChi, u.SDT FROM Users u
            JOIN TaiKhoan t ON u.id = t.MaTK WHERE t.MaQuyen = 1 AND u.id = ?
        """, (id,))
        row = cur.fetchone()
        return QuanLy(id=row[0], ten=row[1], dia_chi=row[2], sdt=row[3]) if row else None

    def dem(self):
        cur.execute("SELECT COUNT(*) FROM TaiKhoan WHERE MaQuyen = 1")
        return cur.fetchone()[0]

    def tao(self, quan_ly):
        cur.execute("INSERT INTO Users (Ten, DiaChi, SDT) VALUES (?, ?, ?)",
                    (quan_ly.ten, quan_ly.dia_chi, quan_ly.sdt))
        user_id = cur.lastrowid
        cur.execute("INSERT INTO TaiKhoan (MaTK, username, password, MaQuyen) VALUES (?, ?, ?, 1)",
                    (user_id, quan_ly.ten.lower(), "admin123"))
        conn.commit()

    def sua(self, quan_ly):
        cur.execute("UPDATE Users SET Ten = ?, DiaChi = ?, SDT = ? WHERE id = ?",
                    (quan_ly.ten, quan_ly.dia_chi, quan_ly.sdt, quan_ly.id))
        conn.commit()

    def xoa(self, id):
        cur.execute("DELETE FROM TaiKhoan WHERE MaTK = ?", (id,))
        cur.execute("DELETE FROM Users WHERE id = ?", (id,))
        conn.commit()
