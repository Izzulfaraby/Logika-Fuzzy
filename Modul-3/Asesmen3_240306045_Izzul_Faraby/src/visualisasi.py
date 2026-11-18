"""
visualisasi.py
Fungsi pembuat grafik Matplotlib. Setiap fungsi mengembalikan objek Figure
sehingga dapat dirender di Streamlit (st.pyplot) maupun disimpan sebagai PNG.

Menjalankan modul ini langsung membuat semua gambar statis ke folder hasil/:
    python src/visualisasi.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (proyeksi 3D)

import fuzzy_engine as fe

WARNA = {
    "Rendah": "#d62728", "Sesuai": "#2ca02c", "Tinggi": "#1f77b4",
    "Turun": "#d62728", "Stabil": "#2ca02c", "Naik": "#1f77b4",
}
WARNA_OUT = ["#8c1c13", "#d62728", "#ff9896", "#7f7f7f", "#aec7e8", "#1f77b4", "#08306b"]


def _plot_mf(ax, x, sets, judul, xlabel, titik=None, warna=None):
    for i, (nama, p) in enumerate(sets.items()):
        c = (warna or WARNA).get(nama) if isinstance(warna, dict) or warna is None else warna[i]
        ax.plot(x, fe.trapmf(x, *p), linewidth=2, label=nama, color=c)
    if titik is not None:
        ax.axvline(titik, color="black", linestyle="--", linewidth=1.2, label=f"Input = {titik:g}")
    ax.set_title(judul, fontsize=11, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Derajat keanggotaan (μ)")
    ax.set_ylim(-0.03, 1.08)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(fontsize=8, loc="center right")


def fig_mf_ph(ph=None):
    fig, ax = plt.subplots(figsize=(6, 3.4))
    _plot_mf(ax, np.linspace(0, 14, 1401), fe.PH_SETS,
             "Fungsi keanggotaan pH sekarang", "pH", ph)
    fig.tight_layout()
    return fig


def fig_mf_delta(delta=None, lim=1.5):
    """Sumbu diperbesar (-lim s.d. +lim) agar bentuk himpunan terbaca;
    semesta model tetap -14 s.d. +14."""
    fig, ax = plt.subplots(figsize=(6, 3.4))
    _plot_mf(ax, np.linspace(-lim, lim, 1501), fe.DPH_SETS,
             f"Fungsi keanggotaan ΔpH (sumbu diperbesar ±{lim:g})", "ΔpH", delta)
    fig.tight_layout()
    return fig


def fig_mf_koreksi(koreksi=None):
    fig, ax = plt.subplots(figsize=(7, 3.4))
    _plot_mf(ax, fe.X_OUT, fe.OUT_SETS, "Fungsi keanggotaan koreksi (output)",
             "Koreksi (satuan simulasi)", koreksi, warna=WARNA_OUT)
    ax.legend(fontsize=7, ncol=2, loc="upper center")
    fig.tight_layout()
    return fig


def fig_agregasi(hasil):
    """Kurva agregasi MAX dari inferensi aktual beserta garis centroid."""
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for (nama, mf), c in zip(fe.OUT_MF.items(), WARNA_OUT):
        ax.plot(fe.X_OUT, mf, color=c, linewidth=0.9, alpha=0.5, label=nama)
    ax.fill_between(fe.X_OUT, hasil["mu_agg"], color="#ffbb78", alpha=0.7,
                    label="Hasil agregasi (MAX)")
    ax.plot(fe.X_OUT, hasil["mu_agg"], color="#ff7f0e", linewidth=2)
    if hasil["berhasil"]:
        ax.axvline(hasil["koreksi"], color="black", linestyle="--", linewidth=1.5,
                   label=f"Centroid = {hasil['koreksi']:.2f}")
    ax.set_title(f"Agregasi Mamdani (pH {hasil['ph_sekarang']:g}, "
                 f"ΔpH {hasil['delta_ph']:+.2f})", fontsize=11, fontweight="bold")
    ax.set_xlabel("Koreksi (satuan simulasi)")
    ax.set_ylabel("μ")
    ax.set_ylim(-0.03, 1.1)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(fontsize=7, ncol=3, loc="upper center")
    fig.tight_layout()
    return fig


def fig_firing(hasil):
    """Kekuatan aktivasi (α) sembilan aturan."""
    ids = [r[0] for r in fe.RULES]
    nama = [f"{r[0]}: {r[1]}-{r[2]}" for r in fe.RULES]
    nilai = [hasil["alpha"][i] for i in ids]
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.barh(nama[::-1], nilai[::-1], color="#1f77b4")
    for b, v in zip(bars, nilai[::-1]):
        if v > 0:
            ax.text(v + 0.01, b.get_y() + b.get_height() / 2, f"{v:.3f}",
                    va="center", fontsize=8)
    ax.set_xlim(0, 1.15)
    ax.set_xlabel("Firing strength (α)")
    ax.set_title("Tingkat aktivasi aturan", fontsize=11, fontweight="bold")
    fig.tight_layout()
    return fig


def fig_peta_keputusan(ph=None, delta=None, data=None):
    """Peta kontur 2D decision surface, dengan penanda input saat ini."""
    ph_g, d_g, z = data if data is not None else fe.hitung_permukaan_keputusan()
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    cs = ax.contourf(ph_g, d_g, z, levels=np.linspace(-100, 100, 21), cmap="coolwarm_r")
    fig.colorbar(cs, ax=ax, label="Koreksi (+ naikkan pH, − turunkan pH)")
    if ph is not None and delta is not None:
        ax.plot(ph, np.clip(delta, d_g.min(), d_g.max()), "k*", markersize=14,
                markeredgecolor="white", label="Input saat ini")
        ax.legend(loc="upper right", fontsize=8)
    ax.set_xlabel("pH sekarang")
    ax.set_ylabel("ΔpH")
    ax.set_title("Peta keputusan (decision map)", fontsize=11, fontweight="bold")
    fig.tight_layout()
    return fig


def fig_surface3d(data=None):
    ph_g, d_g, z = data if data is not None else fe.hitung_permukaan_keputusan()
    X, Y = np.meshgrid(ph_g, d_g)
    fig = plt.figure(figsize=(8, 5.5))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, z, cmap="coolwarm_r", edgecolor="none", alpha=0.95)
    fig.colorbar(surf, ax=ax, shrink=0.6, pad=0.1, label="Koreksi")
    ax.set_xlabel("pH sekarang")
    ax.set_ylabel("ΔpH")
    ax.set_zlabel("Koreksi (simulasi)")
    ax.set_title("Decision surface 3D (sumbu ΔpH ±1,5)", fontsize=11, fontweight="bold")
    ax.view_init(elev=28, azim=-125)
    fig.tight_layout()
    return fig


def fig_aktual_vs_prediksi(df, mae):
    fig, ax = plt.subplots(figsize=(10, 5.2))
    x = df["id"].to_numpy()
    ax.plot(x, df["koreksi_referensi"], "ro-", label="Referensi (aturan tegas)", linewidth=2)
    ax.plot(x, df["prediksi_fuzzy"], "bs--", label="Output fuzzy Mamdani", linewidth=2)
    ax.set_title(f"Evaluasi: referensi vs prediksi fuzzy (MAE = {mae:.2f})",
                 fontsize=12, fontweight="bold")
    ax.set_xlabel("Nomor kasus uji")
    ax.set_ylabel("Koreksi (satuan simulasi)")
    ax.set_xticks(x)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    return fig


def fig_sensitivitas():
    """Variasikan satu input sambil menahan input lain tetap."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
    ph_x = np.linspace(0, 14, 281)
    for d, gaya in [(-0.3, "--"), (0.0, "-"), (0.3, ":")]:
        y = [fe.inferensi_inti(float(p), d)["koreksi"] for p in ph_x]
        a1.plot(ph_x, y, gaya, linewidth=2, label=f"ΔpH = {d:+.1f}")
    a1.set_title("Sensitivitas terhadap pH (ΔpH ditahan)", fontsize=10, fontweight="bold")
    a1.set_xlabel("pH sekarang")
    a1.set_ylabel("Koreksi")
    a1.grid(True, linestyle=":", alpha=0.6)
    a1.legend(fontsize=8)

    d_x = np.linspace(-1.0, 1.0, 201)
    for p, gaya in [(5.0, "--"), (6.0, "-"), (7.0, ":")]:
        y = [fe.inferensi_inti(p, float(d))["koreksi"] for d in d_x]
        a2.plot(d_x, y, gaya, linewidth=2, label=f"pH = {p:.1f}")
    a2.set_title("Sensitivitas terhadap ΔpH (pH ditahan)", fontsize=10, fontweight="bold")
    a2.set_xlabel("ΔpH")
    a2.set_ylabel("Koreksi")
    a2.grid(True, linestyle=":", alpha=0.6)
    a2.legend(fontsize=8)
    fig.tight_layout()
    return fig


def simpan(fig, nama, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    jalur = folder / nama
    fig.savefig(jalur, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return jalur


def buat_semua(folder):
    """Buat gambar statis: MF, agregasi contoh, firing, decision surface."""
    contoh = fe.hitung_koreksi_ph(5.5, 5.7)
    data = fe.hitung_permukaan_keputusan()
    jalur = [
        simpan(fig_mf_ph(), "mf_ph_sekarang.png", folder),
        simpan(fig_mf_delta(), "mf_delta_ph.png", folder),
        simpan(fig_mf_koreksi(), "mf_koreksi.png", folder),
        simpan(fig_agregasi(contoh), "agregasi_5.50_5.70.png", folder),
        simpan(fig_firing(contoh), "firing_5.50_5.70.png", folder),
        simpan(fig_surface3d(data), "decision_surface.png", folder),
        simpan(fig_peta_keputusan(data=data), "decision_map.png", folder),
        simpan(fig_sensitivitas(), "analisis_sensitivitas.png", folder),
    ]
    return jalur


if __name__ == "__main__":
    keluar = Path(__file__).resolve().parent.parent / "hasil"
    for j in buat_semua(keluar):
        print("Tersimpan:", j)
