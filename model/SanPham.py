class SanPham:
    def __init__(self, ten_sp, so_luong, don_gia, mo_ta, ma_dm, anh, ma_sp=None):
        self.ma_sp = ma_sp
        self.anh = anh
        self.ten_sp = ten_sp
        self.so_luong = so_luong
        self.don_gia = don_gia
        self.mo_ta = mo_ta
        self.ma_dm = ma_dm