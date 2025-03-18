from model.dao.TaiKhoanDAO import TaiKhoanDAO
from model.TaiKhoan import TaiKhoan


class TaiKhoanController:
    def __init__(self):
        self.tai_khoan_dao = TaiKhoanDAO()

    def lay_tc(self):
        try:
            return self.tai_khoan_dao.lay_tat_ca()
        except Exception as e:
            print(e)

    def lay_bang_id(self, ma_tk):
        try:
            return self.tai_khoan_dao.lay_bang_id(int(ma_tk))
        except Exception as e:
            print(e)

    def lay_bang_user_id(self, user_id):
        try:
            data= self.tai_khoan_dao.lay_bang_user_id(int(user_id))
            return TaiKhoan(id=data[0], username=data[1], ma_quyen=data[3], user_id=data[4], password=None)
        except Exception as e:
            print(e)

    def them(self, username, password, ma_quyen):
        try:
            tai_khoan = TaiKhoan(username=username, password=password, ma_quyen=ma_quyen)
            self.tai_khoan_dao.tao(tai_khoan)
        except Exception as e:
            print(e)

    def sua(self, ma_tk, username, password, ma_quyen):
        try:
            tai_khoan = self.tai_khoan_dao.lay_bang_id(int(ma_tk))
            if tai_khoan:
                tai_khoan.username = username or tai_khoan.username
                tai_khoan.password = password or tai_khoan.password
                tai_khoan.ma_quyen = ma_quyen or tai_khoan.ma_quyen
                self.tai_khoan_dao.sua(tai_khoan)
        except Exception as e:
            print(e)

    def xoa(self, ma_tk):
        try:
            self.tai_khoan_dao.xoa(int(ma_tk))
        except Exception as e:
            print(e)

    def kiem_tra_dang_nhap(self, username, password):
        data = self.tai_khoan_dao.kiem_tra_dang_nhap(username, password)
        return TaiKhoan(id=data[0], username=data[1], ma_quyen=data[3], user_id=data[4], password=None)
