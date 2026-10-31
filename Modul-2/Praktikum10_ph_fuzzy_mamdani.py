"""
ph_hidroponik_mamdani.py
SISTEM PENGENDALIAN KADAR PH AIR PADA BUDIDAYA HIDROPONIK BERBASIS LOGIKA FUZZY
Metode: Mamdani | Implikasi: MIN | Agregasi: MAX | Defuzzifikasi: Centroid

SIMULASI saja: output adalah perintah simulasi, BUKAN dosis bahan kimia.

Penggunaan:
  python ph_hidroponik_mamdani.py                    -> mode interaktif
  python ph_hidroponik_mamdani.py --sekarang 6.2 --sebelumnya 5.9
  python ph_hidroponik_mamdani.py --demo             -> grafik MF, decision surface, tabel pengujian
  Grafik otomatis ditampilkan (dan disimpan PNG). Gunakan --no-show bila tanpa layar,
  --out <folder> untuk mengganti folder keluaran
  (default: folder 'hasil' di samping file skrip ini).
"""

import argparse
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (proyeksi 3D)

# ============================================================
# 1. KONSTANTA DAN SEMESTA PEMBICARAAN
# ============================================================
PH_MIN, PH_MAX = 0.0, 14.0          # ph_sekarang dan ph_sebelumnya
DPH_MIN, DPH_MAX = -14.0, 14.0      # delta_ph = ph_sekarang - ph_sebelumnya
OUT_MIN, OUT_MAX = -100.0, 100.0    # koreksi (satuan simulasi)
N_OUT = 1001                        # resolusi diskretisasi output (langkah 0,2)

TARGET_MIN, TARGET_MAX = 5.8, 6.2   # ASUMSI target pH (sesuaikan dengan tanaman)
AMBANG_STABIL = 0.10                # |delta_ph| <= ambang -> tren STABIL (klasifikasi crisp)
TOL = 1e-9                          # toleransi pembulatan floating-point
EPS_LUAS = 1e-9                     # luas agregasi minimum agar centroid sah

X_OUT = np.linspace(OUT_MIN, OUT_MAX, N_OUT)

# ============================================================
# 2. FUNGSI KEANGGOTAAN
# ============================================================
def trapmf(x, a, b, c, d):
    """Trapesium (a,b,c,d). Segitiga: b == c. Bahu kiri: a == b. Bahu kanan: c == d."""
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


PH_SETS = {                                   # input 1: ph_sekarang
    "Rendah": (0.0, 0.0, 5.3, 5.8),
    "Sesuai": (5.3, 5.8, 6.2, 6.7),
    "Tinggi": (6.2, 6.7, 14.0, 14.0),
}
DPH_SETS = {                                  # input 2: delta_ph
    "Turun":  (-14.0, -14.0, -0.3, 0.0),
    "Stabil": (-0.3, 0.0, 0.0, 0.3),
    "Naik":   (0.0, 0.3, 14.0, 14.0),
}
OUT_SETS = {                                  # output: koreksi
    "Turunkan Kuat":   (-100.0, -100.0, -90.0, -60.0),
    "Turunkan Sedang": (-90.0, -60.0, -60.0, -30.0),
    "Turunkan Ringan": (-60.0, -30.0, -30.0, 0.0),
    "Netral":          (-30.0, 0.0, 0.0, 30.0),
    "Naikkan Ringan":  (0.0, 30.0, 30.0, 60.0),
    "Naikkan Sedang":  (30.0, 60.0, 60.0, 90.0),
    "Naikkan Kuat":    (60.0, 90.0, 100.0, 100.0),
}
OUT_MF = {n: trapmf(X_OUT, *p) for n, p in OUT_SETS.items()}

# ============================================================
# 3. BASIS ATURAN 3 x 3 = 9 ATURAN   <<< DI SINILAH ATURAN IF-THEN DIDEFINISIKAN >>>
# ============================================================
# Format setiap aturan: (id, label pH sekarang, label perubahan pH, label output)
# Dibaca: IF ph_sekarang = <label 2> AND delta_ph = <label 3> THEN koreksi = <label 4>
#
# Matriks aturan (baris = pH terhadap target, kolom = perubahan pH):
#
#   pH \ dpH  |      Turun       |      Stabil       |      Naik
#   ----------+------------------+-------------------+------------------
#   Rendah    | R1 Naikkan Kuat  | R2 Naikkan Sedang | R3 Naikkan Ringan
#   Sesuai    | R4 Naikkan Ringan| R5 Netral         | R6 Turunkan Ringan
#   Tinggi    | R7 Turunkan Ringan| R8 Turunkan Sedang| R9 Turunkan Kuat
#
# Untuk menambah/mengubah aturan, cukup edit daftar RULES di bawah ini
# (label harus ada di PH_SETS, DPH_SETS, dan OUT_SETS).
RULES = [
    # --- pH RENDAH: cenderung menaikkan pH ---
    ("R1", "Rendah", "Turun",  "Naikkan Kuat"),     # rendah & masih menjauhi target -> koreksi terkuat
    ("R2", "Rendah", "Stabil", "Naikkan Sedang"),   # rendah & tidak bergerak        -> koreksi sedang
    ("R3", "Rendah", "Naik",   "Naikkan Ringan"),   # rendah tapi sudah naik         -> cukup ringan

    # --- pH SESUAI TARGET: koreksi dini mengikuti arah pergerakan ---
    ("R4", "Sesuai", "Turun",  "Naikkan Ringan"),   # masih sesuai tapi menurun      -> koreksi dini naik
    ("R5", "Sesuai", "Stabil", "Netral"),           # sesuai & stabil                -> tidak perlu tindakan
    ("R6", "Sesuai", "Naik",   "Turunkan Ringan"),  # masih sesuai tapi naik         -> koreksi dini turun

    # --- pH TINGGI: cenderung menurunkan pH ---
    ("R7", "Tinggi", "Turun",  "Turunkan Ringan"),  # tinggi tapi sudah turun        -> cukup ringan
    ("R8", "Tinggi", "Stabil", "Turunkan Sedang"),  # tinggi & tidak bergerak        -> koreksi sedang
    ("R9", "Tinggi", "Naik",   "Turunkan Kuat"),    # tinggi & masih menjauhi target -> koreksi terkuat
]

# ============================================================
# 4. VALIDASI DAN PERHITUNGAN PERUBAHAN PH
# ============================================================
def validasi_ph(nilai, nama):
    """Ubah ke float dan pastikan 0 <= pH <= 14. Raise ValueError bila tidak valid."""
    try:
        v = float(str(nilai).strip().replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError(f"{nama} harus berupa bilangan (contoh: 6.2).")
    if not math.isfinite(v):
        raise ValueError(f"{nama} tidak boleh NaN atau tak hingga.")
    if v < PH_MIN or v > PH_MAX:
        raise ValueError(f"{nama} = {v} di luar rentang {PH_MIN:g}-{PH_MAX:g}.")
    return v


def hitung_delta_ph(ph_sekarang, ph_sebelumnya):
    """delta_ph = ph_sekarang - ph_sebelumnya (rentang -14 s.d. +14).
    Dibulatkan 10 desimal hanya untuk membuang galat floating-point (mis. 4.8-5.1 = -0.2999999999999998)."""
    return round(ph_sekarang - ph_sebelumnya, 10)


# ============================================================
# 5. KLASIFIKASI KONDISI AIR (crisp, memakai nilai asli tanpa pembulatan)
# ============================================================
def status_kimia(ph):
    if ph < 7.0:
        return "ASAM"
    if ph == 7.0:
        return "NETRAL"
    return "BASA"


def status_target(ph):
    if ph < TARGET_MIN - TOL:
        return "TERLALU RENDAH"
    if ph > TARGET_MAX + TOL:
        return "TERLALU TINGGI"
    return "SESUAI TARGET"


def tren_ph(delta):
    if delta > AMBANG_STABIL + TOL:
        return "MENINGKAT"
    if delta < -AMBANG_STABIL - TOL:
        return "MENURUN"
    return "STABIL"


# ============================================================
# 6. MESIN INFERENSI MAMDANI
# ============================================================
def fuzzifikasi(ph, delta):
    """Tahap 1: crisp -> derajat keanggotaan."""
    mu_ph = {n: float(trapmf(ph, *p)[0]) for n, p in PH_SETS.items()}
    mu_dph = {n: float(trapmf(delta, *p)[0]) for n, p in DPH_SETS.items()}
    return mu_ph, mu_dph


def defuzzifikasi_centroid(z, mu_agg):
    """
    Tahap 4: z* = sum(z*mu)/sum(mu) (aproksimasi diskret dari integral, grid seragam).
    Bila luas ~ 0 -> (None, 'luas_nol'); TIDAK ada pembagian dengan nol.
    """
    luas = float(np.sum(mu_agg))
    if luas < EPS_LUAS:
        return None, "luas_nol"
    return float(np.sum(z * mu_agg) / luas), "ok"


def inferensi_inti(ph, delta):
    """Tahap 1-4 pada (ph, delta) yang sudah valid. Dipakai oleh infer() dan decision surface."""
    mu_ph, mu_dph = fuzzifikasi(ph, delta)

    agregat = np.zeros_like(X_OUT)
    aktif = []
    terpotong = {}
    # >>> PEMAKAIAN ATURAN: setiap aturan di RULES (bagian 3) dievaluasi satu per satu di sini <<<
    for rid, l_ph, l_dph, l_out in RULES:
        # IF pH = l_ph AND dpH = l_dph  ->  kekuatan aktivasi (alpha)
        alpha = min(mu_ph[l_ph], mu_dph[l_dph])            # Tahap 2a: MIN (AND)
        if alpha > 0.0:                                    # aturan aktif hanya bila alpha > 0
            # THEN koreksi = l_out  ->  himpunan output dipotong setinggi alpha
            klip = np.minimum(alpha, OUT_MF[l_out])        # Tahap 2b: implikasi MIN
            terpotong[rid] = klip
            agregat = np.maximum(agregat, klip)            # Tahap 3: agregasi MAX
            aktif.append((rid, l_ph, l_dph, l_out, alpha))

    z, st = defuzzifikasi_centroid(X_OUT, agregat)         # Tahap 4: centroid
    return mu_ph, mu_dph, aktif, terpotong, agregat, z, st


def infer(ph_sekarang, ph_sebelumnya):
    """Validasi -> delta -> klasifikasi -> inferensi Mamdani lengkap."""
    ph = validasi_ph(ph_sekarang, "pH sekarang")
    pre = validasi_ph(ph_sebelumnya, "pH sebelumnya")
    delta = hitung_delta_ph(ph, pre)

    mu_ph, mu_dph, aktif, terpotong, agregat, z, st = inferensi_inti(ph, delta)
    berhasil = z is not None
    z_out = z if berhasil else 0.0                         # kegagalan inferensi -> nilai aman 0

    return {
        "ph_sekarang": ph, "ph_sebelumnya": pre, "delta_ph": delta,
        "status_kimia": status_kimia(ph), "status_target": status_target(ph), "tren": tren_ph(delta),
        "mu_ph": mu_ph, "mu_dph": mu_dph, "aturan_aktif": aktif,
        "agregat": agregat, "terpotong": terpotong,
        "koreksi": z_out, "berhasil": berhasil, "status_defuzz": st,
    }


def evaluasi_sistem_fuzzy(ph_sekarang, ph_sebelumnya):
    """Pembungkus: hanya nilai koreksi (dipakai decision surface dan pengujian)."""
    return infer(ph_sekarang, ph_sebelumnya)["koreksi"]


def teks_keputusan(h):
    if not h["berhasil"]:
        return "INFERENSI GAGAL (tidak ada aturan aktif): tidak ada koreksi, periksa sistem"
    z = h["koreksi"]
    a = abs(z)
    if a < 10:
        return "Netral: tidak perlu koreksi (simulasi)"
    arah = "Naikkan" if z > 0 else "Turunkan"
    tingkat = "ringan" if a < 40 else ("sedang" if a < 70 else "kuat")
    return f"{arah} pH tingkat {tingkat} (simulasi)"


# ============================================================
# 7. VISUALISASI
# ============================================================
def plot_agregasi(h, folder):
    """Kurva agregasi: himpunan output, hasil MAX, area, garis centroid (hasil inferensi aktual)."""
    fig, ax = plt.subplots(figsize=(10, 4.8))
    for nama, mf in OUT_MF.items():
        ax.plot(X_OUT, mf, "--", linewidth=0.8, color="gray", alpha=0.7)
    for rid, klip in h["terpotong"].items():
        ax.plot(X_OUT, klip, linewidth=1.0, alpha=0.8, label=f"{rid} (terpotong MIN)")
    ax.fill_between(X_OUT, h["agregat"], color="tab:orange", alpha=0.45, label="Area agregasi (MAX)")
    if h["berhasil"]:
        ax.axvline(h["koreksi"], color="red", linewidth=2, label=f"Centroid z* = {h['koreksi']:+.2f}")
    ax.set_title(f"Kurva Agregasi Mamdani (pH {h['ph_sekarang']:.2f}, sebelumnya {h['ph_sebelumnya']:.2f}, "
                 f"$\\Delta$pH {h['delta_ph']:+.2f})", fontweight="bold")
    ax.set_xlabel("Tindakan koreksi pH (satuan simulasi; + naikkan, - turunkan)")
    ax.set_ylabel("Derajat keanggotaan $\\mu$")
    ax.set_ylim(0, 1.1)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", fontsize=8, ncol=2)
    fig.tight_layout()
    nama = f"agregasi_{h['ph_sekarang']:.2f}_{h['ph_sebelumnya']:.2f}.png"
    fig.savefig(folder / nama, dpi=300)
    return fig, nama


def _plot_mf(x, sets, judul, xlabel, nama_file, folder):
    fig, ax = plt.subplots(figsize=(9, 4))
    for nama, p in sets.items():
        ax.plot(x, trapmf(x, *p), linewidth=2, label=nama)
    ax.set_title(judul, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Derajat keanggotaan $\\mu$")
    ax.set_ylim(-0.05, 1.1)
    ax.grid(alpha=0.3)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5))
    fig.tight_layout()
    fig.savefig(folder / nama_file, dpi=300)
    return fig


def plot_fungsi_keanggotaan(folder):
    _plot_mf(np.linspace(PH_MIN, PH_MAX, 1401), PH_SETS, "Fungsi Keanggotaan pH Sekarang", "pH",
             "mf_ph_sekarang.png", folder)
    _plot_mf(np.linspace(-1.5, 1.5, 1201), DPH_SETS,
             "Fungsi Keanggotaan Perubahan pH (diperbesar: -1,5 s.d. +1,5)", "$\\Delta$pH",
             "mf_delta_ph.png", folder)
    _plot_mf(X_OUT, OUT_SETS, "Fungsi Keanggotaan Tindakan Koreksi",
             "Tindakan koreksi (satuan simulasi)", "mf_koreksi.png", folder)


def plot_decision_surface(folder):
    """X: ph_sekarang (0-14), Y: delta_ph (-14..14), Z: koreksi. Grid dirapatkan di zona transisi."""
    xs = np.unique(np.concatenate([np.linspace(0, 14, 57), np.linspace(5.0, 7.0, 41)]))
    ys = np.unique(np.concatenate([np.linspace(-14, 14, 57), np.linspace(-1.0, 1.0, 41)]))
    X, Y = np.meshgrid(xs, ys)
    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            *_, z, _st = inferensi_inti(X[i, j], Y[i, j])   # Mamdani yang sama dengan infer()
            Z[i, j] = 0.0 if z is None else z

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none", alpha=0.95)
    ax.set_xlabel("pH sekarang")
    ax.set_ylabel("Perubahan pH ($\\Delta$pH)")
    ax.set_zlabel("Koreksi (satuan simulasi)")
    ax.set_title("Decision Surface Mamdani: Pengendalian pH Hidroponik", fontweight="bold")
    fig.colorbar(surf, shrink=0.5, aspect=8, label="Koreksi (satuan simulasi)")
    fig.savefig(folder / "decision_surface.png", dpi=300)
    return fig


# ============================================================
# 8. TAMPILAN HASIL
# ============================================================
def tampilkan_hasil(h, nama_png="-"):
    g = "=" * 40
    print(g)
    print("SISTEM PENGENDALIAN PH HIDROPONIK")
    print("METODE FUZZY MAMDANI")
    print(g)
    print(f"pH sekarang           : {h['ph_sekarang']:.2f}")
    print(f"pH sebelumnya         : {h['ph_sebelumnya']:.2f}")
    print(f"Perubahan pH          : {h['delta_ph']:+.2f}")
    print(f"Status kimia          : {h['status_kimia']}")
    print(f"Status terhadap target: {h['status_target']}")
    print(f"Tren pH               : {h['tren']}")
    print(f"Nilai koreksi         : {h['koreksi']:+.2f} satuan simulasi")
    print(f"Keputusan             : {teks_keputusan(h)}")
    print(f"Visualisasi           : {nama_png}")
    print(g)
    print("Rincian inferensi:")
    print("  mu pH sekarang :", {k: round(v, 3) for k, v in h["mu_ph"].items()})
    print("  mu perubahan pH:", {k: round(v, 3) for k, v in h["mu_dph"].items()})
    if h["aturan_aktif"]:
        for rid, a, b, c, alpha in h["aturan_aktif"]:
            print(f"  {rid}: IF pH={a} AND dpH={b} THEN {c} (alpha={alpha:.3f})")
    else:
        print("  [PERINGATAN] Tidak ada aturan aktif / luas agregasi nol; koreksi diatur aman 0.00.")
    print("Catatan: nilai koreksi = perintah simulasi, BUKAN dosis bahan kimia.")
    print(g)


def proses_dan_tampilkan(ph_sekarang, ph_sebelumnya, folder, tampil=True):
    """Hitung, cetak hasil, simpan PNG kurva agregasi, lalu (opsional) tampilkan jendela grafik."""
    h = infer(ph_sekarang, ph_sebelumnya)
    fig, nama = plot_agregasi(h, folder)
    tampilkan_hasil(h, str(folder / nama))
    if tampil:
        plt.show()          # jendela Matplotlib tampil; tutup jendela untuk melanjutkan
    plt.close(fig)
    return h


# ============================================================
# 9. PENGUJIAN SKENARIO
# ============================================================
SKENARIO = [
    (1, 4.80, 5.10, "Rendah & menurun",   "Naikkan kuat"),
    (2, 4.80, 4.50, "Rendah & meningkat", "Naikkan ringan (lebih kecil dari S1)"),
    (3, 6.00, 6.00, "Sesuai & stabil",    "Netral"),
    (4, 7.50, 7.20, "Tinggi & meningkat", "Turunkan kuat"),
    (5, 7.50, 7.80, "Tinggi & menurun",   "Turunkan ringan (lebih kecil dari S4)"),
]


def jalankan_pengujian():
    print("\n| No | pH sekarang | pH sebelumnya | dpH | Status kimia | Target | Tren | Aturan aktif | Output | Keputusan |")
    print("|---:|---:|---:|---:|---|---|---|---|---:|---|")
    for no, a, b, _, _ in SKENARIO:
        h = infer(a, b)
        ar = ", ".join(f"{r[0]}({r[4]:.2f})" for r in h["aturan_aktif"])
        print(f"| {no} | {a:.2f} | {b:.2f} | {h['delta_ph']:+.2f} | {h['status_kimia']} | {h['status_target']} "
              f"| {h['tren']} | {ar} | {h['koreksi']:+.2f} | {teks_keputusan(h)} |")


# ============================================================
# 10. PROGRAM UTAMA
# ============================================================
def baca_ph(prompt):
    """Minta input sampai valid. Mengembalikan None bila pengguna mengetik 'q'."""
    while True:
        s = input(prompt).strip()
        if s.lower() == "q":
            return None
        try:
            return validasi_ph(s, "Input")
        except ValueError as e:
            print(f"[ERROR] {e} Coba lagi (atau ketik 'q' untuk keluar).")


def mode_interaktif(folder, tampil=True):
    print("Simulasi Pengendalian pH Hidroponik - Fuzzy Mamdani")
    print("Masukkan pH pada rentang 0-14. Ketik 'q' untuk keluar.\n")
    while True:
        try:
            a = baca_ph("pH sekarang   : ")
            if a is None:
                break
            b = baca_ph("pH sebelumnya : ")
            if b is None:
                break
            proses_dan_tampilkan(a, b, folder, tampil)
            jawab = input("Tampilkan decision surface 3D? (y/N): ").strip().lower()
            if jawab == "y":
                fig = plot_decision_surface(folder)
                print(f"Tersimpan: {folder / 'decision_surface.png'}")
                if tampil:
                    plt.show()
                plt.close(fig)
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except Exception as e:  # kegagalan tak terduga: lapor, jangan menjalankan koreksi
            print(f"[GAGAL INFERENSI] {e}. Tidak ada koreksi yang dihasilkan.")


def main():
    p = argparse.ArgumentParser(description="Fuzzy Mamdani - pengendalian pH hidroponik (simulasi)")
    p.add_argument("--sekarang", help="pH sekarang (mode non-interaktif)")
    p.add_argument("--sebelumnya", help="pH sebelumnya (mode non-interaktif)")
    p.add_argument("--demo", action="store_true", help="buat grafik MF, decision surface, dan tabel pengujian")
    p.add_argument("--no-show", action="store_true",
                   help="jangan tampilkan jendela grafik (hanya simpan PNG; untuk server/tanpa layar)")
    p.add_argument("--out", default=None,
                   help="folder keluaran (default: folder 'hasil' di samping file skrip ini, mis. Modul-2/hasil)")
    args = p.parse_args()

    tampil = not args.no_show
    # Default: folder "hasil" dibuat di lokasi file skrip ini (mis. Modul-2/hasil),
    # apa pun folder kerja (current directory) saat program dijalankan.
    folder = Path(args.out) if args.out else Path(__file__).resolve().parent / "hasil"
    folder.mkdir(parents=True, exist_ok=True)

    try:
        if args.demo:
            plot_fungsi_keanggotaan(folder)
            proses_dan_tampilkan(5.5, 5.7, folder, tampil=False)
            plot_decision_surface(folder)
            jalankan_pengujian()
            print(f"\nGambar tersimpan di: {folder.resolve()}")
            if tampil:
                plt.show()          # tampilkan semua grafik sekaligus
        elif args.sekarang is not None and args.sebelumnya is not None:
            proses_dan_tampilkan(args.sekarang, args.sebelumnya, folder, tampil)
        else:
            mode_interaktif(folder, tampil)
    except ValueError as e:
        print(f"[ERROR] {e}")
    except Exception as e:
        print(f"[GAGAL INFERENSI] {e}")


if __name__ == "__main__":
    main()