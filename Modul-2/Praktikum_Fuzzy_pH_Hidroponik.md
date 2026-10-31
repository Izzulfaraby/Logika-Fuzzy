# Praktikum — Asesmen: Fuzzy Decision System
## Final Practical Assignment: Sistem Pengendalian Kadar pH Air pada Budidaya Hidroponik Berbasis Logika Fuzzy (Metode Mamdani)

**Bobot:** 25% | **Bahasa:** Python 3 | **Metode inferensi:** Mamdani (implikasi MIN, agregasi MAX, defuzzifikasi centroid)

---

## A. Tujuan Praktikum

Praktikum ini menguji kompetensi mahasiswa dalam merancang sistem inferensi fuzzy *end-to-end* pada kasus pengendalian pH larutan hidroponik, mulai dari pemodelan variabel, klasifikasi kondisi air, penyusunan aturan, inferensi Mamdani, defuzzifikasi, hingga visualisasi dan pengujian. Setelah menyelesaikan praktikum ini, mahasiswa mampu:

1. Memahami penerapan logika fuzzy untuk pengendalian kadar pH air pada budidaya hidroponik.
2. Menentukan variabel input dan output serta menghitung perubahan pH secara otomatis dari dua pengukuran.
3. Mengklasifikasikan kondisi air (status kimia, kesesuaian terhadap target, dan tren pH).
4. Merancang fungsi keanggotaan segitiga/trapesium untuk setiap variabel.
5. Menyusun basis aturan IF-THEN yang lengkap, konsisten, dan logis.
6. Mengimplementasikan inferensi fuzzy **Mamdani** (fuzzifikasi, implikasi MIN, agregasi MAX, defuzzifikasi centroid) menggunakan Python.
7. Memvisualisasikan kurva agregasi fuzzy dan *decision surface plot* 3D menggunakan Matplotlib.
8. Menguji sistem, menganalisis keputusan koreksi, dan mendokumentasikannya secara ilmiah dan profesional.

---

## B. Deskripsi Tugas Proyek

### B.1 Latar Belakang

Pada budidaya hidroponik, akar tanaman bersentuhan langsung dengan larutan nutrisi. pH larutan menentukan ketersediaan unsur hara: bila pH terlalu rendah atau terlalu tinggi, sebagian unsur sulit diserap tanaman walaupun konsentrasinya cukup. Karena itu pH harus dijaga di sekitar rentang target. Rentang target yang dipakai pada tugas ini adalah **5,8 – 6,2**, yaitu **asumsi desain** untuk sayuran daun yang **dapat disesuaikan** dengan jenis tanaman dan rekomendasi budidaya.

Pengendalian yang baik tidak hanya melihat pH saat ini, tetapi juga arah pergerakannya. Dua larutan dengan pH 5,0 membutuhkan tindakan berbeda bila yang satu masih **turun** (makin menjauhi target) dan yang lain sedang **naik** (mendekati target). Logika fuzzy sesuai untuk kasus ini karena kondisi seperti "agak rendah" atau "hampir sesuai target" bersifat bertingkat, dan pengetahuan operator dapat dinyatakan sebagai aturan IF-THEN yang mudah dipahami.

Sistem pada praktikum ini menerima **dua input** (`ph_sekarang` dan `ph_sebelumnya`), menghitung **perubahan pH otomatis**, menentukan **kondisi air**, memberikan **keputusan koreksi**, dan menampilkan **visualisasi** dengan Matplotlib.

> **Batasan ruang lingkup.** Sistem ini adalah **simulasi menggunakan Python**, bukan sistem perangkat keras yang terhubung dengan sensor atau pompa fisik. Output berupa **besaran perintah simulasi**, **bukan dosis bahan kimia** yang dapat langsung diterapkan.

### B.2 Alur Kerja Sistem

```text
TAHAP 1 (Pemodelan & Klasifikasi)             TAHAP 2 (Decision System Mamdani)

ph_sekarang ──┐
              ├─► Hitung ΔpH ─► Klasifikasi ─► Fuzzifikasi ─► Basis Aturan ─► Implikasi ─► Agregasi ─► Defuzzifikasi ─► Keputusan
ph_sebelumnya ┘   (otomatis)   (kimia/target/   (derajat μ)    IF-THEN         (MIN)       (MAX)       Centroid         Koreksi
                                tren)                                                                                    + PNG
```

| Tahap | Fungsi pada sistem |
|---|---|
| **Input** | Menerima `ph_sekarang` dan `ph_sebelumnya` (0–14) dan memvalidasinya. |
| **Hitung perubahan pH** | $\Delta pH = pH_{\text{sekarang}} - pH_{\text{sebelumnya}}$, dihitung program, bukan dimasukkan pengguna. |
| **Klasifikasi kondisi air** | Menentukan status kimia, status terhadap target, dan tren pH (nilai tegas/*crisp*, untuk pelaporan). |
| **Fuzzifikasi** | Mengubah nilai crisp menjadi derajat keanggotaan pada himpunan fuzzy. |
| **Basis aturan IF-THEN** | Menyimpan pengetahuan pakar: kombinasi kondisi dan tindakan koreksi. |
| **Implikasi (MIN)** | Menghitung kekuatan aktivasi aturan dengan MIN lalu memotong himpunan output aturan. |
| **Agregasi (MAX)** | Menggabungkan semua hasil aturan menjadi satu himpunan fuzzy output. |
| **Defuzzifikasi centroid** | Mengubah hasil agregasi menjadi satu nilai koreksi numerik. |
| **Keputusan & visualisasi** | Menampilkan nilai koreksi, keputusan yang mudah dipahami, dan menyimpan grafik PNG. |

---

## C. Persyaratan Teknis Minimal

| Komponen | Persyaratan |
|---|---|
| **Variabel input 1** | `ph_sekarang`, rentang 0–14 |
| **Variabel input 2** | `ph_sebelumnya`, rentang 0–14 |
| **Variabel turunan** | `delta_ph = ph_sekarang − ph_sebelumnya` (dihitung otomatis), rentang −14 s.d. +14 |
| **Variabel output** | Tindakan koreksi pH, numerik bertanda, rentang −100 s.d. +100 (satuan simulasi) |
| **Himpunan fuzzy input** | Minimal 3 label per variabel (pH: Rendah, Sesuai Target, Tinggi; ΔpH: Turun, Stabil, Naik) |
| **Himpunan fuzzy output** | 7 himpunan (Naikkan Kuat/Sedang/Ringan, Netral, Turunkan Ringan/Sedang/Kuat) |
| **Basis aturan** | Minimal 6 aturan, disarankan matriks penuh 3 × 3 = 9 aturan |
| **Klasifikasi kondisi air** | Status kimia, status terhadap target, tren pH ditampilkan pada output |
| **Metode inferensi** | **Mamdani saja** |
| **Implikasi / Agregasi / Defuzzifikasi** | MIN / MAX / Centroid |
| **Validasi dan penanganan galat** | Input 0–14 divalidasi; input tidak valid dan kegagalan inferensi ditangani |
| **Bahasa pemrograman** | Python 3 |
| **Library** | NumPy, Matplotlib; `scikit-fuzzy` bila diperlukan (atau implementasi mandiri) |
| **Visualisasi** | Kurva agregasi fuzzy (wajib) dan *decision surface plot* 3D, tersimpan sebagai PNG |
| **Pengujian** | Minimal 5 skenario |

> **Ketentuan wajib:** seluruh rancangan, teori, formula, implementasi, dan pengujian **harus menggunakan metode Mamdani**. Metode Sugeno dan Tsukamoto tidak digunakan pada tugas ini.

---

## D. Panduan Langkah Pengerjaan

### Langkah 1: Variabel Input dan Output serta Perhitungan Perubahan pH

**Input 1 — `ph_sekarang`** (rentang 0–14). Digunakan untuk menentukan kondisi kimia air dan kesesuaian pH terhadap target hidroponik.

**Input 2 — `ph_sebelumnya`** (rentang 0–14). Pengguna **tidak** memasukkan selisih secara manual; program menghitung:

$$
\Delta pH = pH_{\text{sekarang}} - pH_{\text{sebelumnya}}
$$

Rentang matematis `delta_ph` adalah **−14 sampai +14**. Nilai positif berarti pH meningkat, negatif berarti menurun, dan mendekati nol berarti stabil. Pada praktik, selisih antar-pengukuran biasanya kecil (sekitar 0,0–0,5), sehingga sebagian besar semesta ±14 jarang terpakai; semesta lebar dipertahankan agar seluruh kombinasi input valid (0–14) tercakup. Tentukan dan tulis selang waktu antar-pengukuran yang Anda asumsikan.

**Output — Tindakan Koreksi pH** (rentang −100 s.d. +100, satuan simulasi):

- **Negatif:** perintah simulasi untuk **menurunkan** pH.
- **Mendekati nol:** **tidak perlu** koreksi.
- **Positif:** perintah simulasi untuk **menaikkan** pH.

Tujuh himpunan output: Naikkan Kuat, Naikkan Sedang, Naikkan Ringan, Netral, Turunkan Ringan, Turunkan Sedang, Turunkan Kuat.

> **Penegasan:** output adalah **perintah simulasi**, bukan dosis bahan kimia nyata. Satuannya relatif dan tidak berkaitan dengan mL, mg, atau satuan fisik lain.

---

### Langkah 2: Klasifikasi Kondisi Air

Selain inferensi fuzzy, program menampilkan tiga status berbasis nilai tegas (*crisp*) agar kondisi air mudah dibaca. Klasifikasi ini untuk **pelaporan**; keputusan koreksi tetap ditentukan oleh inferensi Mamdani.

**1. Status kimia** (menggunakan nilai asli **sebelum pembulatan**):

| Kondisi | Status |
|---|---|
| pH < 7 | ASAM |
| pH = 7 | NETRAL |
| pH > 7 | BASA |

**2. Status terhadap target hidroponik** (asumsi desain: target 5,8 – 6,2, batas inklusif; sesuaikan dengan tanaman):

| Kondisi | Status |
|---|---|
| pH < 5,8 | TERLALU RENDAH |
| 5,8 ≤ pH ≤ 6,2 | SESUAI TARGET |
| pH > 6,2 | TERLALU TINGGI |

**3. Tren pH** (ambang stabilitas $\theta = 0{,}10$ unit pH, dapat diubah; harus dijelaskan di laporan):

| Kondisi | Tren |
|---|---|
| $\Delta pH < -\theta$ | MENURUN |
| $\lvert\Delta pH\rvert \le \theta$ | STABIL |
| $\Delta pH > \theta$ | MENINGKAT |

> **Catatan penting.** Status kimia dan status target adalah dua hal berbeda: pH 6,0 berstatus kimia **ASAM** (kurang dari 7) tetapi **SESUAI TARGET** untuk hidroponik. Jelaskan pula mengapa batas tegas (misalnya 5,79 → "terlalu rendah") tidak identik dengan derajat fuzzy (5,79 sudah hampir penuh anggota "Sesuai"): klasifikasi tegas dipakai untuk pelaporan, sedangkan kendali memakai derajat keanggotaan bertahap.

Seluruh status tersebut ditampilkan bersama nilai input dan selisih pH pada output program.

---

### Langkah 3: Perancangan Fungsi Keanggotaan

Gunakan fungsi keanggotaan **segitiga** dan **trapesium**, dinyatakan dengan parameter $(a,b,c,d)$:

$$
\mu(x)=
\begin{cases}
0, & x \le a \text{ atau } x \ge d\\[2pt]
\dfrac{x-a}{b-a}, & a < x < b\\[6pt]
1, & b \le x \le c\\[2pt]
\dfrac{d-x}{d-c}, & c < x < d
\end{cases}
$$

Segitiga adalah kasus khusus $b=c$. Bentuk "bahu" diperoleh dengan $a=b$ (bahu kiri) atau $c=d$ (bahu kanan).

**Tabel rancangan (acuan; harus identik dengan kode dan grafik):**

| Variabel | Rentang | Himpunan | Parameter $(a,b,c,d)$ | Penjelasan |
|---|---|---|---|---|
| `ph_sekarang` | 0 – 14 | Rendah | (0; 0; 5,3; 5,8) | Bahu kiri: semua pH rendah; derajat turun linear hingga hilang di 5,8. |
| | | Sesuai Target | (5,3; 5,8; 6,2; 6,7) | Trapesium dengan plateau 5,8–6,2 (target); transisi landai di kedua sisi. |
| | | Tinggi | (6,2; 6,7; 14; 14) | Bahu kanan: semua pH tinggi. |
| `delta_ph` | −14 – +14 | Turun | (−14; −14; −0,3; 0) | Bahu kiri: penurunan ≥ 0,3 dianggap penuh "turun". |
| | | Stabil | (−0,3; 0; 0; 0,3) | Segitiga puncak 0: perubahan kecil dianggap stabil. |
| | | Naik | (0; 0,3; 14; 14) | Bahu kanan: kenaikan ≥ 0,3 dianggap penuh "naik". |
| Koreksi | −100 – +100 | Turunkan Kuat | (−100; −100; −90; −60) | Bahu kiri. |
| | | Turunkan Sedang | (−90; −60; −60; −30) | Segitiga puncak −60. |
| | | Turunkan Ringan | (−60; −30; −30; 0) | Segitiga puncak −30. |
| | | Netral | (−30; 0; 0; 30) | Segitiga puncak 0 (tanpa koreksi). |
| | | Naikkan Ringan | (0; 30; 30; 60) | Segitiga puncak +30. |
| | | Naikkan Sedang | (30; 60; 60; 90) | Segitiga puncak +60. |
| | | Naikkan Kuat | (60; 90; 100; 100) | Bahu kanan. |

Himpunan dirancang saling tumpang tindih dengan jumlah derajat keanggotaan 1 di setiap titik semesta (partisi satuan), sehingga setiap nilai input tercakup oleh minimal satu himpunan.

**Tugas Anda:**
1. Gunakan parameter di atas atau revisi Anda sendiri, dengan alasan tertulis (terutama target pH dan lebar zona "Stabil").
2. Buat grafik fungsi keanggotaan ketiga variabel dan jelaskan setiap himpunan (kode tersedia di Langkah 6).
3. Pastikan rentang, label, dan parameter di grafik, kode, dan laporan **sama persis**. Sumbu ΔpH pada grafik boleh diperbesar (misalnya −1,5 s.d. +1,5) agar bentuk himpunan terbaca; sebutkan hal ini pada keterangan gambar.

---

### Langkah 4: Penyusunan Basis Aturan IF-THEN

**Matriks aturan awal (9 aturan, matriks penuh 3 × 3):**

| pH terhadap Target \ Perubahan pH | Turun | Stabil | Naik |
|---|---|---|---|
| **Rendah** | R1: Naikkan Kuat | R2: Naikkan Sedang | R3: Naikkan Ringan |
| **Sesuai Target** | R4: Naikkan Ringan | R5: Netral | R6: Turunkan Ringan |
| **Tinggi** | R7: Turunkan Ringan | R8: Turunkan Sedang | R9: Turunkan Kuat |

| Aturan | IF pH | AND ΔpH | THEN koreksi | Alasan logis |
|---|---|---|---|---|
| R1 | Rendah | Turun | Naikkan Kuat | Sudah rendah dan masih menjauhi target: koreksi terkuat. |
| R2 | Rendah | Stabil | Naikkan Sedang | Rendah dan tidak bergerak sendiri: koreksi sedang. |
| R3 | Rendah | Naik | Naikkan Ringan | Rendah tetapi sudah naik menuju target: koreksi ringan agar tidak melewati target. |
| R4 | Sesuai Target | Turun | Naikkan Ringan | Masih sesuai tetapi menurun: koreksi dini. |
| R5 | Sesuai Target | Stabil | Netral | Sesuai dan stabil: tidak perlu tindakan. |
| R6 | Sesuai Target | Naik | Turunkan Ringan | Masih sesuai tetapi naik: koreksi dini ke arah menurunkan. |
| R7 | Tinggi | Turun | Turunkan Ringan | Tinggi tetapi sudah turun menuju target: koreksi ringan. |
| R8 | Tinggi | Stabil | Turunkan Sedang | Tinggi dan tidak bergerak sendiri: koreksi sedang. |
| R9 | Tinggi | Naik | Turunkan Kuat | Sudah tinggi dan masih menjauhi target: koreksi terkuat. |

**Tugas evaluasi aturan (wajib ditulis di laporan):**
1. **Kelengkapan:** buktikan seluruh 9 kombinasi memiliki aturan dan tidak ada kombinasi input yang tidak tertangani.
2. **Konsistensi:** buktikan tidak ada dua aturan dengan kondisi IF yang sama tetapi THEN berbeda.
3. **Kesesuaian definisi:** setiap himpunan pada THEN sudah didefinisikan di Langkah 3 dan arah tandanya sesuai konvensi (Naikkan = positif, Turunkan = negatif).
4. **Simetri:** matriks simetris terhadap titik tengah (Rendah↔Tinggi, Turun↔Naik, tanda output berlawanan). Jelaskan manfaat dan keterbatasannya bila target pH tanaman tertentu tidak simetris.
5. **Evaluasi kritis:** jika Anda mengubah aturan, jelaskan alasan teknisnya.

---

### Langkah 5: Inferensi Fuzzy Metode Mamdani

Sistem menggunakan **hanya Mamdani** dengan empat tahap berikut.

**1. Fuzzifikasi.** Nilai crisp $x_1=pH_{\text{sekarang}}$ dan $x_2=\Delta pH$ diubah menjadi derajat keanggotaan, misalnya $\mu_{\text{Rendah}}(x_1)$, $\mu_{\text{Sesuai}}(x_1)$, $\mu_{\text{Tinggi}}(x_1)$ dan $\mu_{\text{Turun}}(x_2)$, $\mu_{\text{Stabil}}(x_2)$, $\mu_{\text{Naik}}(x_2)$.

**2. Implikasi (MIN).** Kekuatan aktivasi aturan ke-$k$:

$$
\alpha_k = \min\big(\mu_{A_k}(x_1),\ \mu_{B_k}(x_2)\big)
$$

Himpunan output aturan dipotong setinggi $\alpha_k$:

$$
\mu_{C_k'}(z) = \min\big(\alpha_k,\ \mu_{C_k}(z)\big)
$$

**3. Agregasi (MAX).**

$$
\mu_{\text{agg}}(z) = \max_{k=1,\dots,9}\ \mu_{C_k'}(z)
$$

**4. Defuzzifikasi centroid.**

$$
z^*=\frac{\int z\,\mu_{\mathrm{agg}}(z)\,dz}
{\int \mu_{\mathrm{agg}}(z)\,dz}
$$

| Simbol | Arti pada sistem pengendalian pH |
|---|---|
| $z$ | Titik pada semesta koreksi (−100 s.d. +100 satuan simulasi). |
| $\mu_{\mathrm{agg}}(z)$ | Derajat keanggotaan hasil agregasi semua aturan pada titik $z$. |
| $\int \mu_{\mathrm{agg}}(z)\,dz$ | Luas daerah di bawah kurva agregasi. |
| $\int z\,\mu_{\mathrm{agg}}(z)\,dz$ | Momen daerah terhadap $z=0$. |
| $z^*$ | Titik berat daerah agregasi = nilai koreksi akhir. |

Pada program, integral didekati secara numerik pada grid output 1001 titik yang seragam, sehingga $z^*\approx\sum z_i\,\mu_{\text{agg}}(z_i)\,/\,\sum \mu_{\text{agg}}(z_i)$; lebar grid pada pembilang dan penyebut saling meniadakan.

**Penanganan agregasi kosong / defuzzifikasi tidak dapat dihitung (wajib).** Jika tidak ada aturan aktif sehingga luas agregasi mendekati nol, rumus centroid menjadi pembagian dengan nol. Program memeriksa luas lebih dulu; bila di bawah `EPS_LUAS`, fungsi `defuzzifikasi_centroid` mengembalikan `None` dan status `luas_nol` **tanpa melakukan pembagian**. Program kemudian menandai inferensi **gagal**, menetapkan koreksi aman **0** (tidak ada tindakan), dan menampilkan peringatan pada keputusan. Dengan basis aturan lengkap dan himpunan yang saling menutup, kondisi ini tidak diharapkan untuk input valid 0–14, tetapi pengamanan tetap wajib.

**Contoh perhitungan manual** (untuk verifikasi pemahaman): $pH_{\text{sekarang}}=5{,}5$ dan $pH_{\text{sebelumnya}}=5{,}7$, sehingga $\Delta pH=-0{,}2$.

- Fuzzifikasi pH: $\mu_{\text{Rendah}}=\dfrac{5{,}8-5{,}5}{5{,}8-5{,}3}=0{,}6$; $\mu_{\text{Sesuai}}=\dfrac{5{,}5-5{,}3}{5{,}8-5{,}3}=0{,}4$; $\mu_{\text{Tinggi}}=0$.
- Fuzzifikasi ΔpH: $\mu_{\text{Turun}}=\dfrac{0-(-0{,}2)}{0-(-0{,}3)}\approx 0{,}667$; $\mu_{\text{Stabil}}=\dfrac{-0{,}2-(-0{,}3)}{0-(-0{,}3)}\approx 0{,}333$; $\mu_{\text{Naik}}=0$.
- Aturan aktif: R1 $\min(0{,}6;\,0{,}667)=0{,}6$ → Naikkan Kuat; R2 $\min(0{,}6;\,0{,}333)=0{,}333$ → Naikkan Sedang; R4 $\min(0{,}4;\,0{,}667)=0{,}4$ → Naikkan Ringan; R5 $\min(0{,}4;\,0{,}333)=0{,}333$ → Netral.
- Agregasi: MAX dari keempat himpunan output terpotong tersebut.
- Centroid: hitung $z^*$ dengan rumus di atas. Hasilnya harus **positif** (himpunan "Naikkan" mendominasi) dan berada di antara puncak Naikkan Ringan (+30) dan Naikkan Sedang (+60), serta lebih kecil daripada bila hanya R1 yang aktif karena R2, R4, dan R5 (Netral) ikut menarik titik berat ke arah nol. Bandingkan dengan keluaran program Anda dan jelaskan selisihnya bila ada.

---

### Langkah 6: Implementasi Program Python

Berikut program referensi lengkap (implementasi mandiri NumPy). Program meminta dua input pH dan memvalidasinya, menghitung `delta_ph` otomatis, menampilkan status kimia, status terhadap target, dan tren, menjalankan Mamdani, lalu menampilkan keputusan serta menyimpan visualisasi PNG. Bagian MIN, MAX, dan centroid ditandai komentar `Tahap 2a/2b`, `Tahap 3`, dan `Tahap 4` pada fungsi `inferensi_inti()` serta `defuzzifikasi_centroid()`.

Program minimal harus mencakup:

1. Input `ph_sekarang` dan `ph_sebelumnya` (0–14) beserta validasinya.
2. Perhitungan `delta_ph` otomatis.
3. Klasifikasi status kimia, status terhadap target, dan tren pH.
4. Pendefinisian semesta dan fungsi keanggotaan input/output.
5. Sembilan aturan IF-THEN.
6. Fuzzifikasi, implikasi MIN, agregasi MAX, dan defuzzifikasi centroid.
7. Tampilan nilai koreksi numerik dan keputusan yang mudah dipahami.
8. Penanganan input tidak valid dan kegagalan inferensi.
9. Visualisasi Matplotlib yang disimpan sebagai PNG.

**Berkas: `ph_hidroponik_mamdani.py`**

```python
"""
ph_hidroponik_mamdani.py
SISTEM PENGENDALIAN KADAR PH AIR PADA BUDIDAYA HIDROPONIK BERBASIS LOGIKA FUZZY
Metode: Mamdani | Implikasi: MIN | Agregasi: MAX | Defuzzifikasi: Centroid

SIMULASI saja: output adalah perintah simulasi, BUKAN dosis bahan kimia.

Penggunaan:
  python ph_hidroponik_mamdani.py                    -> mode interaktif
  python ph_hidroponik_mamdani.py --sekarang 6.2 --sebelumnya 5.9
  python ph_hidroponik_mamdani.py --demo             -> grafik MF, decision surface, tabel pengujian
  Grafik otomatis ditampilkan (dan disimpan PNG). Gunakan --no-show bila tanpa layar,
  --out <folder> untuk mengganti folder keluaran
  (default: folder 'hasil' di samping file skrip ini).
"""

import argparse
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (proyeksi 3D)

# ============================================================
# 1. KONSTANTA DAN SEMESTA PEMBICARAAN
# ============================================================
PH_MIN, PH_MAX = 0.0, 14.0          # ph_sekarang dan ph_sebelumnya
DPH_MIN, DPH_MAX = -14.0, 14.0      # delta_ph = ph_sekarang - ph_sebelumnya
OUT_MIN, OUT_MAX = -100.0, 100.0    # koreksi (satuan simulasi)
N_OUT = 1001                        # resolusi diskretisasi output (langkah 0,2)

TARGET_MIN, TARGET_MAX = 5.8, 6.2   # ASUMSI target pH (sesuaikan dengan tanaman)
AMBANG_STABIL = 0.10                # |delta_ph| <= ambang -> tren STABIL (klasifikasi crisp)
TOL = 1e-9                          # toleransi pembulatan floating-point
EPS_LUAS = 1e-9                     # luas agregasi minimum agar centroid sah

X_OUT = np.linspace(OUT_MIN, OUT_MAX, N_OUT)

# ============================================================
# 2. FUNGSI KEANGGOTAAN
# ============================================================
def trapmf(x, a, b, c, d):
    """Trapesium (a,b,c,d). Segitiga: b == c. Bahu kiri: a == b. Bahu kanan: c == d."""
    x = np.atleast_1d(np.asarray(x, dtype=float))
    y = np.zeros_like(x)
    if b > a:
        m = (x > a) & (x < b)
        y[m] = (x[m] - a) / (b - a)
    y[(x >= b) & (x <= c)] = 1.0
    if d > c:
        m = (x > c) & (x < d)
        y[m] = (d - x[m]) / (d - c)
    return y


PH_SETS = {                                   # input 1: ph_sekarang
    "Rendah": (0.0, 0.0, 5.3, 5.8),
    "Sesuai": (5.3, 5.8, 6.2, 6.7),
    "Tinggi": (6.2, 6.7, 14.0, 14.0),
}
DPH_SETS = {                                  # input 2: delta_ph
    "Turun":  (-14.0, -14.0, -0.3, 0.0),
    "Stabil": (-0.3, 0.0, 0.0, 0.3),
    "Naik":   (0.0, 0.3, 14.0, 14.0),
}
OUT_SETS = {                                  # output: koreksi
    "Turunkan Kuat":   (-100.0, -100.0, -90.0, -60.0),
    "Turunkan Sedang": (-90.0, -60.0, -60.0, -30.0),
    "Turunkan Ringan": (-60.0, -30.0, -30.0, 0.0),
    "Netral":          (-30.0, 0.0, 0.0, 30.0),
    "Naikkan Ringan":  (0.0, 30.0, 30.0, 60.0),
    "Naikkan Sedang":  (30.0, 60.0, 60.0, 90.0),
    "Naikkan Kuat":    (60.0, 90.0, 100.0, 100.0),
}
OUT_MF = {n: trapmf(X_OUT, *p) for n, p in OUT_SETS.items()}

# ============================================================
# 3. BASIS ATURAN 3 x 3 = 9 ATURAN   <<< DI SINILAH ATURAN IF-THEN DIDEFINISIKAN >>>
# ============================================================
# Format setiap aturan: (id, label pH sekarang, label perubahan pH, label output)
# Dibaca: IF ph_sekarang = <label 2> AND delta_ph = <label 3> THEN koreksi = <label 4>
#
# Matriks aturan (baris = pH terhadap target, kolom = perubahan pH):
#
#   pH \ dpH  |      Turun       |      Stabil       |      Naik
#   ----------+------------------+-------------------+------------------
#   Rendah    | R1 Naikkan Kuat  | R2 Naikkan Sedang | R3 Naikkan Ringan
#   Sesuai    | R4 Naikkan Ringan| R5 Netral         | R6 Turunkan Ringan
#   Tinggi    | R7 Turunkan Ringan| R8 Turunkan Sedang| R9 Turunkan Kuat
#
# Untuk menambah/mengubah aturan, cukup edit daftar RULES di bawah ini
# (label harus ada di PH_SETS, DPH_SETS, dan OUT_SETS).
RULES = [
    # --- pH RENDAH: cenderung menaikkan pH ---
    ("R1", "Rendah", "Turun",  "Naikkan Kuat"),     # rendah & masih menjauhi target -> koreksi terkuat
    ("R2", "Rendah", "Stabil", "Naikkan Sedang"),   # rendah & tidak bergerak        -> koreksi sedang
    ("R3", "Rendah", "Naik",   "Naikkan Ringan"),   # rendah tapi sudah naik         -> cukup ringan

    # --- pH SESUAI TARGET: koreksi dini mengikuti arah pergerakan ---
    ("R4", "Sesuai", "Turun",  "Naikkan Ringan"),   # masih sesuai tapi menurun      -> koreksi dini naik
    ("R5", "Sesuai", "Stabil", "Netral"),           # sesuai & stabil                -> tidak perlu tindakan
    ("R6", "Sesuai", "Naik",   "Turunkan Ringan"),  # masih sesuai tapi naik         -> koreksi dini turun

    # --- pH TINGGI: cenderung menurunkan pH ---
    ("R7", "Tinggi", "Turun",  "Turunkan Ringan"),  # tinggi tapi sudah turun        -> cukup ringan
    ("R8", "Tinggi", "Stabil", "Turunkan Sedang"),  # tinggi & tidak bergerak        -> koreksi sedang
    ("R9", "Tinggi", "Naik",   "Turunkan Kuat"),    # tinggi & masih menjauhi target -> koreksi terkuat
]

# ============================================================
# 4. VALIDASI DAN PERHITUNGAN PERUBAHAN PH
# ============================================================
def validasi_ph(nilai, nama):
    """Ubah ke float dan pastikan 0 <= pH <= 14. Raise ValueError bila tidak valid."""
    try:
        v = float(str(nilai).strip().replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError(f"{nama} harus berupa bilangan (contoh: 6.2).")
    if not math.isfinite(v):
        raise ValueError(f"{nama} tidak boleh NaN atau tak hingga.")
    if v < PH_MIN or v > PH_MAX:
        raise ValueError(f"{nama} = {v} di luar rentang {PH_MIN:g}-{PH_MAX:g}.")
    return v


def hitung_delta_ph(ph_sekarang, ph_sebelumnya):
    """delta_ph = ph_sekarang - ph_sebelumnya (rentang -14 s.d. +14).
    Dibulatkan 10 desimal hanya untuk membuang galat floating-point (mis. 4.8-5.1 = -0.2999999999999998)."""
    return round(ph_sekarang - ph_sebelumnya, 10)


# ============================================================
# 5. KLASIFIKASI KONDISI AIR (crisp, memakai nilai asli tanpa pembulatan)
# ============================================================
def status_kimia(ph):
    if ph < 7.0:
        return "ASAM"
    if ph == 7.0:
        return "NETRAL"
    return "BASA"


def status_target(ph):
    if ph < TARGET_MIN - TOL:
        return "TERLALU RENDAH"
    if ph > TARGET_MAX + TOL:
        return "TERLALU TINGGI"
    return "SESUAI TARGET"


def tren_ph(delta):
    if delta > AMBANG_STABIL + TOL:
        return "MENINGKAT"
    if delta < -AMBANG_STABIL - TOL:
        return "MENURUN"
    return "STABIL"


# ============================================================
# 6. MESIN INFERENSI MAMDANI
# ============================================================
def fuzzifikasi(ph, delta):
    """Tahap 1: crisp -> derajat keanggotaan."""
    mu_ph = {n: float(trapmf(ph, *p)[0]) for n, p in PH_SETS.items()}
    mu_dph = {n: float(trapmf(delta, *p)[0]) for n, p in DPH_SETS.items()}
    return mu_ph, mu_dph


def defuzzifikasi_centroid(z, mu_agg):
    """
    Tahap 4: z* = sum(z*mu)/sum(mu) (aproksimasi diskret dari integral, grid seragam).
    Bila luas ~ 0 -> (None, 'luas_nol'); TIDAK ada pembagian dengan nol.
    """
    luas = float(np.sum(mu_agg))
    if luas < EPS_LUAS:
        return None, "luas_nol"
    return float(np.sum(z * mu_agg) / luas), "ok"


def inferensi_inti(ph, delta):
    """Tahap 1-4 pada (ph, delta) yang sudah valid. Dipakai oleh infer() dan decision surface."""
    mu_ph, mu_dph = fuzzifikasi(ph, delta)

    agregat = np.zeros_like(X_OUT)
    aktif = []
    terpotong = {}
    # >>> PEMAKAIAN ATURAN: setiap aturan di RULES (bagian 3) dievaluasi satu per satu di sini <<<
    for rid, l_ph, l_dph, l_out in RULES:
        # IF pH = l_ph AND dpH = l_dph  ->  kekuatan aktivasi (alpha)
        alpha = min(mu_ph[l_ph], mu_dph[l_dph])            # Tahap 2a: MIN (AND)
        if alpha > 0.0:                                    # aturan aktif hanya bila alpha > 0
            # THEN koreksi = l_out  ->  himpunan output dipotong setinggi alpha
            klip = np.minimum(alpha, OUT_MF[l_out])        # Tahap 2b: implikasi MIN
            terpotong[rid] = klip
            agregat = np.maximum(agregat, klip)            # Tahap 3: agregasi MAX
            aktif.append((rid, l_ph, l_dph, l_out, alpha))

    z, st = defuzzifikasi_centroid(X_OUT, agregat)         # Tahap 4: centroid
    return mu_ph, mu_dph, aktif, terpotong, agregat, z, st


def infer(ph_sekarang, ph_sebelumnya):
    """Validasi -> delta -> klasifikasi -> inferensi Mamdani lengkap."""
    ph = validasi_ph(ph_sekarang, "pH sekarang")
    pre = validasi_ph(ph_sebelumnya, "pH sebelumnya")
    delta = hitung_delta_ph(ph, pre)

    mu_ph, mu_dph, aktif, terpotong, agregat, z, st = inferensi_inti(ph, delta)
    berhasil = z is not None
    z_out = z if berhasil else 0.0                         # kegagalan inferensi -> nilai aman 0

    return {
        "ph_sekarang": ph, "ph_sebelumnya": pre, "delta_ph": delta,
        "status_kimia": status_kimia(ph), "status_target": status_target(ph), "tren": tren_ph(delta),
        "mu_ph": mu_ph, "mu_dph": mu_dph, "aturan_aktif": aktif,
        "agregat": agregat, "terpotong": terpotong,
        "koreksi": z_out, "berhasil": berhasil, "status_defuzz": st,
    }


def evaluasi_sistem_fuzzy(ph_sekarang, ph_sebelumnya):
    """Pembungkus: hanya nilai koreksi (dipakai decision surface dan pengujian)."""
    return infer(ph_sekarang, ph_sebelumnya)["koreksi"]


def teks_keputusan(h):
    if not h["berhasil"]:
        return "INFERENSI GAGAL (tidak ada aturan aktif): tidak ada koreksi, periksa sistem"
    z = h["koreksi"]
    a = abs(z)
    if a < 10:
        return "Netral: tidak perlu koreksi (simulasi)"
    arah = "Naikkan" if z > 0 else "Turunkan"
    tingkat = "ringan" if a < 40 else ("sedang" if a < 70 else "kuat")
    return f"{arah} pH tingkat {tingkat} (simulasi)"


# ============================================================
# 7. VISUALISASI
# ============================================================
def plot_agregasi(h, folder):
    """Kurva agregasi: himpunan output, hasil MAX, area, garis centroid (hasil inferensi aktual)."""
    fig, ax = plt.subplots(figsize=(10, 4.8))
    for nama, mf in OUT_MF.items():
        ax.plot(X_OUT, mf, "--", linewidth=0.8, color="gray", alpha=0.7)
    for rid, klip in h["terpotong"].items():
        ax.plot(X_OUT, klip, linewidth=1.0, alpha=0.8, label=f"{rid} (terpotong MIN)")
    ax.fill_between(X_OUT, h["agregat"], color="tab:orange", alpha=0.45, label="Area agregasi (MAX)")
    if h["berhasil"]:
        ax.axvline(h["koreksi"], color="red", linewidth=2, label=f"Centroid z* = {h['koreksi']:+.2f}")
    ax.set_title(f"Kurva Agregasi Mamdani (pH {h['ph_sekarang']:.2f}, sebelumnya {h['ph_sebelumnya']:.2f}, "
                 f"$\\Delta$pH {h['delta_ph']:+.2f})", fontweight="bold")
    ax.set_xlabel("Tindakan koreksi pH (satuan simulasi; + naikkan, - turunkan)")
    ax.set_ylabel("Derajat keanggotaan $\\mu$")
    ax.set_ylim(0, 1.1)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", fontsize=8, ncol=2)
    fig.tight_layout()
    nama = f"agregasi_{h['ph_sekarang']:.2f}_{h['ph_sebelumnya']:.2f}.png"
    fig.savefig(folder / nama, dpi=300)
    return fig, nama


def _plot_mf(x, sets, judul, xlabel, nama_file, folder):
    fig, ax = plt.subplots(figsize=(9, 4))
    for nama, p in sets.items():
        ax.plot(x, trapmf(x, *p), linewidth=2, label=nama)
    ax.set_title(judul, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Derajat keanggotaan $\\mu$")
    ax.set_ylim(-0.05, 1.1)
    ax.grid(alpha=0.3)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5))
    fig.tight_layout()
    fig.savefig(folder / nama_file, dpi=300)
    return fig


def plot_fungsi_keanggotaan(folder):
    _plot_mf(np.linspace(PH_MIN, PH_MAX, 1401), PH_SETS, "Fungsi Keanggotaan pH Sekarang", "pH",
             "mf_ph_sekarang.png", folder)
    _plot_mf(np.linspace(-1.5, 1.5, 1201), DPH_SETS,
             "Fungsi Keanggotaan Perubahan pH (diperbesar: -1,5 s.d. +1,5)", "$\\Delta$pH",
             "mf_delta_ph.png", folder)
    _plot_mf(X_OUT, OUT_SETS, "Fungsi Keanggotaan Tindakan Koreksi",
             "Tindakan koreksi (satuan simulasi)", "mf_koreksi.png", folder)


def plot_decision_surface(folder):
    """X: ph_sekarang (0-14), Y: delta_ph (-14..14), Z: koreksi. Grid dirapatkan di zona transisi."""
    xs = np.unique(np.concatenate([np.linspace(0, 14, 57), np.linspace(5.0, 7.0, 41)]))
    ys = np.unique(np.concatenate([np.linspace(-14, 14, 57), np.linspace(-1.0, 1.0, 41)]))
    X, Y = np.meshgrid(xs, ys)
    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            *_, z, _st = inferensi_inti(X[i, j], Y[i, j])   # Mamdani yang sama dengan infer()
            Z[i, j] = 0.0 if z is None else z

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none", alpha=0.95)
    ax.set_xlabel("pH sekarang")
    ax.set_ylabel("Perubahan pH ($\\Delta$pH)")
    ax.set_zlabel("Koreksi (satuan simulasi)")
    ax.set_title("Decision Surface Mamdani: Pengendalian pH Hidroponik", fontweight="bold")
    fig.colorbar(surf, shrink=0.5, aspect=8, label="Koreksi (satuan simulasi)")
    fig.savefig(folder / "decision_surface.png", dpi=300)
    return fig


# ============================================================
# 8. TAMPILAN HASIL
# ============================================================
def tampilkan_hasil(h, nama_png="-"):
    g = "=" * 40
    print(g)
    print("SISTEM PENGENDALIAN PH HIDROPONIK")
    print("METODE FUZZY MAMDANI")
    print(g)
    print(f"pH sekarang           : {h['ph_sekarang']:.2f}")
    print(f"pH sebelumnya         : {h['ph_sebelumnya']:.2f}")
    print(f"Perubahan pH          : {h['delta_ph']:+.2f}")
    print(f"Status kimia          : {h['status_kimia']}")
    print(f"Status terhadap target: {h['status_target']}")
    print(f"Tren pH               : {h['tren']}")
    print(f"Nilai koreksi         : {h['koreksi']:+.2f} satuan simulasi")
    print(f"Keputusan             : {teks_keputusan(h)}")
    print(f"Visualisasi           : {nama_png}")
    print(g)
    print("Rincian inferensi:")
    print("  mu pH sekarang :", {k: round(v, 3) for k, v in h["mu_ph"].items()})
    print("  mu perubahan pH:", {k: round(v, 3) for k, v in h["mu_dph"].items()})
    if h["aturan_aktif"]:
        for rid, a, b, c, alpha in h["aturan_aktif"]:
            print(f"  {rid}: IF pH={a} AND dpH={b} THEN {c} (alpha={alpha:.3f})")
    else:
        print("  [PERINGATAN] Tidak ada aturan aktif / luas agregasi nol; koreksi diatur aman 0.00.")
    print("Catatan: nilai koreksi = perintah simulasi, BUKAN dosis bahan kimia.")
    print(g)


def proses_dan_tampilkan(ph_sekarang, ph_sebelumnya, folder, tampil=True):
    """Hitung, cetak hasil, simpan PNG kurva agregasi, lalu (opsional) tampilkan jendela grafik."""
    h = infer(ph_sekarang, ph_sebelumnya)
    fig, nama = plot_agregasi(h, folder)
    tampilkan_hasil(h, str(folder / nama))
    if tampil:
        plt.show()          # jendela Matplotlib tampil; tutup jendela untuk melanjutkan
    plt.close(fig)
    return h


# ============================================================
# 9. PENGUJIAN SKENARIO
# ============================================================
SKENARIO = [
    (1, 4.80, 5.10, "Rendah & menurun",   "Naikkan kuat"),
    (2, 4.80, 4.50, "Rendah & meningkat", "Naikkan ringan (lebih kecil dari S1)"),
    (3, 6.00, 6.00, "Sesuai & stabil",    "Netral"),
    (4, 7.50, 7.20, "Tinggi & meningkat", "Turunkan kuat"),
    (5, 7.50, 7.80, "Tinggi & menurun",   "Turunkan ringan (lebih kecil dari S4)"),
]


def jalankan_pengujian():
    print("\n| No | pH sekarang | pH sebelumnya | dpH | Status kimia | Target | Tren | Aturan aktif | Output | Keputusan |")
    print("|---:|---:|---:|---:|---|---|---|---|---:|---|")
    for no, a, b, _, _ in SKENARIO:
        h = infer(a, b)
        ar = ", ".join(f"{r[0]}({r[4]:.2f})" for r in h["aturan_aktif"])
        print(f"| {no} | {a:.2f} | {b:.2f} | {h['delta_ph']:+.2f} | {h['status_kimia']} | {h['status_target']} "
              f"| {h['tren']} | {ar} | {h['koreksi']:+.2f} | {teks_keputusan(h)} |")


# ============================================================
# 10. PROGRAM UTAMA
# ============================================================
def baca_ph(prompt):
    """Minta input sampai valid. Mengembalikan None bila pengguna mengetik 'q'."""
    while True:
        s = input(prompt).strip()
        if s.lower() == "q":
            return None
        try:
            return validasi_ph(s, "Input")
        except ValueError as e:
            print(f"[ERROR] {e} Coba lagi (atau ketik 'q' untuk keluar).")


def mode_interaktif(folder, tampil=True):
    print("Simulasi Pengendalian pH Hidroponik - Fuzzy Mamdani")
    print("Masukkan pH pada rentang 0-14. Ketik 'q' untuk keluar.\n")
    while True:
        try:
            a = baca_ph("pH sekarang   : ")
            if a is None:
                break
            b = baca_ph("pH sebelumnya : ")
            if b is None:
                break
            proses_dan_tampilkan(a, b, folder, tampil)
            jawab = input("Tampilkan decision surface 3D? (y/N): ").strip().lower()
            if jawab == "y":
                fig = plot_decision_surface(folder)
                print(f"Tersimpan: {folder / 'decision_surface.png'}")
                if tampil:
                    plt.show()
                plt.close(fig)
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except Exception as e:  # kegagalan tak terduga: lapor, jangan menjalankan koreksi
            print(f"[GAGAL INFERENSI] {e}. Tidak ada koreksi yang dihasilkan.")


def main():
    p = argparse.ArgumentParser(description="Fuzzy Mamdani - pengendalian pH hidroponik (simulasi)")
    p.add_argument("--sekarang", help="pH sekarang (mode non-interaktif)")
    p.add_argument("--sebelumnya", help="pH sebelumnya (mode non-interaktif)")
    p.add_argument("--demo", action="store_true", help="buat grafik MF, decision surface, dan tabel pengujian")
    p.add_argument("--no-show", action="store_true",
                   help="jangan tampilkan jendela grafik (hanya simpan PNG; untuk server/tanpa layar)")
    p.add_argument("--out", default=None,
                   help="folder keluaran (default: folder 'hasil' di samping file skrip ini, mis. Modul-2/hasil)")
    args = p.parse_args()

    tampil = not args.no_show
    # Default: folder "hasil" dibuat di lokasi file skrip ini (mis. Modul-2/hasil),
    # apa pun folder kerja (current directory) saat program dijalankan.
    folder = Path(args.out) if args.out else Path(__file__).resolve().parent / "hasil"
    folder.mkdir(parents=True, exist_ok=True)

    try:
        if args.demo:
            plot_fungsi_keanggotaan(folder)
            proses_dan_tampilkan(5.5, 5.7, folder, tampil=False)
            plot_decision_surface(folder)
            jalankan_pengujian()
            print(f"\nGambar tersimpan di: {folder.resolve()}")
            if tampil:
                plt.show()          # tampilkan semua grafik sekaligus
        elif args.sekarang is not None and args.sebelumnya is not None:
            proses_dan_tampilkan(args.sekarang, args.sebelumnya, folder, tampil)
        else:
            mode_interaktif(folder, tampil)
    except ValueError as e:
        print(f"[ERROR] {e}")
    except Exception as e:
        print(f"[GAGAL INFERENSI] {e}")


if __name__ == "__main__":
    main()
```

**Cara menjalankan:**

```bash
pip install numpy matplotlib
python ph_hidroponik_mamdani.py                                   # mode interaktif
python ph_hidroponik_mamdani.py --sekarang 6.2 --sebelumnya 5.9   # satu kali hitung
python ph_hidroponik_mamdani.py --demo                            # grafik MF + decision surface + tabel pengujian
```

**Contoh format output** (angka pada bagian "Nilai koreksi" dan "Keputusan" ditulis oleh program; angka contoh di bawah **hanya format**, bukan hasil pengujian Anda):

```text
========================================
SISTEM PENGENDALIAN PH HIDROPONIK
METODE FUZZY MAMDANI
========================================
pH sekarang           : 6.20
pH sebelumnya         : 5.90
Perubahan pH          : +0.30
Status kimia          : ASAM
Status terhadap target: SESUAI TARGET
Tren pH               : MENINGKAT
Nilai koreksi         : [hasil program]
Keputusan             : [interpretasi hasil]
Visualisasi           : [nama file PNG]
========================================
```

**Penjelasan bagian penting kode:**

| Bagian kode | Fungsi |
|---|---|
| `validasi_ph` | Menolak input non-numerik, NaN, dan di luar 0–14 dengan `ValueError`; `baca_ph` meminta ulang sampai valid. |
| `hitung_delta_ph` | Menghitung $\Delta pH$ otomatis (dibulatkan 10 desimal hanya untuk membuang galat floating-point). |
| `status_kimia`, `status_target`, `tren_ph` | Klasifikasi tegas; status kimia memakai nilai asli tanpa pembulatan. |
| `trapmf` | Fungsi keanggotaan trapesium/segitiga (mendukung bahu). |
| `PH_SETS`, `DPH_SETS`, `OUT_SETS`, `RULES` | Parameter dan aturan; harus sama dengan tabel di Langkah 3 dan 4. |
| `inferensi_inti` | `min(...)` = MIN; `np.minimum(alpha, ...)` = implikasi MIN; `np.maximum(agregat, ...)` = agregasi MAX. |
| `defuzzifikasi_centroid` | Centroid dengan pengaman luas nol. |
| `infer` | Alur lengkap: validasi → delta → klasifikasi → Mamdani. |
| `evaluasi_sistem_fuzzy` | Pembungkus yang dipakai pengujian. |
| `plot_agregasi`, `plot_decision_surface` | Dua visualisasi wajib; surface memakai `inferensi_inti` yang sama dengan sistem. |

**Catatan pendekatan.** Anda boleh memakai `scikit-fuzzy` (`skfuzzy.control`) asalkan konfigurasinya Mamdani (implikasi MIN, agregasi MAX, defuzzifikasi `centroid`) dan bagian MIN, MAX, serta centroid ditunjukkan jelas di laporan. Bila Anda mengubah parameter, ubah juga tabel di laporan.

**Catatan jangkauan output.** Karena centroid adalah rata-rata terbobot luas, koreksi tidak mencapai ±100 secara persis, bahkan bila aturan "Kuat" aktif penuh (hasilnya berada di sekitar ±86). Jelaskan fenomena ini pada analisis.

---

### Langkah 7: Visualisasi Matplotlib

Program menghasilkan berkas berikut di folder `hasil/`:

| Berkas | Isi |
|---|---|
| `mf_ph_sekarang.png`, `mf_delta_ph.png`, `mf_koreksi.png` | Grafik fungsi keanggotaan ketiga variabel. |
| `agregasi_<pH sekarang>_<pH sebelumnya>.png` | **Kurva agregasi fuzzy (wajib):** himpunan output, hasil agregasi MAX, area agregasi, dan garis centroid dari hasil inferensi aktual. Dibuat otomatis setiap perhitungan. |
| `decision_surface.png` | ***Decision Surface Plot* 3D:** pH sekarang (sumbu X, 0–14), perubahan pH (sumbu Y, −14 s.d. +14), koreksi (sumbu Z). |

Ketentuan visualisasi:

- Nilai Z pada *decision surface* dihitung oleh sistem Mamdani yang sama untuk setiap titik grid. **Dilarang** memakai data acak atau hasil simulasi yang tidak berasal dari model.
- Semua grafik memiliki judul, label sumbu, legenda atau *colorbar*, dan disimpan sebagai PNG.
- Karena zona transisi berada di sekitar pH 5–7 dan |ΔpH| < 0,5, grid pada kode dirapatkan di area tersebut agar lereng permukaan tertangkap.

**Panduan interpretasi yang harus ditulis di laporan:**
1. Di mana permukaan bernilai positif, mendekati nol, dan negatif? Apakah sesuai konvensi tanda?
2. Mengapa terdapat daerah datar (*plateau*) yang luas? Hubungkan dengan bahu fungsi keanggotaan dan rentang ±14 yang lebar.
3. Mengapa perubahan tajam terjadi hanya di sekitar pH 5–7 dan ΔpH sekitar 0? Hubungkan dengan lebar zona transisi.
4. Bandingkan pengaruh sumbu pH dan sumbu ΔpH terhadap output.
5. (Opsional, nilai tambah) Buat versi *zoom* (pH 4–8, ΔpH −1 s.d. +1) dan jelaskan perbedaan keterbacaannya.

---

### Langkah 8: Pengujian Minimal Lima Skenario

Uji minimal lima skenario berikut (atau skenario Anda sendiri yang mencakup kondisi ekstrem dan normal):

1. pH rendah dan terus menurun.
2. pH rendah tetapi meningkat.
3. pH sesuai target dan stabil.
4. pH tinggi dan terus meningkat.
5. pH tinggi tetapi menurun.

**Template tabel pengujian (diisi dari hasil program Anda):**

| No | pH sekarang | pH sebelumnya | ΔpH (otomatis) | Status air (kimia / target / tren) | Aturan aktif | Hasil yang diharapkan (logis) | Output aktual | Keputusan | Analisis |
|:--:|:--:|:--:|:--:|---|---|---|:--:|---|---|
| 1 | 4,80 | 5,10 | *(isi)* | *(isi)* | *(isi)* | Naikkan kuat | *(isi dari program)* | *(isi)* | *(isi)* |
| 2 | 4,80 | 4,50 | *(isi)* | *(isi)* | *(isi)* | Naikkan ringan (lebih kecil dari S1) | *(isi dari program)* | *(isi)* | *(isi)* |
| 3 | 6,00 | 6,00 | *(isi)* | *(isi)* | *(isi)* | Netral | *(isi dari program)* | *(isi)* | *(isi)* |
| 4 | 7,50 | 7,20 | *(isi)* | *(isi)* | *(isi)* | Turunkan kuat | *(isi dari program)* | *(isi)* | *(isi)* |
| 5 | 7,50 | 7,80 | *(isi)* | *(isi)* | *(isi)* | Turunkan ringan (lebih kecil dari S4) | *(isi dari program)* | *(isi)* | *(isi)* |

**Aturan pengisian:**
- Kolom **"Hasil yang diharapkan"** adalah prediksi logis **sebelum** program dijalankan, berdasarkan matriks aturan.
- Kolom **"Output aktual"**, status, aturan aktif, dan keputusan diisi **hanya** dari eksekusi program Anda. Fungsi `jalankan_pengujian()` (dijalankan via `--demo`) mencetak tabel Markdown berisi kolom-kolom tersebut. Dilarang mengarang angka.
- Bedakan secara jelas yang diharapkan dari yang aktual; bila tidak sesuai, jelaskan penyebabnya (efek MIN, tumpang tindih himpunan, atau efek centroid).
- Tambahkan minimal dua skenario tambahan, misalnya pH di zona transisi (5,5 → 5,7), pH tepat 7,0, batas target 6,2, dan input tidak valid (misalnya 15 atau "abc") untuk menguji validasi.

**Analisis yang diminta untuk setiap skenario:**
1. Himpunan input mana yang aktif dan berapa derajatnya?
2. Aturan mana yang aktif dan berapa $\alpha$-nya?
3. Mengapa output bernilai demikian menurut proses MIN → MAX → centroid?
4. Apakah keputusan konsisten dengan status air (kimia, target, tren)?
5. Bandingkan skenario 1 dengan 4 dan skenario 2 dengan 5: apa yang Anda amati tentang simetri sistem?

---

### Langkah 9: Analisis Hasil, Keterbatasan, dan Keselamatan

Bahas pada laporan:

1. **Konsistensi keputusan:** apakah tanda dan besar output selalu sejalan dengan status air dan aturan?
2. **Keterbatasan model:** hanya dua pengukuran (tanpa riwayat panjang), asumsi target tunggal dan simetris, aturan hanya 9 sehingga resolusi terbatas, tidak memodelkan dinamika kimia larutan (kapasitas penyangga, volume, suhu), serta output centroid yang tidak mencapai ujung semesta.
3. **Pengaruh parameter:** eksperimen sederhana (misalnya lebar zona Stabil atau plateau Sesuai Target) dan dampaknya pada *decision surface*.
4. **Kualitas sistem** dipengaruhi oleh rancangan variabel, parameter fungsi keanggotaan, dan kualitas basis aturan.

> **Catatan keselamatan.** Output simulasi **tidak boleh** langsung dijadikan dosis bahan kimia atau perintah pompa. Penerapan pada perangkat fisik memerlukan **kalibrasi sensor pH, validasi rentang target untuk tanaman terkait, pengujian respons aktuator, pengukuran volume larutan, dan kalibrasi dosis**, serta prosedur keselamatan kerja untuk bahan pengatur pH. Tugas ini tidak mengklaim pengujian atau integrasi perangkat keras apa pun.

---

## E. Template Struktur Laporan Praktikum

Laporan disusun dalam format Markdown (`Laporan_Praktikum_pH_Hidroponik_<NIM>.md`) dengan sistematika berikut. Setiap bagian menyertakan arahan konten.

1. **Identitas dan Judul Proyek.** Judul, nama, NIM, kelas, mata kuliah, tanggal, tautan repositori.
2. **Latar Belakang dan Tujuan.** Pentingnya pengendalian pH, alasan memakai logika fuzzy, tujuan sistem, batasan (simulasi), serta jenis tanaman dan target pH yang diasumsikan beserta rujukannya.
3. **Perancangan Input dan Perhitungan Perubahan pH.** Variabel `ph_sekarang`, `ph_sebelumnya`, `delta_ph`, rentang, rumus, interpretasi tanda, dan selang pengukuran yang diasumsikan.
4. **Fungsi Keanggotaan Fuzzy.** Tabel parameter dan penjelasan tiap himpunan, tiga grafik fungsi keanggotaan, alasan pemilihan parameter.
5. **Basis Aturan IF-THEN.** Matriks 3 × 3, tabel aturan dengan alasan, bukti kelengkapan, konsistensi, dan kesesuaian output.
6. **Inferensi Mamdani dan Defuzzifikasi.** Tahapan, formula, justifikasi pemilihan Mamdani (satu paragraf argumentatif, misalnya aturan linguistik mudah divalidasi pakar, output himpunan yang halus, dan penalaran dapat ditelusuri aturan demi aturan), contoh hitung manual, serta penanganan agregasi kosong.
7. **Implementasi Python.** Kode lengkap, penjelasan modul demi modul, baris yang menjalankan MIN, MAX, dan centroid, validasi input, dan penanganan kegagalan.
8. **Hasil Klasifikasi dan Keputusan Koreksi.** Contoh keluaran program (tangkapan layar/salinan teks asli) beserta penjelasan status kimia, target, tren, dan keputusan.
9. **Visualisasi Matplotlib.** Kurva agregasi dan *decision surface* hasil program, beserta interpretasi sesuai panduan Langkah 7.
10. **Pengujian dan Analisis.** Tabel pengujian (harapan vs. aktual) dan analisis tiap skenario, termasuk skenario tambahan dan uji input tidak valid.
11. **Kesimpulan dan Keterbatasan.** Capaian terhadap tujuan, keterbatasan model, dan catatan keselamatan.
12. **Pengembangan Sistem.** Rencana yang **belum dilakukan** (jangan ditulis sebagai hasil): pembacaan sensor berkala, kalibrasi keluaran menjadi dosis/durasi dengan batas keselamatan, pencatatan data, dan antarmuka aplikasi web; jelaskan tahapan validasi sebelum penerapan fisik.

---

## F. Rubrik Penilaian Praktikum (Bobot: 25%)

| No | Kriteria Penilaian | Deskripsi dan Indikator Terukur | Bobot |
|:--:|---|---|:---:|
| 1 | **Rancangan fuzzy (variabel dan fungsi keanggotaan)** | Variabel input/output sesuai ketentuan; minimal 3 himpunan per input dan 7 himpunan output; semesta dan parameter jelas serta beralasan; grafik benar; rentang di grafik, kode, dan laporan konsisten. | 15% |
| 2 | **Perhitungan perubahan pH** | `delta_ph` dihitung otomatis dengan rumus benar; rentang −14 s.d. +14 dijelaskan; interpretasi tanda dan penanganan galat numerik tepat. | 10% |
| 3 | **Basis aturan** | Minimal 6 (disarankan 9) aturan; seluruh kombinasi tercakup; tidak ada konflik; konvensi tanda konsisten; alasan tiap aturan logis. | 15% |
| 4 | **Implementasi Mamdani** | Fuzzifikasi benar; kekuatan aktivasi MIN; implikasi MIN; agregasi MAX; centroid benar; pengaman agregasi kosong; tanpa Sugeno/Tsukamoto; kode modular dan dapat dijalankan; validasi input dan penanganan kegagalan; justifikasi metode tertulis. | 20% |
| 5 | **Klasifikasi kondisi air** | Status kimia (nilai asli), status terhadap target, dan tren pH benar, dijelaskan asumsinya, dan ditampilkan bersama input serta selisih pH. | 10% |
| 6 | **Visualisasi** | Kurva agregasi dari inferensi aktual (himpunan output, area MAX, centroid) dan *decision surface* 3D dari model yang sama; sumbu X/Y/Z benar; judul, label, legenda/*colorbar*; PNG tersimpan; interpretasi tepat. | 15% |
| 7 | **Pengujian dan dokumentasi** | Minimal 5 skenario; harapan dibedakan dari hasil aktual; output berasal dari eksekusi nyata; analisis mendalam; keterbatasan dan keselamatan dibahas; laporan sesuai sistematika; tidak ada klaim perangkat keras yang belum dilakukan. | 15% |
| | **TOTAL** | | **100%** |

---

## G. Ketentuan Pengumpulan

Berkas wajib dikumpulkan:

- Laporan praktikum `.md`.
- Source code Python `.py` (atau notebook `.ipynb`).
- Gambar visualisasi (grafik fungsi keanggotaan, kurva agregasi, *decision surface*).
- Tabel hasil pengujian (dalam laporan; opsional `.csv`).
- Berkas pendukung lain jika diperlukan (misalnya `requirements.txt`).

**Contoh struktur folder proyek:**

```text
Modul-2/
└── Asesmen2_<NIM>_<Nama>/
    ├── Laporan_Praktikum_pH_Hidroponik_<NIM>.md
    ├── ph_hidroponik_mamdani.py        (atau ph_hidroponik_mamdani.ipynb)
    ├── requirements.txt
    ├── hasil/
    │   ├── mf_ph_sekarang.png
    │   ├── mf_delta_ph.png
    │   ├── mf_koreksi.png
    │   ├── agregasi_<pH sekarang>_<pH sebelumnya>.png
    │   ├── decision_surface.png
    │   └── hasil_pengujian.csv         (opsional)
    └── README.md                       (opsional: cara menjalankan)
```

**Perintah Git:**

```bash
git add Modul-2/
git commit -m "feat(modul2): kumpulkan sistem fuzzy mamdani pengendalian pH hidroponik"
git push origin main
```

---

## H. Ketentuan Penulisan dan Catatan Akhir

1. Gunakan bahasa Indonesia baku dan format Markdown.
2. Pastikan variabel, rumus, aturan, kode, visualisasi, dan pengujian saling konsisten.
3. Gunakan **hanya metode Mamdani** (implikasi MIN, agregasi MAX, defuzzifikasi centroid).
4. **Jangan mengarang hasil eksekusi** dan jangan mengklaim pengujian atau integrasi perangkat keras yang belum dilakukan.
5. Cantumkan sumber untuk setiap rujukan (misalnya target pH tanaman); nilai pada dokumen ini adalah asumsi simulasi.