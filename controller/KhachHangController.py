from model.dao.KhachHangDAO import KhachHangDAO
from model.KhachHang import KhachHang

class KhachHangController:
    def __init__(self):
        self.khach_hang_dao = KhachHangDAO()

    def lay_tc(self):
        try:
            return self.khach_hang_dao.lay_tc()
        except Exception as e:
            print(e)

    def lay_bang_id(self, ma_kh):
        try:
            return self.khach_hang_dao.lay_bang_id(int(ma_kh))
        except Exception as e:
            print(e)

    def dem(self):
        try:
            return self.khach_hang_dao.dem()
        except Exception as e:
            print(e)

    def them(self, ten, dia_chi, sdt):
        try:
            khach_hang = KhachHang(ten, dia_chi, sdt)
            self.khach_hang_dao.tao(khach_hang)
        except Exception as e:
            print(e)

    def sua(self, ma_kh, ten, dia_chi, sdt):
        try:
            khach_hang = self.khach_hang_dao.lay_bang_id(int(ma_kh))
            if khach_hang:
                khach_hang.ten = ten or khach_hang.ten
                khach_hang.dia_chi = dia_chi or khach_hang.dia_chi
                khach_hang.sdt = sdt or khach_hang.sdt
                self.khach_hang_dao.sua(khach_hang)
        except Exception as e:
            print(e)

    def xoa(self, ma_kh):
        try:
            self.khach_hang_dao.xoa(int(ma_kh))
        except Exception as e:
            print(e)
