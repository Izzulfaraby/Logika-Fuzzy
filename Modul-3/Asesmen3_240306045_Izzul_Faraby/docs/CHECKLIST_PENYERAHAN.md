# Checklist Penyerahan (Praktikum 15 dan 16)

Status: ✅ sudah ada dan diverifikasi di lingkungan pembuatan · ✍️ perlu Anda isi/kerjakan.

## Asesmen 3 (10 persyaratan)
| No | Komponen | Status | Catatan |
|:--:|---|:--:|---|
| 1 | UI Streamlit (slider/form) | ✅ | `src/app.py`; lolos uji asap dengan Streamlit tiruan |
| 2 | Validasi masukan | ✅ | Diuji TC-11 s.d. TC-15 |
| 3 | Engine modular | ✅ | `src/fuzzy_engine.py` |
| 4 | Mesin inferensi Mamdani | ✅ | Cocok dengan hitung manual (5,5; 5,7) |
| 5 | Output crisp | ✅ | Centroid numerik |
| 6 | Interpretasi keputusan | ✅ | Badge, label, kalimat saran |
| 7 | Visualisasi di web | ✅ | MF, agregasi, firing, peta keputusan |
| 8 | Dataset ≥ 10 skenario | ✅ | 22 baris |
| 9 | README | ✅ | `README.md`, `Modul-3/README_APP.md` |
| 10 | Video demo 3–5 menit | ✍️ | Naskah di `demo/naskah_video_demo.md` |

## Final Project (Pertemuan 16)
- [x] ✍️ Isi nama, NIM, tautan GitHub (cari `<ISI`) pada README, proposal, laporan, slide.
- [x] ✍️ Ganti `NIM` dan `Nama` pada nama folder/berkas.
- [ ] ✍️ Jalankan `streamlit run src/app.py` di komputer Anda; simpan screenshot ke `assets/screenshot_aplikasi.png` dan 3 skenario berbeda (Praktikum 13).
- [ ] ✍️ Rekam video dan isi `demo/link_video_demo.txt`.
- [ ] ✍️ Cantumkan sumber rujukan untuk target pH tanaman Anda dan isi selang pengukuran.
- [ ] ✍️ Jika ada data pakar/operator, ganti kolom `koreksi_referensi` lalu jalankan ulang evaluasi dan perbarui laporan.
- [ ] ✍️ Salin `Modul-1/` dan `Modul-2/` ke repositori (tidak termasuk paket ini).
- [ ] ✅ `requirements.txt`, `data/test_cases.csv`, laporan akhir, slide di `presentation/`.
- [ ] Uji `pip install -r requirements.txt` pada environment baru.
- [ ] `git add Modul-3/ && git commit -m "feat(modul3): rilis final practical assignment 3 fuzzy application" && git push origin main`

## Pemetaan tugas Praktikum 11–14
| Praktikum | Tugas | Berkas |
|:--:|---|---|
| 11 | Proposal, struktur folder | `Modul-3/Proposal_Produk_240306045.md` |
| 12 | CSV ≥ 15 baris, MAE/RMSE, grafik, 2 error terbesar | `data/test_cases.csv`, `src/evaluasi_data.py`, `Modul-3/Praktikum12_240306045.py`, `laporan/` bagian 6 |
| 13 | engine, app, 3 screenshot | `src/`; screenshot perlu Anda ambil |
| 14 | Black-box ≥ 10 kasus, validasi, requirements, README_APP | `tests/`, `hasil/hasil_blackbox.md`, `Modul-3/README_APP.md` |
