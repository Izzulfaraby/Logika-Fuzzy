"""
Asesmen Modul 1 - Pemodelan Fuzzy (Tahap 1)
Sistem Deteksi Dini Beban Server (Server Overload Warning System)

Cakupan : variabel input/output, fungsi keanggotaan, fuzzifikasi, visualisasi, pengujian.
Di luar cakupan (Modul 2): rule base, inferensi, agregasi, defuzzifikasi.
Library : hanya NumPy dan Matplotlib (tanpa library fuzzy).
"""
import os
import numpy as np
import matplotlib.pyplot as plt

# Gambar disimpan di folder yang SAMA dengan file .py ini, apa pun folder tempat program dijalankan.
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:          # jika dijalankan di Jupyter/Colab (tidak ada __file__)
    BASE_DIR = os.getcwd()
OUTPUT_DIR = BASE_DIR


# ==========================================================
# 1. FUNGSI KEANGGOTAAN DASAR
# ==========================================================
def trapmf(x, a, b, c, d):
    """
    Trapesium Trap(a,b,c,d). Mendukung bahu: a == b (bahu kiri) dan c == d (bahu kanan).
    Kondisi plateau (b <= x <= c) diperiksa lebih dulu agar bahu bernilai 1 tepat di batas
    semesta (mis. x = 0 pada [0,0,20,40]).
    """
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        naik = (x - a) / (b - a)
        turun = (d - x) / (d - c)
    hasil = np.select(
        [(x >= b) & (x <= c), (x > a) & (x < b), (x > c) & (x < d)],
        [1.0, naik, turun],
        default=0.0,
    )
    return hasil


def trimf(x, a, b, c):
    """Segitiga Tri(a,b,c) dengan puncak di b (mu(b) = 1)."""
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        naik = (x - a) / (b - a)
        turun = (c - x) / (c - b)
    return np.select([x == b, (x > a) & (x < b), (x > b) & (x < c)],
                     [1.0, naik, turun], default=0.0)


# ==========================================================
# 2. FUNGSI KEANGGOTAAN PER LABEL
# ==========================================================
def cpu_rendah(x):   return trapmf(x, 0, 0, 20, 40)
def cpu_normal(x):   return trimf(x, 30, 50, 70)
def cpu_tinggi(x):   return trapmf(x, 60, 80, 100, 100)

def memory_rendah(x): return trapmf(x, 0, 0, 20, 40)
def memory_normal(x): return trimf(x, 30, 50, 70)
def memory_tinggi(x): return trapmf(x, 60, 80, 100, 100)

def warning_aman(x):    return trapmf(x, 0, 0, 25, 45)
def warning_waspada(x): return trimf(x, 30, 50, 70)
def warning_kritis(x):  return trapmf(x, 55, 75, 100, 100)


# ==========================================================
# 3. MODEL VARIABEL LINGUISTIK
# ==========================================================
VARIABEL = {
    "cpu": {
        "nama": "CPU Usage", "satuan": "%", "semesta": (0, 100),
        "label": {"rendah": cpu_rendah, "normal": cpu_normal, "tinggi": cpu_tinggi},
        "warna": {"rendah": "#2ca02c", "normal": "#ff7f0e", "tinggi": "#d62728"},
        "file": "cpu_usage.png",
    },
    "memory": {
        "nama": "Memory Usage", "satuan": "%", "semesta": (0, 100),
        "label": {"rendah": memory_rendah, "normal": memory_normal, "tinggi": memory_tinggi},
        "warna": {"rendah": "#2ca02c", "normal": "#ff7f0e", "tinggi": "#d62728"},
        "file": "memory_usage.png",
    },
    "warning": {
        "nama": "Server Overload Warning", "satuan": "Skor Peringatan", "semesta": (0, 100),
        "label": {"aman": warning_aman, "waspada": warning_waspada, "kritis": warning_kritis},
        "warna": {"aman": "#2ca02c", "waspada": "#ff7f0e", "kritis": "#d62728"},
        "file": "server_overload_warning.png",
    },
}
VARIABEL_INPUT = ("cpu", "memory")


# ==========================================================
# 4. FUZZIFIKASI
# ==========================================================
def fuzzifikasi_variabel(nama_var, nilai):
    """Derajat keanggotaan satu nilai crisp pada seluruh label sebuah variabel."""
    var = VARIABEL[nama_var]
    lo, hi = var["semesta"]
    if not (lo <= nilai <= hi):
        raise ValueError(f"{var['nama']}={nilai} di luar semesta [{lo}, {hi}]")
    return {lbl: round(float(f(nilai)), 4) for lbl, f in var["label"].items()}


def fuzzifikasi(input_dict):
    """
    input_dict : {"cpu": 65, "memory": 70}
    return     : {"cpu": {"rendah":..,"normal":..,"tinggi":..}, "memory": {...}}
    """
    return {k: fuzzifikasi_variabel(k, v) for k, v in input_dict.items()}


def label_dominan(derajat, eps=1e-9):
    maks = max(derajat.values())
    kandidat = [k for k, v in derajat.items() if abs(v - maks) < eps]
    return "/".join(kandidat), maks


def interpretasi(hasil):
    """Ringkasan teks otomatis berdasarkan angka hasil fuzzifikasi."""
    bagian = []
    for k in VARIABEL_INPUT:
        dom, nilai = label_dominan(hasil[k])
        aktif = [l for l, v in hasil[k].items() if v > 0]
        status = "transisi" if len(aktif) > 1 else "tunggal"
        bagian.append(f"{k.upper()}: {dom} ({nilai:.2f}), {status}")
    return "; ".join(bagian)


# ==========================================================
# 5. VISUALISASI
# ==========================================================
def plot_variabel(nama_var, folder=OUTPUT_DIR, tampilkan=True):
    """Membuat grafik, menyimpannya ke PNG, lalu menampilkannya di layar (tampilkan=True)."""
    var = VARIABEL[nama_var]
    os.makedirs(folder, exist_ok=True)
    x = np.linspace(*var["semesta"], 1001)
    plt.figure(figsize=(10, 5.2))
    for lbl, f in var["label"].items():
        plt.plot(x, f(x), label=lbl.capitalize(), color=var["warna"][lbl], linewidth=2.6)
    plt.title(f"Fungsi Keanggotaan: {var['nama']}", fontsize=13, fontweight="bold")
    plt.xlabel(f"{var['nama']} ({var['satuan']})")
    plt.ylabel("Derajat Keanggotaan μ(x)")
    plt.ylim(-0.05, 1.1)
    plt.xlim(*var["semesta"])
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="center right")
    plt.tight_layout()
    path = os.path.join(folder, var["file"])
    plt.savefig(path, dpi=300)          # simpan SEBELUM show() agar file tidak kosong
    if tampilkan:
        plt.show()
    plt.close()
    return path


# ==========================================================
# 6. DATA UJI (DATA SIMULASI UNTUK PENGUJIAN MODEL - bukan data monitoring nyata)
# ==========================================================
DATA_UJI = [
    ("Ekstrem bawah (idle)",      {"cpu": 5,   "memory": 10}),
    ("Server normal",             {"cpu": 20,  "memory": 30}),
    ("Beban mulai meningkat",     {"cpu": 55,  "memory": 60}),
    ("Transisi",                  {"cpu": 65,  "memory": 68}),
    ("Waspada",                   {"cpu": 70,  "memory": 75}),
    ("Titik batas parameter",     {"cpu": 60,  "memory": 40}),
    ("Beban sangat tinggi",       {"cpu": 90,  "memory": 92}),
    ("Ekstrem atas (saturasi)",   {"cpu": 100, "memory": 100}),
]


def tabel_pengujian():
    baris = []
    baris.append("| No | Kasus | CPU | Mem | CPU Rendah | CPU Normal | CPU Tinggi | "
                 "Mem Rendah | Mem Normal | Mem Tinggi | Interpretasi |")
    baris.append("|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for i, (kasus, data) in enumerate(DATA_UJI, 1):
        h = fuzzifikasi(data)
        c, m = h["cpu"], h["memory"]
        baris.append(f"| {i} | {kasus} | {data['cpu']} | {data['memory']} | "
                     f"{c['rendah']:.2f} | {c['normal']:.2f} | {c['tinggi']:.2f} | "
                     f"{m['rendah']:.2f} | {m['normal']:.2f} | {m['tinggi']:.2f} | {interpretasi(h)} |")
    return "\n".join(baris)


# ==========================================================
# 7. VALIDASI MODEL
# ==========================================================
def validasi_model():
    """Memeriksa rentang [0,1], tidak ada gap, dan overlap antar label bersebelahan."""
    print("VALIDASI MODEL")
    for nama, var in VARIABEL.items():
        x = np.linspace(*var["semesta"], 10001)
        mus = [f(x) for f in var["label"].values()]
        semua = np.array(mus)
        assert semua.min() >= 0.0 and semua.max() <= 1.0, "mu di luar [0,1]"
        cakupan = semua.max(axis=0).min()
        assert cakupan > 0.0, "ada gap"
        overlap = []
        for i in range(len(mus) - 1):
            mask = (mus[i] > 0) & (mus[i + 1] > 0)
            assert mask.any(), "label bersebelahan tidak overlap"
            overlap.append(f"[{x[mask].min():.1f}, {x[mask].max():.1f}]")
        print(f"  {var['nama']:<24}: mu dalam [0,1]; cakupan minimum max-mu = {cakupan:.4f} (>0, tanpa gap); "
              f"overlap = {', '.join(overlap)}")


def verifikasi_manual():
    """Membandingkan hitungan manual (laporan) dengan hasil program."""
    manual = [
        ("cpu", 65, {"rendah": 0.0, "normal": 0.25, "tinggi": 0.25}),
        ("cpu", 55, {"rendah": 0.0, "normal": 0.75, "tinggi": 0.0}),
        ("cpu", 35, {"rendah": 0.25, "normal": 0.25, "tinggi": 0.0}),
        ("memory", 68, {"rendah": 0.0, "normal": 0.1, "tinggi": 0.4}),
        ("memory", 75, {"rendah": 0.0, "normal": 0.0, "tinggi": 0.75}),
        ("warning", 40, {"aman": 0.25, "waspada": 0.5, "kritis": 0.0}),
        ("warning", 60, {"aman": 0.0, "waspada": 0.5, "kritis": 0.25}),
    ]
    for var, nilai, harapan in manual:
        hasil = fuzzifikasi_variabel(var, nilai)
        for lbl, v in harapan.items():
            assert abs(hasil[lbl] - v) < 1e-9, f"{var}({nilai}).{lbl}: program {hasil[lbl]} != manual {v}"
    print(f"  Verifikasi hitungan manual vs program: {len(manual)} titik cocok.")


# ==========================================================
# 8. PROGRAM UTAMA
# ==========================================================
if __name__ == "__main__":
    for nama in VARIABEL:
        path_gambar = plot_variabel(nama, tampilkan=True)
        print("Grafik tersimpan:", path_gambar, "| ada:", os.path.exists(path_gambar))

    print()
    validasi_model()
    verifikasi_manual()

    print("\nTABEL HASIL FUZZIFIKASI (data simulasi untuk pengujian model)")
    print(tabel_pengujian())

    print("\nDEMO FUNGSI OUTPUT (evaluasi fungsi keanggotaan skor; BUKAN hasil inferensi)")
    print("| Skor | Aman | Waspada | Kritis |")
    print("|---:|---:|---:|---:|")
    for s in (10, 40, 50, 60, 90):
        w = fuzzifikasi_variabel("warning", s)
        print(f"| {s} | {w['aman']:.2f} | {w['waspada']:.2f} | {w['kritis']:.2f} |")