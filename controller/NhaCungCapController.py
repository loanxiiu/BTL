from model.dao.NhaCungCapDAO import NhaCungCapDAO
from model.NhaCungCap import NhaCungCap

class NhaCungCapController:
    def __init__(self):
        self.nha_cung_cap_dao = NhaCungCapDAO()

    def lay_tc(self):
        try:
            nha_cung_cap = self.lay_tc()
            return nha_cung_cap
        except Exception as e:
            print(e)

    def lay_bang_id(self, ma_ncc):
        try:
            nha_cung_cap = self.nha_cung_cap_dao.lay_bang_id(int(ma_ncc))
            return nha_cung_cap
        except Exception as e:
            print(e)
            
    def dem(self):
        try:
            return self.nha_cung_cap_dao.dem()
        except Exception as e:
            print(e)

    def them(self, ten_ncc, dia_chi, sdt):
        try:
            nha_cung_cap = NhaCungCap(ten_ncc, dia_chi, sdt)
            self.nha_cung_cap_dao.tao(nha_cung_cap)
        except Exception as e:
            print(e)

    def sua(self, ma_ncc, ten_ncc, dia_chi, sdt):
        try:
            nha_cung_cap = self.nha_cung_cap_dao.lay_bang_id(int(ma_ncc))
            if nha_cung_cap:
                nha_cung_cap.ten_ncc = ten_ncc or nha_cung_cap.ten_ncc
                nha_cung_cap.dia_chi = dia_chi or nha_cung_cap.dia_chi
                nha_cung_cap.sdt = sdt or nha_cung_cap.sdt
                self.nha_cung_cap_dao.sua(nha_cung_cap)
        except Exception as e:
            print(e)

    def xoa(self, ma_ncc):
        try:
            self.nha_cung_cap_dao.xoa(int(ma_ncc))
        except Exception as e:
            print(e)