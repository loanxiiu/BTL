from model.dao.QuanLyDAO import QuanLyDAO
from model.QuanLy import QuanLy

class QuanLyController:
    def __init__(self):
        self.quan_ly_dao = QuanLyDAO()

    def lay_tc(self):
        try:
            return self.quan_ly_dao.lay_tc()
        except Exception as e:
            print(e)

    def lay_bang_id(self, ma_ql):
        try:
            return self.quan_ly_dao.lay_bang_id(int(ma_ql))
        except Exception as e:
            print(e)

    def dem(self):
        try:
            return self.quan_ly_dao.dem()
        except Exception as e:
            print(e)

    def dem(self):
        try:
            return self.quan_ly_dao.dem()
        except Exception as e:
            print(e)

    def them(self, ten, dia_chi, sdt):
        try:
            quan_ly = QuanLy(ten, dia_chi, sdt)
            self.quan_ly_dao.tao(quan_ly)
        except Exception as e:
            print(e)

    def sua(self, ma_ql, ten, dia_chi, sdt):
        try:
            quan_ly = self.quan_ly_dao.lay_bang_id(int(ma_ql))
            if quan_ly:
                quan_ly.ten = ten or quan_ly.ten
                quan_ly.dia_chi = dia_chi or quan_ly.dia_chi
                quan_ly.sdt = sdt or quan_ly.sdt
                self.quan_ly_dao.sua(quan_ly)
        except Exception as e:
            print(e)

    def xoa(self, ma_ql):
        try:
            self.quan_ly_dao.xoa(int(ma_ql))
        except Exception as e:
            print(e)
