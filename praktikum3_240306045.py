"""
Praktikum 3 - Fungsi Keanggotaan dan Fuzzifikasi (Python + MySQL)
Tanpa library fuzzy (scikit-fuzzy dsb). Database hanya menyimpan interval dan NAMA fungsi.

Alur:
Nilai Crisp -> Database -> Interval -> Nama Fungsi -> Fungsi Python -> mu(x)

Persiapan:
  1. pip install mysql-connector-python
  2. Jalankan database.sql di MySQL
  3. Ganti PASSWORD_MYSQL_ANDA di bawah
"""
import mysql.connector

# ==========================================================
# 1. KONEKSI DATABASE
# ==========================================================
KONFIGURASI = {
    "host": "localhost",
    "user": "root",
    "password": "PASSWORD_MYSQL_ANDA",   # isi "" jika MySQL tanpa password
    "database": "fuzzy_modul1",
}

db = mysql.connector.connect(**KONFIGURASI)
print("Koneksi database berhasil!")


# ==========================================================
# 2. FUNGSI KEANGGOTAAN (hasil perhitungan manual)
# ==========================================================
def fungsi_anak_turun(x):
    """Anak, 6 <= x <= 12 : mu(x) = (12 - x) / 6"""
    return (12 - x) / 6


def fungsi_remaja_naik(x):
    """Remaja, 10 <= x <= 15 : mu(x) = (x - 10) / 5"""
    return (x - 10) / 5


def fungsi_remaja_turun(x):
    """Remaja, 15 <= x <= 20 : mu(x) = (20 - x) / 5"""
    return (20 - x) / 5


def fungsi_dewasa_naik(x):
    """Dewasa, 18 <= x <= 25 : mu(x) = (x - 18) / 7"""
    return (x - 18) / 7


# ==========================================================
# 3. DAFTAR FUNGSI (nama di database -> fungsi Python)
# ==========================================================
fungsi = {
    "fungsi_anak_turun": fungsi_anak_turun,
    "fungsi_remaja_naik": fungsi_remaja_naik,
    "fungsi_remaja_turun": fungsi_remaja_turun,
    "fungsi_dewasa_naik": fungsi_dewasa_naik,
}

# Nama tabel yang diizinkan (mencegah nama tabel sembarang pada query)
TABEL_USIA = {"Anak": "usia_anak", "Remaja": "usia_remaja", "Dewasa": "usia_dewasa"}


# ==========================================================
# 4. FUNGSI FUZZIFIKASI
# ==========================================================
def cari_interval(x, variabel):
    """Mengambil (usia_min, usia_max, nilai_fuzzy) dari database untuk nilai crisp x."""
    tabel = TABEL_USIA[variabel]
    cursor = db.cursor()
    query = f"""
        SELECT usia_min, usia_max, nilai_fuzzy
        FROM {tabel}
        WHERE %s >= usia_min
        AND %s <= usia_max
        ORDER BY usia_min
    """
    cursor.execute(query, (x, x))
    data = cursor.fetchone()
    cursor.close()
    return data


def fuzzifikasi_usia(x, variabel="Remaja"):
    """Mengembalikan mu(x) untuk variabel usia tertentu; None jika di luar semesta."""
    data = cari_interval(x, variabel)
    if data is None:
        return None

    usia_min, usia_max, nama_fungsi = data

    # Database memberikan konstanta ('0' atau '1')
    if nama_fungsi in ("0", "1"):
        return float(nama_fungsi)

    # Database memberikan nama fungsi
    if nama_fungsi in fungsi:
        return fungsi[nama_fungsi](x)

    raise ValueError(f"Fungsi '{nama_fungsi}' belum dibuat di Python.")


# ==========================================================
# 5. PENGUJIAN TUGAS (10 data, minimal 2 per variabel usia)
# ==========================================================
DATA_UJI = [
    ("Anak", 4), ("Anak", 9), ("Anak", 13),
    ("Remaja", 8), ("Remaja", 12), ("Remaja", 17),
    ("Dewasa", 10), ("Dewasa", 19), ("Dewasa", 22), ("Dewasa", 30),
]


def jalankan_pengujian():
    print()
    print("| No | Variabel | Input Usia | Interval Database | Fungsi              | mu(x)  |")
    print("|---:|----------|-----------:|-------------------|---------------------|-------:|")
    for no, (variabel, usia) in enumerate(DATA_UJI, 1):
        data = cari_interval(usia, variabel)
        interval = f"{data[0]} - {data[1]}"
        nama = data[2] if data[2] not in ("0", "1") else f"konstanta {data[2]}"
        nilai = fuzzifikasi_usia(usia, variabel)
        print(f"| {no:>2} | {variabel:<8} | {usia:>10} | {interval:<17} | {nama:<19} | {nilai:>6.4f} |")


# ==========================================================
# 6. PROGRAM UTAMA
# ==========================================================
if __name__ == "__main__":
    jalankan_pengujian()

    print()
    masukan = input("Masukkan usia untuk fuzzifikasi (Enter untuk lewati): ").strip()
    if masukan:
        usia = float(masukan)
        print("================================")
        print("HASIL FUZZIFIKASI")
        print("================================")
        print(f"Usia : {usia}")
        for v in TABEL_USIA:
            print(f"  mu {v:<7}: {fuzzifikasi_usia(usia, v)}")
        print("================================")

    db.close()
