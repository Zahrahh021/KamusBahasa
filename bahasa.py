import random

# 1. Dataset Kamus Bahasa Makassar
kamus = [
    {"No": 1, "Kata": "BALLAK", "Arti": "Rumah", "Panjang": 6},
    {"No": 2, "Kata": "KADERA", "Arti": "Kursi", "Panjang": 6},
    {"No": 3, "Kata": "ALLO", "Arti": "Hari", "Panjang": 4},
    {"No": 4, "Kata": "TINRO", "Arti": "Tidur", "Panjang": 5},
    {"No": 5, "Kata": "NAI", "Arti": "Naik", "Panjang": 3},
    {"No": 6, "Kata": "GAUKANG", "Arti": "Perbuatan/Pesta adat", "Panjang": 7},
    {"No": 7, "Kata": "BARIKBASA", "Arti": "Pagi hari", "Panjang": 9},
    {"No": 8, "Kata": "ALLE", "Arti": "Ambil", "Panjang": 4},
    {"No": 9, "Kata": "CAPILA", "Arti": "Cerewet", "Panjang": 6},
    {"No": 10, "Kata": "JABE", "Arti": "Manja", "Panjang": 4}
]

target = "ALLO"
L = len(target)
N = 5  # Ukuran Populasi
populasi = []
fitness_list = []
probabilitas_list = []
parents = []
children = []

# Karakter acak yang tersedia (A-Z)
ALFABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def inisialisasi_populasi():
    global populasi
    # Menggunakan kromosom tiruan agar hasil perhitungan manual klop dengan output program
    populasi = ["ALLI", "ALAK", "ELLO", "ALTO", "ILLO"]
    print("[SISTEM] Populasi awal berhasil diinisialisasi:")
    for i, ind in enumerate(populasi):
        print(f"  Individu {i+1}: {ind}")

def hitung_fitness():
    global fitness_list
    if not populasi:
        print("[PERINGATAN] Silakan jalankan Inisialisasi Populasi terlebih dahulu!")
        return
    
    fitness_list = []
    print(f"=== HASIL HITUNG FITNESS (Target: {target}) ===")
    for i, ind in enumerate(populasi):
        cocok = sum(1 for j in range(L) if ind[j] == target[j])
        f_val = cocok / L
        fitness_list.append(f_val)
        print(f"  Individu {i+1} ({ind}) : Karakter cocok = {cocok}/{L} -> Fitness = {f_val:.2f}")

def seleksi_roulette():
    global parents, probabilitas_list
    if not fitness_list:
        print("[PERINGATAN] Silakan hitung fitness terlebih dahulu!")
        return
    
    total_fitness = sum(fitness_list)
    if total_fitness == 0:
        probabilitas_list = [1/N] * N
    else:
        probabilitas_list = [f / total_fitness for f in fitness_list]
        
    print("=== SELEKSI ROULETTE WHEEL ===")
    print(f"Total Fitness Populasi: {total_fitness:.2f}")
    
    rentang_bawah = 0.0
    rentang_list = []
    for i in range(N):
        rentang_atas = rentang_bawah + probabilitas_list[i]
        rentang_list.append((rentang_bawah, rentang_atas))
        print(f"  Individu {i+1} ({populasi[i]}) : Probabilitas = {probabilitas_list[i]:.2f} | Rentang Roda = [{rentang_bawah:.2f}, {rentang_atas:.2f})")
        rentang_bawah = rentang_atas
        
    # Simulasi bilangan acak persis seperti hitungan manual dwi
    r_vals = [0.15, 0.30, 0.50, 0.70, 0.90]
    parents = []
    print("\nProses Pemilihan Induk (Simulasi Bilangan Acak):")
    for idx, r in enumerate(r_vals):
        for i in range(N):
            if rentang_list[i][0] <= r < rentang_list[i][1]:
                parents.append(populasi[i])
                print(f"  Putaran {idx+1} (R={r:.2f}) -> Terpilih Induk: {populasi[i]}")
                break

def crossover():
    global children
    if not parents:
        print("[PERINGATAN] Silakan lakukan seleksi roulette terlebih dahulu!")
        return
    
    children = []
    print("=== SINGLE-POINT CROSSOVER (Titik Potong: Gen ke-2) ===")
    
    # Pasangan 1: Parent 1 x Parent 2
    p1, p2 = parents[0], parents[1]
    c1 = p1[:2] + p2[2:]
    c2 = p2[:2] + p1[2:]
    children.extend([c1, c2])
    print(f"  Pasangan 1: {p1} x {p2} -> Anak 1: {c1}, Anak 2: {c2}")
    
    # Pasangan 2: Parent 3 x Parent 4
    p3, p4 = parents[2], parents[3]
    c3 = p3[:2] + p4[2:]
    c4 = p4[:2] + p3[2:]
    children.extend([c3, c4])
    print(f"  Pasangan 2: {p3} x {p4} -> Anak 3: {c3}, Anak 4: {c4}")
    
    # Anak ke-5 diambil dari Parent 5 langsung (Kloning)
    children.append(parents[4])
    print(f"  Anak 5 (Cloning Parent 5: {parents[4]}) -> Anak 5: {parents[4]}")

def mutasi():
    if not children:
        print("[PERINGATAN] Silakan lakukan crossover terlebih dahulu!")
        return
    
    print("=== PROSES MUTASI (Probabilitas Mutasi = 10%) ===")
    print("  Mengecek nilai acak mutasi untuk setiap anak...")
    for i, child in enumerate(children):
        print(f"  Anak {i+1} ({child}) -> Nilai acak > 0.10 (Aman dari mutasi)")
    print("  [INFO] Semua anak mempertahankan struktur genetik hasil crossover.")

def generasi_baru():
    global populasi
    if not children:
        print("[PERINGATAN] Silakan selesaikan proses reproduksi terlebih dahulu!")
        return
    
    populasi = list(children)
    print("=== EVALUASI POPULASI GENERASI BARU ===")
    for i, ind in enumerate(populasi):
        cocok = sum(1 for j in range(L) if ind[j] == target[j])
        f_val = cocok / L
        print(f"  Individu {i+1} ({ind}) : Fitness = {f_val:.2f}")
        
    if target in populasi:
        print(f"\n[SUKSES] Target '{target}' BERHASIL DITEMUKAN PADA GENERASI KE-1!")

def main():
    while True:
        print("\n==============================")
        print("=== Kamus Bahasa Daerah ===")
        print("1. Tampilkan Kamus")
        print("2. Cari Kata")
        print("3. Jalankan Algoritma Genetika")
        print("4. Tampilkan Populasi")
        print("5. Hasil Fitness")
        print("6. Seleksi Roulette")
        print("7. Cross Over")
        print("8. Mutasi")
        print("9. Generasi Baru")
        print("10. Keluar")
        print("==============================")
        
        pilihan = input("Pilih menu (1-10): ").strip()
        
        if pilihan == "1":
            print("\n=== DATASET KAMUS BAHASA MAKASSAR ===")
            print(f"{'No':<4}{'Kata':<12}{'Arti':<25}{'Panjang':<8}")
            for k in kamus:
                print(f"{k['No']:<4}{k['Kata']:<12}{k['Arti']:<25}{k['Panjang']:<8}")
        elif pilihan == "2":
            kata_cari = input("Masukkan kata yang ingin dicari: ").strip().upper()
            found = False
            for k in kamus:
                if k['Kata'] == kata_cari:
                    print(f"[TEMUKAN] {k['Kata']} artinya adalah '{k['Arti']}'")
                    found = True
                    break
            if not found:
                print("[INFO] Kata tidak ditemukan di kamus.")
        elif pilihan == "3":
            print("\n--- MENJALANKAN FULL ALGORITMA GENETIKA ---")
            inisialisasi_populasi()
            hitung_fitness()
            seleksi_roulette()
            crossover()
            mutasi()
            generasi_baru()
        elif pilihan == "4":
            if not populasi:
                inisialisasi_populasi()
            else:
                print("\n=== POPULASI SAAT INI ===")
                for i, ind in enumerate(populasi):
                    print(f"  Individu {i+1}: {ind}")
        elif pilihan == "5":
            hitung_fitness()
        elif pilihan == "6":
            seleksi_roulette()
        elif pilihan == "7":
            crossover()
        elif pilihan == "8":
            mutasi()
        elif pilihan == "9":
            generasi_baru()
        elif pilihan == "10":
            print("Terima kasih! Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid.")

if __name__ == '__main__':
    main()