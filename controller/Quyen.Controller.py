from model.dao.QuyenDAO import QuyenDAO
from model.Quyen import Quyen

class QuyenController:
    def __init__(self):
        self.quyen_dao = QuyenDAO()

    def lay_tc(self):
        try:
            quyen = self.quyen_dao.lay_tc()
            return quyen
        except Exception as e:
            print(e)

    def lay_bang_id(self, ma_quyen):
        try:
            quyen = self.quyen_dao.lay_bang_id(int(ma_quyen))
            return quyen
        except Exception as e:
            print(e)

    def them(self, ten_quyen):
        try:
            quyen = Quyen(ten_quyen=ten_quyen)
            self.quyen_dao.tao(quyen)
        except Exception as e:
            print(e)

    def sua(self, ma_quyen, ten_quyen):
        try:
            quyen = self.quyen_dao.lay_bang_id(int(ma_quyen))
            if quyen:
                quyen.ten_quyen = ten_quyen or quyen.ten_quyen
                self.quyen_dao.sua(quyen)
        except Exception as e:
            print(e)


    def xoa(self, ma_quyen):
        try:
            self.quyen_dao.xoa(int(ma_quyen))
        except Exception as e:
            print(e)