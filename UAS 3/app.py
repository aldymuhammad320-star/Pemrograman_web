from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

data_parkir = []

# Tarif per kendaraan
TARIF = {"motor": 180000, "mobil": 360000}

# RIWAYAT MASUK (BULANAN & MINGGUAN SUDAH ADA)
riwayat_masuk = [
    # BULANAN
    {"plat": "B1234XYZ", "jenis": "motor", "merk": "Honda Beat", "tanggal": datetime(2025, 12, 5, 9, 10)},
    {"plat": "B5678ABC", "jenis": "mobil", "merk": "Avanza", "tanggal": datetime(2025, 12, 12, 14, 30)},
    {"plat": "B4321DEF", "jenis": "motor", "merk": "Yamaha Mio", "tanggal": datetime(2025, 12, 20, 10, 45)},
    {"plat": "B8765GHI", "jenis": "mobil", "merk": "Xenia", "tanggal": datetime(2025, 12, 28, 16, 20)},

    # MINGGUAN
    {"plat": "B1111JKL", "jenis": "motor", "merk": "Honda Vario", "tanggal": datetime(2026, 1, 8, 8, 30)},
    {"plat": "B2222MNO", "jenis": "mobil", "merk": "Innova", "tanggal": datetime(2026, 1, 9, 13, 15)},
    {"plat": "B3333PQR", "jenis": "motor", "merk": "Suzuki Nex", "tanggal": datetime(2026, 1, 10, 9, 50)},
]

# ================= ROUTE =================
@app.route("/")
def index():
    return render_template("index.html")

# ===== MASUK PARKIR =====
@app.route("/masuk", methods=["GET", "POST"])
def masuk():
    hasil = None
    if request.method == "POST":
        kendaraan = {
            "plat": request.form["plat"],
            "jenis": request.form["jenis"],
            "merk": request.form["merk"],
            "masuk": datetime.now()
        }
        data_parkir.append(kendaraan)

        # MASUK KE RIWAYAT (untuk analisis harian)
        riwayat_masuk.append({
            "plat": kendaraan["plat"],
            "jenis": kendaraan["jenis"],
            "merk": kendaraan["merk"],
            "tanggal": kendaraan["masuk"]
        })

        hasil = kendaraan

    return render_template("masuk.html", hasil=hasil)

# ===== LIHAT PARKIR =====
@app.route("/lihat")
def lihat():
    return render_template("lihat.html", data=data_parkir)

# ===== KELUAR PARKIR =====
@app.route("/keluar", methods=["GET", "POST"])
def keluar():
    hasil = None
    if request.method == "POST":
        plat = request.form["plat"]
        for p in data_parkir:
            if p["plat"] == plat:
                data_parkir.remove(p)
                hasil = p
                break
    return render_template("keluar.html", hasil=hasil)

# ===== ANALISIS =====
@app.route("/analisis")
def analisis():
    now = datetime.now()
    harian = []
    mingguan = []
    bulanan = []

    for r in riwayat_masuk:
        selisih = (now.date() - r["tanggal"].date()).days
        harga = TARIF[r["jenis"]]

        entry = {
            "plat": r["plat"],
            "jenis": r["jenis"],
            "merk": r["merk"],
            "tanggal": r["tanggal"],
            "harga": harga
        }

        if selisih == 0:
            harian.append(entry)
        if selisih <= 7:
            mingguan.append(entry)
        if selisih <= 30:
            bulanan.append(entry)

    # Hitung jumlah motor, mobil, dan total pendapatan per periode
    def hitung_total(data):
        total_motor = sum(1 for d in data if d["jenis"]=="motor")
        total_mobil = sum(1 for d in data if d["jenis"]=="mobil")
        total_uang = sum(d["harga"] for d in data)
        return total_motor, total_mobil, total_uang

    h_motor, h_mobil, h_total = hitung_total(harian)
    w_motor, w_mobil, w_total = hitung_total(mingguan)
    b_motor, b_mobil, b_total = hitung_total(bulanan)

    return render_template(
        "analisis.html",
        harian=harian,
        mingguan=mingguan,
        bulanan=bulanan,
        h_motor=h_motor,
        h_mobil=h_mobil,
        h_total=h_total,
        w_motor=w_motor,
        w_mobil=w_mobil,
        w_total=w_total,
        b_motor=b_motor,
        b_mobil=b_mobil,
        b_total=b_total
    )

if __name__ == "__main__":
    app.run(debug=True)