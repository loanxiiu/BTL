from model.dao.connect.DatabaseConnect import conn, cur
from model.Face import Face

class FaceDAO:
    def __init__(self):
        pass

    def tao(self, face: Face):
        cur.execute("INSERT INTO face_data (id, MaTK, face_encoding, created_at) VALUES (?, ?, ?, ?)",
                                (face.id, face.user_id, face.face_encoding, face.created_at))
        conn.commit()

    def sua(self, face: Face):
        cur.execute("UPDATE face_data SET face_encoding = ? WHERE MaTK = ?",(face.face_encoding, face.user_id))
        conn.commit()

    def xoa(self, user_id):
        cur.execute("DELETE FROM face_data WHERE MaTK = ?",(user_id))
        conn.commit()

    def lay_tat_ca(self):
        cur.execute("SELECT * FROM face_data")
        return cur.fetchall()

    def lay_bang_face_encoding(self, face_encoding):
        cur.execute("SELECT MaTK FROM face_data WHERE face_encoding = ?", (face_encoding,))
        print(cur.fetchone())
        return cur.fetchone()