"""
Praktikum 8 - Metode Mamdani dan Metode Defuzzifikasi
Studi kasus: Pengendalian pH Air Hidroponik (parameter dari file asesmen; target 5,8-6,2 = asumsi).

Isi:
  1. Mamdani (MIN - MAX) pada 9 aturan pH hidroponik
  2. Lima metode defuzzifikasi (implementasi mandiri NumPy): Centroid, Bisector, MOM, SOM, LOM
  3. Perbandingan pada contoh manual (5,5 / 5,7) dan 5 skenario pengujian asesmen
  4. Demo kurva bimodal untuk pertanyaan analisis nomor 3
Jalankan: python Praktikum8_NIM.py            (tambah --no-show bila tanpa layar)
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib
if "--no-show" in sys.argv:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

TOL = 1e-9
Z = np.linspace(-100, 100, 1001)          # semesta output, langkah 0,2


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
OUT_MF = {k: trapmf(Z, *p) for k, p in OUT_SETS.items()}
RULES = [("R1", "Rendah", "Turun", "Naikkan Kuat"), ("R2", "Rendah", "Stabil", "Naikkan Sedang"),
         ("R3", "Rendah", "Naik", "Naikkan Ringan"), ("R4", "Sesuai", "Turun", "Naikkan Ringan"),
         ("R5", "Sesuai", "Stabil", "Netral"), ("R6", "Sesuai", "Naik", "Turunkan Ringan"),
         ("R7", "Tinggi", "Turun", "Turunkan Ringan"), ("R8", "Tinggi", "Stabil", "Turunkan Sedang"),
         ("R9", "Tinggi", "Naik", "Turunkan Kuat")]


# ==========================================================
# 1. MAMDANI: fuzzifikasi -> implikasi MIN -> agregasi MAX
# ==========================================================
def agregasi_dari_alpha(alphas):
    """alphas: dict {label_output: alpha}. Implikasi MIN lalu agregasi MAX."""
    agg = np.zeros_like(Z)
    for lbl, a in alphas.items():
        agg = np.maximum(agg, np.minimum(a, OUT_MF[lbl]))
    return agg


def mamdani_agregasi(ph, prev):
    delta = round(ph - prev, 10)
    mu_ph = {k: float(trapmf(ph, *p)[0]) for k, p in PH_SETS.items()}
    mu_dph = {k: float(trapmf(delta, *p)[0]) for k, p in DPH_SETS.items()}
    alphas, aktif = {}, []
    for rid, lp, ld, lo in RULES:
        a = min(mu_ph[lp], mu_dph[ld])
        if a > 0:
            aktif.append((rid, lo, a))
            alphas[lo] = max(alphas.get(lo, 0.0), a)       # konklusi sama -> MAX
    return agregasi_dari_alpha(alphas), aktif, delta


# ==========================================================
# 2. LIMA METODE DEFUZZIFIKASI (grid seragam)
# ==========================================================
def defuzz(z, mu, metode):
    luas = float(np.sum(mu))
    if luas < TOL:
        raise ValueError("Luas agregasi nol: defuzzifikasi tidak dapat dihitung.")
    if metode == "centroid":
        return float(np.sum(z * mu) / luas)
    if metode == "bisector":                       # titik pertama di mana luas kumulatif >= separuh
        # toleransi 1e-9 agar galat floating-point tidak melompatkan hasil melewati celah nol
        # (pada kurva bimodal, seluruh celah nol sebenarnya adalah bisector yang sah)
        return float(z[np.searchsorted(np.cumsum(mu), luas / 2.0 - TOL)])
    mx = mu.max()
    zmax = z[np.isclose(mu, mx, atol=TOL)]        # himpunan nilai z dengan mu maksimum
    if metode == "mom":
        return float(np.mean(zmax))
    if metode == "som":
        return float(np.min(zmax))
    if metode == "lom":
        return float(np.max(zmax))
    raise ValueError(f"Metode '{metode}' tidak dikenali.")


METODE = ["centroid", "bisector", "mom", "som", "lom"]
WARNA = {"centroid": "red", "bisector": "purple", "mom": "black", "som": "green", "lom": "orange"}


def semua_metode(mu):
    return {m: defuzz(Z, mu, m) for m in METODE}


def plot_defuzz(mu, hasil, judul, nama_file, folder):
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(Z, mu, "b", linewidth=2.5, label="Kurva agregasi")
    ax.fill_between(Z, 0, mu, color="skyblue", alpha=0.4)
    for m, v in hasil.items():
        ax.axvline(v, color=WARNA[m], linestyle="--", linewidth=2, label=f"{m.upper()} ({v:+.2f})")
    ax.set_title(judul, fontweight="bold")
    ax.set_xlabel("Tindakan koreksi pH (satuan simulasi; + naikkan, - turunkan)")
    ax.set_ylabel("Derajat keanggotaan $\\mu$(z)")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(linestyle=":", alpha=0.6)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(folder / nama_file, dpi=300)
    return fig


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent / "hasil"
    folder.mkdir(exist_ok=True)

    # --- A. Contoh manual asesmen: pH 5,5 (sebelumnya 5,7) ---
    agg, aktif, delta = mamdani_agregasi(5.5, 5.7)
    hasil = semua_metode(agg)
    print("=" * 70)
    print(f"A. CONTOH MANUAL pH 5.5 (sebelumnya 5.7), dpH = {delta:+.2f}")
    print("   Aturan aktif :", ", ".join(f"{r}->{o}({a:.3f})" for r, o, a in aktif))
    print(f"   mu maksimum  : {agg.max():.3f}  (luas = {np.sum(agg) * 0.2:.2f})")
    for m, v in hasil.items():
        print(f"   {m.upper():<9}: {v:+8.2f}")
    plot_defuzz(agg, hasil, "Perbandingan 5 Metode Defuzzifikasi (pH 5,5; sebelumnya 5,7)",
                "praktikum8_defuzz_contoh.png", folder)

    # --- B. Lima skenario pengujian asesmen ---
    print("\n" + "=" * 70)
    print("B. PERBANDINGAN 5 METODE PADA 5 SKENARIO ASESMEN")
    skenario = [(1, 4.8, 5.1), (2, 4.8, 4.5), (3, 6.0, 6.0), (4, 7.5, 7.2), (5, 7.5, 7.8)]
    print(f"{'No':<4}{'pH':>6}{'sebelum':>9}{'dpH':>8}" + "".join(f"{m.upper():>10}" for m in METODE))
    for no, a, b in skenario:
        g, _, dl = mamdani_agregasi(a, b)
        h = semua_metode(g)
        print(f"{no:<4}{a:>6.2f}{b:>9.2f}{dl:>+8.2f}" + "".join(f"{h[m]:>+10.2f}" for m in METODE))
        if no in (2, 5):
            plot_defuzz(g, h, f"5 Metode Defuzzifikasi - skenario {no} (pH {a}, sebelumnya {b})",
                        f"praktikum8_defuzz_skenario{no}.png", folder)

    # --- C. Kurva bimodal hipotetis (pertanyaan analisis 3) ---
    print("\n" + "=" * 70)
    print("C. DEMO KURVA BIMODAL HIPOTETIS: Naikkan Kuat dan Turunkan Kuat sama-sama alpha = 0.8")
    bim = agregasi_dari_alpha({"Naikkan Kuat": 0.8, "Turunkan Kuat": 0.8})
    hb = semua_metode(bim)
    for m, v in hb.items():
        print(f"   {m.upper():<9}: {v:+8.2f}")
    plot_defuzz(bim, hb, "Kurva Bimodal Hipotetis: kelemahan MOM (hasil jatuh di antara dua puncak)",
                "praktikum8_defuzz_bimodal.png", folder)

    print(f"\nGambar tersimpan di: {folder}")
    if "--no-show" not in sys.argv:
        plt.show()
