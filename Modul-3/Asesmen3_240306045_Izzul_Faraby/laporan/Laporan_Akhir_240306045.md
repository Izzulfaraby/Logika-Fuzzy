# LAPORAN AKHIR PROYEK
## HidroFuzzy-pH: Sistem Pengendalian Kadar pH Larutan Hidroponik Berbasis Logika Fuzzy (Mamdani)

| | |
|---|---|
| **Nama / NIM** | Izzul Faraby / 240306045 |
| **Mata kuliah** | Logika Fuzzy, S1 Teknologi Informasi |
| **Repositori** | https://github.com/Izzulfaraby/Logika-Fuzzy |
| **Cakupan** | Praktikum 11 sampai 16 (Modul 3) |

> **Catatan keterbukaan.** Seluruh angka pada bagian hasil berasal dari eksekusi program di repositori ini (`python src/evaluasi_data.py` dan `python tests/test_blackbox.py`). Sistem adalah **simulasi**; output bukan dosis bahan kimia dan tidak ada pengujian perangkat keras. Antarmuka Streamlit perlu Anda jalankan dan screenshot sendiri (bagian 8).

---

## 1. Identifikasi dan Formulasi Masalah (Praktikum 11)

pH larutan nutrisi hidroponik menentukan ketersediaan unsur hara bagi akar. Rentang target yang dipakai adalah **5,8–6,2** (asumsi desain sayuran daun; sesuaikan dan cantumkan sumber rujukan untuk tanaman Anda). Pengendalian yang baik mempertimbangkan pH saat ini **dan** arah geraknya.

**Mengapa logika fuzzy.** Kondisi seperti "agak rendah" atau "hampir sesuai" bersifat bertingkat. Aturan tegas menimbulkan lompatan keputusan di batas (pH 5,79 vs 5,80), sedangkan fuzzy memberi keputusan yang berubah halus. Pengetahuan operator juga dapat dinyatakan langsung sebagai aturan IF-THEN.

**Batasan.** Simulasi Python; dua pengukuran saja; target tunggal dan simetris; tanpa model kimia larutan.

**Kebutuhan sistem.** Fungsional: input numerik, validasi semesta, ΔpH otomatis, derajat keanggotaan, firing strength, koreksi crisp, label keputusan, grafik, evaluasi batch. Non-fungsional: inferensi < 1 detik, antarmuka intuitif, kode modular.

## 2. Perancangan Model Fuzzy

| Variabel | Semesta | Himpunan | Parameter (a, b, c, d) |
|---|---|---|---|
| `ph_sekarang` | 0–14 | Rendah | (0; 0; 5,3; 5,8) |
| | | Sesuai | (5,3; 5,8; 6,2; 6,7) |
| | | Tinggi | (6,2; 6,7; 14; 14) |
| `delta_ph` | −14 s.d. +14 | Turun | (−14; −14; −0,3; 0) |
| | | Stabil | (−0,3; 0; 0; 0,3) |
| | | Naik | (0; 0,3; 14; 14) |
| `koreksi` | −100 s.d. +100 | Turunkan Kuat | (−100; −100; −90; −60) |
| | | Turunkan Sedang | (−90; −60; −60; −30) |
| | | Turunkan Ringan | (−60; −30; −30; 0) |
| | | Netral | (−30; 0; 0; 30) |
| | | Naikkan Ringan | (0; 30; 30; 60) |
| | | Naikkan Sedang | (30; 60; 60; 90) |
| | | Naikkan Kuat | (60; 90; 100; 100) |

ΔpH = pH sekarang − pH sebelumnya (dihitung otomatis). Selang pengukuran yang diasumsikan: `<ISI>`. Himpunan saling tumpang tindih dan membentuk partisi satuan (jumlah μ = 1) sehingga setiap input tercakup. Zona transisi pH selebar 0,5 di kiri dan kanan plateau target (5,3–5,8 dan 6,2–6,7) dipilih agar keputusan berubah bertahap di sekitar target. Zona "Stabil" ±0,3 dipilih karena selisih antar-pengukuran praktis biasanya di bawah 0,5.

Gambar: `hasil/mf_ph_sekarang.png`, `hasil/mf_delta_ph.png` (sumbu diperbesar ±1,5 agar bentuk terbaca; semesta model tetap ±14), `hasil/mf_koreksi.png`.

**Klasifikasi kondisi air (nilai tegas, untuk pelaporan):** status kimia (pH < 7 ASAM, = 7 NETRAL, > 7 BASA); terhadap target (< 5,8 TERLALU RENDAH, 5,8–6,2 SESUAI TARGET, > 6,2 TERLALU TINGGI); tren (ΔpH < −0,10 MENURUN, |ΔpH| ≤ 0,10 STABIL, > +0,10 MENINGKAT). Contoh: pH 6,0 berstatus kimia ASAM tetapi SESUAI TARGET.

## 3. Basis Aturan

| pH \ ΔpH | Turun | Stabil | Naik |
|---|---|---|---|
| **Rendah** | R1: Naikkan Kuat | R2: Naikkan Sedang | R3: Naikkan Ringan |
| **Sesuai** | R4: Naikkan Ringan | R5: Netral | R6: Turunkan Ringan |
| **Tinggi** | R7: Turunkan Ringan | R8: Turunkan Sedang | R9: Turunkan Kuat |

- **Kelengkapan:** 9 dari 9 kombinasi tercakup.
- **Konsistensi:** tidak ada dua aturan dengan IF sama dan THEN berbeda.
- **Kesesuaian tanda:** Naikkan = positif, Turunkan = negatif; semua himpunan THEN terdefinisi di bagian 2.
- **Simetri:** matriks simetris terhadap titik tengah (Rendah↔Tinggi, Turun↔Naik, tanda berlawanan). Keterbatasannya, tanaman dengan target tidak simetris memerlukan penyesuaian aturan.

## 4. Inferensi Mamdani dan Defuzzifikasi

1. **Fuzzifikasi** μ untuk pH dan ΔpH.
2. **Implikasi (MIN):** α_k = min(μ_A(pH), μ_B(ΔpH)); himpunan output dipotong setinggi α_k.
3. **Agregasi (MAX):** μ_agg(z) = max_k μ_C'k(z).
4. **Centroid:** z* = Σ z·μ_agg(z) / Σ μ_agg(z) pada grid 1001 titik.

**Justifikasi Mamdani.** Aturan linguistik mudah divalidasi pakar budidaya, output berupa himpunan fuzzy menghasilkan keputusan halus, dan penalaran dapat ditelusuri aturan demi aturan melalui kurva agregasi.

**Contoh hitung manual (pH 5,5; sebelumnya 5,7; ΔpH = −0,2).**
μ pH: Rendah = (5,8−5,5)/0,5 = 0,6; Sesuai = (5,5−5,3)/0,5 = 0,4; Tinggi = 0.
μ ΔpH: Turun = 0,2/0,3 ≈ 0,667; Stabil = 0,1/0,3 ≈ 0,333; Naik = 0.
Aturan aktif: R1 = min(0,6; 0,667) = 0,6 (Naikkan Kuat); R2 = 0,333 (Naikkan Sedang); R4 = 0,4 (Naikkan Ringan); R5 = 0,333 (Netral).
Program menghasilkan aturan aktif yang sama dan centroid **43.87** (label Naikkan Ringan). Kurva: `hasil/agregasi_5.50_5.70.png`.

**Agregasi kosong.** Bila luas agregasi < 1e-9, fungsi centroid mengembalikan status `luas_nol` tanpa pembagian; koreksi aman = 0 dan peringatan ditampilkan. Dengan basis aturan lengkap dan himpunan yang saling menutup, kondisi ini tidak muncul untuk input valid.

## 5. Implementasi Python dan Arsitektur (Praktikum 13–14)

| Berkas | Peran |
|---|---|
| `src/fuzzy_engine.py` | Mesin Mamdani murni (NumPy): validasi, ΔpH, klasifikasi, fuzzifikasi, MIN, MAX, centroid, interpretasi keputusan |
| `src/visualisasi.py` | Grafik Matplotlib (Figure) untuk aplikasi dan PNG |
| `src/evaluasi_data.py` | Preprocessing CSV, batch testing, MAE, RMSE, error terbesar |
| `src/app.py` | Antarmuka Streamlit dengan tab Simulasi, Evaluasi Dataset, Tentang |
| `tests/test_blackbox.py` | 20 kasus uji black-box |

Pemisahan engine dan antarmuka membuat engine dapat diuji tanpa web server (dipakai oleh `evaluasi_data.py` dan `test_blackbox.py`). Validasi: rentang 0–14, penolakan teks/NaN/kosong, koma desimal diterima; galat tak terduga ditangkap dan ditampilkan sebagai pesan, bukan crash.

## 6. Hasil Evaluasi Dataset (Praktikum 12)

Dataset `data/test_cases.csv` berisi **22 skenario** (melebihi minimum 15) yang mencakup seluruh sembilan aturan (R1–R9), titik batas target (5,8 dan 6,2), batas semesta (0 dan 14), zona transisi, dan perubahan tepat di ambang tren.

**Referensi.** Kolom `koreksi_referensi` dihitung dari **pembanding aturan tegas (Boolean)** memakai matriks 9 aturan yang sama, dengan batas tegas pada pH (5,8 / 6,2) dan tren (±0,10), serta nilai tegas tiap label sama dengan puncak himpunannya (±90, ±60, ±30, 0). Ini **bukan data pakar sungguhan**. Akibatnya MAE dan RMSE di bawah mengukur *selisih fuzzy terhadap aturan tegas*, bukan akurasi terhadap kebenaran lapangan.

| ID | Skenario | pH sekarang | pH sebelumnya | ΔpH | Referensi | Prediksi fuzzy | Aturan aktif | Error abs |
|:--:|---|:--:|:--:|:--:|:--:|:--:|---|:--:|
| 1 | Rendah dan terus menurun | 4.8 | 5.1 | -0.30 | +90 | +86.06 | R1 | 3.94 |
| 2 | Rendah tetapi meningkat | 4.8 | 4.5 | +0.30 | +30 | +30.00 | R3 | 0.00 |
| 3 | Sesuai target dan stabil | 6 | 6 | +0.00 | +0 | +0.00 | R5 | 0.00 |
| 4 | Tinggi dan terus meningkat | 7.5 | 7.2 | +0.30 | -90 | -86.06 | R9 | 3.94 |
| 5 | Tinggi tetapi menurun | 7.5 | 7.8 | -0.30 | -30 | -30.00 | R7 | 0.00 |
| 6 | Transisi rendah-sesuai (contoh manual) | 5.5 | 5.7 | -0.20 | +90 | +43.87 | R1+R2+R4+R5 | 46.13 |
| 7 | Batas bawah target | 5.8 | 5.8 | +0.00 | +0 | +0.00 | R5 | 0.00 |
| 8 | Batas atas target | 6.2 | 6.2 | +0.00 | +0 | +0.00 | R5 | 0.00 |
| 9 | pH netral 7,0 stabil | 7 | 7 | +0.00 | -60 | -60.00 | R8 | 0.00 |
| 10 | Batas bawah semesta | 0 | 0 | +0.00 | +60 | +60.00 | R2 | 0.00 |
| 11 | Batas atas semesta | 14 | 14 | +0.00 | -60 | -60.00 | R8 | 0.00 |
| 12 | Rendah dan stabil | 5 | 5 | +0.00 | +60 | +60.00 | R2 | 0.00 |
| 13 | Sesuai target tetapi naik | 6 | 5.7 | +0.30 | -30 | -30.00 | R6 | 0.00 |
| 14 | Sesuai target tetapi turun | 6 | 6.3 | -0.30 | +30 | +30.00 | R4 | 0.00 |
| 15 | Tinggi dan stabil | 6.8 | 6.8 | +0.00 | -60 | -60.00 | R8 | 0.00 |
| 16 | Transisi sesuai-tinggi, naik pelan | 6.5 | 6.4 | +0.10 | -60 | -39.35 | R5+R6+R8+R9 | 20.65 |
| 17 | Transisi rendah-sesuai, stabil | 5.6 | 5.6 | +0.00 | +60 | +25.95 | R2+R5 | 34.05 |
| 18 | Sesuai target, perubahan sangat kecil | 6.1 | 6.05 | +0.05 | +0 | -6.22 | R5+R6 | 6.22 |
| 19 | Sangat tinggi dan menurun | 9 | 9.5 | -0.50 | -30 | -30.00 | R7 | 0.00 |
| 20 | Sangat rendah, perubahan tepat -0,1 | 3.5 | 3.6 | -0.10 | +60 | +65.12 | R1+R2 | 5.12 |
| 21 | Transisi sesuai-tinggi, naik cepat | 6.4 | 6 | +0.40 | -90 | -48.57 | R6+R9 | 41.43 |
| 22 | Rendah dan naik sedang | 5.2 | 5 | +0.20 | +30 | +40.91 | R2+R3 | 10.91 |

| Metrik | Nilai |
|---|---|
| Jumlah sampel (N) | 22 |
| **MAE** | **7.836** poin |
| **RMSE** | **16.019** poin |
| Bias rata-rata (fuzzy − referensi) | -0.377 poin |
| Kesesuaian arah koreksi | 95.5% (21 dari 22) |
| Waktu rata-rata per inferensi | sekitar 0.14 ms (target NFR < 1 detik) |

Grafik: `hasil/evaluasi_prediksi_vs_aktual.png`.

**Pola error.** 13 dari 22 kasus berselisih nol dan 15 kasus berselisih di bawah 5 poin. Error terkonsentrasi pada kasus zona transisi (ID 6, 16, 17, 21 dengan selisih ≥ 20) dan kasus perubahan kecil (ID 18, 20, 22 dengan selisih 5–20). Dua kasus bernilai 3,94 (ID 1 dan 4) muncul karena centroid himpunan bahu tidak mencapai puncak 90 (menghasilkan 86,06).

### Dua kasus error terbesar

**1. ID 6: pH 5.5, sebelumnya 5.7 (ΔpH -0.20).** Referensi +90, fuzzy +43.87, selisih 46.13. Aturan tegas melihat pH 5,5 sebagai "Rendah" dan ΔpH −0,2 sebagai "Turun" sehingga langsung R1 (Naikkan Kuat). Fuzzy melihat pH 5,5 sebagian "Rendah" (0,6) dan sebagian "Sesuai" (0,4), ΔpH sebagian "Turun" dan sebagian "Stabil", sehingga empat aturan aktif (R1, R2, R4, R5) dengan output berbeda arah kekuatan, lalu centroid merata-ratakannya. Selisih ini bukan kesalahan sistem, melainkan ciri keputusan bertahap. Perbaikan bila operator menilai koreksi di zona ini harus lebih kuat: persempit zona transisi pH (mis. dari 5,3–5,8 menjadi 5,5–5,8), atau lebarkan batas "Turun" agar ΔpH −0,2 sudah penuh "Turun", atau minta penilaian pakar sungguhan untuk menentukan nilai yang benar.

**2. ID 21: pH 6.4, sebelumnya 6 (ΔpH +0.40).** Referensi -90, fuzzy -48.57, selisih 41.43. pH 6,4 berada di zona transisi Sesuai–Tinggi (μ Sesuai = 0,6; μ Tinggi = 0,4) dengan ΔpH +0,4 (Naik penuh), sehingga R6 (Turunkan Ringan) dan R9 (Turunkan Kuat) aktif bersamaan. Hasilnya berada di antara keduanya (sekitar Turunkan Sedang). Perbaikan: sama seperti kasus 1, penyempitan zona transisi atau penambahan himpunan perantara pada pH bila pakar menghendaki respons lebih tegas di zona ini.

### Analisis sensitivitas

Grafik `hasil/analisis_sensitivitas.png`: terhadap pH, koreksi datar di luar pita 5,3–6,7 (jenuh) dan paling curam di dalam pita itu; terhadap ΔpH, koreksi berubah hanya pada selang −0,3 s.d. +0,3 dan jenuh di luarnya. Artinya ΔpH berpengaruh kuat hanya untuk perubahan kecil, sesuai asumsi bahwa selisih antar-pengukuran biasanya di bawah 0,5. Kurva tidak melompat tiba-tiba, sehingga parameter tidak terlalu sempit. Peta keputusan: `hasil/decision_map.png` dan `hasil/decision_surface.png`.

## 7. Pengujian Black-Box (Praktikum 14)

Teknik: Equivalence Partitioning dan Boundary Value Analysis. Kolom "diharapkan" ditetapkan dari matriks aturan sebelum program dijalankan; "aktual" dan status berasal dari eksekusi `python tests/test_blackbox.py`.

| ID | Skenario | Input (pH sekarang / sebelumnya) | Output diharapkan | Output aktual | Status |
|:--:|---|:---:|---|---|:---:|
| TC-01 | Batas bawah semesta | 0.0 / 0.0 | Naikkan Sedang (+45 s.d. +75) | Koreksi +60.00 (Naikkan Sedang); TERLALU RENDAH; STABIL | **PASS** |
| TC-02 | Batas atas semesta | 14.0 / 14.0 | Turunkan Sedang (-75 s.d. -45) | Koreksi -60.00 (Turunkan Sedang); TERLALU TINGGI; STABIL | **PASS** |
| TC-03 | Nilai tengah target, stabil | 6.0 / 6.0 | Netral (koreksi antara -15 dan +15) | Koreksi +0.00 (Netral); SESUAI TARGET; STABIL | **PASS** |
| TC-04 | Rendah dan menurun | 4.8 / 5.1 | Naikkan Kuat (>= +75) | Koreksi +86.06 (Naikkan Kuat); TERLALU RENDAH; MENURUN | **PASS** |
| TC-05 | Tinggi dan meningkat | 7.5 / 7.2 | Turunkan Kuat (<= -75) | Koreksi -86.06 (Turunkan Kuat); TERLALU TINGGI; MENINGKAT | **PASS** |
| TC-06 | Rendah tetapi sudah naik | 4.8 / 4.5 | Naikkan Ringan (+15 s.d. +45), lebih kecil dari TC-04 | Koreksi +30.00 (Naikkan Ringan); TERLALU RENDAH; MENINGKAT | **PASS** |
| TC-07 | Tinggi tetapi sudah turun | 7.5 / 7.8 | Turunkan Ringan (-45 s.d. -15), lebih kecil dari TC-05 | Koreksi -30.00 (Turunkan Ringan); TERLALU TINGGI; MENURUN | **PASS** |
| TC-08 | BVA: tepat di batas bawah target | 5.8 / 5.8 | Netral (koreksi antara -15 dan +15) | Koreksi +0.00 (Netral); SESUAI TARGET; STABIL | **PASS** |
| TC-09 | BVA: tepat di bawah batas target | 5.79 / 5.79 | Hampir netral (kontinu, koreksi antara -15 dan +15) | Koreksi +2.29 (Netral); TERLALU RENDAH; STABIL | **PASS** |
| TC-10 | BVA: tepat di atas batas target | 6.21 / 6.21 | Hampir netral (kontinu, koreksi antara -15 dan +15) | Koreksi -2.29 (Netral); TERLALU TINGGI; STABIL | **PASS** |
| TC-11 | Input negatif (di luar semesta) | -0.1 / 6.0 | Ditolak dengan pesan error | Ditolak: pH sekarang = -0.1 di luar rentang 0-14. | **PASS** |
| TC-12 | Input melebihi batas atas | 14.1 / 6.0 | Ditolak dengan pesan error | Ditolak: pH sekarang = 14.1 di luar rentang 0-14. | **PASS** |
| TC-13 | Input teks bukan angka | abc / 6.0 | Ditolak dengan pesan error | Ditolak: pH sekarang harus berupa bilangan (contoh: 6.2). | **PASS** |
| TC-14 | Input NaN | nan / 6.0 | Ditolak dengan pesan error | Ditolak: pH sekarang tidak boleh NaN atau tak hingga. | **PASS** |
| TC-15 | Input kosong |  / 6.0 | Ditolak dengan pesan error | Ditolak: pH sekarang harus berupa bilangan (contoh: 6.2). | **PASS** |
| TC-16 | Koma desimal diterima | 6,2 / 6,0 | Diterima; delta pH = +0,2 | Koreksi -19.09 (Turunkan Ringan); SESUAI TARGET; MENINGKAT | **PASS** |
| TC-17 | Simetri terhadap target 6,0 | 4.8 / 5.1 | koreksi(4,8; 5,1) = -koreksi(7,2; 6,9) | Koreksi +86.06 (Naikkan Kuat); TERLALU RENDAH; MENURUN | **PASS** |
| TC-18 | Delta ekstrem +14 | 14.0 / 0.0 | Turunkan Kuat (<= -75) | Koreksi -86.06 (Turunkan Kuat); TERLALU TINGGI; MENINGKAT | **PASS** |
| TC-19 | Batas stabilitas tren (delta = -0,10) | 3.5 / 3.6 | Diterima; tren STABIL, koreksi positif | Koreksi +65.12 (Naikkan Sedang); TERLALU RENDAH; STABIL | **PASS** |
| TC-20 | Waktu respon inferensi | 6.0 / 5.7 | Selesai < 1 detik (NFR) | 0.07 ms (koreksi -30.0) | **PASS** |

Seluruh kasus lulus. Perlu dicatat, kelulusan 20 dari 20 hanya membuktikan perilaku pada kasus yang dirancang; tidak menjamin kebenaran lapangan.

## 8. Antarmuka dan Dokumentasi (Praktikum 13–15)

Antarmuka `src/app.py` menyediakan slider/ketik manual, badge keputusan berwarna, metrik koreksi, status air, tabel aturan aktif, dan grafik. Dokumentasi: `README.md` (teknis) dan `Modul-3/README_APP.md` (panduan pengguna).

**Status verifikasi.** Kode `app.py` telah lolos uji asap (smoke test) memakai modul Streamlit tiruan pada jalur normal dan jalur input tidak valid. Aplikasi **belum dijalankan di Streamlit asli** pada lingkungan pembuatan ini. Sebelum pameran, jalankan `streamlit run src/app.py`, uji tiga skenario, dan simpan screenshot ke `assets/`.

## 9. Kesimpulan, Keterbatasan, dan Keselamatan

**Kesimpulan.** Sistem Mamdani 9 aturan menghasilkan keputusan koreksi yang berubah halus, konsisten secara tanda dan simetris, dan berjalan jauh di bawah 1 detik. Perbedaan terhadap aturan tegas terkonsentrasi di zona transisi, tempat nilai tambah fuzzy berada.

**Keterbatasan.**
1. Referensi evaluasi adalah aturan tegas, bukan data pakar; MAE/RMSE belum mewakili akurasi lapangan.
2. Hanya dua pengukuran; target tunggal dan simetris.
3. Hanya 9 aturan sehingga resolusi keputusan terbatas.
4. Tidak memodelkan dinamika kimia (kapasitas penyangga, volume, suhu).
5. Centroid tidak mencapai ujung semesta (maksimum sekitar ±86).

**Keselamatan.** Output simulasi tidak boleh dijadikan dosis atau perintah pompa. Penerapan fisik memerlukan kalibrasi sensor pH, validasi rentang target tanaman, pengujian respons aktuator, pengukuran volume larutan, kalibrasi dosis, dan prosedur keselamatan kerja bahan pengatur pH.

## 10. Rencana Pengembangan (belum dilakukan)

- Pembacaan sensor berkala dan pencatatan data riwayat.
- Kalibrasi keluaran menjadi dosis/durasi dengan batas keselamatan, setelah validasi.
- Penalaan otomatis parameter fungsi keanggotaan dengan pendekatan Neuro-Fuzzy/ANFIS memakai data pakar atau data riil.
- Penambahan variabel (suhu, EC) dan lebih banyak himpunan.
- Deploy publik untuk pengujian pengguna.

---

# Lampiran A. Jawaban Pertanyaan Analisis

## Praktikum 11
1. **Mengapa analisis kebutuhan menentukan keberhasilan (bobot 15%)?** Variabel, semesta, dan aturan diturunkan dari rumusan masalah. Bila masalah atau variabel salah, penyetelan parameter tidak dapat memperbaikinya, dan kesalahan itu terbawa ke seluruh tahap (rancangan, kode, uji).
2. **Menguji relevansi dan independensi input.** Lakukan analisis sensitivitas (ubah satu input, tahan yang lain; bila output tidak berubah, input tidak relevan), uji korelasi antar-input pada data riil, dan validasi oleh pakar. Pada proyek ini, `ph_sekarang` dan `delta_ph` saling melengkapi karena `delta_ph` bergantung pada `ph_sebelumnya` yang bebas; grafik sensitivitas menunjukkan keduanya memengaruhi output.
3. **Keuntungan arsitektur modular.** Engine dapat diuji tanpa web server (dipakai oleh skrip evaluasi dan uji black-box), dipakai ulang oleh antarmuka lain (CLI, web, sensor), dan lebih mudah dirawat serta dinilai.

## Praktikum 12
1. **Apakah MAE rendah menjamin semua aturan teruji?** Tidak. Pada data ini 13 dari 22 kasus berselisih nol karena jatuh di titik plateau yang sama untuk fuzzy dan aturan tegas; dataset yang hanya berisi kasus semacam itu akan menghasilkan MAE rendah tanpa menguji zona transisi. Dataset harus mencakup seluruh sel aturan (di sini R1–R9 semuanya aktif) dan zona transisi.
2. **Mengapa RMSE ≥ MAE?** Rata-rata kuadrat (kuadratik) selalu ≥ rata-rata aritmetik (ketidaksetaraan power mean); sama hanya bila semua error sama besar. Di sini RMSE 16.02 vs MAE 7.84 menandakan error yang terpusat pada beberapa kasus. Minimalkan RMSE bila kesalahan besar jauh lebih merugikan (mis. over-koreksi besar), minimalkan MAE bila semua kesalahan setara.
3. **Strategi bila sistem selalu under-estimation.** Geser atau lebarkan himpunan output ke nilai lebih besar, perluas bahu himpunan agar centroid mendekati puncak (di sini saturasi 86,06 < 90), persempit zona transisi, tambah aturan atau himpunan perantara, atau beri bobot aturan; lalu evaluasi ulang. Pada data ini bias rata-rata kecil (-0.38), jadi tidak ada under-estimation sistematis.

## Praktikum 13
1. **Siklus reaktivitas Streamlit.** Setiap interaksi widget membuat Streamlit menjalankan ulang skrip dari atas ke bawah; widget mengembalikan nilai terbaru, inferensi dihitung ulang, dan layar diperbarui. Data yang mahal (decision surface) dicache dengan `st.cache_data` agar tidak dihitung ulang.
2. **Mengapa progress bar dan badge lebih mudah dipahami?** Warna dan ukuran bilah dibaca cepat tanpa interpretasi angka, serta langsung terhubung ke tindakan (aman, waspada, segera), sedangkan derajat keanggotaan desimal memerlukan pengetahuan teori fuzzy.
3. **Langkah deploy publik (verifikasi ke dokumentasi terbaru).** Unggah repositori ke GitHub; pastikan `requirements.txt` berada di akar repositori atau satu folder dengan `app.py`; masuk ke Streamlit Community Cloud, pilih repositori, cabang, dan berkas utama (`Modul-3/Asesmen3_240306045_Izzul_Faraby/src/app.py`); deploy dan bagikan tautannya. Alternatif: jalankan di server dengan `streamlit run src/app.py --server.address 0.0.0.0` dan buka port, atau gunakan Docker.

## Praktikum 14
1. **Mengapa BVA sering menemukan bug pada sistem fuzzy?** Fungsi keanggotaan bersifat sepotong-sepotong dengan titik sambung (a, b, c, d); kesalahan operator pembanding (< vs ≤), pembagian dengan nol pada bahu (a = b), dan galat floating-point (mis. 4,8 − 5,1 = −0,29999…) muncul tepat di batas. Pada proyek ini TC-08 sampai TC-10 dan TC-19 menguji batas target dan ambang tren; hasilnya TC-09 dan TC-10 kontinu (±2,29) walau status tegasnya berganti.
2. **Membuktikan sistem tidak bias.** Sistem ini tidak memakai atribut personal, tetapi bias dapat berupa asimetri arah. Buktinya: uji simetri (TC-17: koreksi(4,8; 5,1) = −koreksi(7,2; 6,9)), kurva sensitivitas yang monoton dan transparan, tabel aturan dan firing strength yang dapat diaudit, cakupan dataset pada semua sel aturan, dan bias rata-rata kecil (-0.38). Catatan: simetri adalah asumsi desain; tanaman dengan target tidak simetris memerlukan penyesuaian.
3. **Pentingnya `requirements.txt` dan dokumentasi.** Keduanya memungkinkan orang lain mereproduksi lingkungan dan hasil tanpa menebak versi atau langkah, mempercepat penilaian, dan menjadi bukti kualitas repositori.

---

# Lampiran B. Antisipasi Pertanyaan Penguji (Defending)

1. **Mengapa memilih bentuk trapesium/segitiga?** Sederhana, murah dihitung, mudah diinterpretasi, dan plateau trapesium mewakili rentang target yang seluruhnya "sesuai".
2. **Mengapa Mamdani, bukan Sugeno?** Aturan dan output linguistik mudah divalidasi pakar, dan kurva agregasi memungkinkan penelusuran. Sugeno lebih ringan secara komputasi tetapi output berupa konstanta kurang ekspresif untuk tujuan interpretasi.
3. **Apakah rule base lengkap dan konsisten?** Ya: 9 dari 9 kombinasi tercakup dan tidak ada IF sama dengan THEN berbeda.
4. **Apa yang terjadi di titik batas?** Lihat TC-08 sampai TC-10: keputusan kontinu karena derajat keanggotaan berubah bertahap.
5. **Bagaimana bila tidak ada aturan aktif?** Fungsi centroid mengembalikan `luas_nol`, koreksi aman = 0, dan peringatan ditampilkan; tidak ada pembagian dengan nol.
6. **Apakah MAE 7.84 baik?** MAE ini mengukur selisih terhadap aturan tegas, bukan data pakar; nilai kecil menunjukkan fuzzy sejalan dengan aturan tegas di luar zona transisi, dan selisih di zona transisi adalah ciri keputusan bertahap. Validasi sungguhan memerlukan data pakar atau operator.
7. **Apakah hasilnya dosis kimia?** Tidak. Output adalah perintah simulasi relatif; tidak berkaitan dengan mL atau mg.
8. **Bagaimana ANFIS dapat membantu?** ANFIS dapat menala parameter fungsi keanggotaan dan aturan dari data berlabel, menggantikan penentuan manual.
