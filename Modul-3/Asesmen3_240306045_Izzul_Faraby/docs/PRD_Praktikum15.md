# PRD — Praktikum 15: Asesmen Modul 3 (Aplikasi Fuzzy)

**Mata kuliah:** Logika Fuzzy · **Program studi:** S1 Teknologi Informasi **Sumber:** `Praktikum15.md` (dengan konteks Praktikum 11–14) **Status:** Draft v1.0 · **Bobot penilaian:** 25%

## 1. Ringkasan Eksekutif

Praktikum 15 adalah *technical milestone* Modul 3: mahasiswa mewujudkan model fuzzy dan mesin inferensi yang sudah dirancang menjadi **aplikasi web interaktif yang berfungsi penuh** (Python + Streamlit), lengkap dengan validasi, visualisasi, dataset uji, dokumentasi, dan video demo.

PRD ini mendefinisikan apa yang harus diserahkan, bagaimana diverifikasi, dan kapan dianggap selesai. Hasil asesmen ini menjadi fondasi Final Project Exhibition (Praktikum 16, bobot 20%).

## 2. Tujuan

1. Menghasilkan aplikasi web interaktif berbasis Python dan Streamlit.
2. Mengintegrasikan seluruh siklus inferensi (fuzzifikasi, inferensi aturan, defuzzifikasi) dalam arsitektur modular.
3. Menyajikan visualisasi dan interpretasi keputusan yang mudah dipahami pengguna.
4. Memvalidasi keandalan fungsional dengan dataset uji minimal 10 kasus.
5. Menyusun dokumentasi lengkap dan video demo singkat.

### Indikator Keberhasilan

| Indikator | Target |
| --- | --- |
| 10 persyaratan minimal (bagian 5) terpenuhi | 10 dari 10 |
| Aplikasi berjalan di environment bersih tanpa error | `pip install -r requirements.txt` lalu `streamlit run src/app.py` berhasil |
| Dataset uji | CSV dengan minimal 10 skenario (disarankan ≥ 15) |
| Durasi video | 3–5 menit |
| Skor rubrik | Sesuai target kelas (ditetapkan dosen) |

## 3. Pemangku Kepentingan

| Peran | Kebutuhan |
| --- | --- |
| Mahasiswa (pengembang) | Daftar persyaratan jelas, struktur repo baku, panduan video |
| Dosen/penguji | Dapat menjalankan aplikasi sendiri, menilai per rubrik, memverifikasi checklist |
| Pengguna akhir (simulasi) | Antarmuka mudah dipahami, rekomendasi jelas |

## 4. Ruang Lingkup

**Dalam lingkup:** aplikasi Streamlit, engine fuzzy modular, validasi input, visualisasi, dataset CSV, `README.md`, `requirements.txt`, screenshot, video demo, commit dan push ke GitHub.

**Di luar lingkup:** deployment publik produksi, integrasi perangkat keras, ANFIS (cukup dibahas sebagai rencana pengembangan), slide presentasi (masuk Praktikum 16).

## 5. Kebutuhan Fungsional (10 Persyaratan Wajib)

| ID | Komponen | Persyaratan minimal | Kriteria penerimaan (cara verifikasi) |
| --- | --- | --- | --- |
| FR-01 | Antarmuka masukan (UI) | Streamlit dengan slider atau formulir input interaktif | Menggeser slider/mengubah input memperbarui hasil tanpa memuat ulang manual |
| FR-02 | Validasi masukan | Proteksi input di luar rentang semesta | Input negatif, di atas batas, teks, atau kosong menampilkan pesan galat dan tidak membuat aplikasi crash |
| FR-03 | Fuzzy engine backend | Terpisah dalam `fuzzy_engine.py` | Engine dapat diimpor dan dijalankan tanpa Streamlit |
| FR-04 | Mesin inferensi | Mamdani, Sugeno, atau Tsukamoto diimplementasikan benar | Hasil program sama dengan hitung manual pada minimal satu contoh |
| FR-05 | Defuzzifikasi | Menghasilkan nilai output numerik riil (crisp) | Output berupa bilangan, bukan hanya label |
| FR-06 | Interpretasi keputusan | Label kategori, badge status, atau teks rekomendasi | Setiap rentang output memiliki label dan saran yang terbaca |
| FR-07 | Visualisasi interaktif | Grafik kurva keanggotaan atau aktivasi aturan di web | Grafik tampil di halaman dan ikut berubah mengikuti input |
| FR-08 | Dataset pengujian | CSV minimal 10 skenario pengujian | `data/test_cases.csv` ada, terbaca, dan seluruh baris dapat dijalankan |
| FR-09 | Dokumentasi lengkap | `README.md` panduan instalasi dan penggunaan | Orang lain dapat mereplikasi hanya dengan mengikuti README |
| FR-10 | Video demo singkat | Rekaman 3–5 menit yang menjelaskan fitur | Tautan di `demo/link_video_demo.txt` dapat dibuka dan durasi sesuai |

## 6. Kebutuhan Non-Fungsional

| ID | Kategori | Kebutuhan |
| --- | --- | --- |
| NFR-01 | Replikabilitas | `requirements.txt` sudah dicoba pada environment baru |
| NFR-02 | Kualitas kode | Modular, bersih (PEP 8), docstring pada fungsi inti |
| NFR-03 | Performa | Inferensi selesai < 1 detik (mengacu NFR Praktikum 11) |
| NFR-04 | Usability | Teks bantuan pada input, hasil dapat dipahami pengguna awam |
| NFR-05 | Ketahanan | Tidak ada eksepsi tak tertangani pada input batas atau tidak valid (mengacu Praktikum 14) |

## 7. Struktur Repositori Wajib

```text
Modul-3/Asesmen3_240306045_Izzul_Faraby/
├── README.md                      # Dokumentasi teknis & panduan instalasi
├── requirements.txt               # Daftar dependensi pustaka Python
├── data/
│   └── test_cases.csv             # Dataset pengujian minimal 10 kasus
├── src/
│   ├── __init__.py
│   ├── fuzzy_engine.py            # Logika murni inferensi fuzzy
│   └── app.py                     # Antarmuka web interaktif Streamlit
├── assets/
│   └── screenshot_aplikasi.png    # Gambar tangkapan layar antarmuka
└── demo/
    └── link_video_demo.txt        # Tautan video rekaman demo (YouTube / Google Drive)
```

Berkas tambahan (skrip evaluasi, grafik hasil, laporan) boleh ada selama struktur di atas tetap utuh.

## 8. Spesifikasi Video Demo

Durasi **3–5 menit**.

| Waktu | Isi |
| --- | --- |
| 0:00–1:00 | Perkenalan, judul produk, latar belakang masalah nyata |
| 1:00–2:00 | Arsitektur sistem: variabel input, basis aturan, metode inferensi |
| 2:00–4:00 | Live demo: jalankan aplikasi, skenario normal, skenario ekstrem/kritis, tampilkan grafik keputusan |
| 4:00–5:00 | Kesimpulan, keterbatasan, rencana pengembangan |

## 9. Rubrik Penilaian (Bobot 25%)

| No | Aspek | Bobot | Indikator | Bukti yang disiapkan |
| --- | --- | --- | --- | --- |
| 1 | Fungsionalitas aplikasi (CPMK-4, 6) | 35% | Berjalan lancar tanpa error, inferensi akurat, input interaktif, visualisasi informatif | Aplikasi, uji black-box, hasil perbandingan manual vs program |
| 2 | Kualitas kode dan arsitektur (CPMK-4) | 20% | Clean code, modularitas `src/`, validasi data, efisiensi | `fuzzy_engine.py` terpisah, docstring, validasi |
| 3 | Validasi dan dataset uji (CPMK-5) | 15% | Minimal 10 kasus pada CSV dan analisis hasil evaluasi | `test_cases.csv`, tabel hasil, MAE/RMSE bila ada |
| 4 | Dokumentasi perangkat lunak (CPMK-6) | 15% | Panduan instalasi jelas, `requirements.txt` lengkap, mudah direplikasi | `README.md`, `requirements.txt` yang teruji |
| 5 | Video demonstrasi (CPMK-6) | 15% | Penyampaian jelas, demo profesional, alur logika tepat | Video 3–5 menit sesuai format |
|  | **Total** | **100%** |  |  |

## 10. Ketentuan Pengumpulan

1. Seluruh kode, dataset, dan dokumentasi diunggah ke repositori GitHub.
2. Uji pada environment baru:

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

3. Commit dan push:

```bash
git add Modul-3/
git commit -m "feat(modul3): rilis final practical assignment 3 fuzzy application"
git push origin main
```

## 11. Rencana Verifikasi (Acceptance Test)

| Langkah | Pemeriksaan | Lulus bila |
| --- | --- | --- |
| 1 | Clone repo ke folder baru, buat virtualenv, pasang dependensi | Tidak ada galat instalasi |
| 2 | Jalankan `streamlit run src/app.py` | Aplikasi terbuka di `localhost:8501` |
| 3 | Uji skenario normal, ekstrem, dan input tidak valid | Hasil masuk akal; input tidak valid ditolak dengan pesan |
| 4 | Bandingkan satu contoh hitung manual dengan output program | Selisih dapat diabaikan (pembulatan) |
| 5 | Buka grafik di web dan ubah input | Grafik berubah mengikuti input |
| 6 | Jalankan seluruh baris `test_cases.csv` | Tidak ada baris yang membuat program error |
| 7 | Buka tautan video | Dapat diputar, durasi 3–5 menit |
| 8 | Periksa struktur folder terhadap bagian 7 | Semua berkas wajib ada |

## 12. Risiko dan Mitigasi

| Risiko | Dampak | Mitigasi |
| --- | --- | --- |
| Dependensi gagal terpasang di komputer penguji | Aplikasi tidak bisa dijalankan | Uji di environment baru; cantumkan versi Python di README |
| Logika engine tidak cocok dengan perhitungan manual | Skor fungsionalitas turun | Sertakan satu contoh hitung manual dan bandingkan |
| Input tak terduga membuat aplikasi crash | Demo gagal | Validasi rentang, tipe, NaN, dan input kosong; bungkus komputasi dengan try/except |
| Video melebihi atau kurang dari 3–5 menit | Kehilangan poin video | Ikuti skrip waktu pada bagian 8 |
| Screenshot atau tautan video terlupa | Checklist tidak lengkap | Gunakan checklist bagian 13 sebelum push |

## 13. Definition of Done

- [ ] Aplikasi berjalan di environment baru dengan dua perintah
- [ ] FR-01 sampai FR-10 terpenuhi
- [ ] `fuzzy_engine.py` terpisah dari `app.py`
- [ ] Validasi input teruji (negatif, melebihi batas, teks, kosong)
- [ ] `data/test_cases.csv` berisi minimal 10 skenario
- [ ] `README.md` dan `requirements.txt` lengkap dan teruji
- [ ] `assets/screenshot_aplikasi.png` tersedia
- [ ] Video 3–5 menit diunggah dan tautannya tercantum
- [ ] Struktur repositori sesuai bagian 7
- [ ] Commit dan push selesai

## 14. Status pada Proyek HidroFuzzy-pH

Status berikut mengacu pada paket proyek yang sudah dibuat (topik pH hidroponik, Mamdani).

| ID | Status | Catatan |
| --- | --- | --- |
| FR-01 | Siap | `src/app.py`; lolos uji asap dengan modul Streamlit tiruan, belum dijalankan di Streamlit asli |
| FR-02 | Siap | Diuji pada TC-11 sampai TC-15 (semua PASS) |
| FR-03 | Siap | `src/fuzzy_engine.py` |
| FR-04 | Siap | Cocok dengan hitung manual (pH 5,5; sebelumnya 5,7: centroid 43,87) |
| FR-05 | Siap | Centroid numerik |
| FR-06 | Siap | Badge, label, kalimat saran |
| FR-07 | Siap | Kurva keanggotaan, agregasi, firing strength, peta keputusan |
| FR-08 | Siap | 22 skenario |
| FR-09 | Siap | `README.md` dan `Modul-3/README_APP.md` |
| FR-10 | Belum | Naskah tersedia; video belum direkam |

**Sisa pekerjaan:** jalankan aplikasi di Streamlit asli dan ambil `assets/screenshot_aplikasi.png`, rekam dan unggah video, isi nama/NIM/tautan, uji instalasi di environment baru, lalu push.

## 15. Ketidakkonsistenan Materi dan Asumsi

| Temuan | Asumsi PRD ini |
| --- | --- |
| Bagian D `Praktikum15.md` menyebut `streamlit run app.py`, sedangkan Bagian F menyebut `streamlit run src/app.py` | Gunakan `streamlit run src/app.py` dari root proyek |
| Praktikum 15 meminta dataset minimal 10 skenario, Praktikum 12 meminta minimal 15 baris | Gunakan 15 baris atau lebih agar aman untuk keduanya |
| Praktikum 14 menyebut `README_APP.md`, Praktikum 15 menyebut `README.md` | Wajib `README.md`; `README_APP.md` boleh sebagai panduan pengguna tambahan |
| Rubrik menyebut "analisis hasil evaluasi" tanpa metrik wajib | Sertakan MAE/RMSE atau tabel hasil uji dan ringkasan analisis |

## 16. Penutup

Asesmen ini dinilai dari tiga hal: aplikasi yang benar-benar berjalan (35%), kualitas kode dan arsitektur (20%), serta bukti validasi, dokumentasi, dan video (45% gabungan). Dokumen ini dapat dipakai sebagai lembar kendali sebelum pengumpulan.
