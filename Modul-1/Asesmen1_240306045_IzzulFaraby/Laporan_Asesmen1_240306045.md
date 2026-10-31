# 1. JUDUL PROYEK & IDENTITAS MAHASISWA

**Sistem Deteksi Dini Beban Server Berbasis Fuzzy (*Server Overload Warning System*)**
Final Practical Assignment 1 — Fuzzy Modeling Project (Tahap 1: Modeling)

```text
Nama        : [NAMA MAHASISWA]
NIM         : [NIM]
Kelas       : [KELAS]
Mata Kuliah : [MATA KULIAH]
```

> **Status eksekusi:** `server_overload_fuzzy.py` telah dijalankan (Python 3.12, NumPy 2.4, Matplotlib 3.10). Seluruh angka pada laporan adalah hasil program (`output/hasil_eksekusi.txt`) dan cocok dengan hitungan manual (diverifikasi otomatis oleh `verifikasi_manual()`).
> **Data uji adalah data simulasi untuk pengujian model**, bukan data monitoring server nyata.

### CATATAN KETIDAKSESUAIAN
1. **Rumus trapesium pada instruksi** menulis "μ = 0 jika x ≤ a" sebagai kondisi pertama. Untuk bahu kiri `[0,0,20,40]` hal ini menghasilkan μ(0) = 0, padahal seharusnya 1. Implementasi memeriksa plateau (b ≤ x ≤ c) lebih dulu, sehingga bahu bernilai 1 tepat di batas semesta.
2. **Skenario "Kondisi Waspada" (CPU 70, Memory 75)** pada instruksi bukan berarti kedua input berlabel Normal: dengan parameter yang dipakai, CPU 70 → Tinggi 0.50 dan Normal 0.00, Memory 75 → Tinggi 0.75. Nama kasus dipertahankan sebagai konteks, tetapi interpretasi mengikuti angka. Kategori peringatan akhir (Aman/Waspada/Kritis) baru ditentukan oleh rule base di Modul 2.
3. **"Tidak ada gap" tidak sama dengan "partisi menjumlah 1".** Di zona transisi (mis. 35 dan 65) jumlah derajat dua label hanya 0.5; tidak ada celah (selalu ada label dengan μ > 0), tetapi derajat tertinggi di titik itu hanya 0.25.
4. Berkas modul diunggah sebagai `Praktikum5.md` (instruksi menyebut `Praktikum5(1).md`); isinya yang dipakai.

---

# 2. LATAR BELAKANG & DESKRIPSI PERMASALAHAN

Server yang menerima beban melebihi kapasitas dapat mengalami respons lambat, time-out, atau berhenti melayani. Administrator perlu peringatan dini sebelum kondisi itu terjadi. Dua indikator dasar adalah **penggunaan CPU** (kapasitas komputasi) dan **penggunaan memori** (kapasitas penyimpanan kerja; memori hampir penuh dapat memicu *swapping* dan penurunan performa).

Pendekatan ambang tegas (mis. "overload jika CPU > 80%") kurang fleksibel: CPU 79,9% dan 80,1% hanya berbeda 0,2 poin tetapi diperlakukan berlawanan, dan pembacaan sensor yang berfluktuasi di sekitar ambang membuat status peringatan berganti-ganti. Selain itu CPU 65% belum tentu overload, sedangkan 90% sangat mungkin kritis — ada daerah peralihan yang tidak tegas.

Logika fuzzy memodelkan peralihan itu dengan derajat keanggotaan [0,1]. Nilai 65% dapat sekaligus agak Normal dan agak Tinggi. **Tujuan** proyek tahap ini adalah membangun model fuzzy: variabel input (CPU, Memory), variabel output (Server Overload Warning), fungsi keanggotaannya, serta proses fuzzifikasi. **Manfaat**: dasar bagi sistem pendukung keputusan operasional TI yang tahan terhadap fluktuasi dan peralihan kondisi.

**Batasan:** ini adalah *pemodelan fuzzy* (Modul 1). Rule base, inferensi, defuzzifikasi, dan aplikasi monitoring real-time belum dibuat.

**Variabel ketiga tidak ditambahkan** (mis. Network Traffic) agar model tetap fokus pada persyaratan minimal 2 input dan 1 output; dapat ditambahkan pada pengembangan berikutnya.

---

# 3. PERANCANGAN SISTEM FUZZY

## 3.1 Semesta Pembicaraan dan Domain Variabel

| Jenis | Variabel | Satuan | Semesta | Label | Bentuk | Parameter |
|---|---|---|---|---|---|---|
| Input | CPU Usage | % | [0,100] | Rendah | Trapesium (bahu kiri) | [0, 0, 20, 40] |
| Input | CPU Usage | % | [0,100] | Normal | Segitiga | [30, 50, 70] |
| Input | CPU Usage | % | [0,100] | Tinggi | Trapesium (bahu kanan) | [60, 80, 100, 100] |
| Input | Memory Usage | % | [0,100] | Rendah | Trapesium (bahu kiri) | [0, 0, 20, 40] |
| Input | Memory Usage | % | [0,100] | Normal | Segitiga | [30, 50, 70] |
| Input | Memory Usage | % | [0,100] | Tinggi | Trapesium (bahu kanan) | [60, 80, 100, 100] |
| Output | Warning Level | Skor | [0,100] | Aman | Trapesium (bahu kiri) | [0, 0, 25, 45] |
| Output | Warning Level | Skor | [0,100] | Waspada | Segitiga | [30, 50, 70] |
| Output | Warning Level | Skor | [0,100] | Kritis | Trapesium (bahu kanan) | [55, 75, 100, 100] |

**Evaluasi parameter (dihitung program, `validasi_model()`):**

| Variabel | Overlap label bersebelahan | Gap | μ di [0,1] |
|---|---|---|---|
| CPU Usage | Rendah–Normal [30,40]; Normal–Tinggi [60,70] | Tidak ada | Ya |
| Memory Usage | Rendah–Normal [30,40]; Normal–Tinggi [60,70] | Tidak ada | Ya |
| Warning Level | Aman–Waspada [30,45]; Waspada–Kritis [55,70] | Tidak ada | Ya |

Parameter contoh dari instruksi memenuhi syarat sehingga **dipakai tanpa perubahan**. Alasan teknis: bahu kiri/kanan pada label ekstrem menjaga bahwa nilai di ujung semesta terwakili penuh; segitiga Normal bersifat simetris di sekitar 50%; zona transisi 30–40 dan 60–70 cukup lebar untuk peralihan halus. Parameter memory dibuat sama dengan CPU demi kesederhanaan (pada sistem nyata dapat dikalibrasi berbeda karena memori bersifat lebih "mengendap" daripada CPU). Output memakai batas yang lebih rendah di sisi Aman/Kritis (25/75) agar kondisi ekstrem terwakili penuh.

## 3.2 Penurunan Matematis Fungsi Keanggotaan

**Trapesium Trap(a,b,c,d)** (naik dari titik (a,0) ke (b,1): `(y−0)/(1−0) = (x−a)/(b−a)`; turun dari (c,1) ke (d,0): `(y−1)/(0−1) = (x−c)/(d−c)` → `y = (d−x)/(d−c)`):

```
μ(x) = 1               , b ≤ x ≤ c
     = (x − a)/(b − a) , a < x < b
     = (d − x)/(d − c) , c < x < d
     = 0               , selainnya
```

**Segitiga Tri(a,b,c):**

```
μ(x) = (x − a)/(b − a) , a < x ≤ b
     = (c − x)/(c − b) , b < x < c
     = 0               , x ≤ a atau x ≥ c
```

**CPU Usage dan Memory Usage (rumus sama):**

```
Rendah  [0,0,20,40]    : 1 (x ≤ 20) ; (40 − x)/20 (20 < x < 40) ; 0 (x ≥ 40)
Normal  [30,50,70]     : (x − 30)/20 (30 < x ≤ 50) ; (70 − x)/20 (50 < x < 70) ; 0 selainnya
Tinggi  [60,80,100,100]: 0 (x ≤ 60) ; (x − 60)/20 (60 < x < 80) ; 1 (x ≥ 80)
```

**Server Overload Warning:**

```
Aman    [0,0,25,45]     : 1 (x ≤ 25) ; (45 − x)/20 (25 < x < 45) ; 0 (x ≥ 45)
Waspada [30,50,70]      : (x − 30)/20 (30 < x ≤ 50) ; (70 − x)/20 (50 < x < 70) ; 0 selainnya
Kritis  [55,75,100,100] : 0 (x ≤ 55) ; (x − 55)/20 (55 < x < 75) ; 1 (x ≥ 75)
```

### Perhitungan manual

| Nilai | Fungsi | Substitusi | Hasil | Interpretasi |
|---|---|---|---:|---|
| CPU = 65 | μ_Tinggi | (65 − 60)/(80 − 60) = 5/20 | 0.25 | Mulai Tinggi |
| CPU = 65 | μ_Normal | (70 − 65)/(70 − 50) = 5/20 | 0.25 | Masih agak Normal |
| CPU = 65 | μ_Rendah | 65 ≥ 40 | 0.00 | Tidak Rendah |
| CPU = 55 | μ_Normal | (70 − 55)/20 = 15/20 | 0.75 | Cenderung Normal |
| CPU = 55 | μ_Tinggi | 55 ≤ 60 | 0.00 | Belum Tinggi |
| CPU = 35 | μ_Rendah | (40 − 35)/(40 − 20) = 5/20 | 0.25 | Peralihan Rendah–Normal |
| CPU = 35 | μ_Normal | (35 − 30)/20 = 5/20 | 0.25 | Peralihan Rendah–Normal |
| CPU = 70 | μ_Tinggi | (70 − 60)/20 = 10/20 | 0.50 | Setengah Tinggi |
| CPU = 70 | μ_Normal | x ≥ 70 | 0.00 | Di luar Normal |
| Mem = 68 | μ_Tinggi | (68 − 60)/20 = 8/20 | 0.40 | Condong Tinggi |
| Mem = 68 | μ_Normal | (70 − 68)/20 = 2/20 | 0.10 | Sedikit Normal |
| Mem = 75 | μ_Tinggi | (75 − 60)/20 = 15/20 | 0.75 | Cukup Tinggi |
| CPU = 90 | μ_Tinggi | 90 ≥ 80 | 1.00 | Penuh Tinggi |
| Skor = 40 | μ_Aman | (45 − 40)/20 = 5/20 | 0.25 | |
| Skor = 40 | μ_Waspada | (40 − 30)/20 = 10/20 | 0.50 | |
| Skor = 60 | μ_Waspada | (70 − 60)/20 = 10/20 | 0.50 | |
| Skor = 60 | μ_Kritis | (60 − 55)/20 = 5/20 | 0.25 | |

Semua nilai di atas dicocokkan otomatis dengan program (`verifikasi_manual()`: 7 titik cocok, termasuk titik dari tabel ini).

## 3.3 Ilustrasi Grafik Desain

- `output/cpu_usage.png` — tiga label CPU; overlap pada 30–40% dan 60–70%.
- `output/memory_usage.png` — tiga label Memory; bentuk sama dengan CPU.
- `output/server_overload_warning.png` — tiga label output; overlap 30–45 dan 55–70.

Setiap grafik memiliki judul, label sumbu X dan Y, legenda, dan seluruh label linguistik.

![CPU](output/cpu_usage.png)
![Memory](output/memory_usage.png)
![Warning](output/server_overload_warning.png)

---

# 4. IMPLEMENTASI PYTHON

## 4.1 Source Code Lengkap

File `server_overload_fuzzy.py`:

```python
"""
Asesmen Modul 1 - Pemodelan Fuzzy (Tahap 1)
Sistem Deteksi Dini Beban Server (Server Overload Warning System)

Cakupan : variabel input/output, fungsi keanggotaan, fuzzifikasi, visualisasi, pengujian.
Di luar cakupan (Modul 2): rule base, inferensi, agregasi, defuzzifikasi.
Library : hanya NumPy dan Matplotlib (tanpa library fuzzy).
"""
import os
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "output"


# ==========================================================
# 1. FUNGSI KEANGGOTAAN DASAR
# ==========================================================
def trapmf(x, a, b, c, d):
    """
    Trapesium Trap(a,b,c,d). Mendukung bahu: a == b (bahu kiri) dan c == d (bahu kanan).
    Kondisi plateau (b <= x <= c) diperiksa lebih dulu agar bahu bernilai 1 tepat di batas
    semesta (mis. x = 0 pada [0,0,20,40]).
    """
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        naik = (x - a) / (b - a)
        turun = (d - x) / (d - c)
    hasil = np.select(
        [(x >= b) & (x <= c), (x > a) & (x < b), (x > c) & (x < d)],
        [1.0, naik, turun],
        default=0.0,
    )
    return hasil


def trimf(x, a, b, c):
    """Segitiga Tri(a,b,c) dengan puncak di b (mu(b) = 1)."""
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        naik = (x - a) / (b - a)
        turun = (c - x) / (c - b)
    return np.select([x == b, (x > a) & (x < b), (x > b) & (x < c)],
                     [1.0, naik, turun], default=0.0)


# ==========================================================
# 2. FUNGSI KEANGGOTAAN PER LABEL
# ==========================================================
def cpu_rendah(x):   return trapmf(x, 0, 0, 20, 40)
def cpu_normal(x):   return trimf(x, 30, 50, 70)
def cpu_tinggi(x):   return trapmf(x, 60, 80, 100, 100)

def memory_rendah(x): return trapmf(x, 0, 0, 20, 40)
def memory_normal(x): return trimf(x, 30, 50, 70)
def memory_tinggi(x): return trapmf(x, 60, 80, 100, 100)

def warning_aman(x):    return trapmf(x, 0, 0, 25, 45)
def warning_waspada(x): return trimf(x, 30, 50, 70)
def warning_kritis(x):  return trapmf(x, 55, 75, 100, 100)


# ==========================================================
# 3. MODEL VARIABEL LINGUISTIK
# ==========================================================
VARIABEL = {
    "cpu": {
        "nama": "CPU Usage", "satuan": "%", "semesta": (0, 100),
        "label": {"rendah": cpu_rendah, "normal": cpu_normal, "tinggi": cpu_tinggi},
        "warna": {"rendah": "#2ca02c", "normal": "#ff7f0e", "tinggi": "#d62728"},
        "file": "cpu_usage.png",
    },
    "memory": {
        "nama": "Memory Usage", "satuan": "%", "semesta": (0, 100),
        "label": {"rendah": memory_rendah, "normal": memory_normal, "tinggi": memory_tinggi},
        "warna": {"rendah": "#2ca02c", "normal": "#ff7f0e", "tinggi": "#d62728"},
        "file": "memory_usage.png",
    },
    "warning": {
        "nama": "Server Overload Warning", "satuan": "Skor Peringatan", "semesta": (0, 100),
        "label": {"aman": warning_aman, "waspada": warning_waspada, "kritis": warning_kritis},
        "warna": {"aman": "#2ca02c", "waspada": "#ff7f0e", "kritis": "#d62728"},
        "file": "server_overload_warning.png",
    },
}
VARIABEL_INPUT = ("cpu", "memory")


# ==========================================================
# 4. FUZZIFIKASI
# ==========================================================
def fuzzifikasi_variabel(nama_var, nilai):
    """Derajat keanggotaan satu nilai crisp pada seluruh label sebuah variabel."""
    var = VARIABEL[nama_var]
    lo, hi = var["semesta"]
    if not (lo <= nilai <= hi):
        raise ValueError(f"{var['nama']}={nilai} di luar semesta [{lo}, {hi}]")
    return {lbl: round(float(f(nilai)), 4) for lbl, f in var["label"].items()}


def fuzzifikasi(input_dict):
    """
    input_dict : {"cpu": 65, "memory": 70}
    return     : {"cpu": {"rendah":..,"normal":..,"tinggi":..}, "memory": {...}}
    """
    return {k: fuzzifikasi_variabel(k, v) for k, v in input_dict.items()}


def label_dominan(derajat, eps=1e-9):
    maks = max(derajat.values())
    kandidat = [k for k, v in derajat.items() if abs(v - maks) < eps]
    return "/".join(kandidat), maks


def interpretasi(hasil):
    """Ringkasan teks otomatis berdasarkan angka hasil fuzzifikasi."""
    bagian = []
    for k in VARIABEL_INPUT:
        dom, nilai = label_dominan(hasil[k])
        aktif = [l for l, v in hasil[k].items() if v > 0]
        status = "transisi" if len(aktif) > 1 else "tunggal"
        bagian.append(f"{k.upper()}: {dom} ({nilai:.2f}), {status}")
    return "; ".join(bagian)


# ==========================================================
# 5. VISUALISASI
# ==========================================================
def plot_variabel(nama_var, folder=OUTPUT_DIR, tampilkan=False):
    var = VARIABEL[nama_var]
    os.makedirs(folder, exist_ok=True)
    x = np.linspace(*var["semesta"], 1001)
    plt.figure(figsize=(10, 5.2))
    for lbl, f in var["label"].items():
        plt.plot(x, f(x), label=lbl.capitalize(), color=var["warna"][lbl], linewidth=2.6)
    plt.title(f"Fungsi Keanggotaan: {var['nama']}", fontsize=13, fontweight="bold")
    plt.xlabel(f"{var['nama']} ({var['satuan']})")
    plt.ylabel("Derajat Keanggotaan μ(x)")
    plt.ylim(-0.05, 1.1)
    plt.xlim(*var["semesta"])
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="center right")
    plt.tight_layout()
    path = os.path.join(folder, var["file"])
    plt.savefig(path, dpi=300)
    if tampilkan:
        plt.show()
    plt.close()
    return path


# ==========================================================
# 6. DATA UJI (DATA SIMULASI UNTUK PENGUJIAN MODEL - bukan data monitoring nyata)
# ==========================================================
DATA_UJI = [
    ("Ekstrem bawah (idle)",      {"cpu": 5,   "memory": 10}),
    ("Server normal",             {"cpu": 20,  "memory": 30}),
    ("Beban mulai meningkat",     {"cpu": 55,  "memory": 60}),
    ("Transisi",                  {"cpu": 65,  "memory": 68}),
    ("Waspada",                   {"cpu": 70,  "memory": 75}),
    ("Titik batas parameter",     {"cpu": 60,  "memory": 40}),
    ("Beban sangat tinggi",       {"cpu": 90,  "memory": 92}),
    ("Ekstrem atas (saturasi)",   {"cpu": 100, "memory": 100}),
]


def tabel_pengujian():
    baris = []
    baris.append("| No | Kasus | CPU | Mem | CPU Rendah | CPU Normal | CPU Tinggi | "
                 "Mem Rendah | Mem Normal | Mem Tinggi | Interpretasi |")
    baris.append("|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for i, (kasus, data) in enumerate(DATA_UJI, 1):
        h = fuzzifikasi(data)
        c, m = h["cpu"], h["memory"]
        baris.append(f"| {i} | {kasus} | {data['cpu']} | {data['memory']} | "
                     f"{c['rendah']:.2f} | {c['normal']:.2f} | {c['tinggi']:.2f} | "
                     f"{m['rendah']:.2f} | {m['normal']:.2f} | {m['tinggi']:.2f} | {interpretasi(h)} |")
    return "\n".join(baris)


# ==========================================================
# 7. VALIDASI MODEL
# ==========================================================
def validasi_model():
    """Memeriksa rentang [0,1], tidak ada gap, dan overlap antar label bersebelahan."""
    print("VALIDASI MODEL")
    for nama, var in VARIABEL.items():
        x = np.linspace(*var["semesta"], 10001)
        mus = [f(x) for f in var["label"].values()]
        semua = np.array(mus)
        assert semua.min() >= 0.0 and semua.max() <= 1.0, "mu di luar [0,1]"
        cakupan = semua.max(axis=0).min()
        assert cakupan > 0.0, "ada gap"
        overlap = []
        for i in range(len(mus) - 1):
            mask = (mus[i] > 0) & (mus[i + 1] > 0)
            assert mask.any(), "label bersebelahan tidak overlap"
            overlap.append(f"[{x[mask].min():.1f}, {x[mask].max():.1f}]")
        print(f"  {var['nama']:<24}: mu dalam [0,1]; cakupan minimum max-mu = {cakupan:.4f} (>0, tanpa gap); "
              f"overlap = {', '.join(overlap)}")


def verifikasi_manual():
    """Membandingkan hitungan manual (laporan) dengan hasil program."""
    manual = [
        ("cpu", 65, {"rendah": 0.0, "normal": 0.25, "tinggi": 0.25}),
        ("cpu", 55, {"rendah": 0.0, "normal": 0.75, "tinggi": 0.0}),
        ("cpu", 35, {"rendah": 0.25, "normal": 0.25, "tinggi": 0.0}),
        ("memory", 68, {"rendah": 0.0, "normal": 0.1, "tinggi": 0.4}),
        ("memory", 75, {"rendah": 0.0, "normal": 0.0, "tinggi": 0.75}),
        ("warning", 40, {"aman": 0.25, "waspada": 0.5, "kritis": 0.0}),
        ("warning", 60, {"aman": 0.0, "waspada": 0.5, "kritis": 0.25}),
    ]
    for var, nilai, harapan in manual:
        hasil = fuzzifikasi_variabel(var, nilai)
        for lbl, v in harapan.items():
            assert abs(hasil[lbl] - v) < 1e-9, f"{var}({nilai}).{lbl}: program {hasil[lbl]} != manual {v}"
    print(f"  Verifikasi hitungan manual vs program: {len(manual)} titik cocok.")


# ==========================================================
# 8. PROGRAM UTAMA
# ==========================================================
if __name__ == "__main__":
    for nama in VARIABEL:
        print("Grafik tersimpan:", plot_variabel(nama))

    print()
    validasi_model()
    verifikasi_manual()

    print("\nTABEL HASIL FUZZIFIKASI (data simulasi untuk pengujian model)")
    print(tabel_pengujian())

    print("\nDEMO FUNGSI OUTPUT (evaluasi fungsi keanggotaan skor; BUKAN hasil inferensi)")
    print("| Skor | Aman | Waspada | Kritis |")
    print("|---:|---:|---:|---:|")
    for s in (10, 40, 50, 60, 90):
        w = fuzzifikasi_variabel("warning", s)
        print(f"| {s} | {w['aman']:.2f} | {w['waspada']:.2f} | {w['kritis']:.2f} |")
```

## 4.2 Penjelasan Modul & Struktur Data

| Komponen | Fungsi |
|---|---|
| `trapmf(x,a,b,c,d)` | Fungsi trapesium (mendukung bahu a=b atau c=d); plateau diperiksa lebih dulu agar μ(0)=1 pada bahu kiri. |
| `trimf(x,a,b,c)` | Fungsi segitiga, puncak μ(b)=1. |
| `cpu_*`, `memory_*`, `warning_*` | Sembilan fungsi keanggotaan, masing-masing memanggil `trapmf`/`trimf` dengan parameter pada tabel 3.1. |
| `VARIABEL` | Dictionary pemodelan variabel linguistik: nama, satuan, semesta, kamus label → fungsi, warna, nama file grafik. |
| `fuzzifikasi_variabel(nama, nilai)` | Derajat keanggotaan satu nilai; menolak nilai di luar semesta (`ValueError`). |
| `fuzzifikasi(input_dict)` | Menerima `{"cpu":..,"memory":..}`, mengembalikan kamus bersarang derajat per label (nilai dibulatkan 4 desimal). |
| `label_dominan`, `interpretasi` | Menentukan label dengan μ tertinggi (imbang bila sama) dan menandai status transisi bila ≥ 2 label aktif. |
| `plot_variabel(nama)` | Membuat dan menyimpan grafik PNG ke folder `output/`. |
| `DATA_UJI`, `tabel_pengujian()` | 8 data simulasi dan pembuat tabel Markdown. |
| `validasi_model()` | Memeriksa μ ∈ [0,1], tidak ada gap, overlap bersebelahan. |
| `verifikasi_manual()` | Membandingkan 7 titik hitungan manual dengan program (`assert`). |

Contoh keluaran `fuzzifikasi({"cpu": 65, "memory": 68})`:

```python
{"cpu": {"rendah": 0.0, "normal": 0.25, "tinggi": 0.25},
 "memory": {"rendah": 0.0, "normal": 0.1, "tinggi": 0.4}}
```

---

# 5. HASIL PENGUJIAN & EVALUASI FUZZIFIKASI

## 5.1 Tabel Pengujian (8 skenario ≥ 5; **data simulasi untuk pengujian model**)

Data dipilih untuk mewakili ekstrem bawah, normal, peningkatan, transisi, batas parameter, dan ekstrem atas; nilai 20/30, 55/60, 70/75, 90/92, 65/68 berasal dari instruksi, sisanya ditambahkan agar ekstrem bawah/atas dan titik batas terwakili.

| No | Kasus | CPU | Mem | CPU Rendah | CPU Normal | CPU Tinggi | Mem Rendah | Mem Normal | Mem Tinggi |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Ekstrem bawah (idle) | 5 | 10 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 |
| 2 | Server normal | 20 | 30 | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 0.00 |
| 3 | Beban mulai meningkat | 55 | 60 | 0.00 | 0.75 | 0.00 | 0.00 | 0.50 | 0.00 |
| 4 | Transisi | 65 | 68 | 0.00 | 0.25 | 0.25 | 0.00 | 0.10 | 0.40 |
| 5 | Waspada | 70 | 75 | 0.00 | 0.00 | 0.50 | 0.00 | 0.00 | 0.75 |
| 6 | Titik batas parameter | 60 | 40 | 0.00 | 0.50 | 0.00 | 0.00 | 0.50 | 0.00 |
| 7 | Beban sangat tinggi | 90 | 92 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 |
| 8 | Ekstrem atas (saturasi) | 100 | 100 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 |

Demo evaluasi fungsi keanggotaan output (bukan hasil inferensi):

| Skor | Aman | Waspada | Kritis |
|---:|---:|---:|---:|
| 10 | 1.00 | 0.00 | 0.00 |
| 40 | 0.25 | 0.50 | 0.00 |
| 50 | 0.00 | 1.00 | 0.00 |
| 60 | 0.00 | 0.50 | 0.25 |
| 90 | 0.00 | 0.00 | 1.00 |

## 5.2 Interpretasi Hasil Derajat Keanggotaan

1. **Ekstrem bawah (5, 10).** CPU dan Memory sepenuhnya Rendah (1.00); tanpa overlap. Server idle; tidak ada indikasi overload.
2. **Server normal (20, 30).** CPU Rendah penuh (1.00). Memory 30 berada di lereng Rendah (0.50) dan belum masuk Normal (0.00, karena segitiga Normal baru mulai di atas 30). Kondisi cenderung aman; memory setengah Rendah, belum Normal.
3. **Beban mulai meningkat (55, 60).** CPU dominan Normal (0.75), Tinggi masih 0 (55 < 60). Memory 60 setengah Normal (0.50) dan Tinggi baru mulai tepat di 60 (0.00). Beban meningkat tetapi belum Tinggi; ini kondisi pantau.
4. **Transisi (65, 68).** CPU Normal 0.25 dan Tinggi 0.25 — sama kuat, kategori tidak dapat dipastikan; Memory condong Tinggi (0.40) dengan sisa Normal (0.10). Contoh nyata daerah peralihan yang tidak dapat ditangani ambang tegas.
5. **"Waspada" (70, 75).** CPU 70 sudah keluar dari Normal (0.00) dan setengah Tinggi (0.50); Memory Tinggi 0.75. Keduanya condong Tinggi, namun belum penuh; beban berat yang perlu perhatian. Keputusan peringatan akhirnya ditentukan rule base di Modul 2.
6. **Titik batas parameter (60, 40).** CPU 60 tepat di titik awal naiknya Tinggi, sehingga Tinggi 0.00 dan Normal 0.50; Memory 40 tepat di akhir Rendah (0.00) dan Normal 0.50. Menunjukkan bahwa di titik batas fungsi bersifat kontinu (tanpa lompatan).
7. **Beban sangat tinggi (90, 92).** CPU dan Memory Tinggi penuh (1.00) — indikasi kuat kondisi kritis.
8. **Ekstrem atas (100, 100).** Tinggi penuh pada keduanya; bahu kanan menjamin nilai di ujung semesta tetap terwakili.

**Overlap dan pembacaan derajat:** hanya kasus 4 yang memiliki dua label CPU aktif dan memory dua label aktif sekaligus; kasus lain berada pada satu label dominan atau pada lereng satu label (jumlah derajat < 1, mis. Memory 30 → 0.50). Ini sah dalam fuzzy karena derajat keanggotaan bukan probabilitas.

---

# 6. KESIMPULAN & RENCANA PENGEMBANGAN MODUL 2

**Kesimpulan.** Model fuzzy Tahap 1 telah dirancang dengan 2 input (CPU, Memory) dan 1 output (Warning Level), masing-masing 3 label, kombinasi trapesium dan segitiga, tanpa gap dan dengan overlap yang divalidasi program. Fuzzifikasi 8 data simulasi memberikan derajat yang sama dengan hitungan manual, dan kasus transisi (CPU 65, Memory 68) memperlihatkan keunggulan fuzzy dibanding ambang tegas.

**Keterbatasan:** parameter memory sama dengan CPU dan tidak dikalibrasi dengan data server nyata; data uji bersifat simulasi; belum ada rule base maupun keluaran peringatan hasil inferensi.

**Rencana Modul 2:** menyusun rule base (mis. JIKA CPU Tinggi DAN Memory Tinggi MAKA Kritis), inferensi Mamdani dengan operator min/max, agregasi, defuzzifikasi (centroid) untuk menghasilkan skor peringatan. Modul 3: antarmuka web; opsional input Network Traffic atau Response Time dan integrasi pembacaan metrik server.

**Pengumpulan (sesuai modul):**
```bash
git add Modul-1/
git commit -m "feat(modul1): kumpulkan final practical assignment 1 fuzzy modeling"
git push origin main
```
