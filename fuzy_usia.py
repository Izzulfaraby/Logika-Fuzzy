import mysql.connector

# Konfigurasi koneksi MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Sesuaikan dengan password MySQL Anda
    "database": "db_fuzzy_usia"
}

def hitung_derajat_otomatis(cursor, nama_tabel, x):
    # Query mengambil baris yang rentang batasnya mencakup nilai x
    query = f"""
        SELECT b_bawah, b_atas, fungsi 
        FROM {nama_tabel} 
        WHERE %s >= b_bawah AND %s <= b_atas 
        LIMIT 1
    """
    cursor.execute(query, (x, x))
    row = cursor.fetchone()
    
    if not row:
        return 0.0
    
    b_bawah, b_atas, fungsi = row
    
    # Perhitungan otomatis berdasarkan isi kolom 'fungsi'
    if fungsi == '1':
        return 1.0
    elif fungsi == '0':
        return 0.0
    elif fungsi == 'trapezium_up':
        # Mencegah error pembagian dengan nol (meskipun tidak mungkin di data ini)
        if b_atas == b_bawah: return 1.0 
        return (x - b_bawah) / (b_atas - b_bawah)
    elif fungsi == 'trapezium_down':
        if b_atas == b_bawah: return 1.0
        return (b_atas - x) / (b_atas - b_bawah)
    else:
        return 0.0

def main():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        print(f"Error koneksi ke database: {err}")
        return

    # Membuat perulangan agar bisa input berkali-kali tanpa harus merestart program
    while True:
        try:
            # MEMINTA INPUT DINAMIS DARI PENGGUNA
            input_user = input("\nMasukkan usia yang ingin dihitung (atau ketik 'keluar' untuk berhenti): ")
            
            if input_user.lower() == 'keluar':
                print("Program dihentikan. Terima kasih!")
                break
                
            x = float(input_user) # Mengubah input teks menjadi angka desimal/float
            
            if x < 0:
                print("Usia tidak boleh negatif. Silakan coba lagi.")
                continue

        except ValueError:
            print("Input tidak valid! Harap masukkan angka.")
            continue
        
        daftar_tabel = [
            ("Bayi", "tb_domain_usia_bayi"),
            ("Anak-anak", "tb_domain_usia_anak"),
            ("Remaja", "tb_domain_usia_remaja"),
            ("Pemuda", "tb_domain_usia_pemuda"),
            ("Dewasa", "tb_domain_usia_dewasa"),
            ("Lansia", "tb_domain_usia_lansia")
        ]
        
        print(f"\n--- Derajat Keanggotaan untuk Usia x = {x} tahun ---")
        for label, tabel in daftar_tabel:
            derajat = hitung_derajat_otomatis(cursor, tabel, x)
            print(f"{label:<12}: {round(derajat, 3)}")
            
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()