from model.dao.connect.DatabaseConnect import conn, cur
from model.Quyen import Quyen


class QuyenDAO:
    def __init__(self):
        pass

    def lay_tc(self):
        cur.execute("SELECT * FROM Quyen")
        quyen = cur.fetchall()
        return [Quyen(ma_quyen=row[0], ten_quyen=row[1]) for row in quyen]

    def lay_bang_id(self, id):
        cur.execute("SELECT * FROM Quyen WHERE MaQuyen = ?", (id,))
        row = cur.fetchone()
        if row:
            return Quyen(ma_quyen=row[0], ten_quyen=row[1])
        else:
            return None

    def tao(self, quyen: Quyen):
        cur.execute("INSERT INTO Quyen(MaQuyen, TenQuyen) VALUES (?, ?)", (quyen.ma_quyen, quyen.ten_quyen))
        conn.commit()

    def sua(self, quyen: Quyen):
        cur.execute("UPDATE Quyen SET TenQuyen= ? WHERE MaQuyen = ?", (quyen.ma_quyen, quyen.ten_quyen))
        conn.commit()

    def xoa(self, id):
        cur.execute("DELETE FROM Quyen WHERE MaQuyen = ?", (id,))
        conn.commit()