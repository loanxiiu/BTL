from model.dao.connect.DatabaseConnect import conn, cur


class NhanVienDAO:
    def __init__(self):
        pass

    def lay_tc(self):
        cur.execute("""
            SELECT u.id, u.Ten, u.DiaChi, u.SDT FROM Users u
            JOIN TaiKhoan t ON u.id = t.MaTK WHERE t.MaQuyen = 2
        """)
        return cur.fetchall()

    def lay_bang_id(self, id):
        cur.execute("""
            SELECT u.id, u.Ten, u.DiaChi, u.SDT FROM Users u
            JOIN TaiKhoan t ON u.id = t.MaTK WHERE t.MaQuyen = 2 AND u.id = ?
        """, (id,))
        return cur.fetchone()

    def dem(self):
        cur.execute("""
            SELECT COUNT(*) FROM TaiKhoan WHERE MaQuyen = 2
        """)
        count = cur.fetchone()[0]
        return count

    def tao(self, nhan_vien):
        cur.execute("INSERT INTO Users (Ten, DiaChi, SDT) VALUES (?, ?, ?)", (nhan_vien.ten, nhan_vien.dia_chi, nhan_vien.sdt))
        user_id = cur.lastrowid
        cur.execute("INSERT INTO TaiKhoan (MaTK, username, password, MaQuyen) VALUES (?, ?, ?, 2)",
                    (user_id, nhan_vien.ten, "123456"))
        conn.commit()

    def sua(self, nhan_vien):
        cur.execute("UPDATE Users SET Ten = ?, DiaChi = ?, SDT = ? WHERE id = ?",
                    (nhan_vien.ten, nhan_vien.dia_chi, nhan_vien.sdt, nhan_vien.id))
        conn.commit()

    def xoa(self, id):
        cur.execute("DELETE FROM TaiKhoan WHERE MaTK = ?", (id,))
        conn.commit()

    def lay_bang_ten(self, ten):
        cur.execute("SELECT u.id, u.Ten, u.DiaChi, u.SDT FROM Users u JOIN TaiKhoan t ON u.id = t.MaTK WHERE t.MaQuyen = 2 AND u.Ten like ?", ('%'+ten+'%',))
        return cur.fetchall()
