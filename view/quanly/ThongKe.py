import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from controller.ThongKeController import ThongKeController

class ThongKe:
    def __init__(self, root):
        self.root = root
        self.root.title("FieldCheck - Dashboard")
        self.root.geometry("1920x1080")
        self.controller = ThongKeController()

        # Filtres et plages de dates
        self.time_frame = tk.StringVar(value="Tháng")
        self.start_date = datetime.now() - timedelta(days=30)
        self.end_date = datetime.now()

        self.create_main_content()

    def create_main_content(self):
        main_container = tk.Frame(self.root, bg="white")
        main_container.pack(fill="both", expand=True, padx=20)

        filter_frame = tk.Frame(main_container, bg="white")
        filter_frame.pack(fill="x", pady=(0, 10))

        self.create_filters(filter_frame)

        notebook = ttk.Notebook(main_container)
        notebook.pack(fill="both", expand=True)

        tab_doanhthu = tk.Frame(notebook, bg="white")
        tab_sanpham = tk.Frame(notebook, bg="white")
        tab_donhang = tk.Frame(notebook, bg="white")
        notebook.add(tab_doanhthu, text="Doanh thu")
        notebook.add(tab_sanpham, text="Sản phẩm")
        notebook.add(tab_donhang, text="Đơn hàng")

        self.load_doanhthu_tab(tab_doanhthu)
        self.load_sanpham_tab(tab_sanpham)
        self.load_donhang_tab(tab_donhang)

    def create_filters(self, parent):
        tk.Label(parent, text="Khung thời gian:", bg="white").pack(side="left", padx=(0, 5))
        time_frame_menu = ttk.Combobox(parent, textvariable=self.time_frame, values=["Ngày", "Tuần", "Tháng", "Năm"], width=10)
        time_frame_menu.pack(side="left", padx=(0, 15))
        time_frame_menu.bind("<<ComboboxSelected>>", self.refresh_data)

        tk.Label(parent, text="Từ ngày:", bg="white").pack(side="left", padx=(0, 5))
        start_date_entry = tk.Entry(parent, width=12)
        start_date_entry.insert(0, self.start_date.strftime("%Y-%m-%d"))
        start_date_entry.pack(side="left", padx=(0, 10))

        tk.Label(parent, text="Đến ngày:", bg="white").pack(side="left", padx=(0, 5))
        end_date_entry = tk.Entry(parent, width=12)
        end_date_entry.insert(0, self.end_date.strftime("%Y-%m-%d"))
        end_date_entry.pack(side="left", padx=(0, 10))

        apply_btn = tk.Button(parent, text="Áp dụng", bg="#4CAF50", fg="white",
                              command=lambda: self.update_date_range(start_date_entry.get(), end_date_entry.get()))
        apply_btn.pack(side="left", padx=(10, 0))

        export_btn = tk.Button(parent, text="Xuất báo cáo", bg="#2196F3", fg="white", command=self.export_report)
        export_btn.pack(side="left", padx=10)

        home_btn = tk.Button(parent, text="Trở lại trang chủ", bg="red", fg="white", command=self.home_view)
        home_btn.pack(side="right", padx=(10, 0))

    def home_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from view.chung.TrangChu import TrangChu
        TrangChu(self.root)

    def update_date_range(self, start_date_str, end_date_str):
        try:
            self.start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            self.end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            self.refresh_data()
        except ValueError:
            messagebox.showerror("Lỗi định dạng", "Vui lòng nhập ngày theo định dạng YYYY-MM-DD")

    def refresh_data(self, event=None):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_main_content()

    def export_report(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Lưu báo cáo thống kê",
            initialfile=f"ThongKe_{self.start_date.strftime('%Y%m%d')}_{self.end_date.strftime('%Y%m%d')}"
        )
        if file_path:
            success, message = self.controller.export_report(
                self.start_date.strftime("%Y-%m-%d"),
                self.end_date.strftime("%Y-%m-%d"),
                self.time_frame.get(),
                file_path
            )
            if success:
                messagebox.showinfo("Thành công", message)
            else:
                messagebox.showerror("Lỗi xuất báo cáo", message)

    def load_doanhthu_tab(self, parent):
        df = self.controller.get_doanhthu_data(
            self.start_date.strftime("%Y-%m-%d"),
            self.end_date.strftime("%Y-%m-%d"),
            self.time_frame.get()
        )
        total_revenue = self.controller.get_doanhthu_summary(
            self.start_date.strftime("%Y-%m-%d"),
            self.end_date.strftime("%Y-%m-%d")
        )

        summary_frame = tk.Frame(parent, bg="white")
        summary_frame.pack(fill="x", pady=10)
        chart_frame = tk.Frame(parent, bg="white")
        chart_frame.pack(fill="both", expand=True)

        tk.Label(summary_frame, text="Tổng doanh thu:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(summary_frame, text=f"{total_revenue:,.0f} VNĐ", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=1, padx=10, pady=5, sticky="w")

        if not df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(df['ThoiGian'], df['DoanhThu'], color="blue")
            ax.set_title(f"Doanh thu theo {self.time_frame.get().lower()}")
            ax.set_xlabel(f"{self.time_frame.get()}")
            ax.set_ylabel("Doanh thu (VNĐ)")
            plt.xticks(rotation=45)
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()
        else:
            tk.Label(chart_frame, text="Không có dữ liệu", font=("Arial", 12), bg="white").pack(pady=50)

    def load_sanpham_tab(self, parent):
        sanpham_data = self.controller.get_sanpham_data(
            self.start_date.strftime("%Y-%m-%d"),
            self.end_date.strftime("%Y-%m-%d")
        )
        df = sanpham_data['data']
        total_sold = sanpham_data['total_sold']
        total_inventory = sanpham_data['total_inventory']

        summary_frame = tk.Frame(parent, bg="white")
        summary_frame.pack(fill="x", pady=10)
        chart_frame = tk.Frame(parent, bg="white")
        chart_frame.pack(fill="both", expand=True)

        tk.Label(summary_frame, text="Số lượng bán ra:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(summary_frame, text=f"{total_sold:,.0f}", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        tk.Label(summary_frame, text="Tổng tồn kho:", font=("Arial", 12), bg="white").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        tk.Label(summary_frame, text=f"{total_inventory:,.0f}", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=3, padx=10, pady=5, sticky="w")

        if not df.empty:
            top_df = df[df['SoLuongBan'] > 0].head(10)
            if not top_df.empty:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(top_df['TenSPham'], top_df['SoLuongBan'], color="green")
                ax.set_title("Top 10 sản phẩm bán chạy")
                ax.set_xlabel("Sản phẩm")
                ax.set_ylabel("Số lượng bán")
                plt.xticks(rotation=45, ha='right')
                canvas = FigureCanvasTkAgg(fig, master=chart_frame)
                canvas.get_tk_widget().pack(fill="both", expand=True)
                canvas.draw()
            else:
                tk.Label(chart_frame, text="Không có sản phẩm nào được bán trong khoảng thời gian này",
                         font=("Arial", 12), bg="white").pack(pady=50)
        else:
            tk.Label(chart_frame, text="Không có dữ liệu", font=("Arial", 12), bg="white").pack(pady=50)

    def load_donhang_tab(self, parent):
        df = self.controller.get_donhang_data(
            self.start_date.strftime("%Y-%m-%d"),
            self.end_date.strftime("%Y-%m-%d"),
            self.time_frame.get()
        )
        summary = self.controller.get_donhang_summary(
            self.start_date.strftime("%Y-%m-%d"),
            self.end_date.strftime("%Y-%m-%d")
        )

        summary_frame = tk.Frame(parent, bg="white")
        summary_frame.pack(fill="x", pady=10)
        chart_frame = tk.Frame(parent, bg="white")
        chart_frame.pack(fill="both", expand=True)

        tk.Label(summary_frame, text="Số lượng đơn hàng:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(summary_frame, text=f"{summary['SoLuongDon']:,.0f}", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        tk.Label(summary_frame, text="Giá trị trung bình:", font=("Arial", 12), bg="white").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        tk.Label(summary_frame, text=f"{summary['GiaTriTrungBinh']:,.0f} VNĐ", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=3, padx=10, pady=5, sticky="w")
        tk.Label(summary_frame, text="Tổng giá trị:", font=("Arial", 12), bg="white").grid(row=0, column=4, padx=10, pady=5, sticky="w")
        tk.Label(summary_frame, text=f"{summary['TongGiaTri']:,.0f} VNĐ", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=5, padx=10, pady=5, sticky="w")

        if not df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(df['ThoiGian'], df['SoDon'], color="purple")
            ax.set_title(f"Số lượng đơn hàng theo {self.time_frame.get().lower()}")
            ax.set_xlabel(f"{self.time_frame.get()}")
            ax.set_ylabel("Số đơn hàng")
            plt.xticks(rotation=45)
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()
        else:
            tk.Label(chart_frame, text="Không có dữ liệu", font=("Arial", 12), bg="white").pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = ThongKe(root)
    root.mainloop()