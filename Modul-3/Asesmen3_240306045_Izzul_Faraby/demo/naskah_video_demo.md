# Naskah Video Demo (target 4:30, batas 3–5 menit)

Rekam layar aplikasi (`streamlit run src/app.py`) dan suara Anda. Ganti teks dalam `<...>`.

## 0:00–1:00 — Perkenalan dan masalah
"Halo, saya Izzul Faraby, NIM 240306045. Produk saya HidroFuzzy-pH, sistem pendukung keputusan untuk mengendalikan pH larutan hidroponik.
pH menentukan apakah akar dapat menyerap hara. Target yang saya asumsikan 5,8 sampai 6,2 untuk sayuran daun.
Aturan kaku bermasalah: pH 5,79 dan 5,80 hampir sama, tetapi aturan tegas memberi keputusan berbeda. Selain itu, pH 5,0 yang sedang turun butuh tindakan lain daripada pH 5,0 yang sedang naik. Karena itu saya memakai logika fuzzy.
Ini simulasi, bukan dosis bahan kimia."

## 1:00–2:00 — Arsitektur sistem
(Tampilkan slide 3–5 atau tab Tentang.)
"Input: pH sekarang dan pH sebelumnya. Program menghitung ΔpH otomatis. Ada tiga himpunan untuk pH, tiga untuk ΔpH, dan tujuh untuk koreksi.
Basis aturan 3 kali 3, sembilan aturan. Metode Mamdani: implikasi MIN, agregasi MAX, defuzzifikasi centroid.
Kode dipisah: fuzzy_engine.py untuk logika, app.py untuk antarmuka."

## 2:00–4:00 — Demo langsung
1. (2:00) Jalankan `streamlit run src/app.py`. Tunjukkan sidebar dan panel hasil.
2. (2:20) **Skenario normal:** pH 6,0 sebelumnya 6,0 → Netral. Tunjukkan status air dan grafik.
3. (2:50) **Skenario kritis:** pH 4,8 sebelumnya 5,1 → Naikkan Kuat (sekitar +86). Tunjukkan aturan aktif R1 dan kurva agregasi dengan garis centroid.
4. (3:20) **Zona transisi:** pH 5,5 sebelumnya 5,7 → empat aturan aktif, koreksi sekitar +43,87. Jelaskan firing strength.
5. (3:40) **Validasi:** mode "Ketik manual", ketik `abc` lalu `15` → tampil pesan galat.
6. (3:50) Tab Evaluasi Dataset: tunjukkan MAE dan RMSE serta grafik referensi vs prediksi.

## 4:00–5:00 — Penutup
"Hasil: 20 dari 20 kasus black-box lulus; evaluasi pada 22 skenario menghasilkan MAE 7,84 dan RMSE 16,02 terhadap pembanding aturan tegas. Selisih terbesar ada di zona transisi, yang justru nilai tambah fuzzy.
Keterbatasan: hanya dua pengukuran, target simetris, belum ada data pakar sungguhan, dan belum terhubung perangkat keras.
Rencana: data pakar untuk validasi, penalaan dengan ANFIS, dan sensor setelah kalibrasi. Terima kasih."

Unggah ke YouTube (Unlisted) atau Google Drive, lalu tempel tautan di `demo/link_video_demo.txt`.
