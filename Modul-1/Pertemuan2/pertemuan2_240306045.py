import mysql.connector

# ==========================================================
# 1. KONEKSI DATABASE
# ==========================================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", # Isi dengan password MySQL Anda (jika ada)
    database="db_fuzzy_usia"
)

print("Koneksi database berhasil!")


# ==========================================================
# 2. FUNGSI KEANGGOTAAN
# ==========================================================

# --- Kategori Bayi ---
def fungsi_bayi_turun(x):
    return (5 - x) / 3

# --- Kategori Anak ---
def fungsi_anak_naik(x):
    return (x - 6) / 2

def fungsi_anak_turun(x):
    return (11 - x) / 2

# --- Kategori Remaja ---
def fungsi_remaja_naik(x):
    return (x - 10) / 2

def fungsi_remaja_turun(x):
    return (19 - x) / 2

# --- Kategori Pemuda ---
def fungsi_pemuda_naik(x):
    return (x - 15) / 2

def fungsi_pemuda_turun(x):
    return (24 - x) / 2

# --- Kategori Dewasa ---
def fungsi_dewasa_naik(x):
    return (x - 20) / 2

def fungsi_dewasa_turun(x):
    return (65 - x) / 2

# --- Kategori Lansia ---
def fungsi_lansia_naik(x):
    return (x - 65) / 5

def fungsi_lansia_turun(x):
    return (100 - x) / 5


# ==========================================================
# 3. DAFTAR FUNGSI
# ==========================================================
# Karena fungsi di DB menggunakan nama umum (trapezium_up / down),
# kita kelompokkan berdasarkan nama tabel.

fungsi = {
    "tb_domain_usia_bayi": {
        "trapezium_down": fungsi_bayi_turun
    },
    "tb_domain_usia_anak": {
        "trapezium_up": fungsi_anak_naik,
        "trapezium_down": fungsi_anak_turun
    },
    "tb_domain_usia_remaja": {
        "trapezium_up": fungsi_remaja_naik,
        "trapezium_down": fungsi_remaja_turun
    },
    "tb_domain_usia_pemuda": {
        "trapezium_up": fungsi_pemuda_naik,
        "trapezium_down": fungsi_pemuda_turun
    },
    "tb_domain_usia_dewasa": {
        "trapezium_up": fungsi_dewasa_naik,
        "trapezium_down": fungsi_dewasa_turun
    },
    "tb_domain_usia_lansia": {
        "trapezium_up": fungsi_lansia_naik,
        "trapezium_down": fungsi_lansia_turun
    }
}


# ==========================================================
# 4. FUNGSI FUZZIFIKASI
# ==========================================================

def fuzzifikasi_usia(x, nama_tabel):

    cursor = db.cursor()

    # PERBAIKAN: Menambahkan LIMIT 1 di akhir query
    query = f"""
        SELECT b_bawah, b_atas, fungsi
        FROM {nama_tabel}
        WHERE %s >= b_bawah
        AND %s <= b_atas
        LIMIT 1 
    """

    cursor.execute(query, (x, x))
    data = cursor.fetchone()
    cursor.close()

    if data is None:
        return 0.0

    b_bawah, b_atas, nama_fungsi = data

    # Jika database memberikan nilai 0
    if nama_fungsi == "0":
        return 0.0
        
    # Jika database memberikan nilai 1
    if nama_fungsi == "1":
        return 1.0

    # Jika database memberikan nama fungsi
    if nama_fungsi in fungsi[nama_tabel]:
        fungsi_y = fungsi[nama_tabel][nama_fungsi]
        nilai = fungsi_y(x)
        return round(nilai, 4)

    raise ValueError(
        f"Fungsi '{nama_fungsi}' pada {nama_tabel} belum dibuat di Python."
    )


# ==========================================================
# 5. INPUT USIA
# ==========================================================

usia = float(input("Masukkan usia: "))


# ==========================================================
# 6. PROSES FUZZIFIKASI
# ==========================================================

nilai_bayi   = fuzzifikasi_usia(usia, "tb_domain_usia_bayi")
nilai_anak   = fuzzifikasi_usia(usia, "tb_domain_usia_anak")
nilai_remaja = fuzzifikasi_usia(usia, "tb_domain_usia_remaja")
nilai_pemuda = fuzzifikasi_usia(usia, "tb_domain_usia_pemuda")
nilai_dewasa = fuzzifikasi_usia(usia, "tb_domain_usia_dewasa")
nilai_lansia = fuzzifikasi_usia(usia, "tb_domain_usia_lansia")


# ==========================================================
# 7. MENAMPILKAN HASIL
# ==========================================================

print()
print("================================")
print("HASIL FUZZIFIKASI")
print("================================")
print(f"Usia               : {usia}")
print(f"Keanggotaan Bayi   : {nilai_bayi}")
print(f"Keanggotaan Anak   : {nilai_anak}")
print(f"Keanggotaan Remaja : {nilai_remaja}")
print(f"Keanggotaan Pemuda : {nilai_pemuda}")
print(f"Keanggotaan Dewasa : {nilai_dewasa}")
print(f"Keanggotaan Lansia : {nilai_lansia}")
print("================================")


# ==========================================================
# 8. MENUTUP DATABASE
# ==========================================================

db.close()