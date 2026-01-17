data_antrian = []

def tampil_menu():
    print("1. Tambah")
    print("2. Panggil")
    print("3. Tampilkan")
    print("4. Keluar")

def baca_pilihan():
    pilih = input("Masukkan pilihan: ")
    return pilih

def tambah_data():
    orang = input("Masukkan nama: ")

    sudah_ada = False
    for x in data_antrian:
        if x == orang:
            sudah_ada = True
            break

    if sudah_ada == True:
        print(" Nama sudah ada dalam antrian!")
    else:
        data_antrian.append(orang)
        print(" Nama berhasil ditambahkan")

def panggil_data():
    if len(data_antrian) <= 0:
        print("Antrian masih kosong")
    else:
        dipanggil = data_antrian.pop(0)
        print("Memanggil:", dipanggil)

def tampil_data():
    if len(data_antrian) < 1:
        print("Belum ada antrian")
    else:
        print("Daftar antrian:")
        nomor = 1
        for orang in data_antrian:
            print(nomor, orang)
            nomor += 1

def bersih():
    import os
    os.system("clear")
    