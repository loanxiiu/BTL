from model.dao.ChiTietPhieuNhapDAO import ChiTietPhieuNhapDAO
from model.ChiTietPhieuNhap import ChiTietPhieuNhap

class ChiTietPhieuNhapController:
    def __init__(self):
        self.chi_tiet_pn_dao = ChiTietPhieuNhapDAO()

    def lay_tat_ca(self):
        try:
            return self.chi_tiet_pn_dao.lay_tat_ca()
        except Exception as e:
            print(e)

    def lay_bang_id(self, ma_ctpn):
        try:
            return self.chi_tiet_pn_dao.lay_bang_id(int(ma_ctpn))
        except Exception as e:
            print(e)

    def them(self, ma_sp, so_luong, don_gia):
        try:
            chi_tiet_pn = ChiTietPhieuNhap(ma_sp=ma_sp, so_luong=so_luong, don_gia=don_gia)
            self.chi_tiet_pn_dao.tao(chi_tiet_pn)
        except Exception as e:
            print(e)

    def sua(self, ma_ctpn, ma_sp=None, so_luong=None, don_gia=None):
        try:
            chi_tiet_pn = self.chi_tiet_pn_dao.lay_bang_id(int(ma_ctpn))
            if chi_tiet_pn:
                chi_tiet_pn.ma_sp = ma_sp or chi_tiet_pn.ma_sp
                chi_tiet_pn.so_luong = so_luong or chi_tiet_pn.so_luong
                chi_tiet_pn.don_gia = don_gia or chi_tiet_pn.don_gia
                self.chi_tiet_pn_dao.sua(chi_tiet_pn)
        except Exception as e:
            print(e)

    def xoa(self, ma_ctpn):
        try:
            self.chi_tiet_pn_dao.xoa(int(ma_ctpn))
        except Exception as e:
            print(e)
