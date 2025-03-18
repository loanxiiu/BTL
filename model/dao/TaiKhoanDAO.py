from model.dao.connect.DatabaseConnect import conn, cur
from model.TaiKhoan import TaiKhoan

class TaiKhoanDAO:
    def __init__(self):
        pass

    def lay_tat_ca(self):
        cur.execute("SELECT * FROM TaiKhoan")
        rows = cur.fetchall()
        return [TaiKhoan(id=row[0], username=row[1], password=row[2], ma_quyen=row[3]) for row in rows]

    def lay_bang_id(self, id):
        cur.execute("SELECT * FROM TaiKhoan WHERE MaTK = ?", (id,))
        return cur.fetchone()

    def lay_bang_user_id(self, user_id):
        cur.execute("SELECT * FROM TaiKhoan WHERE user_id = ?", (user_id,))
        return cur.fetchone()

    def tao(self, tai_khoan: TaiKhoan):
        cur.execute("INSERT INTO TaiKhoan (username, password, MaQuyen) VALUES (?, ?, ?)",
                    (tai_khoan.username, tai_khoan.password, tai_khoan.ma_quyen))
        conn.commit()

    def sua(self, tai_khoan: TaiKhoan):
        cur.execute("UPDATE TaiKhoan SET username = ?, password = ?, MaQuyen = ? WHERE MaTK = ?",
                    (tai_khoan.username, tai_khoan.password, tai_khoan.ma_quyen, tai_khoan.id))
        conn.commit()

    def xoa(self, id):
        cur.execute("DELETE FROM TaiKhoan WHERE MaTK = ?", (id,))
        conn.commit()

    def kiem_tra_dang_nhap(self, username, password):
        cur.execute("SELECT * FROM TaiKhoan WHERE username = ? AND password = ?", (username, password))
        return cur.fetchone()

    def kiem_tra_tai_khoan(self, username):
        cur.execute("SELECT * FROM TaiKhoan WHERE username = ?", (username,))
        return cur.fetchone()
