# controller/parkir_controller.py

from flask import session
from service.parkir_service import *

def log(teks):
    session.setdefault("log", []).append(teks)


def tampil_menu():
    log("1. Kendaraan Masuk")
    log("2. Kendaraan Keluar")
    log("3. Lihat Parkir")
    log("4. Analisis")
    log("5. Keluar")

def format_uang(n):
    return f"Rp {n:,}".replace(",", ".")

# ===== FUNGSI TABEL =====
def tabel(judul, data):
    log("")
    log(f"=== {judul} ===")
    log(f"{'Periode/Tanggal':<20} | {'Jumlah':<22} | {'Pendapatan':<20}")
    log("-" * 75)

    for k, v in data.items():
        
        log(f"{k:<20} | Mobil: {v['mobil']['jml']} mobil {' ':<5}  | Mobil: {format_uang(v['mobil']['biaya'])}")
        
        log(f"{'':<20} | Motor: {v['motor']['jml']} motor {' ':<5}  | Motor: {format_uang(v['motor']['biaya'])}")
        
        log(f"{'':<20} | Total: {v['total_jml']} Kendaraan {' ':<1} | Jumlah: {format_uang(v['total_biaya'])}")
        log("-" * 75)


def proses(inp):
    step = session.get("step", "menu")

    if step == "menu":
        log(f"Pilihan : {inp}")

        if inp == "1":
            session["step"] = "plat"

        elif inp == "2":
            if not daftar_parkir():
                log("Parkiran kosong")
                session["step"] = "pause"
            else:
                session["step"] = "keluar"

        elif inp == "3":
            data = daftar_parkir()
            if not data:
                log("Parkiran kosong")
            else:
                for i, k in enumerate(data, 1):
                    log(f"{i}. {k['plat']}")
            session["step"] = "pause"

        # ===== ANALISIS  =====
        elif inp == "4":
            jml, uang, mobil, motor = total_laporan()
            log(f"Total Kendaraan : {jml} ({mobil} mobil dan {motor} motor)")
            log(f"Total Pendapatan : {format_uang(uang)}")

            tabel("HARI INI", laporan_harian())
            tabel("MINGGU TERAKHIR", laporan_mingguan())
            tabel("BULAN TERAKHIR", laporan_bulanan())
            tabel("TAHUN TERAKHIR", laporan_tahunan())

            session["step"] = "pause"

        elif inp == "5":
            reset_data()
            session.clear()
            return "reset"

    elif step == "plat":
        log(f"Plat : {inp}")
        session["plat"] = inp
        session["step"] = "jenis"

    elif step == "jenis":
        log(f"Jenis : {inp}")
        session["jenis"] = inp
        session["step"] = "merk"

    elif step == "merk":
        log(f"Merk : {inp}")

        hasil = kendaraan_masuk(
            session["plat"],
            session["jenis"],
            inp
        )

        if hasil:
            log("Kendaraan berhasil masuk")
        else:
            log(f'Kendaraan dengan Plat "{session["plat"]}" sudah ada di parkiran')

        session["step"] = "pause"

    elif step == "keluar":
        log(f"Plat : {inp}")
        h = kendaraan_keluar(inp)
        if not h:
            log("Kendaraan tidak ditemukan")
        else:
            log(f"{h['plat']} {h['jenis']} {h['merk']}")
            log(f"Masuk  : {h['masuk']}")
            log(f"Keluar : {h['keluar']}")
            log(f"Durasi : {h['menit']} menit")
            log(f"Biaya  : {format_uang(h['biaya'])}")
        session["step"] = "pause"

    elif step == "pause":
        session["log"] = []
        tampil_menu()
        session["step"] = "menu"

    return "lanjut"
