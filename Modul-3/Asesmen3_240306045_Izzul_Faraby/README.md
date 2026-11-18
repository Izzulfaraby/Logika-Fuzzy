# Sistem Pengendalian pH Hidroponik Berbasis Logika Fuzzy (Mamdani)

Aplikasi web Streamlit untuk menyarankan koreksi pH larutan nutrisi hidroponik dari dua pengukuran (pH sekarang dan pH sebelumnya).

- **Nama / NIM:** Izzul Faraby / 240306045
- **Mata kuliah:** Logika Fuzzy, S1 Teknologi Informasi
- **Repositori:** https://github.com/Izzulfaraby/Logika-Fuzzy
- **Metode:** Mamdani (implikasi MIN, agregasi MAX, defuzzifikasi centroid)
- **Video demo:** lihat `demo/link_video_demo.txt`

> **Simulasi.** Output adalah perintah simulasi (−100 s.d. +100), **bukan dosis bahan kimia** dan bukan perintah pompa. Tidak ada pengujian atau integrasi perangkat keras.

## Fitur

![Tampilan Aplikasi Streamlit](assets/screenshot_aplikasi.png)

- Input interaktif (slider atau ketik manual) dengan validasi rentang 0–14, penolakan teks/NaN/kosong, dan koma desimal.
- ΔpH dihitung otomatis dari dua pengukuran.
- Klasifikasi kondisi air: status kimia, status terhadap target, tren pH.
- Inferensi Mamdani 9 aturan, keputusan berlabel (Netral / Naikkan / Turunkan × Ringan / Sedang / Kuat).
- Visualisasi: fungsi keanggotaan dengan penanda input, kurva agregasi dan centroid, firing strength, peta keputusan.
- Tab evaluasi batch: MAE, RMSE, waktu komputasi, grafik referensi vs prediksi, unduh hasil CSV.

## Instalasi

Prasyarat: Python 3.9+ dan pip.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Menjalankan

```bash
streamlit run src/app.py
```

Aplikasi terbuka di `http://localhost:8501`.

Skrip pendukung (dari root proyek):

```bash
python src/evaluasi_data.py          # Praktikum 12: MAE, RMSE, grafik, 2 error terbesar
python tests/test_blackbox.py        # Praktikum 14: 20 kasus black-box -> hasil/hasil_blackbox.md
python src/visualisasi.py            # gambar statis ke hasil/
python src/buat_dataset.py           # membangun ulang data/test_cases.csv
```

## Struktur Proyek

```text
Asesmen3_240306045_Izzul_Faraby/
├── .gitignore
├── README.md
├── requirements.txt
├── assets/
│   └── PETUNJUK_SCREENSHOT.txt
├── data/
│   └── test_cases.csv
├── demo/
│   ├── link_video_demo.txt
│   └── naskah_video_demo.md
├── docs/
│   ├── CHECKLIST_PENYERAHAN.md
│   ├── Naskah_Presentasi.md
│   └── PRD_Praktikum15.md
├── hasil/
│   ├── agregasi_5.50_5.70.png
│   ├── analisis_sensitivitas.png
│   ├── decision_map.png
│   ├── decision_surface.png
│   ├── evaluasi_prediksi_vs_aktual.png
│   ├── firing_5.50_5.70.png
│   ├── hasil_blackbox.csv
│   ├── hasil_blackbox.md
│   ├── hasil_evaluasi.csv
│   ├── mf_delta_ph.png
│   ├── mf_koreksi.png
│   └── mf_ph_sekarang.png
├── laporan/
│   └── Laporan_Akhir_240306045.md
├── presentation/
│   ├── Slide_Final_Project_240306045.pdf
│   └── Slide_Final_Project_240306045.pptx
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── buat_dataset.py
│   ├── evaluasi_data.py
│   ├── fuzzy_engine.py
│   └── visualisasi.py
└── tests/
    └── test_blackbox.py
```

## Ringkasan Model

| Variabel | Semesta | Himpunan |
|---|---|---|
| `ph_sekarang` | 0–14 | Rendah, Sesuai, Tinggi |
| `delta_ph` = sekarang − sebelumnya | −14 s.d. +14 | Turun, Stabil, Naik |
| `koreksi` (output) | −100 s.d. +100 | Turunkan Kuat/Sedang/Ringan, Netral, Naikkan Ringan/Sedang/Kuat |

Target pH 5,8–6,2 adalah **asumsi desain** (sayuran daun) dan harus disesuaikan serta dirujuk pada tanaman yang dipakai.

| pH \ ΔpH | Turun | Stabil | Naik |
|---|---|---|---|
| **Rendah** | Naikkan Kuat | Naikkan Sedang | Naikkan Ringan |
| **Sesuai** | Naikkan Ringan | Netral | Turunkan Ringan |
| **Tinggi** | Turunkan Ringan | Turunkan Sedang | Turunkan Kuat |

Parameter fungsi keanggotaan lengkap ada di `src/fuzzy_engine.py` dan `laporan/Laporan_Akhir_240306045.md`.

## Dataset Uji

`data/test_cases.csv` berisi 22 skenario (kolom `id, skenario, ph_sekarang, ph_sebelumnya, koreksi_referensi`). Kolom `koreksi_referensi` berasal dari **pembanding aturan tegas (Boolean)** pada matriks aturan yang sama, **bukan data pakar sungguhan**. Jika Anda memiliki penilaian pakar atau operator, ganti kolom tersebut, lalu jalankan ulang `python src/evaluasi_data.py`.

## Hasil Pengujian (eksekusi nyata)

| Pengujian | Hasil |
|---|---|
| Black-box (EP dan BVA) | 20 dari 20 kasus PASS |
| Evaluasi dataset (N = 22) | MAE 7,84; RMSE 16,02 |
| Waktu inferensi | sekitar 0,1 ms per kasus (batas NFR: < 1 detik) |

Angka MAE dan RMSE bergantung pada pembanding aturan tegas; penjelasan lengkap ada di laporan.

## Catatan

- Antarmuka Streamlit perlu diuji dan di-screenshot di komputer Anda: simpan ke `assets/screenshot_aplikasi.png`.
- Keselamatan: penerapan pada perangkat fisik memerlukan kalibrasi sensor pH, validasi target tanaman, pengujian aktuator, pengukuran volume larutan, dan kalibrasi dosis.
