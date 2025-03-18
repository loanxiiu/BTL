from model.dao.PhieuNhapDAO import PhieuNhapDAO
from model.PhieuNhap import PhieuNhap

class PhieuNhapController:
    def __init__(self):
        self.phieu_nhap_dao = PhieuNhapDAO()

    def lay_tc(self):
        try:
            return self.phieu_nhap_dao.lay_tat_ca()
        except Exception as e:
            print(e)

    def lay_bang_id(self, ma_pn):
        try:
            return self.phieu_nhap_dao.lay_bang_id(int(ma_pn))
        except Exception as e:
            print(e)

    def dem(self):
        try:
            return self.phieu_nhap_dao.dem()
        except Exception as e:
            print(e)

    def them(self, ngay_nhap, ma_quan_ly, ma_ncc):
        try:
            phieu_nhap = PhieuNhap(ngay_nhap=ngay_nhap, ma_quan_ly=ma_quan_ly, ma_ncc=ma_ncc)
            self.phieu_nhap_dao.tao(phieu_nhap)
        except Exception as e:
            print(e)

    def sua(self, ma_pn, ngay_nhap, ma_quan_ly, ma_ncc):
        try:
            phieu_nhap = self.phieu_nhap_dao.lay_bang_id(int(ma_pn))
            if phieu_nhap:
                phieu_nhap.ngay_nhap = ngay_nhap or phieu_nhap.ngay_nhap
                phieu_nhap.ma_quan_ly = ma_quan_ly or phieu_nhap.ma_quan_ly
                phieu_nhap.ma_ncc = ma_ncc or phieu_nhap.ma_ncc
                self.phieu_nhap_dao.sua(phieu_nhap)
        except Exception as e:
            print(e)

    def xoa(self, ma_pn):
        try:
            self.phieu_nhap_dao.xoa(int(ma_pn))
        except Exception as e:
            print(e)
