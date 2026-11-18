"""
test_blackbox.py  (Praktikum 14)
Pengujian black-box fuzzy_engine: Equivalence Partitioning dan Boundary Value Analysis.

Kolom "diharapkan" dan predikat 'cek' ditetapkan dari matriks aturan SEBELUM
program dijalankan. Kolom "aktual" dan status PASS/FAIL diisi dari eksekusi nyata.

Penggunaan:
    python tests/test_blackbox.py      -> cetak tabel dan simpan ke hasil/
    pytest tests/test_blackbox.py      -> bila pytest terpasang
"""

import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import fuzzy_engine as fe  # noqa: E402


def _z(a, b):
    return fe.hitung_koreksi_ph(a, b)["koreksi"]


# (id, skenario, input pH sekarang, input pH sebelumnya, diharapkan, predikat)
KASUS = [
    ("TC-01", "Batas bawah semesta", 0.0, 0.0,
     "Naikkan Sedang (+45 s.d. +75)", lambda r: 45 <= r["koreksi"] < 75),
    ("TC-02", "Batas atas semesta", 14.0, 14.0,
     "Turunkan Sedang (-75 s.d. -45)", lambda r: -75 < r["koreksi"] <= -45),
    ("TC-03", "Nilai tengah target, stabil", 6.0, 6.0,
     "Netral (koreksi antara -15 dan +15)", lambda r: abs(r["koreksi"]) < 15),
    ("TC-04", "Rendah dan menurun", 4.8, 5.1,
     "Naikkan Kuat (>= +75)", lambda r: r["koreksi"] >= 75),
    ("TC-05", "Tinggi dan meningkat", 7.5, 7.2,
     "Turunkan Kuat (<= -75)", lambda r: r["koreksi"] <= -75),
    ("TC-06", "Rendah tetapi sudah naik", 4.8, 4.5,
     "Naikkan Ringan (+15 s.d. +45), lebih kecil dari TC-04",
     lambda r: 15 <= r["koreksi"] < 45 and r["koreksi"] < _z(4.8, 5.1)),
    ("TC-07", "Tinggi tetapi sudah turun", 7.5, 7.8,
     "Turunkan Ringan (-45 s.d. -15), lebih kecil dari TC-05",
     lambda r: -45 < r["koreksi"] <= -15 and abs(r["koreksi"]) < abs(_z(7.5, 7.2))),
    ("TC-08", "BVA: tepat di batas bawah target", 5.8, 5.8,
     "Netral (koreksi antara -15 dan +15)", lambda r: abs(r["koreksi"]) < 15),
    ("TC-09", "BVA: tepat di bawah batas target", 5.79, 5.79,
     "Hampir netral (kontinu, koreksi antara -15 dan +15)", lambda r: abs(r["koreksi"]) < 15),
    ("TC-10", "BVA: tepat di atas batas target", 6.21, 6.21,
     "Hampir netral (kontinu, koreksi antara -15 dan +15)", lambda r: abs(r["koreksi"]) < 15),
    ("TC-11", "Input negatif (di luar semesta)", -0.1, 6.0,
     "Ditolak dengan pesan error", "ditolak"),
    ("TC-12", "Input melebihi batas atas", 14.1, 6.0,
     "Ditolak dengan pesan error", "ditolak"),
    ("TC-13", "Input teks bukan angka", "abc", 6.0,
     "Ditolak dengan pesan error", "ditolak"),
    ("TC-14", "Input NaN", "nan", 6.0,
     "Ditolak dengan pesan error", "ditolak"),
    ("TC-15", "Input kosong", "", 6.0,
     "Ditolak dengan pesan error", "ditolak"),
    ("TC-16", "Koma desimal diterima", "6,2", "6,0",
     "Diterima; delta pH = +0,2", lambda r: abs(r["delta_ph"] - 0.2) < 1e-9),
    ("TC-17", "Simetri terhadap target 6,0", 4.8, 5.1,
     "koreksi(4,8; 5,1) = -koreksi(7,2; 6,9)",
     lambda r: abs(r["koreksi"] + _z(7.2, 6.9)) < 1e-6),
    ("TC-18", "Delta ekstrem +14", 14.0, 0.0,
     "Turunkan Kuat (<= -75)", lambda r: r["koreksi"] <= -75),
    ("TC-19", "Batas stabilitas tren (delta = -0,10)", 3.5, 3.6,
     "Diterima; tren STABIL, koreksi positif", lambda r: r["tren"] == "STABIL" and r["koreksi"] > 0),
    ("TC-20", "Waktu respon inferensi", 6.0, 5.7,
     "Selesai < 1 detik (NFR)", "waktu"),
]


def jalankan_kasus(kasus):
    kid, skenario, a, b, diharapkan, cek = kasus
    inp = f"{a} / {b}"
    if cek == "ditolak":
        try:
            fe.hitung_koreksi_ph(a, b)
            return kid, skenario, inp, diharapkan, "Tidak ditolak", False
        except ValueError as e:
            return kid, skenario, inp, diharapkan, f"Ditolak: {e}", True
    if cek == "waktu":
        t0 = time.perf_counter()
        r = fe.hitung_koreksi_ph(a, b)
        dt = time.perf_counter() - t0
        return kid, skenario, inp, diharapkan, f"{dt * 1000:.2f} ms (koreksi {r['koreksi']})", dt < 1.0
    r = fe.hitung_koreksi_ph(a, b)
    aktual = f"Koreksi {r['koreksi']:+.2f} ({r['label']}); {r['status_target']}; {r['tren']}"
    return kid, skenario, inp, diharapkan, aktual, bool(cek(r))


def jalankan_semua():
    return [jalankan_kasus(k) for k in KASUS]


def test_semua_kasus_lulus():
    gagal = [h for h in jalankan_semua() if not h[5]]
    assert not gagal, f"Kasus gagal: {gagal}"


def main():
    hasil = jalankan_semua()
    folder = ROOT / "hasil"
    folder.mkdir(exist_ok=True)
    with open(folder / "hasil_blackbox.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Skenario", "Input (pH sekarang / sebelumnya)",
                    "Output diharapkan", "Output aktual", "Status"])
        for h in hasil:
            w.writerow([*h[:5], "PASS" if h[5] else "FAIL"])
    baris = ["| ID | Skenario | Input (pH sekarang / sebelumnya) | Output diharapkan | Output aktual | Status |",
             "|:--:|---|:---:|---|---|:---:|"]
    for h in hasil:
        baris.append(f"| {h[0]} | {h[1]} | {h[2]} | {h[3]} | {h[4]} | **{'PASS' if h[5] else 'FAIL'}** |")
    (folder / "hasil_blackbox.md").write_text("\n".join(baris) + "\n", encoding="utf-8")
    print("\n".join(baris))
    lulus = sum(1 for h in hasil if h[5])
    print(f"\nRingkasan: {lulus}/{len(hasil)} kasus PASS")
    return 0 if lulus == len(hasil) else 1


if __name__ == "__main__":
    sys.exit(main())
