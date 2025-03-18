from model.dao.connect.DatabaseConnect import cur, conn
from model.User import User


class UserDAO:
    def __init__(self):
        pass

    def lay_tc(self):
        cur.execute("SELECT * FROM Users")
        users = cur.fetchall()
        return [User(id=row[0], ten=row[1], dia_chi=row[2], sdt=row[3]) for row in users]

    def lay_bang_id(self, user_id):
        cur.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            return User(id=row[0], ten=row[1], dia_chi=row[2], sdt=row[3])
        return None

    def tao(self, user: User):
        cur.execute("INSERT INTO Users (Ten, DiaChi, SDT) VALUES (?, ?, ?)",
                            (user.ten, user.dia_chi, user.sdt))
        conn.commit()

    def sua(self, user: User):
        cur.execute("UPDATE Users SET ten = ?, DiaChi = ?, SDT = ? WHERE id = ?",
                            (user.ten, user.dia_chi, user.sdt, user.id))
        conn.commit()

    def xoa(self, user_id):
        cur.execute("DELETE FROM Users WHERE id = ?", (user_id,))
        conn.commit()
