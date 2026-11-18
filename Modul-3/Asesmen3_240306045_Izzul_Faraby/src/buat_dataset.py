"""
buat_dataset.py
Membangun data/test_cases.csv (22 skenario uji).

Kolom koreksi_referensi dihitung dari pembanding ATURAN TEGAS (Boolean) pada
fuzzy_engine.koreksi_aturan_tegas. Ini BUKAN data pakar sungguhan. Bila Anda
memiliki penilaian pakar/operator, ganti kolom tersebut dengan nilai pakar.
"""
import csv
from pathlib import Path

import fuzzy_engine as fe

SKENARIO = [
    ("Rendah dan terus menurun", 4.8, 5.1),
    ("Rendah tetapi meningkat", 4.8, 4.5),
    ("Sesuai target dan stabil", 6.0, 6.0),
    ("Tinggi dan terus meningkat", 7.5, 7.2),
    ("Tinggi tetapi menurun", 7.5, 7.8),
    ("Transisi rendah-sesuai (contoh manual)", 5.5, 5.7),
    ("Batas bawah target", 5.8, 5.8),
    ("Batas atas target", 6.2, 6.2),
    ("pH netral 7,0 stabil", 7.0, 7.0),
    ("Batas bawah semesta", 0.0, 0.0),
    ("Batas atas semesta", 14.0, 14.0),
    ("Rendah dan stabil", 5.0, 5.0),
    ("Sesuai target tetapi naik", 6.0, 5.7),
    ("Sesuai target tetapi turun", 6.0, 6.3),
    ("Tinggi dan stabil", 6.8, 6.8),
    ("Transisi sesuai-tinggi, naik pelan", 6.5, 6.4),
    ("Transisi rendah-sesuai, stabil", 5.6, 5.6),
    ("Sesuai target, perubahan sangat kecil", 6.1, 6.05),
    ("Sangat tinggi dan menurun", 9.0, 9.5),
    ("Sangat rendah, perubahan tepat -0,1", 3.5, 3.6),
    ("Transisi sesuai-tinggi, naik cepat", 6.4, 6.0),
    ("Rendah dan naik sedang", 5.2, 5.0),
]


def main():
    out = Path(__file__).resolve().parent.parent / "data" / "test_cases.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "skenario", "ph_sekarang", "ph_sebelumnya", "koreksi_referensi"])
        for i, (nama, ph, ph0) in enumerate(SKENARIO, start=1):
            delta = fe.hitung_delta_ph(ph, ph0)
            w.writerow([i, nama, ph, ph0, fe.koreksi_aturan_tegas(ph, delta)])
    print(f"Tersimpan: {out} ({len(SKENARIO)} baris)")


if __name__ == "__main__":
    main()
