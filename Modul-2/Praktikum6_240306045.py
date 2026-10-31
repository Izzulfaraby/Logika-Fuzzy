"""
Praktikum 6 - Fuzzy Rule dan Knowledge Base
Studi kasus: Sistem Pengendalian pH Air Hidroponik (parameter mengikuti file asesmen
Praktikum_Fuzzy_pH_Hidroponik.md; target pH 5,8-6,2 adalah ASUMSI desain).

Isi:
  1. Knowledge Base: fungsi keanggotaan (database) + 9 aturan IF-THEN (rule base)
  2. Kelas FuzzyRule + perhitungan firing strength (alpha)
  3. Uji kelengkapan & konsistensi basis aturan
  4. Pengujian skenario + demo untuk pertanyaan analisis (rule tidak aktif, urutan aturan)
Output: tabel di terminal (tanpa file gambar)
Jalankan: python Praktikum6_NIM.py
"""
import itertools
import random
import numpy as np


# ==========================================================
# 1. DATABASE: FUNGSI KEANGGOTAAN (trapesium a,b,c,d; segitiga b==c)
# ==========================================================
def trapmf(x, a, b, c, d):
    x = float(x)
    if x <= a or x >= d:
        # bahu: nilai di tepi yang berimpit dengan plateau tetap 1
        if (x == a == b) or (x == c == d):
            return 1.0
        return 0.0
    if x < b:
        return (x - a) / (b - a)
    if x <= c:
        return 1.0
    return (d - x) / (d - c)


PH_SETS = {"Rendah": (0.0, 0.0, 5.3, 5.8),
           "Sesuai": (5.3, 5.8, 6.2, 6.7),
           "Tinggi": (6.2, 6.7, 14.0, 14.0)}
DPH_SETS = {"Turun": (-14.0, -14.0, -0.3, 0.0),
            "Stabil": (-0.3, 0.0, 0.0, 0.3),
            "Naik": (0.0, 0.3, 14.0, 14.0)}
OUT_LABELS = ["Turunkan Kuat", "Turunkan Sedang", "Turunkan Ringan", "Netral",
              "Naikkan Ringan", "Naikkan Sedang", "Naikkan Kuat"]


def fuzzifikasi(ph, delta):
    """crisp -> derajat keanggotaan (format dict bersarang seperti di modul)."""
    return {"ph": {k: trapmf(ph, *p) for k, p in PH_SETS.items()},
            "dph": {k: trapmf(delta, *p) for k, p in DPH_SETS.items()}}


# ==========================================================
# 2. KELAS ATURAN FUZZY
# ==========================================================
class FuzzyRule:
    def __init__(self, rule_id, antecedent, consequent, operator="AND"):
        self.rule_id = rule_id
        self.antecedent = antecedent      # {'ph': 'Rendah', 'dph': 'Turun'}
        self.consequent = consequent      # {'koreksi': 'Naikkan Kuat'}
        self.operator = operator.upper()

    def hitung_firing_strength(self, derajat, metode_and="min"):
        nilai = [derajat[v].get(l, 0.0) for v, l in self.antecedent.items()]
        if not nilai:
            return 0.0
        if self.operator == "AND":
            return min(nilai) if metode_and == "min" else float(np.prod(nilai))
        if self.operator == "OR":
            return max(nilai)
        raise ValueError(f"Operator {self.operator} tidak dikenali.")

    def __str__(self):
        syarat = f" {self.operator} ".join(f"{v} is {l}" for v, l in self.antecedent.items())
        hasil = ", ".join(f"{v} is {l}" for v, l in self.consequent.items())
        return f"[{self.rule_id}] IF {syarat} THEN {hasil}"


# ==========================================================
# 3. RULE BASE 3 x 3 = 9 ATURAN (identik dengan matriks asesmen)
# ==========================================================
#   pH \ dpH  |      Turun        |      Stabil        |      Naik
#   Rendah    | R1 Naikkan Kuat   | R2 Naikkan Sedang  | R3 Naikkan Ringan
#   Sesuai    | R4 Naikkan Ringan | R5 Netral          | R6 Turunkan Ringan
#   Tinggi    | R7 Turunkan Ringan| R8 Turunkan Sedang | R9 Turunkan Kuat
MATRIKS = {
    ("Rendah", "Turun"): "Naikkan Kuat",    ("Rendah", "Stabil"): "Naikkan Sedang",
    ("Rendah", "Naik"): "Naikkan Ringan",
    ("Sesuai", "Turun"): "Naikkan Ringan",  ("Sesuai", "Stabil"): "Netral",
    ("Sesuai", "Naik"): "Turunkan Ringan",
    ("Tinggi", "Turun"): "Turunkan Ringan", ("Tinggi", "Stabil"): "Turunkan Sedang",
    ("Tinggi", "Naik"): "Turunkan Kuat",
}
rule_base = [
    FuzzyRule(f"R{i}", {"ph": p, "dph": d}, {"koreksi": out})
    for i, ((p, d), out) in enumerate(MATRIKS.items(), start=1)
]


# ==========================================================
# 4. EVALUASI ATURAN
# ==========================================================
def evaluasi(rules, derajat, metode_and="min"):
    """Kembalikan list (rule_id, label_output, alpha) untuk semua aturan (alpha bisa 0)."""
    return [(r.rule_id, r.consequent["koreksi"], r.hitung_firing_strength(derajat, metode_and))
            for r in rules]


def evaluasi_ringkas(ph, prev, rules=rule_base):
    """Kembalikan (delta, derajat, hasil_semua_aturan, aturan_aktif)."""
    delta = round(ph - prev, 10)
    der = fuzzifikasi(ph, delta)
    hasil = evaluasi(rules, der)
    aktif = [(i, o, a) for i, o, a in hasil if a > 0]
    return delta, der, hasil, aktif


def tabel_detail(judul, ph, prev, rules=rule_base):
    """Tabel fuzzifikasi + tabel evaluasi 9 aturan untuk satu kasus."""
    delta, der, hasil, aktif = evaluasi_ringkas(ph, prev, rules)
    print("\n" + "=" * 78)
    print(f"{judul}: pH sekarang = {ph} | pH sebelumnya = {prev} | dpH = {delta:+.2f}")
    fz = [["pH sekarang", l, f"{v:.3f}"] for l, v in der["ph"].items()] + \
         [["Perubahan pH", l, f"{v:.3f}"] for l, v in der["dph"].items()]
    tampilkan_tabel(f"Fuzzifikasi - {judul}", ["Variabel", "Label", "Derajat (mu)"], fz)
    baris = [[r.rule_id, r.antecedent["ph"], r.antecedent["dph"], lo, f"{a:.3f}",
              "AKTIF" if a > 0 else "-"] for r, (_, lo, a) in zip(rules, hasil)]
    tampilkan_tabel(f"Evaluasi aturan - {judul}",
                    ["Aturan", "IF pH", "AND dpH", "THEN koreksi", "alpha", "Status"], baris)
    if not aktif:
        print("[PERINGATAN] Tidak ada aturan yang tercetus (semua alpha = 0).")
    return aktif


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
    # --- 1. Knowledge base ---
    header_m = ["pH \\ dpH"] + list(DPH_SETS)
    baris_m = [[p] + [MATRIKS[(p, d)] for d in DPH_SETS] for p in PH_SETS]
    tampilkan_tabel("1. MATRIKS BASIS ATURAN (baris: pH, kolom: perubahan pH)", header_m, baris_m)
    baris_r = [[r.rule_id, r.antecedent["ph"], r.antecedent["dph"], r.consequent["koreksi"]] for r in rule_base]
    tampilkan_tabel("2. DAFTAR 9 ATURAN IF-THEN", ["Aturan", "IF pH", "AND dpH", "THEN koreksi"], baris_r)

    # --- 2. Kelengkapan & konsistensi ---
    kombinasi = set(itertools.product(PH_SETS, DPH_SETS))
    terdef = [(r.antecedent["ph"], r.antecedent["dph"]) for r in rule_base]
    konflik = {}
    for r in rule_base:
        konflik.setdefault((r.antecedent["ph"], r.antecedent["dph"]), set()).add(r.consequent["koreksi"])
    ada_konflik = [k for k, v in konflik.items() if len(v) > 1]
    tak_dikenal = {r.consequent["koreksi"] for r in rule_base} - set(OUT_LABELS)
    baris_k = [
        ["Kombinasi seharusnya (3 x 3)", len(kombinasi), "-"],
        ["Kombinasi tercakup aturan", len(set(terdef)), "LENGKAP" if kombinasi == set(terdef) else "TIDAK LENGKAP"],
        ["IF sama tetapi THEN beda", len(ada_konflik), "KONSISTEN" if not ada_konflik else "ADA KONFLIK"],
        ["Label THEN belum didefinisikan", len(tak_dikenal), "OK" if not tak_dikenal else "PERIKSA"],
    ]
    tampilkan_tabel("3. UJI KELENGKAPAN DAN KONSISTENSI", ["Pemeriksaan", "Jumlah", "Hasil"], baris_k)

    # --- 3. Contoh manual (detail) ---
    tabel_detail("CONTOH MANUAL ASESMEN", 5.5, 5.7)

    # --- 4. Ringkasan skenario ---
    skenario = [("A rendah & menurun", 4.8, 5.1), ("B sesuai & stabil", 6.0, 6.0),
                ("C tinggi & meningkat", 7.5, 7.2), ("D zona transisi", 6.4, 6.3),
                ("E rendah, dpH kecil", 5.2, 5.3), ("Contoh manual", 5.5, 5.7)]
    baris_s = []
    for nama, a, b in skenario:
        delta, _, _, aktif = evaluasi_ringkas(a, b)
        baris_s.append([nama, f"{a:.2f}", f"{b:.2f}", f"{delta:+.2f}",
                        ", ".join(f"{i}({al:.3f})" for i, _, al in aktif)])
    tampilkan_tabel("4. RINGKASAN SKENARIO PENGUJIAN (aturan tercetus dan alpha)",
                    ["Skenario", "pH", "Sebelumnya", "dpH", "Aturan aktif (alpha)"], baris_s)

    # --- 5. Demo pertanyaan analisis ---
    delta, _, _, aktif = evaluasi_ringkas(7.5, 7.2, rule_base[:3])
    tampilkan_tabel("5. DEMO ANALISIS 1: rule base TIDAK lengkap (hanya R1-R3), input pH 7,5 / 7,2",
                    ["Aturan dipakai", "Aturan tercetus", "Kesimpulan"],
                    [["R1, R2, R3", len(aktif), "TIDAK ADA aturan tercetus -> perlu fallback"
                      if not aktif else "ada aturan tercetus"]])

    a1, a2 = 0.3, 0.5
    tampilkan_tabel("6. DEMO ANALISIS 2: dua aturan konklusi sama digabung dengan MAX",
                    ["alpha aturan 1", "alpha aturan 2", "alpha gabungan = max(...)"],
                    [[a1, a2, max(a1, a2)]])

    der = fuzzifikasi(5.5, round(5.5 - 5.7, 10))
    asli = {i: round(a, 6) for i, _, a in evaluasi(rule_base, der)}
    acak = rule_base[:]
    random.Random(1).shuffle(acak)
    hasil_acak = {i: round(a, 6) for i, _, a in evaluasi(acak, der)}
    tampilkan_tabel("7. DEMO ANALISIS 3: urutan aturan tidak memengaruhi hasil",
                    ["Urutan aturan", "Hasil alpha sama dengan urutan asli?"],
                    [["R1..R9 (asli)", "-"], [" ".join(r.rule_id for r in acak), "YA" if asli == hasil_acak else "TIDAK"]])