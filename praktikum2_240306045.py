"""
Praktikum 2 - Himpunan Fuzzy dan Variabel Linguistik
  Bagian A : Contoh modul (Waktu Respons Server) + verifikasi tabel skenario
  Bagian B : TUGAS - Penggunaan CPU Server (Rendah, Normal, Tinggi)
Library: hanya NumPy dan Matplotlib.
"""
import numpy as np
import matplotlib.pyplot as plt


# ==========================================================
# BAGIAN A - CONTOH MODUL: WAKTU RESPONS
# ==========================================================
def mf_cepat(x):
    x = np.asarray(x, dtype=float)
    return np.select([x <= 2.0, (x > 2.0) & (x < 4.0), x >= 4.0],
                     [1.0, (4.0 - x) / 2.0, 0.0])


def mf_sedang(x):
    x = np.asarray(x, dtype=float)
    return np.select([(x <= 3.0) | (x >= 7.0), (x > 3.0) & (x <= 5.0), (x > 5.0) & (x < 7.0)],
                     [0.0, (x - 3.0) / 2.0, (7.0 - x) / 2.0])


def mf_lambat(x):
    x = np.asarray(x, dtype=float)
    return np.select([x <= 6.0, (x > 6.0) & (x < 8.0), x >= 8.0],
                     [0.0, (x - 6.0) / 2.0, 1.0])


variabel_waktu_respons = {
    "nama": "Waktu Respons Server", "satuan": "detik", "semesta": (0.0, 10.0),
    "label": {"Cepat": mf_cepat, "Sedang": mf_sedang, "Lambat": mf_lambat},
}


def fuzzifikasi(nilai_crisp, variabel):
    u_min, u_max = variabel["semesta"]
    if not (u_min <= nilai_crisp <= u_max):
        raise ValueError(f"Input {nilai_crisp} di luar semesta [{u_min}, {u_max}]")
    return {n: round(float(f(np.array([nilai_crisp]))[0]), 4) for n, f in variabel["label"].items()}


def label_dominan(hasil, eps=1e-9):
    maks = max(hasil.values())
    kandidat = [k for k, v in hasil.items() if abs(v - maks) < eps]
    return kandidat[0] if len(kandidat) == 1 else "Imbang (" + "/".join(kandidat) + ")"


print("=" * 70)
print("BAGIAN A - SKENARIO PENGUJIAN MODUL: Waktu Respons Server")
print("=" * 70)
print("| No | x (s) | Cepat | Sedang | Lambat | Dominan |")
print("|---:|------:|------:|-------:|-------:|---------|")
for i, x in enumerate([1.0, 2.5, 3.5, 5.0, 6.5, 7.5, 9.0], 1):
    h = fuzzifikasi(x, variabel_waktu_respons)
    print(f"| {i} | {x:>5} | {h['Cepat']:.3f} | {h['Sedang']:.3f}  | {h['Lambat']:.3f}  | {label_dominan(h)} |")

xs = np.linspace(0, 10, 500)
plt.figure(figsize=(10, 5.5))
plt.plot(xs, mf_cepat(xs), label='Cepat', color='#2ca02c', linewidth=2.5)
plt.plot(xs, mf_sedang(xs), label='Sedang', color='#ff7f0e', linewidth=2.5)
plt.plot(xs, mf_lambat(xs), label='Lambat', color='#d62728', linewidth=2.5)
x_uji = 3.5
d = fuzzifikasi(x_uji, variabel_waktu_respons)
plt.axvline(x=x_uji, color='purple', linestyle='--', linewidth=1.8, label=f'Input x = {x_uji}s')
plt.scatter([x_uji, x_uji], [d['Cepat'], d['Sedang']], color='purple', s=70, zorder=5)
plt.title('Variabel Linguistik: Waktu Respons Server', fontsize=13, fontweight='bold')
plt.xlabel('Waktu Respons (detik)')
plt.ylabel('Derajat Keanggotaan μ(x)')
plt.ylim(-0.05, 1.1)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='center right')
plt.tight_layout()
plt.savefig('variabel_linguistik_waktu_respons.png', dpi=300)
plt.show()


# ==========================================================
# BAGIAN B - TUGAS: PENGGUNAAN CPU SERVER, U = [0, 100] %
#   Rendah : 1 (x<=20) ; (40-x)/20 (20<x<40) ; 0 (x>=40)
#   Normal : 0 (x<=30 atau x>=70) ; (x-30)/20 (30<x<=50) ; (70-x)/20 (50<x<70)
#   Tinggi : 0 (x<=60) ; (x-60)/20 (60<x<80) ; 1 (x>=80)
# ==========================================================
def mf_rendah(x):
    x = np.asarray(x, dtype=float)
    return np.select([x <= 20.0, (x > 20.0) & (x < 40.0), x >= 40.0],
                     [1.0, (40.0 - x) / (40.0 - 20.0), 0.0])


def mf_normal(x):
    x = np.asarray(x, dtype=float)
    return np.select([(x <= 30.0) | (x >= 70.0), (x > 30.0) & (x <= 50.0), (x > 50.0) & (x < 70.0)],
                     [0.0, (x - 30.0) / (50.0 - 30.0), (70.0 - x) / (70.0 - 50.0)])


def mf_tinggi(x):
    x = np.asarray(x, dtype=float)
    return np.select([x <= 60.0, (x > 60.0) & (x < 80.0), x >= 80.0],
                     [0.0, (x - 60.0) / (80.0 - 60.0), 1.0])


variabel_cpu = {
    "nama": "Penggunaan CPU Server", "satuan": "%", "semesta": (0.0, 100.0),
    "label": {"Rendah": mf_rendah, "Normal": mf_normal, "Tinggi": mf_tinggi},
}

print()
print("=" * 70)
print("BAGIAN B - TUGAS: Penggunaan CPU Server")
print("=" * 70)
print("| No | CPU (%) | Rendah | Normal | Tinggi | Dominan |")
print("|---:|--------:|-------:|-------:|-------:|---------|")
for i, x in enumerate([10, 35, 50, 65, 75, 95], 1):
    h = fuzzifikasi(x, variabel_cpu)
    assert all(0.0 <= v <= 1.0 for v in h.values())
    print(f"| {i} | {x:>7} | {h['Rendah']:.3f}  | {h['Normal']:.3f}  | {h['Tinggi']:.3f}  | {label_dominan(h)} |")

xc = np.linspace(0, 100, 1000)
plt.figure(figsize=(10, 5.5))
plt.plot(xc, mf_rendah(xc), label='Rendah', color='#2ca02c', linewidth=2.5)
plt.plot(xc, mf_normal(xc), label='Normal', color='#ff7f0e', linewidth=2.5)
plt.plot(xc, mf_tinggi(xc), label='Tinggi', color='#d62728', linewidth=2.5)
for x in [10, 35, 50, 65, 75, 95]:
    plt.axvline(x, color='purple', linestyle=':', alpha=0.45)
plt.title('Variabel Linguistik: Penggunaan CPU Server', fontsize=13, fontweight='bold')
plt.xlabel('Beban CPU (%)')
plt.ylabel('Derajat Keanggotaan μ(x)')
plt.ylim(-0.05, 1.1)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='center right')
plt.tight_layout()
plt.savefig('variabel_linguistik_cpu.png', dpi=300)
plt.show()
print("\nGrafik tersimpan: variabel_linguistik_waktu_respons.png, variabel_linguistik_cpu.png")
