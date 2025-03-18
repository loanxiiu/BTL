class ChiTietDonHang:
    def __init__(self, ma_dh, so_luong, don_gia, ma_sp, ma_ctdh=None):
        self.ma_ctdh = ma_ctdh
        self.ma_dh = ma_dh
        self.so_luong = so_luong
        self.don_gia = don_gia
        self.ma_sp = ma_sp