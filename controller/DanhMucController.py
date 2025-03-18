from model.dao.DanhMucDAO import DanhMucDAO
from model.DanhMuc import DanhMuc

class DanhMucController:
    def __init__(self):
        self.danh_muc_dao = DanhMucDAO()

    def lay_tc(self):
        try:
            danh_muc = self.danh_muc_dao.lay_tc()
            return danh_muc
        except Exception as e:
            print(e)

    def lay_bang_id(self, ma_dm):
        try:
            danh_muc = self.danh_muc_dao.lay_bang_id(int(ma_dm))
            return danh_muc
        except Exception as e:
            print(e)

    def dem(self):
        try:
            return self.danh_muc_dao.dem()
        except Exception as e:
            print(e)

    def them(self, ten_dm):
        try:
            danh_muc = DanhMuc(ten_dm=ten_dm)
            self.danh_muc_dao.tao(danh_muc)
        except Exception as e:
            print(e)

    def sua(self, ma_dm, ten_dm):
        try:
            danh_muc = self.danh_muc_dao.lay_bang_id(int(ma_dm))
            if danh_muc:
                danh_muc.ten_dm = ten_dm or danh_muc.ten_dm
                self.danh_muc_dao.sua(danh_muc)
        except Exception as e:
            print(e)

    def xoa(self, ma_dm):
        try:
            self.danh_muc_dao.xoa(int(ma_dm))
        except Exception as e:
            print(e)
