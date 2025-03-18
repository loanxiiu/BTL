from model.dao.NhanVienDAO import NhanVienDAO
from model.NhanVien import NhanVien

class NhanVienController:
    def __init__(self):
        self.nhan_vien_dao = NhanVienDAO()

    def lay_tc(self):
        try:
            return self.nhan_vien_dao.lay_tc()
        except Exception as e:
            print(e)

    def lay_bang_id(self, ma_nv):
        try:
            return self.nhan_vien_dao.lay_bang_id(int(ma_nv))
        except Exception as e:
            print(e)

    def dem(self):
        try:
            return self.nhan_vien_dao.dem()
        except Exception as e:
            print(e)

    def them(self, ten, dia_chi, sdt):
        try:
            nhan_vien = NhanVien(ten, dia_chi, sdt)
            self.nhan_vien_dao.tao(nhan_vien)
        except Exception as e:
            print(e)

    def sua(self, ma_nv, ten, dia_chi, sdt):
        try:
            nhan_vien = self.nhan_vien_dao.lay_bang_id(int(ma_nv))
            if nhan_vien:
                nhan_vien.ten = ten or nhan_vien.ten
                nhan_vien.dia_chi = dia_chi or nhan_vien.dia_chi
                nhan_vien.sdt = sdt or nhan_vien.sdt
                self.nhan_vien_dao.sua(nhan_vien)
        except Exception as e:
            print(e)

    def xoa(self, ma_nv):
        try:
            self.nhan_vien_dao.xoa(int(ma_nv))
        except Exception as e:
            print(e)

    def lay_bang_ten(self, ten):
        try:
            return self.nhan_vien_dao.lay_bang_ten(ten)
        except Exception as e:
            print(e)
