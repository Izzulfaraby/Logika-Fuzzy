# Naskah Presentasi & Lembar Kendali Tanya Jawab
**Proyek:** HidroFuzzy-pH — Sistem Pengendalian Kadar pH Larutan Hidroponik Berbasis Logika Fuzzy (Mamdani)  
**Pemateri:** Izzul Faraby (NIM: 240306045)  
**Program Studi:** S1 Teknologi Informasi  
**Alokasi Waktu (10 Menit):** 5 menit Slide Presentasi · 3 menit Live Demo Aplikasi · 2 menit Tanya Jawab  

---

## Panduan dan Tips Membawakan Presentasi

### Tips Membawakan (5 Butir Praktis)
1. **Atur tempo dan artikulasi:** Bicara dengan ritme stabil (~130 kata/menit), jangan terburu-buru, dan gunakan jeda 1 detik saat pergantian slide.
2. **Fokus pada makna visual:** Tatap penguji dan gunakan slide sebagai penguat visual; jelaskan intuisi sistem, jangan membaca teks slide kata demi kata.
3. **Kuasai angka patokan (Ground Truth):** Ingat angka utama di luar kepala: target pH 5,8–6,2; 20/20 uji black-box lulus; MAE 7,84; RMSE 16,02; dan centroid 43,87 untuk skenario transisi pH 5,5 / 5,7.
4. **Jujur dan tegas mengenai batasan:** Sampaikan secara terbuka bahwa evaluasi memakai pembanding aturan tegas dan keluaran berupa simulasi kendali, bukan takaran dosis kimia.
5. **Jaga disiplin waktu:** Selesaikan naskah slide tepat pada menit ke-05:00 agar Anda memiliki 3 menit penuh untuk demo aplikasi Streamlit dan 2 menit tanya jawab.

### Kalimat Pembuka (Hafalkan)
> *"Selamat pagi Bapak, Ibu dosen penguji, dan rekan-rekan sekalian; hari ini saya mempresentasikan HidroFuzzy-pH, sistem pendukung keputusan pengendali pH hidroponik berbasis logika fuzzy Mamdani yang adaptif, halus, dan dapat ditelusuri."*

### Kalimat Penutup Slide (Hafalkan)
> *"Demikian paparan arsitektur dan evaluasi HidroFuzzy-pH; sistem fuzzy yang berhasil mengubah kekakuan batas Boolean menjadi keputusan kendali yang halus dan andal; mari kita lanjutkan ke sesi demonstrasi interaktif."*

---

## Naskah Lisan Presentasi Per Slide (Total: ~5 Menit / 300 Detik)

### [Slide 1: Judul Proyek] [10 Detik]
Selamat pagi Bapak, Ibu, dan rekan-rekan. Saya Izzul Faraby, mempersembahkan HidroFuzzy-pH, sistem kendali pH hidroponik berbasis logika fuzzy Mamdani.  
*Kata kunci:* HidroFuzzy-pH, kendali pH, Mamdani.

---

### [Slide 2: Masalah dan Urgensi] [40 Detik]
Tanaman hidroponik memerlukan pH yang tepat agar akar dapat menyerap nutrisi dengan optimal. Target ideal sayuran daun diasumsikan berada pada rentang 5,8 hingga 6,2. Pengambilan keputusan tidak cukup melihat pH saat ini saja, tetapi juga arah perubahannya. Kondisi pH 5,0 yang sedang turun tentu memerlukan tindakan berbeda dibanding pH yang sedang naik. Pendekatan aturan tegas memiliki kelemahan mendasar berupa lonjakan keputusan di batas nilai. Pada pH 5,79 sistem tegas menganggap terlalu rendah, sedangkan pada 5,80 dianggap sesuai target. Sebaliknya, logika fuzzy memberikan respons yang sangat halus, yaitu koreksi plus 2,29 berbanding nol koma nol.  
*Kata kunci:* Serapan hara, arah perubahan, diskontinuitas batas.

---

### [Slide 3: Variabel Linguistik] [40 Detik]
Sistem ini memodelkan tiga variabel linguistik. Input pertama adalah pH sekarang dengan rentang semesta 0 hingga 14. Himpunannya mencakup Rendah, Sesuai, dan Tinggi dengan plateau target 5,8 hingga 6,2. Input kedua adalah delta pH yang dihitung otomatis dari selisih dua pengukuran. Himpunannya adalah Turun, Stabil, dan Naik dengan rentang diperbesar untuk visualisasi. Kedua input membentuk partisi satuan sehingga seluruh kombinasi nilai selalu terlayani. Variabel output berupa perintah koreksi simulasi minus 100 hingga plus 100. Output dibagi menjadi tujuh himpunan dari Turunkan Kuat hingga Naikkan Kuat.  
*Kata kunci:* Tiga variabel, partisi satuan, tujuh tindakan.

---

### [Slide 4: Basis Aturan IF-THEN] [40 Detik]
Hubungan antara masukan dan keluaran dirumuskan ke dalam sembilan aturan IF-THEN. Matriks aturan berukuran tiga kali tiga dan mencakup seluruh kombinasi secara lengkap. Rasional perancangan aturan mengikuti kaidah praktis budidaya hidroponik. Jika pH jauh dan terus menjauhi target, sistem memberi koreksi terkuat. Sebaliknya, jika pH sudah bergerak mendekati target, sistem hanya memberi koreksi ringan. Saat pH sesuai dan stabil pada aturan R5, keputusan menjadi netral. Seluruh aturan konsisten tanpa konflik dan bersifat simetris terhadap titik tengah target. Hal ini menjamin perilaku sistem dapat diprediksi dengan andal.  
*Kata kunci:* Matriks sembilan aturan, konsistensi, simetri target.

---

### [Slide 5: Inferensi Mamdani] [50 Detik]
Proses inferensi Mamdani berjalan melalui empat tahap utama. Tahapan tersebut meliputi fuzzifikasi, implikasi MIN, agregasi MAX, dan defuzzifikasi centroid. Sebagai contoh, masukan pH 5,5 dan delta minus 0,2 mengaktifkan empat aturan sekaligus. Hasil defuzzifikasi menghasilkan nilai crisp 43,87 yang bermakna Naikkan Ringan. Angka ini terbukti cocok antara perhitungan manual dan eksekusi program. Kami memilih metode Mamdani karena tiga alasan utama. Pertama, aturan dan keluarannya berbentuk bahasa alami sehingga mudah diverifikasi pakar. Kedua, keluaran berupa himpunan fuzzy yang di-centroid menghasilkan keputusan halus di zona transisi. Ketiga, seluruh proses inferensi dapat ditelusuri visual lewat kurva agregasi kepada pengguna. Meskipun komputasi centroid lebih berat daripada Sugeno, waktu sembilan aturan hanya 0,1 milidetik.  
*Kata kunci:* Fuzzifikasi centroid, verifikasi pakar, transisi halus.

---

### [Slide 6: Arsitektur dan Antarmuka] [40 Detik]
Arsitektur perangkat lunak dirancang modular untuk menjamin keandalan dan keterujian kode. Modul logika murni dipisahkan ke dalam file fuzzy_engine dot py berbasis pustaka NumPy. Pemisahan ini memungkinkan mesin inferensi diuji otomatis tanpa perlu menjalankan server web. Sementara itu, antarmuka pengguna dibangun menggunakan kerangka kerja Streamlit pada file app dot py. Tampilan menyediakan kontrol interaktif, indikator badge status air, serta kurva keanggotaan langsung. Modul visualisasi dan evaluasi data melengkapi sistem untuk analisis grafik serta batch. Seluruh masukan divalidasi ketat sehingga berhasil meloloskan 20 skenario pengujian black-box.  
*Kata kunci:* Arsitektur modular, antarmuka Streamlit, validasi masukan.

---

### [Slide 7: Hasil Evaluasi] [60 Detik]
Keandalan sistem diverifikasi melalui pengujian black-box dan evaluasi dataset batch. Pada pengujian black-box, seluruh 20 skenario dinyatakan lulus seratus persen. Pengujian mencakup kondisi normal, batas ekstrim, simetri target, serta penolakan masukan tidak valid. Untuk evaluasi batch, kami menguji 22 skenario yang mencakup seluruh aturan. Hasil pengujian mencatat nilai MAE 7,84 poin dan RMSE 16,02 poin. Waktu komputasi rata-rata per inferensi sangat cepat, yaitu sekitar 0,1 milidetik. Perlu kami tegaskan bahwa referensi evaluasi berasal dari pembanding aturan tegas, bukan pakar. Sebanyak 13 dari 22 kasus menunjukkan selisih nol karena berada di plateau. Selisih terbesar justru muncul di zona transisi, seperti kasus ID 6 dan 21. Hal ini bukan kesalahan sistem, melainkan bukti bahwa fuzzy memberikan keputusan bertingkat yang halus. Karakteristik transisi bertahap ini menghindarkan aktuator dari sentakan aksi yang mendadak.  
*Kata kunci:* Seratus persen lulus, evaluasi batch, keunggulan transisi.

---

### [Slide 8: Kesimpulan dan Pengembangan] [20 Detik]
Sebagai kesimpulan, HidroFuzzy-pH berhasil menghasilkan keputusan kendali yang halus, cepat, dan simetris. Sistem ini masih berstatus simulasi numerik dan bukan dosis bahan kimia fisik. Pengembangan berikutnya adalah validasi data pakar, penalaan ANFIS, serta integrasi sensor fisik. Terima kasih atas perhatian Anda, mari kita lanjutkan ke demonstrasi aplikasi.  
*Kata kunci:* Keputusan halus, simulasi numerik, rencana ANFIS.

---

## Lembar Tanya Jawab (Prediksi 6 Pertanyaan Penguji)

### 1. Kenapa memilih metode Mamdani, bukan Sugeno atau Tsukamoto?
> **Jawaban:**  
> Mamdani dipilih karena anteseden dan konsekuensinya dinyatakan dalam himpunan linguistik alami ("Naikkan Ringan", "Turunkan Kuat") sehingga sangat intuitif dan mudah divalidasi oleh pakar budidaya hidroponik. Berbeda dengan Sugeno yang menghasilkan nilai konstanta matematis atau Tsukamoto yang mensyaratkan fungsi monoton, Mamdani mempertahankan bentuk kurva fuzzy hingga agregasi sehingga menghasilkan permukaan keputusan yang sangat halus di zona transisi. Meskipun komputasi centroid numerik Mamdani lebih berat daripada rata-rata berbobot Sugeno, waktu inferensi sistem ini hanya 0,1 milidetik untuk 9 aturan, sehingga performa tetap instan dan efisien.

### 2. Kenapa memilih fungsi keanggotaan trapesium daripada segitiga atau Gaussian?
> **Jawaban:**  
> Bentuk trapesium dipilih karena memiliki area puncak datar (*plateau*) yang merepresentasikan rentang toleransi optimal target tanaman (pH 5,8 hingga 6,2) dengan derajat keanggotaan penuh satu. Karakteristik ini lebih realistis untuk nutrisi tanaman daun dibanding segitiga yang hanya memiliki satu titik puncak tunggal. Selain itu, trapesium memakai persamaan linier sepotong-sepotong (*piecewise linear*) yang sangat ringan dikomputasi serta memiliki batas bahu tegas yang mudah diaudit dibanding kurva Gaussian.

### 3. Apakah rule base 3x3 (9 aturan) ini sudah lengkap dan konsisten?
> **Jawaban:**  
> Ya, basis aturan terbukti lengkap karena memetakan seluruh kombinasi 3 himpunan pH sekarang dan 3 himpunan delta pH ($3 \times 3 = 9$ aturan), sehingga tidak ada ruang input yang tidak tertangani. Aturan juga sepenuhnya konsisten tanpa konflik, artinya tidak ada pasangan aturan dengan masukan sama yang menghasilkan aksi kontradiktif. Selain itu, matriks dirancang simetris terhadap titik tengah target 6,0, menjamin perlakuan yang berimbang antara penyimpangan asam dan basa.

### 4. Apa yang terjadi di titik kritis perbatasan, misalnya antara pH 5,79 dan 5,80?
> **Jawaban:**  
> Pada sistem aturan tegas (*Boolean*), terjadi lonjakan diskontinu di mana pH 5,79 divonis "Terlalu Rendah" dengan koreksi penuh, sementara pH 5,80 mendadak dianggap "Sesuai Target" dengan koreksi nol. Pada logika fuzzy, titik 5,79 menghasilkan derajat keanggotaan $\mu_{\text{Rendah}} = 0,02$ dan $\mu_{\text{Sesuai}} = 0,98$, yang menghasilkan keluaran kontinu sebesar $+2,29$ (sangat dekat dengan netral $0,00$). Sifat kontinu ini mencegah aktuator atau pompa dosing mengalami sentakan (*hunting/chattering*) akibat fluktuasi kecil sensor.

### 5. Apakah nilai MAE 7,84 itu tergolong bagus, dan terhadap apa nilai tersebut diukur?
> **Jawaban:**  
> Nilai MAE 7,84 poin dan RMSE 16,02 poin diukur terhadap pembanding aturan tegas (*Boolean*) pada matriks yang sama dalam skala output $-100$ hingga $+100$, bukan terhadap data pakar sungguhan. Nilai selisih ini tergolong sangat wajar karena 13 dari 22 kasus pengujian berada di zona plateau dengan selisih nol ($0,00$), sedangkan selisih terbesar hanya terkonsentrasi pada zona transisi (misalnya kasus ID 6 sebesar 46,13 poin). Selisih di zona transisi tersebut justru membuktikan keunggulan inferensi fuzzy yang memberikan respons bertingkat halus, bukan keputusan biner yang kaku.

### 6. Apakah angka keluaran sistem (misalnya koreksi +43,87) merupakan dosis bahan kimia?
> **Jawaban:**  
> Bukan, keluaran sistem adalah besaran perintah kendali simulasi (*control action*) pada skala relatif $-100$ hingga $+100$, bukan takaran mililiter larutan asam atau basa pekat. Untuk menerapkannya pada sistem fisik nyata, angka tersebut harus dikalibrasi lebih lanjut terhadap volume air tandon nutrisi, kapasitas penyangga (*buffer capacity*) larutan, dan laju alir pompa *dosing*. Proyek ini sengaja dibatasi pada lingkup perancangan algoritma inferensi cerdas dan verifikasi keandalan perangkat lunak.
