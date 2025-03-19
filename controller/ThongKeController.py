from model.dao.ThongKeDAO import ThongKeDAO
import pandas as pd

class ThongKeController:
    def __init__(self):
        self.dao = ThongKeDAO()

    def get_time_format(self, time_frame):
        time_format_map = {
            "Ngày": "%Y-%m-%d",
            "Tuần": "%Y-%W",
            "Tháng": "%Y-%m",
            "Năm": "%Y"
        }
        return time_format_map.get(time_frame, "%Y-%m")

    def get_doanhthu_data(self, start_date, end_date, time_frame):
        time_format = self.get_time_format(time_frame)
        return self.dao.get_doanhthu_data(start_date, end_date, time_format)

    def get_sanpham_data(self, start_date, end_date):
        df = self.dao.get_sanpham_data(start_date, end_date)
        if not df.empty:
            return {
                'data': df,
                'total_sold': df['SoLuongBan'].sum(),
                'total_inventory': df['TonKho'].sum()
            }
        return {'data': df, 'total_sold': 0, 'total_inventory': 0}

    def get_donhang_data(self, start_date, end_date, time_frame):
        time_format = self.get_time_format(time_frame)
        return self.dao.get_donhang_data(start_date, end_date, time_format)

    def get_doanhthu_summary(self, start_date, end_date):
        return self.dao.get_doanhthu_summary(start_date, end_date)

    def get_donhang_summary(self, start_date, end_date):
        return self.dao.get_donhang_summary(start_date, end_date)

    def export_report(self, start_date, end_date, time_frame, file_path):
        try:
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                # Récupérer les données
                doanhthu_df = self.get_doanhthu_data(start_date, end_date, time_frame)
                sanpham_data = self.get_sanpham_data(start_date, end_date)
                sanpham_df = sanpham_data['data']
                donhang_df = self.get_donhang_data(start_date, end_date, time_frame)

                # Résumés
                doanhthu_summary = pd.DataFrame({'Tổng doanh thu (VNĐ)': [doanhthu_df['DoanhThu'].sum() if not doanhthu_df.empty else 0]})
                sanpham_summary = pd.DataFrame({
                    'Tổng số lượng bán ra': [sanpham_df['SoLuongBan'].sum() if not sanpham_df.empty else 0],
                    'Tổng tồn kho': [sanpham_df['TonKho'].sum() if not sanpham_df.empty else 0]
                })
                donhang_summary = pd.DataFrame({
                    'Tổng số đơn hàng': [donhang_df['SoDon'].sum() if not donhang_df.empty else 0],
                    'Giá trị trung bình (VNĐ)': [donhang_df['GiaTriTrungBinh'].mean() if not donhang_df.empty else 0],
                    'Tổng giá trị (VNĐ)': [donhang_df['SoDon'].sum() * donhang_df['GiaTriTrungBinh'].mean() if not donhang_df.empty else 0]
                })

                # Écrire dans les feuilles Excel
                doanhthu_summary.to_excel(writer, sheet_name='DoanhThu', startrow=0, index=False)
                doanhthu_df.to_excel(writer, sheet_name='DoanhThu', startrow=len(doanhthu_summary) + 2, index=False)
                sanpham_summary.to_excel(writer, sheet_name='SanPham', startrow=0, index=False)
                sanpham_df.to_excel(writer, sheet_name='SanPham', startrow=len(sanpham_summary) + 2, index=False)
                donhang_summary.to_excel(writer, sheet_name='DonHang', startrow=0, index=False)
                donhang_df.to_excel(writer, sheet_name='DonHang', startrow=len(donhang_summary) + 2, index=False)
            return True, f"Đã xuất báo cáo thành công đến {file_path}"
        except Exception as e:
            return False, f"Có lỗi xảy ra: {str(e)}"