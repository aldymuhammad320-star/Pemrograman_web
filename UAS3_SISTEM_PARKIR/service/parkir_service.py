# service/parkir_service.py
from datetime import datetime
import math
from collections import defaultdict
from constants import parkir, riwayat, TARIF
from utils.waktu import hitung_durasi_menit, hitung_biaya

def init_riwayat():
    for r in riwayat:
        # Cek jika data belum memiliki perhitungan menit atau biaya
        if r.get("menit") is None or r.get("biaya") is None:
            
            menit = hitung_durasi_menit(r["masuk"], r["keluar"])

            biaya = hitung_biaya(r["jenis"], menit)
            
            
            r["menit"] = menit
            r["biaya"] = biaya


# ---  Laporan ---
def buat_struktur_kosong():
    return {
        "mobil": {"jml": 0, "biaya": 0},
        "motor": {"jml": 0, "biaya": 0},
        "total_jml": 0,
        "total_biaya": 0
    }

def proses_analisis(format_waktu):
    init_riwayat()
    hasil = defaultdict(buat_struktur_kosong)
    for r in riwayat:
        dt = datetime.strptime(r["keluar"], "%Y-%m-%d %H:%M:%S")
        key = dt.strftime(format_waktu)
        jenis = r["jenis"].lower()
        biaya = r["biaya"]

        if jenis == "mobil":
            hasil[key]["mobil"]["jml"] += 1
            hasil[key]["mobil"]["biaya"] += biaya
        elif jenis == "motor":
            hasil[key]["motor"]["jml"] += 1
            hasil[key]["motor"]["biaya"] += biaya
            
        hasil[key]["total_jml"] += 1
        hasil[key]["total_biaya"] += biaya
    return hasil

# --- Fungsi Menu 4 (Analisis) ---
def laporan_harian(): 
    return proses_analisis("%d-%m-%Y")

def laporan_mingguan(): 
    return proses_analisis("Minggu %U %Y")

def laporan_bulanan(): 
    return proses_analisis("%B %Y")

def laporan_tahunan(): 
    return proses_analisis("%Y")

def total_laporan():
    init_riwayat()
    mobil = sum(1 for r in riwayat if r["jenis"] == "mobil")
    motor = sum(1 for r in riwayat if r["jenis"] == "motor")
    total_biaya = sum(r["biaya"] for r in riwayat)
    return len(riwayat), total_biaya, mobil, motor


# ================= PARKIR =================
def kendaraan_masuk(plat, jenis, merk):
    if any(k["plat"] == plat for k in parkir):
        return False

    parkir.append({
        "plat": plat,
        "jenis": jenis.lower(),
        "merk": merk,
        "masuk": datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    })
    return True

def kendaraan_keluar(plat):
    for i, k in enumerate(parkir):
        if k["plat"] == plat:
            keluar = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Hitung durasi
            durasi_menit = hitung_durasi_menit(k["masuk"], keluar)

            
            if k["jenis"] == "motor":
                tarif = TARIF["motor"]
            elif k["jenis"] == "mobil":
                tarif = TARIF["mobil"]
            else:
                tarif = TARIF["lain"]

            biaya = hitung_biaya(k["jenis"], durasi_menit)

            data = {
                "plat": k["plat"],
                "jenis": k["jenis"],
                "merk": k["merk"],
                "masuk": k["masuk"],
                "keluar": keluar,
                "menit": durasi_menit,
                "biaya": biaya
            }

            parkir.pop(i)
            riwayat.append(data)
            return data

    return None

def daftar_parkir():
    return parkir


def reset_data():
    parkir.clear()
    riwayat.clear()
