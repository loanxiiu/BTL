from model.dao.ChiTietDonHangDAO import ChiTietDonHangDAO
from model.ChiTietDonHang import ChiTietDonHang

class ChiTietDonHangController:
    def __init__(self):
        self.chi_tiet_dh_dao = ChiTietDonHangDAO()

    def lay_tc(self):
        try:
            return self.chi_tiet_dh_dao.lay_tat_ca()
        except Exception as e:
            print(e)

    def lay_bang_id(self, ma_ctdh):
        try:
            return self.chi_tiet_dh_dao.lay_bang_id(int(ma_ctdh))
        except Exception as e:
            print(e)

    def them(self, ma_dh, so_luong, don_gia, ma_sp):
        try:
            chi_tiet_dh = ChiTietDonHang(ma_dh=ma_dh, so_luong=so_luong, don_gia=don_gia, ma_sp=ma_sp)
            self.chi_tiet_dh_dao.tao(chi_tiet_dh)
        except Exception as e:
            print(e)

    def sua(self, ma_ctdh, ma_dh=None, so_luong=None, don_gia=None):
        try:
            chi_tiet_dh = self.chi_tiet_dh_dao.lay_bang_id(int(ma_ctdh))
            if chi_tiet_dh:
                chi_tiet_dh.ma_dh = ma_dh or chi_tiet_dh.ma_dh
                chi_tiet_dh.so_luong = so_luong or chi_tiet_dh.so_luong
                chi_tiet_dh.don_gia = don_gia or chi_tiet_dh.don_gia
                chi_tiet_dh.ma_sp = so_luong or chi_tiet_dh.ma_sp
                self.chi_tiet_dh_dao.sua(chi_tiet_dh)
        except Exception as e:
            print(e)

    def xoa(self, ma_ctdh):
        try:
            self.chi_tiet_dh_dao.xoa(int(ma_ctdh))
        except Exception as e:
            print(e)
