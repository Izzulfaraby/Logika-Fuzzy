"""
Praktikum 7 - Arsitektur Fuzzy Inference System (FIS)
Studi kasus: Pengendalian pH Air Hidroponik (Mamdani: implikasi MIN, agregasi MAX, centroid).
Parameter mengikuti file asesmen Praktikum_Fuzzy_pH_Hidroponik.md (target 5,8-6,2 = asumsi).

Isi:
  1. Kelas FuzzyInferenceSystem: add_input_variable, set_output_variable, add_rule, compute
  2. Pengujian 3 kasus + contoh manual 5,5 -> 5,7
  3. Fallback agregasi kosong (semua alpha = 0)
  4. Perbandingan implikasi Clipping (MIN) vs Scaling (PRODUCT)
  5. Visualisasi tahapan: implikasi, agregasi, centroid
Jalankan: python Praktikum7_NIM.py            (tambah --no-show bila tanpa layar)
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib
if "--no-show" in sys.argv:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

EPS_LUAS = 1e-9


def trapmf(x, a, b, c, d):
    """Trapesium (a,b,c,d); segitiga b==c; bahu kiri a==b; bahu kanan c==d. Mendukung array."""
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


# ==========================================================
# 1. KELAS FUZZY INFERENCE SYSTEM
# ==========================================================
class FuzzyInferenceSystem:
    def __init__(self, implikasi="min"):
        self.inputs = {}        # nama -> (universe, {label: (a,b,c,d)})
        self.output = None      # (nama, universe, {label: (a,b,c,d)})
        self.rules = []         # (id, {var: label}, label_output)
        self.implikasi = implikasi   # 'min' (clipping) atau 'prod' (scaling)
        self.detail = {}        # hasil tahapan terakhir, untuk visualisasi

    # --- Knowledge Base ---
    def add_input_variable(self, name, universe, mf_dict):
        self.inputs[name] = (np.asarray(universe, dtype=float), mf_dict)

    def set_output_variable(self, name, universe, mf_dict):
        self.output = (name, np.asarray(universe, dtype=float), mf_dict)

    def add_rule(self, rule_tuple):
        """rule_tuple = (id, {'ph_sekarang': 'Rendah', 'delta_ph': 'Turun'}, 'Naikkan Kuat')"""
        rid, antecedent, konsekuen = rule_tuple
        for var, lbl in antecedent.items():
            if var not in self.inputs or lbl not in self.inputs[var][1]:
                raise ValueError(f"{rid}: variabel/label '{var}={lbl}' belum didefinisikan.")
        if konsekuen not in self.output[2]:
            raise ValueError(f"{rid}: label output '{konsekuen}' belum didefinisikan.")
        self.rules.append((rid, antecedent, konsekuen))

    # --- Tahap 1: Fuzzifikasi ---
    def fuzzifikasi(self, input_values):
        derajat = {}
        for var, (uni, mfs) in self.inputs.items():
            x = float(input_values[var])
            if not (uni.min() <= x <= uni.max()):
                raise ValueError(f"{var}={x} di luar semesta [{uni.min():g}, {uni.max():g}].")
            derajat[var] = {lbl: float(trapmf(x, *p)[0]) for lbl, p in mfs.items()}
        return derajat

    # --- Tahap 2-4: evaluasi aturan, implikasi, agregasi, defuzzifikasi ---
    def compute(self, input_values, fallback=0.0):
        """Mengembalikan nilai crisp output. Bila agregasi kosong -> fallback (tanpa pembagian nol)."""
        nama_out, z, mf_out = self.output
        derajat = self.fuzzifikasi(input_values)
        agregat = np.zeros_like(z)
        aktif, terpotong = [], {}
        for rid, ant, lbl_out in self.rules:
            alpha = min(derajat[v][l] for v, l in ant.items())       # AND = MIN
            if alpha > 0:
                mu_c = trapmf(z, *mf_out[lbl_out])
                klip = np.minimum(alpha, mu_c) if self.implikasi == "min" else alpha * mu_c
                terpotong[rid] = klip
                agregat = np.maximum(agregat, klip)                  # agregasi MAX
                aktif.append((rid, lbl_out, alpha))
        luas = float(np.sum(agregat))
        berhasil = luas >= EPS_LUAS
        crisp = float(np.sum(z * agregat) / luas) if berhasil else fallback   # centroid
        self.detail = {"derajat": derajat, "aktif": aktif, "terpotong": terpotong,
                       "agregat": agregat, "crisp": crisp, "berhasil": berhasil}
        return crisp


# ==========================================================
# 2. KONFIGURASI SISTEM pH HIDROPONIK
# ==========================================================
def bangun_fis(implikasi="min", rules_dipakai=None):
    fis = FuzzyInferenceSystem(implikasi)
    fis.add_input_variable("ph_sekarang", np.linspace(0, 14, 1401), {
        "Rendah": (0, 0, 5.3, 5.8), "Sesuai": (5.3, 5.8, 6.2, 6.7), "Tinggi": (6.2, 6.7, 14, 14)})
    fis.add_input_variable("delta_ph", np.linspace(-14, 14, 2801), {
        "Turun": (-14, -14, -0.3, 0), "Stabil": (-0.3, 0, 0, 0.3), "Naik": (0, 0.3, 14, 14)})
    fis.set_output_variable("koreksi", np.linspace(-100, 100, 1001), {
        "Turunkan Kuat": (-100, -100, -90, -60), "Turunkan Sedang": (-90, -60, -60, -30),
        "Turunkan Ringan": (-60, -30, -30, 0), "Netral": (-30, 0, 0, 30),
        "Naikkan Ringan": (0, 30, 30, 60), "Naikkan Sedang": (30, 60, 60, 90),
        "Naikkan Kuat": (60, 90, 100, 100)})
    matriks = [("Rendah", "Turun", "Naikkan Kuat"), ("Rendah", "Stabil", "Naikkan Sedang"),
               ("Rendah", "Naik", "Naikkan Ringan"), ("Sesuai", "Turun", "Naikkan Ringan"),
               ("Sesuai", "Stabil", "Netral"), ("Sesuai", "Naik", "Turunkan Ringan"),
               ("Tinggi", "Turun", "Turunkan Ringan"), ("Tinggi", "Stabil", "Turunkan Sedang"),
               ("Tinggi", "Naik", "Turunkan Kuat")]
    for i, (p, d, o) in enumerate(matriks, start=1):
        if rules_dipakai is None or f"R{i}" in rules_dipakai:
            fis.add_rule((f"R{i}", {"ph_sekarang": p, "delta_ph": d}, o))
    return fis


def hitung(fis, ph, prev):
    """Pembungkus: delta_ph dihitung otomatis dari dua pengukuran."""
    delta = round(ph - prev, 10)
    return fis.compute({"ph_sekarang": ph, "delta_ph": delta}), delta


def label_keputusan(z):
    a = abs(z)
    if a < 10:
        return "Netral (tidak perlu koreksi)"
    return f"{'Naikkan' if z > 0 else 'Turunkan'} pH tingkat {'ringan' if a < 40 else 'sedang' if a < 70 else 'kuat'}"


# ==========================================================
# 3. VISUALISASI
# ==========================================================
def plot_tahapan(fis, ph, prev, ax):
    z = fis.output[1]
    hitung(fis, ph, prev)
    d = fis.detail
    for lbl, p in fis.output[2].items():
        ax.plot(z, trapmf(z, *p), "--", color="gray", linewidth=0.7, alpha=0.7)
    for rid, klip in d["terpotong"].items():
        ax.plot(z, klip, linewidth=1.0, label=f"{rid} (terpotong)")
    ax.fill_between(z, d["agregat"], color="purple", alpha=0.35, label="Agregasi (MAX)")
    ax.axvline(d["crisp"], color="black", linewidth=2, label=f"Centroid = {d['crisp']:+.2f}")
    ax.set_title(f"pH {ph} (sebelumnya {prev})", fontsize=10, fontweight="bold")
    ax.set_xlabel("Koreksi (satuan simulasi)")
    ax.set_ylabel("Derajat keanggotaan $\\mu$")
    ax.set_ylim(0, 1.1)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=7, loc="upper left")


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent / "hasil"
    folder.mkdir(exist_ok=True)

    fis = bangun_fis()
    print("=" * 78)
    print("PENGUJIAN FIS pH HIDROPONIK (Mamdani: MIN - MAX - Centroid)")
    print("=" * 78)
    kasus = [("Kasus 1", 4.8, 5.1), ("Kasus 2", 6.0, 6.0), ("Kasus 3", 7.5, 7.2),
             ("Contoh manual asesmen", 5.5, 5.7)]
    print(f"{'Kasus':<24}{'pH':>6}{'sebelum':>9}{'dpH':>8}  {'Aturan aktif':<40}{'Output':>9}  Keputusan")
    for nama, a, b in kasus:
        z, delta = hitung(fis, a, b)
        ar = ", ".join(f"{r}({al:.2f})" for r, _, al in fis.detail["aktif"])
        print(f"{nama:<24}{a:>6.2f}{b:>9.2f}{delta:>+8.2f}  {ar:<40}{z:>+9.2f}  {label_keputusan(z)}")

    # --- Pertanyaan 3: agregasi kosong -> fallback ---
    print("\n" + "=" * 78)
    print("UJI FALLBACK: FIS hanya berisi R1 (rule base tidak lengkap), input pH 7,5 / 7,2")
    fis_parsial = bangun_fis(rules_dipakai={"R1"})
    z = fis_parsial.compute({"ph_sekarang": 7.5, "delta_ph": 0.3})
    print(f"  agregasi berhasil = {fis_parsial.detail['berhasil']}, luas = "
          f"{np.sum(fis_parsial.detail['agregat']):.1f}, output fallback = {z:+.2f}")

    # --- Pertanyaan 2: Clipping (MIN) vs Scaling (PRODUCT) ---
    print("\n" + "=" * 78)
    print("PERBANDINGAN IMPLIKASI: Clipping (MIN) vs Scaling (PRODUCT)")
    fis_prod = bangun_fis("prod")
    print(f"{'Kasus':<24}{'MIN':>10}{'PRODUCT':>10}")
    for nama, a, b in kasus:
        zm, _ = hitung(fis, a, b)
        zp, _ = hitung(fis_prod, a, b)
        print(f"{nama:<24}{zm:>+10.2f}{zp:>+10.2f}")

    # --- Validasi input di luar semesta ---
    try:
        hitung(fis, 15, 6)
    except ValueError as e:
        print(f"\nUji input tidak valid -> ValueError: {e}")

    # --- Grafik: 3 kasus + contoh manual ---
    fig, axs = plt.subplots(2, 2, figsize=(13, 8))
    for ax, (nama, a, b) in zip(axs.ravel(), kasus):
        plot_tahapan(fis, a, b, ax)
    fig.suptitle("Praktikum 7 - Implikasi, Agregasi, dan Defuzzifikasi Centroid (FIS pH Hidroponik)",
                 fontweight="bold")
    fig.tight_layout()
    fig.savefig(folder / "praktikum7_pipeline_fis.png", dpi=300)

    # --- Grafik: MIN vs PRODUCT pada contoh manual ---
    fig2, axs2 = plt.subplots(1, 2, figsize=(13, 4.5))
    for ax, f, jd in zip(axs2, (fis, fis_prod), ("Implikasi MIN (clipping)", "Implikasi PRODUCT (scaling)")):
        plot_tahapan(f, 5.5, 5.7, ax)
        ax.set_title(f"{jd} - pH 5,5 (sebelumnya 5,7)", fontsize=10, fontweight="bold")
    fig2.tight_layout()
    fig2.savefig(folder / "praktikum7_min_vs_product.png", dpi=300)
    print(f"\nGambar tersimpan di: {folder}")
    if "--no-show" not in sys.argv:
        plt.show()
