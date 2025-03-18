import sqlite3

with sqlite3.connect(r'E:\Users\ploan\python_EAUT\BTL\model\dao\connect\ITSHOP.db') as conn:
    cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Ten VARCHAR NOT NULL,
    DiaChi VARCHAR NOT NULL,
    SDT VARCHAR NOT NULL
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS Quyen(
    MaQuyen INTEGER PRIMARY KEY AUTOINCREMENT,
    TenQuyen VARCHAR NOT NULL
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS DanhMuc(
    MaDM INTEGER PRIMARY KEY AUTOINCREMENT,
    TenDM VARCHAR NOT NULL
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS NhaCungCap(
    MaNCC INTEGER PRIMARY KEY AUTOINCREMENT,
    TenNCC VARCHAR NOT NULL,
    DiaChi VARCHAR NOT NULL,
    SDT VARCHAR NOT NULL
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS TaiKhoan(
    MaTK INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    MaQuyen INTEGER,
    user_id INTEGER,
    FOREIGN KEY (MaQuyen) REFERENCES Quyen(MaQuyen),
    FOREIGN KEY (user_id) REFERENCES Users(id)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS SanPham(
    MaSPham INTEGER PRIMARY KEY AUTOINCREMENT,
    TenSPham VARCHAR NOT NULL,
    SoLuong INTEGER NOT NULL,
    DonGia FLOAT NOT NULL,
    MaDM INTEGER,
    Anh VARCHAR NOT NULL,
    MoTa VARCHAR ,
    FOREIGN KEY (MaDM) REFERENCES DanhMuc(MaDM)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS DonHang(
    MaDH INTEGER PRIMARY KEY AUTOINCREMENT,
    DonGia FLOAT NOT NULL,
    NgayBan DATE NOT NULL,
    MaNV INTEGER,
    MaKH INTEGER,
    FOREIGN KEY (MaNV) REFERENCES Users(id),
    FOREIGN KEY (MaKH) REFERENCES Users(id)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS ChiTietDonHang(
    MaCTDH INTEGER PRIMARY KEY AUTOINCREMENT,
    MaDH INTEGER,
    SoLuong INTEGER NOT NULL,
    DonGia FLOAT NOT NULL,
    MaSP INTEGER,
    FOREIGN KEY (MaDH) REFERENCES DonHang(MaDH),
    FOREIGN KEY (MaSP) REFERENCES SanPham(MaSPham)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS PhieuNhap(
    MaPN INTEGER PRIMARY KEY AUTOINCREMENT,
    NgayNhap VARCHAR NOT NULL,
    MaQL INTEGER,
    MaNCC INTEGER,
    FOREIGN KEY (MaQL) REFERENCES Users(id),
    FOREIGN KEY (MaNCC) REFERENCES NhaCungCap(MaNCC)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS ChiTietPhieuNhap(
    MaCTPN INTEGER PRIMARY KEY AUTOINCREMENT,
    MaSP INTEGER,
    SoLuong INTEGER NOT NULL,
    DonGia FLOAT NOT NULL,
    MaPN INTEGER,
    FOREIGN KEY (MaSP) REFERENCES SanPham(MaSPham),
    FOREIGN KEY (MaPN) REFERENCES PhieuNhap(MaPN)
)""")

cur.execute("""
            CREATE TABLE IF NOT EXISTS face_data (
                id TEXT PRIMARY KEY,
                MaTK TEXT UNIQUE NOT NULL,
                face_encoding BLOB NOT NULL,
                created_at TIMESTAMP NOT NULL,
                FOREIGN KEY (MaTK) REFERENCES TaiKhoan(MaTK)
)""")

print("Tables created successfully!")
