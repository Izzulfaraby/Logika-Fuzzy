"""
fuzzy_engine.py
Mesin inferensi fuzzy Mamdani untuk pengendalian kadar pH larutan hidroponik.

Metode  : Mamdani
Implikasi: MIN | Agregasi: MAX | Defuzzifikasi: Centroid

PENTING: sistem ini SIMULASI. Output koreksi adalah perintah simulasi
(-100 s.d. +100), BUKAN dosis bahan kimia dan bukan perintah pompa.

Modul ini murni logika (hanya NumPy) sehingga dapat diuji tanpa web server.
"""

import math

import numpy as np

# ============================================================
# 1. KONSTANTA DAN SEMESTA PEMBICARAAN
# ============================================================
PH_MIN, PH_MAX = 0.0, 14.0
DPH_MIN, DPH_MAX = -14.0, 14.0
OUT_MIN, OUT_MAX = -100.0, 100.0
N_OUT = 1001                      # resolusi diskretisasi output (langkah 0,2)

TARGET_MIN, TARGET_MAX = 5.8, 6.2  # ASUMSI desain (sayuran daun); sesuaikan
AMBANG_STABIL = 0.10               # |delta_ph| <= ambang -> tren STABIL (crisp)
EPS_LUAS = 1e-9                    # luas agregasi minimum agar centroid sah

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


PH_SETS = {
    "Rendah": (0.0, 0.0, 5.3, 5.8),
    "Sesuai": (5.3, 5.8, 6.2, 6.7),
    "Tinggi": (6.2, 6.7, 14.0, 14.0),
}
DPH_SETS = {
    "Turun":  (-14.0, -14.0, -0.3, 0.0),
    "Stabil": (-0.3, 0.0, 0.0, 0.3),
    "Naik":   (0.0, 0.3, 14.0, 14.0),
}
OUT_SETS = {
    "Turunkan Kuat":   (-100.0, -100.0, -90.0, -60.0),
    "Turunkan Sedang": (-90.0, -60.0, -60.0, -30.0),
    "Turunkan Ringan": (-60.0, -30.0, -30.0, 0.0),
    "Netral":          (-30.0, 0.0, 0.0, 30.0),
    "Naikkan Ringan":  (0.0, 30.0, 30.0, 60.0),
    "Naikkan Sedang":  (30.0, 60.0, 60.0, 90.0),
    "Naikkan Kuat":    (60.0, 90.0, 100.0, 100.0),
}
OUT_MF = {nama: trapmf(X_OUT, *p) for nama, p in OUT_SETS.items()}

# ============================================================
# 3. BASIS ATURAN 3 x 3 = 9 ATURAN
# ============================================================
# (id, label pH, label delta pH, label koreksi)
RULES = [
    ("R1", "Rendah", "Turun",  "Naikkan Kuat"),
    ("R2", "Rendah", "Stabil", "Naikkan Sedang"),
    ("R3", "Rendah", "Naik",   "Naikkan Ringan"),
    ("R4", "Sesuai", "Turun",  "Naikkan Ringan"),
    ("R5", "Sesuai", "Stabil", "Netral"),
    ("R6", "Sesuai", "Naik",   "Turunkan Ringan"),
    ("R7", "Tinggi", "Turun",  "Turunkan Ringan"),
    ("R8", "Tinggi", "Stabil", "Turunkan Sedang"),
    ("R9", "Tinggi", "Naik",   "Turunkan Kuat"),
]


# ============================================================
# 4. VALIDASI, DELTA pH, DAN KLASIFIKASI KONDISI AIR
# ============================================================
def validasi_ph(nilai, nama="pH"):
    """Ubah ke float dan pastikan 0 <= pH <= 14. Raise ValueError bila tidak valid.

    Menerima koma desimal ("6,2") dan menolak NaN, tak hingga, teks, dan None.
    """
    try:
        v = float(str(nilai).strip().replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError(f"{nama} harus berupa bilangan (contoh: 6.2).")
    if not math.isfinite(v):
        raise ValueError(f"{nama} tidak boleh NaN atau tak hingga.")
    if v < PH_MIN or v > PH_MAX:
        raise ValueError(f"{nama} = {v:g} di luar rentang {PH_MIN:g}-{PH_MAX:g}.")
    return v


def hitung_delta_ph(ph_sekarang, ph_sebelumnya):
    """delta_ph = ph_sekarang - ph_sebelumnya (rentang -14 s.d. +14).

    Dibulatkan 10 desimal hanya untuk membuang galat floating-point.
    """
    return round(ph_sekarang - ph_sebelumnya, 10)


def status_kimia(ph):
    """Status kimia berdasarkan nilai asli (tanpa pembulatan)."""
    if ph < 7.0:
        return "ASAM"
    if ph == 7.0:
        return "NETRAL"
    return "BASA"


def status_target(ph):
    """Status terhadap target hidroponik (batas inklusif)."""
    if ph < TARGET_MIN:
        return "TERLALU RENDAH"
    if ph <= TARGET_MAX:
        return "SESUAI TARGET"
    return "TERLALU TINGGI"


def tren_ph(delta):
    """Tren pH dengan ambang stabilitas AMBANG_STABIL."""
    if delta < -AMBANG_STABIL:
        return "MENURUN"
    if delta <= AMBANG_STABIL:
        return "STABIL"
    return "MENINGKAT"


# ============================================================
# 5. INFERENSI MAMDANI
# ============================================================
def fuzzifikasi(ph, delta):
    """Derajat keanggotaan crisp -> fuzzy untuk kedua input."""
    mu_ph = {k: float(trapmf(ph, *p)[0]) for k, p in PH_SETS.items()}
    mu_dph = {k: float(trapmf(delta, *p)[0]) for k, p in DPH_SETS.items()}
    return mu_ph, mu_dph


def defuzzifikasi_centroid(z, mu_agg):
    """Centroid diskret. Mengembalikan (nilai, status).

    Bila luas agregasi < EPS_LUAS, TIDAK membagi dengan nol: (None, "luas_nol").
    """
    luas = float(np.sum(mu_agg))
    if luas < EPS_LUAS:
        return None, "luas_nol"
    return float(np.sum(z * mu_agg) / luas), "ok"


def inferensi_inti(ph, delta):
    """Fuzzifikasi -> implikasi MIN -> agregasi MAX -> centroid."""
    mu_ph, mu_dph = fuzzifikasi(ph, delta)

    alpha = {}
    mu_agg = np.zeros_like(X_OUT)
    for rid, lbl_ph, lbl_dph, lbl_out in RULES:
        # Tahap 2a: kekuatan aktivasi aturan (MIN)
        a = min(mu_ph[lbl_ph], mu_dph[lbl_dph])
        alpha[rid] = a
        if a > 0.0:
            # Tahap 2b: implikasi MIN (pemotongan himpunan output)
            terpotong = np.minimum(a, OUT_MF[lbl_out])
            # Tahap 3: agregasi MAX
            mu_agg = np.maximum(mu_agg, terpotong)

    # Tahap 4: defuzzifikasi centroid
    z_star, status = defuzzifikasi_centroid(X_OUT, mu_agg)
    return {
        "mu_ph": mu_ph, "mu_dph": mu_dph,
        "alpha": alpha, "mu_agg": mu_agg,
        "koreksi": z_star, "status_defuzz": status,
    }


def interpretasi_keputusan(koreksi):
    """Ubah koreksi numerik menjadi (label, rekomendasi, tingkat).

    tingkat: 0 = netral, 1 = ringan, 2 = sedang, 3 = kuat.
    Ambang 15 / 45 / 75 adalah titik tengah antar puncak himpunan output.
    """
    besar = abs(koreksi)
    if besar < 15.0:
        return ("Netral", "Tidak perlu koreksi. Pertahankan dan pantau berkala.", 0)
    arah = "naikkan" if koreksi > 0 else "turunkan"
    if besar < 45.0:
        tingkat, nama = 1, "Ringan"
    elif besar < 75.0:
        tingkat, nama = 2, "Sedang"
    else:
        tingkat, nama = 3, "Kuat"
    label = f"{arah.capitalize()} {nama}"
    saran = {
        1: f"Koreksi {nama.lower()} untuk {arah} pH; ukur ulang setelah beberapa saat.",
        2: f"Koreksi {nama.lower()} untuk {arah} pH; pantau perubahan secara rutin.",
        3: f"Koreksi {nama.lower()} untuk {arah} pH; kondisi menjauhi target, segera tindak lanjuti.",
    }[tingkat]
    return (label, saran, tingkat)


def hitung_koreksi_ph(ph_sekarang, ph_sebelumnya):
    """Fungsi utama untuk antarmuka dan pengujian.

    Input boleh berupa angka atau teks. Raise ValueError untuk input tidak valid.
    Bila defuzzifikasi gagal (agregasi kosong), koreksi aman = 0 dan 'berhasil' = False.
    """
    ph = validasi_ph(ph_sekarang, "pH sekarang")
    ph0 = validasi_ph(ph_sebelumnya, "pH sebelumnya")
    delta = hitung_delta_ph(ph, ph0)

    h = inferensi_inti(ph, delta)
    berhasil = h["status_defuzz"] == "ok"
    koreksi = round(h["koreksi"], 2) if berhasil else 0.0
    label, saran, tingkat = interpretasi_keputusan(koreksi)
    if not berhasil:
        label, saran, tingkat = ("Netral", "Inferensi gagal (agregasi kosong); koreksi aman = 0.", 0)

    aktif = {rid: a for rid, a in h["alpha"].items() if a > 0.0}
    return {
        "ph_sekarang": ph, "ph_sebelumnya": ph0, "delta_ph": delta,
        "status_kimia": status_kimia(ph),
        "status_target": status_target(ph),
        "tren": tren_ph(delta),
        "mu_ph": h["mu_ph"], "mu_dph": h["mu_dph"],
        "alpha": h["alpha"], "aturan_aktif": aktif,
        "mu_agg": h["mu_agg"],
        "koreksi": koreksi, "berhasil": berhasil,
        "label": label, "rekomendasi": saran, "tingkat": tingkat,
    }


def hitung_permukaan_keputusan(n_ph=57, n_dph=41, dph_lim=1.5):
    """Grid koreksi untuk decision surface. dph_lim memperbesar sumbu delta pH
    agar bentuk permukaan terbaca (semesta model tetap -14 s.d. +14)."""
    ph_grid = np.linspace(PH_MIN, PH_MAX, n_ph)
    dph_grid = np.linspace(-dph_lim, dph_lim, n_dph)
    z = np.zeros((n_dph, n_ph))
    for i, d in enumerate(dph_grid):
        for j, p in enumerate(ph_grid):
            r = inferensi_inti(float(p), float(d))
            z[i, j] = r["koreksi"] if r["status_defuzz"] == "ok" else 0.0
    return ph_grid, dph_grid, z


# ============================================================
# 6. PEMBANDING: ATURAN TEGAS (CRISP / BOOLEAN)
# ============================================================
# Puncak himpunan output dipakai sebagai nilai tegas tiap label.
NILAI_TEGAS = {
    "Turunkan Kuat": -90.0, "Turunkan Sedang": -60.0, "Turunkan Ringan": -30.0,
    "Netral": 0.0,
    "Naikkan Ringan": 30.0, "Naikkan Sedang": 60.0, "Naikkan Kuat": 90.0,
}


def koreksi_aturan_tegas(ph, delta):
    """Keputusan pembanding: matriks 9 aturan yang SAMA, tetapi dengan batas tegas
    (Boolean) pada pH dan tren, tanpa derajat keanggotaan. Dipakai sebagai
    referensi pada evaluasi dataset (lihat laporan untuk batasannya)."""
    st = status_target(ph)
    kolom_ph = {"TERLALU RENDAH": "Rendah", "SESUAI TARGET": "Sesuai", "TERLALU TINGGI": "Tinggi"}[st]
    kolom_dph = {"MENURUN": "Turun", "STABIL": "Stabil", "MENINGKAT": "Naik"}[tren_ph(delta)]
    for _, lp, ld, lo in RULES:
        if lp == kolom_ph and ld == kolom_dph:
            return NILAI_TEGAS[lo]
    raise RuntimeError("Basis aturan tidak lengkap")
