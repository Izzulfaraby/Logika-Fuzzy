"""
evaluasi_data.py  (Praktikum 12)
Evaluasi batch sistem fuzzy Mamdani terhadap data/test_cases.csv:
preprocessing, inferensi batch, MAE, RMSE, waktu komputasi, 2 kasus error
terbesar, grafik referensi vs prediksi, dan analisis sensitivitas.

Penggunaan:
    python src/evaluasi_data.py [jalur_csv]
"""

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

import fuzzy_engine as fe
import visualisasi as vz

ROOT = Path(__file__).resolve().parent.parent
KOLOM_WAJIB = ["id", "ph_sekarang", "ph_sebelumnya", "koreksi_referensi"]


def muat_dan_bersihkan(jalur):
    """Baca CSV, buang baris bernilai hilang, dan buang baris di luar semesta pH.

    Mengembalikan (df_bersih, catatan) agar jumlah baris yang dibuang terdokumentasi.
    """
    df = pd.read_csv(jalur)
    kurang = [k for k in KOLOM_WAJIB if k not in df.columns]
    if kurang:
        raise ValueError(f"Kolom wajib tidak ada pada CSV: {kurang}")
    catatan = []
    n0 = len(df)
    df = df.dropna(subset=KOLOM_WAJIB)
    if len(df) < n0:
        catatan.append(f"{n0 - len(df)} baris dibuang karena nilai hilang")
    n1 = len(df)
    valid = df["ph_sekarang"].between(fe.PH_MIN, fe.PH_MAX) & \
        df["ph_sebelumnya"].between(fe.PH_MIN, fe.PH_MAX)
    df = df[valid].copy()
    if len(df) < n1:
        catatan.append(f"{n1 - len(df)} baris dibuang karena pH di luar 0-14")
    return df.reset_index(drop=True), catatan


def jalankan_batch(df):
    """Inferensi untuk setiap baris; kembalikan df dengan kolom prediksi dan error,
    serta waktu rata-rata per inferensi (ms)."""
    prediksi, aturan = [], []
    t0 = time.perf_counter()
    for _, r in df.iterrows():
        h = fe.hitung_koreksi_ph(r["ph_sekarang"], r["ph_sebelumnya"])
        prediksi.append(h["koreksi"])
        aturan.append("+".join(h["aturan_aktif"]))
    ms = (time.perf_counter() - t0) / max(len(df), 1) * 1000.0

    out = df.copy()
    out["delta_ph"] = (out["ph_sekarang"] - out["ph_sebelumnya"]).round(10)
    out["prediksi_fuzzy"] = prediksi
    out["aturan_aktif"] = aturan
    out["error_absolut"] = (out["koreksi_referensi"] - out["prediksi_fuzzy"]).abs()
    out["error_kuadrat"] = (out["koreksi_referensi"] - out["prediksi_fuzzy"]) ** 2
    return out, ms


def hitung_metrik(df):
    mae = float(df["error_absolut"].mean())
    rmse = float(np.sqrt(df["error_kuadrat"].mean()))
    bias = float((df["prediksi_fuzzy"] - df["koreksi_referensi"]).mean())
    return {"N": len(df), "MAE": mae, "RMSE": rmse, "bias": bias,
            "arah_sama": float((np.sign(df["prediksi_fuzzy"].round(0)) ==
                                np.sign(df["koreksi_referensi"])).mean())}


def main(jalur_csv=None):
    jalur_csv = Path(jalur_csv) if jalur_csv else ROOT / "data" / "test_cases.csv"
    df, catatan = muat_dan_bersihkan(jalur_csv)
    hasil, ms = jalankan_batch(df)
    m = hitung_metrik(hasil)

    print("=" * 70)
    print("EVALUASI SISTEM FUZZY MAMDANI - PENGENDALIAN pH HIDROPONIK")
    print("=" * 70)
    for c in catatan:
        print("Preprocessing:", c)
    print(f"Total sampel uji (N)        : {m['N']}")
    print(f"Mean Absolute Error (MAE)   : {m['MAE']:.3f} poin")
    print(f"Root Mean Squared Error     : {m['RMSE']:.3f} poin")
    print(f"Bias rata-rata (fuzzy - ref): {m['bias']:+.3f} poin")
    print(f"Kesesuaian arah koreksi     : {m['arah_sama'] * 100:.1f}%")
    print(f"Waktu rata-rata per inferensi: {ms:.3f} ms")

    top2 = hasil.sort_values("error_absolut", ascending=False).head(2)
    print("\nDUA KASUS ERROR TERBESAR:")
    print(top2[["id", "skenario", "ph_sekarang", "ph_sebelumnya", "delta_ph",
                "koreksi_referensi", "prediksi_fuzzy", "aturan_aktif",
                "error_absolut"]].to_string(index=False))

    folder = ROOT / "hasil"
    folder.mkdir(exist_ok=True)
    hasil.to_csv(folder / "hasil_evaluasi.csv", index=False)
    vz.simpan(vz.fig_aktual_vs_prediksi(hasil, m["MAE"]),
              "evaluasi_prediksi_vs_aktual.png", folder)
    vz.simpan(vz.fig_sensitivitas(), "analisis_sensitivitas.png", folder)
    print(f"\nTersimpan di: {folder}")
    return hasil, m, ms


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
