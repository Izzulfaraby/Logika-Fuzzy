"""
app.py  (Praktikum 13-15)
Antarmuka Streamlit: Sistem Pengendalian pH Hidroponik berbasis Logika Fuzzy Mamdani.

Menjalankan (dari root proyek):
    streamlit run src/app.py

SIMULASI: output adalah perintah simulasi, BUKAN dosis bahan kimia.
"""

import sys
from pathlib import Path

# Pastikan folder modul lokal (src/) terdaftar dalam sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import evaluasi_data as ev
import fuzzy_engine as fe
import visualisasi as vz

ROOT = Path(__file__).resolve().parent.parent

# ==========================================================
# 1. KONFIGURASI HALAMAN
# ==========================================================
st.set_page_config(
    page_title="Kendali pH Hidroponik (Fuzzy Mamdani)",
    page_icon="🌱",
    layout="wide",
)

st.title("🌱 Sistem Pengendalian pH Hidroponik Berbasis Logika Fuzzy")
st.markdown(
    "Aplikasi ini memakai **inferensi Mamdani** (implikasi MIN, agregasi MAX, "
    "defuzzifikasi centroid) untuk menyarankan koreksi pH dari dua pengukuran: "
    "pH sekarang dan pH sebelumnya."
)
st.warning(
    "⚠️ **Simulasi.** Nilai koreksi adalah perintah simulasi (−100 s.d. +100), "
    "bukan dosis bahan kimia dan bukan perintah pompa."
)


def tampilkan_fig(fig):
    """Render Figure Matplotlib lalu tutup agar memori tidak bocor."""
    st.pyplot(fig)
    plt.close(fig)


@st.cache_data(show_spinner=False)
def data_permukaan():
    """Decision surface dihitung sekali lalu di-cache."""
    return fe.hitung_permukaan_keputusan()


# ==========================================================
# 2. SIDEBAR: MASUKAN PENGGUNA DAN VALIDASI
# ==========================================================
st.sidebar.header("⚙️ Parameter Masukan")
mode = st.sidebar.radio("Mode masukan", ["Slider", "Ketik manual"], horizontal=True)

if mode == "Slider":
    in_sekarang = st.sidebar.slider(
        "🧪 pH sekarang", 0.0, 14.0, 6.0, 0.1,
        help="Hasil pengukuran pH terbaru (0–14). Target asumsi: 5,8–6,2.")
    in_sebelumnya = st.sidebar.slider(
        "🕒 pH sebelumnya", 0.0, 14.0, 6.0, 0.1,
        help="Hasil pengukuran pH pada pengukuran sebelumnya (0–14).")
else:
    in_sekarang = st.sidebar.text_input("🧪 pH sekarang (0–14)", value="6.0")
    in_sebelumnya = st.sidebar.text_input("🕒 pH sebelumnya (0–14)", value="6.0")

st.sidebar.caption(
    "Koma desimal diterima (6,2). Nilai di luar 0–14 atau bukan angka akan ditolak."
)

# Validasi masukan dan inferensi, dibungkus penanganan galat
try:
    hasil = fe.hitung_koreksi_ph(in_sekarang, in_sebelumnya)
except ValueError as galat:
    st.error(f"⚠️ Masukan tidak valid: {galat}")
    st.stop()
except Exception as galat:  # kegagalan tak terduga pada komputasi
    st.error(f"Terjadi kesalahan komputasi: {galat}")
    st.stop()

# ==========================================================
# 3. TAB UTAMA
# ==========================================================
tab_sim, tab_eval, tab_info = st.tabs(["🧪 Simulasi", "📊 Evaluasi Dataset", "ℹ️ Tentang"])

# ---------------------------------------------------------- Simulasi
with tab_sim:
    kiri, kanan = st.columns([1, 1])

    with kiri:
        st.subheader("Hasil Rekomendasi")
        teks = f"### {hasil['label']}"
        if hasil["tingkat"] == 0:
            st.success(teks)
        elif hasil["tingkat"] == 1:
            st.info(teks)
        elif hasil["tingkat"] == 2:
            st.warning(teks)
        else:
            st.error(teks)
        st.write(hasil["rekomendasi"])
        if not hasil["berhasil"]:
            st.warning("Inferensi gagal (agregasi kosong); koreksi aman = 0 ditampilkan.")

        st.metric("Koreksi (satuan simulasi)", f"{hasil['koreksi']:+.2f}",
                  help="Positif = naikkan pH, negatif = turunkan pH.")
        st.progress(int(min(100, abs(hasil["koreksi"]))))
        st.caption("Bilah menunjukkan besar koreksi (0–100), arah tertulis pada label.")

    with kanan:
        st.subheader("Kondisi Air")
        k1, k2 = st.columns(2)
        k1.metric("ΔpH (otomatis)", f"{hasil['delta_ph']:+.2f}")
        k2.metric("Status kimia", hasil["status_kimia"])
        k3, k4 = st.columns(2)
        k3.metric("Terhadap target", hasil["status_target"])
        k4.metric("Tren pH", hasil["tren"])
        st.caption(
            f"Target asumsi {fe.TARGET_MIN:g}–{fe.TARGET_MAX:g}; tren STABIL bila "
            f"|ΔpH| ≤ {fe.AMBANG_STABIL:g}. Klasifikasi ini untuk pelaporan; "
            "keputusan ditentukan inferensi fuzzy."
        )

    st.divider()
    st.subheader("Derajat Keanggotaan dan Aturan Aktif")
    d1, d2 = st.columns(2)
    d1.dataframe(
        pd.DataFrame({"Himpunan": list(hasil["mu_ph"]), "μ": list(hasil["mu_ph"].values())})
        .assign(Variabel="pH sekarang"),
        hide_index=True)
    d2.dataframe(
        pd.DataFrame({"Himpunan": list(hasil["mu_dph"]), "μ": list(hasil["mu_dph"].values())})
        .assign(Variabel="ΔpH"),
        hide_index=True)

    baris = []
    for rid, lp, ld, lo in fe.RULES:
        a = hasil["alpha"][rid]
        baris.append({"Aturan": rid, "IF pH": lp, "AND ΔpH": ld, "THEN koreksi": lo,
                      "α (firing)": round(a, 3), "Aktif": "✅" if a > 0 else ""})
    st.dataframe(pd.DataFrame(baris), hide_index=True)

    st.divider()
    st.subheader("Visualisasi")
    g1, g2 = st.columns(2)
    with g1:
        tampilkan_fig(vz.fig_mf_ph(hasil["ph_sekarang"]))
        tampilkan_fig(vz.fig_agregasi(hasil))
    with g2:
        tampilkan_fig(vz.fig_mf_delta(hasil["delta_ph"]))
        tampilkan_fig(vz.fig_firing(hasil))
    tampilkan_fig(vz.fig_peta_keputusan(hasil["ph_sekarang"], hasil["delta_ph"], data_permukaan()))

# ---------------------------------------------------------- Evaluasi
with tab_eval:
    st.subheader("Evaluasi Batch (MAE dan RMSE)")
    st.markdown(
        "Kolom wajib CSV: `id, ph_sekarang, ph_sebelumnya, koreksi_referensi`. "
        "Kolom `skenario` bersifat opsional. Bawaan: `data/test_cases.csv`."
    )
    unggahan = st.file_uploader("Unggah CSV uji (opsional)", type="csv")
    try:
        sumber = unggahan if unggahan is not None else ROOT / "data" / "test_cases.csv"
        df, catatan = ev.muat_dan_bersihkan(sumber)
        for c in catatan:
            st.info(c)
        if "skenario" not in df.columns:
            df["skenario"] = ""
        hasil_batch, ms = ev.jalankan_batch(df)
        m = ev.hitung_metrik(hasil_batch)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Jumlah sampel (N)", m["N"])
        c2.metric("MAE", f"{m['MAE']:.2f}")
        c3.metric("RMSE", f"{m['RMSE']:.2f}")
        c4.metric("Waktu / inferensi", f"{ms:.2f} ms")
        st.caption(
            "Referensi = keputusan aturan tegas (Boolean) pada matriks yang sama, bukan data "
            "pakar sungguhan. Selisih terbesar muncul di zona transisi, tempat fuzzy "
            "memberi keputusan bertahap."
        )
        tampilkan_fig(vz.fig_aktual_vs_prediksi(hasil_batch, m["MAE"]))
        st.dataframe(
            hasil_batch[["id", "skenario", "ph_sekarang", "ph_sebelumnya", "delta_ph",
                         "koreksi_referensi", "prediksi_fuzzy", "aturan_aktif",
                         "error_absolut"]].round(2),
            hide_index=True)
        st.download_button("⬇️ Unduh hasil evaluasi (CSV)",
                           hasil_batch.to_csv(index=False).encode("utf-8"),
                           file_name="hasil_evaluasi.csv", mime="text/csv")
        with st.expander("Analisis sensitivitas"):
            tampilkan_fig(vz.fig_sensitivitas())
    except Exception as galat:
        st.error(f"Gagal memproses dataset: {galat}")

# ---------------------------------------------------------- Tentang
with tab_info:
    st.subheader("Tentang Sistem")
    st.markdown(
        """
**Variabel:** `pH sekarang` (0–14), `ΔpH = pH sekarang − pH sebelumnya` (dihitung otomatis),
dan `koreksi` (−100 s.d. +100, satuan simulasi).

**Interpretasi keputusan**

| Label | Arti | Tindakan yang disarankan (simulasi) |
|---|---|---|
| Netral | Koreksi sangat kecil | Pertahankan dan pantau |
| Naikkan/Turunkan Ringan | Penyimpangan kecil atau sudah menuju target | Koreksi ringan lalu ukur ulang |
| Naikkan/Turunkan Sedang | Penyimpangan jelas | Koreksi sedang dan pantau rutin |
| Naikkan/Turunkan Kuat | Jauh dan menjauhi target | Tindak lanjut segera |

**Keterbatasan:** hanya dua pengukuran, target tunggal dan simetris, tanpa model kimia
larutan (kapasitas penyangga, volume, suhu). Penerapan fisik memerlukan kalibrasi sensor,
validasi target tanaman, dan kalibrasi dosis.
        """
    )

st.divider()
st.caption("Praktikum Logika Fuzzy — S1 Teknologi Informasi. Metode: Mamdani.")
