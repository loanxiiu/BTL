from model.dao.connect.DatabaseConnect import cur, conn
from model.SanPham import SanPham

class SanPhamDAO:
    def __init__(self):
        pass

    def lay_tat_ca(self):
        cur.execute("SELECT * FROM SanPham")
        san_pham = cur.fetchall()
        return san_pham

    def lay_bang_id(self, ma_sp):
        cur.execute("SELECT * FROM SanPham WHERE MaSPham = ?", (ma_sp,))
        row = cur.fetchone()
        return row if row else None

    def lay_bang_ten(self, ten_sp):
        cur.execute("SELECT * FROM SanPham WHERE TenSPham LIKE ?", ('%' + ten_sp + '%',))
        san_pham = cur.fetchall()
        return san_pham

    def dem(self):
        cur.execute("SELECT COUNT(*) FROM SanPham")
        return cur.fetchone()[0]

    def tao(self, san_pham: SanPham):
        cur.execute("INSERT INTO SanPham (TenSPham, SoLuong, DonGia, MoTa, MaDM, Anh) VALUES (?, ?, ?, ?, ?,?)",
                    (san_pham.ten_sp, san_pham.so_luong, san_pham.don_gia, san_pham.mo_ta, san_pham.ma_dm, san_pham.anh))
        conn.commit()

    def sua(self, san_pham: SanPham):
        cur.execute("UPDATE SanPham SET TenSPham=?, SoLuong=?, DonGia=?, MoTa=?, MaDM=?, Anh=? WHERE MaSPham=?",
                    (san_pham.ten_sp, san_pham.so_luong, san_pham.don_gia, san_pham.mo_ta, san_pham.ma_dm, san_pham.anh, san_pham.ma_sp))
        conn.commit()

    def xoa(self, ma_sp):
        cur.execute("DELETE FROM SanPham WHERE MaSPham = ?", (ma_sp,))
        conn.commit()

    def test(self):
        cur.execute("""SELECT SanPham.TenSPham, SUM(ChiTietDonHang.SoLuong) AS TongBan, strftime('%Y-%m', DonHang.NgayBan) AS Thang
FROM ChiTietDonHang
JOIN SanPham ON ChiTietDonHang.MaSP = SanPham.MaSPham
JOIN DonHang ON ChiTietDonHang.MaDH = DonHang.MaDH
GROUP BY SanPham.TenSPham, Thang
ORDER BY Thang DESC""")
        return cur.fetchall()