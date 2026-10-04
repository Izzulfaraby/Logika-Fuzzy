# ==========================================================
# 1. FUNGSI KEANGGOTAAN SEGITIGA (UMUM)
# ==========================================================
# Rumus segitiga dengan titik (a, b, c):
#   0                   , x <= a atau x >= c
#   (x - a) / (b - a)   , a <= x <= b
#   (c - x) / (c - b)   , b <= x <= c

def segitiga(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:  # b < x < c
        return (c - x) / (c - b)


# ==========================================================
# 2. FUNGSI KEANGGOTAAN TIAP KATEGORI
# ==========================================================

# --- Kategori Bayi (0, 3, 5) ---
def fungsi_bayi(x):
    return segitiga(x, 0, 3, 5)

# --- Kategori Anak (6, 9, 11) ---
def fungsi_anak(x):
    return segitiga(x, 6, 9, 11)

# --- Kategori Remaja (10, 15, 19) ---
def fungsi_remaja(x):
    return segitiga(x, 10, 15, 19)

# --- Kategori Pemuda (15, 20, 24) ---
def fungsi_pemuda(x):
    return segitiga(x, 15, 20, 24)

# --- Kategori Dewasa (20, 43, 65) ---
def fungsi_dewasa(x):
    return segitiga(x, 20, 43, 65)

# --- Kategori Lansia (65, 80, 100) ---
def fungsi_lansia(x):
    return segitiga(x, 65, 80, 100)


# ==========================================================
# 3. INPUT USIA
# ==========================================================

usia = float(input("Masukkan usia: "))


# ==========================================================
# 4. PROSES FUZZIFIKASI
# ==========================================================

nilai_bayi   = round(fungsi_bayi(usia), 4)
nilai_anak   = round(fungsi_anak(usia), 4)
nilai_remaja = round(fungsi_remaja(usia), 4)
nilai_pemuda = round(fungsi_pemuda(usia), 4)
nilai_dewasa = round(fungsi_dewasa(usia), 4)
nilai_lansia = round(fungsi_lansia(usia), 4)


# ==========================================================
# 5. MENAMPILKAN HASIL
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