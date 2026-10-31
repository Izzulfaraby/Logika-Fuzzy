"""
Praktikum 9 - Metode Sugeno dan Tsukamoto (komparasi dengan Mamdani)
Studi kasus: Pengendalian pH Air Hidroponik (parameter dari file asesmen; target 5,8-6,2 = asumsi).

Isi:
  1. Fuzzifikasi + 9 aturan (sama dengan asesmen) -> firing strength alpha (MIN)
  2. Sugeno Orde 0   : konsekuen konstanta, z* = sum(alpha*k)/sum(alpha)
  3. Tsukamoto       : konsekuen monoton, z_i = invers MF(alpha_i), z* = sum(alpha*z)/sum(alpha)
  4. Mamdani (centroid) sebagai pembanding
  5. Tabel perbandingan, selisih, dan waktu komputasi
Output: tabel di terminal + 1 grafik batang PNG di folder 'hasil/'
Jalankan: python Praktikum9_NIM.py            (tambah --no-show bila tanpa layar)

Catatan: asesmen pH utama WAJIB hanya Mamdani; berkas ini khusus Praktikum 9 sebagai komparasi.
"""
import sys
import time
from pathlib import Path
import numpy as np
import matplotlib
if "--no-show" in sys.argv:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

Z = np.linspace(-100, 100, 1001)


def trapmf(x, a, b, c, d):
    x = np.atleast_1d(np.asarray(x, dtype=float))
    y = np.zeros_like(x)
    if b > a:
        m = (x > a) & (x < b)
        y[m] = (x[m] - a) / (b - a)
    y[(x >= b) & (x <= c)] = 1.0
    if d > c:
        m = (x > c) & (x < d)
        y[m] = (d - x[m]) / (d - c)
    return y


PH_SETS = {"Rendah": (0, 0, 5.3, 5.8), "Sesuai": (5.3, 5.8, 6.2, 6.7), "Tinggi": (6.2, 6.7, 14, 14)}
DPH_SETS = {"Turun": (-14, -14, -0.3, 0), "Stabil": (-0.3, 0, 0, 0.3), "Naik": (0, 0.3, 14, 14)}
OUT_SETS = {"Turunkan Kuat": (-100, -100, -90, -60), "Turunkan Sedang": (-90, -60, -60, -30),
            "Turunkan Ringan": (-60, -30, -30, 0), "Netral": (-30, 0, 0, 30),
            "Naikkan Ringan": (0, 30, 30, 60), "Naikkan Sedang": (30, 60, 60, 90),
            "Naikkan Kuat": (60, 90, 100, 100)}
RULES = [("R1", "Rendah", "Turun", "Naikkan Kuat"), ("R2", "Rendah", "Stabil", "Naikkan Sedang"),
         ("R3", "Rendah", "Naik", "Naikkan Ringan"), ("R4", "Sesuai", "Turun", "Naikkan Ringan"),
         ("R5", "Sesuai", "Stabil", "Netral"), ("R6", "Sesuai", "Naik", "Turunkan Ringan"),
         ("R7", "Tinggi", "Turun", "Turunkan Ringan"), ("R8", "Tinggi", "Stabil", "Turunkan Sedang"),
         ("R9", "Tinggi", "Naik", "Turunkan Kuat")]

# --- Sugeno Orde 0: konstanta = puncak himpunan output Mamdani (Kuat memakai +-90) ---
KONSTANTA = {"Turunkan Kuat": -90.0, "Turunkan Sedang": -60.0, "Turunkan Ringan": -30.0, "Netral": 0.0,
             "Naikkan Ringan": 30.0, "Naikkan Sedang": 60.0, "Naikkan Kuat": 90.0}

# --- Tsukamoto: konsekuen HARUS monoton. (a, b, arah): 'naik' z=a+alpha(b-a); 'turun' z=b-alpha(b-a)
#     Naikkan_*  : monoton naik dari 0 ke puncak  | Turunkan_* : z menjauhi 0 ke arah negatif
#     Netral     : tidak bisa monoton (puncak di tengah) -> didegenerasi menjadi konstanta 0
MONOTON = {"Turunkan Kuat": (-90.0, 0.0, "turun"), "Turunkan Sedang": (-60.0, 0.0, "turun"),
           "Turunkan Ringan": (-30.0, 0.0, "turun"), "Netral": (0.0, 0.0, "naik"),
           "Naikkan Ringan": (0.0, 30.0, "naik"), "Naikkan Sedang": (0.0, 60.0, "naik"),
           "Naikkan Kuat": (0.0, 90.0, "naik")}


def invers_monoton_naik(alpha, a, b):
    return a + alpha * (b - a)


def invers_monoton_turun(alpha, a, b):
    return b - alpha * (b - a)


def firing_strengths(ph, prev):
    delta = round(ph - prev, 10)
    mu_ph = {k: float(trapmf(ph, *p)[0]) for k, p in PH_SETS.items()}
    mu_dph = {k: float(trapmf(delta, *p)[0]) for k, p in DPH_SETS.items()}
    return [(rid, lo, min(mu_ph[lp], mu_dph[ld])) for rid, lp, ld, lo in RULES], delta


def rata_terbobot(alphas, zs):
    tot = float(np.sum(alphas))
    if tot < 1e-9:
        return 0.0                                  # fallback aman: tidak ada aturan aktif
    return float(np.sum(np.asarray(alphas) * np.asarray(zs)) / tot)


def sugeno0(fs):
    return rata_terbobot([a for _, _, a in fs], [KONSTANTA[lo] for _, lo, _ in fs])


def tsukamoto(fs):
    zs = []
    for _, lo, a in fs:
        lo_, hi_, arah = MONOTON[lo]
        zs.append(invers_monoton_naik(a, lo_, hi_) if arah == "naik" else invers_monoton_turun(a, lo_, hi_))
    return rata_terbobot([a for _, _, a in fs], zs), zs


def mamdani(fs):
    agg = np.zeros_like(Z)
    for _, lo, a in fs:
        if a > 0:
            agg = np.maximum(agg, np.minimum(a, trapmf(Z, *OUT_SETS[lo])))
    luas = float(np.sum(agg))
    return float(np.sum(Z * agg) / luas) if luas > 1e-9 else 0.0


# ==========================================================
# UTILITAS TABEL (tampil di terminal)
# ==========================================================
def _angka(s):
    try:
        float(str(s).replace("+", "").replace(",", "."))
        return True
    except ValueError:
        return False


def cetak_tabel(judul, header, baris):
    """Cetak tabel rapi dengan garis (ASCII, aman untuk semua terminal)."""
    teks = [[str(c) for c in r] for r in baris]
    lebar = [max([len(str(h))] + [len(r[i]) for r in teks]) for i, h in enumerate(header)]
    garis = "+" + "+".join("-" * (w + 2) for w in lebar) + "+"

    def fmt(r, rata_kanan=True):
        sel = [(c.rjust(w) if rata_kanan and _angka(c) else c.ljust(w)) for c, w in zip(r, lebar)]
        return "| " + " | ".join(sel) + " |"

    print(f"\n{judul}")
    print(garis)
    print(fmt([str(h) for h in header], rata_kanan=False))
    print(garis)
    for r in teks:
        print(fmt(r))
    print(garis)


def tampilkan_tabel(judul, header, baris):
    cetak_tabel(judul, header, baris)


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent / "hasil"
    folder.mkdir(exist_ok=True)

    skenario = [("S1 rendah & menurun", 4.8, 5.1), ("S2 rendah & meningkat", 4.8, 4.5),
                ("S3 sesuai & stabil", 6.0, 6.0), ("S4 tinggi & meningkat", 7.5, 7.2),
                ("S5 tinggi & menurun", 7.5, 7.8),
                ("S6 transisi (contoh manual)", 5.5, 5.7), ("S7 transisi atas", 6.4, 6.3),
                ("S8 rendah, dpH kecil", 5.2, 5.3)]

    # --- 1. Rancangan konsekuen ---
    baris = []
    for lbl in KONSTANTA:
        lo, hi, arah = MONOTON[lbl]
        baris.append([lbl, f"{KONSTANTA[lbl]:+.0f}", f"[{lo:+.0f}, {hi:+.0f}]", arah])
    tampilkan_tabel("1. RANCANGAN KONSEKUEN: konstanta Sugeno dan rampa monoton Tsukamoto",
                    ["Label konsekuen", "k Sugeno 0", "Rentang Tsukamoto [a, b]", "Arah rampa"], baris)

    # --- 2. Rincian S6 ---
    fs, delta = firing_strengths(5.5, 5.7)
    zt = tsukamoto(fs)[1]
    baris = [[r, lo, f"{a:.3f}", f"{KONSTANTA[lo]:+.1f}", f"{z_t:+.2f}", f"{a * KONSTANTA[lo]:+.2f}",
              f"{a * z_t:+.2f}"] for (r, lo, a), z_t in zip(fs, zt) if a > 0]
    tot = sum(a for _, _, a in fs)
    baris.append(["Jumlah", "", f"{tot:.3f}", "", "", f"{sum(a * KONSTANTA[lo] for _, lo, a in fs):+.2f}",
                  f"{sum(a * z for (_, _, a), z in zip(fs, zt)):+.2f}"])
    tampilkan_tabel(f"2. RINCIAN HITUNG S6: pH 5,5 (sebelumnya 5,7), dpH {delta:+.2f} (baris Jumlah = pembilang rata-rata terbobot)",
                    ["Aturan", "Konsekuen", "alpha", "k Sugeno", "z Tsukamoto", "alpha*k", "alpha*z"], baris)
    tampilkan_tabel("   Hasil akhir S6 (rata-rata terbobot = total alpha*nilai / total alpha)",
                    ["Metode", "Koreksi"],
                    [["Mamdani (centroid)", f"{mamdani(fs):+.2f}"], ["Sugeno Orde 0", f"{sugeno0(fs):+.2f}"],
                     ["Tsukamoto", f"{tsukamoto(fs)[0]:+.2f}"]])

    # --- 3. Tabel perbandingan ---
    baris, data = [], []
    for nama, a, b in skenario:
        fs, d = firing_strengths(a, b)
        m, s_, t = mamdani(fs), sugeno0(fs), tsukamoto(fs)[0]
        data.append((nama, m, s_, t))
        baris.append([nama, f"{a:.2f}", f"{b:.2f}", f"{d:+.2f}", f"{m:+.2f}", f"{s_:+.2f}", f"{t:+.2f}",
                      f"{s_ - m:+.2f}", f"{t - m:+.2f}", f"{t - s_:+.2f}"])
    tampilkan_tabel("3. PERBANDINGAN KOREKSI MAMDANI vs SUGENO 0 vs TSUKAMOTO (satuan simulasi)",
                    ["Skenario", "pH", "Sebelumnya", "dpH", "Mamdani", "Sugeno0", "Tsukamoto",
                     "S0-M", "T-M", "T-S0"], baris)

    # --- 4. Waktu komputasi ---
    N = 2000
    fs, _ = firing_strengths(5.5, 5.7)
    waktu = {}
    for nama, f in (("Mamdani", mamdani), ("Sugeno0", sugeno0), ("Tsukamoto", lambda x: tsukamoto(x)[0])):
        t0 = time.perf_counter()
        for _ in range(N):
            f(fs)
        waktu[nama] = (time.perf_counter() - t0) / N * 1e6
    dasar = waktu["Sugeno0"]
    tampilkan_tabel(f"4. WAKTU KOMPUTASI RATA-RATA ({N} ulangan; Mamdani memakai grid 1001 titik)",
                    ["Metode", "Waktu (mikrodetik)", "Relatif terhadap Sugeno0"],
                    [[k, f"{v:.1f}", f"{v / dasar:.1f}x"] for k, v in waktu.items()])

    # --- Grafik batang ---
    fig, ax = plt.subplots(figsize=(12, 5.5))
    x = np.arange(len(data))
    w = 0.27
    ax.bar(x - w, [b[1] for b in data], w, label="Mamdani (centroid)", color="tab:blue")
    ax.bar(x, [b[2] for b in data], w, label="Sugeno Orde 0", color="tab:green")
    ax.bar(x + w, [b[3] for b in data], w, label="Tsukamoto", color="tab:orange")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([b[0].split(" ")[0] for b in data])
    ax.set_xlabel("Skenario")
    ax.set_ylabel("Koreksi (satuan simulasi; + naikkan, - turunkan)")
    ax.set_title("Perbandingan Mamdani vs Sugeno Orde 0 vs Tsukamoto - Pengendalian pH Hidroponik",
                 fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(folder / "praktikum9_perbandingan_metode.png", dpi=300)
    print(f"\nGambar tersimpan di: {folder}")
    if "--no-show" not in sys.argv:
        plt.show()