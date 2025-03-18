from model.dao.DonHangDAO import DonHangDAO
from model.DonHang import DonHang

class DonHangController:
    def __init__(self):
        self.don_hang_dao = DonHangDAO()

    def lay_tc(self):
        try:
            return self.don_hang_dao.lay_tat_ca()
        except Exception as e:
            print(e)

    def lay_bang_id(self, ma_dh):
        try:
            return self.don_hang_dao.lay_bang_id(int(ma_dh))
        except Exception as e:
            print(e)

    def dem(self):
        try:
            return self.don_hang_dao.dem()
        except Exception as e:
            print(e)

    def them(self, ma_kh, ngay_ban, don_gia, ma_nv):
        try:
            don_hang = DonHang(ma_kh=ma_kh, ngay_ban=ngay_ban, don_gia=don_gia, ma_nv=ma_nv)
            self.don_hang_dao.tao(don_hang)
        except Exception as e:
            print(e)

    def sua(self, ma_dh, ma_kh=None, ngay_ban=None, don_gia=None, ma_nv=None):
        try:
            don_hang = self.don_hang_dao.lay_bang_id(int(ma_dh))
            if don_hang:
                don_hang.ma_kh = ma_kh or don_hang.ma_kh
                don_hang.ngay_ban = ngay_ban or don_hang.ngay_ban
                don_hang.don_gia = don_gia or don_hang.don_gia
                don_hang.ma_nv = ma_nv or don_hang.ma_nv
                self.don_hang_dao.sua(don_hang)
        except Exception as e:
            print(e)

    def xoa(self, ma_dh):
        try:
            self.don_hang_dao.xoa(int(ma_dh))
        except Exception as e:
            print(e)
