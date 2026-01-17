#utils/waktu.py

from datetime import datetime
import math
from constants import TARIF


def hitung_durasi_menit(masuk_str, keluar_str):
    masuk = datetime.strptime(masuk_str, "%Y-%m-%d %H:%M:%S")
    keluar = datetime.strptime(keluar_str, "%Y-%m-%d %H:%M:%S")

    return math.ceil((keluar - masuk).total_seconds() / 60)


def hitung_biaya(jenis, menit):
    if menit < 2:
        return 0

    unit = math.floor((menit - 2) / 2) + 1
    tarif = TARIF.get(jenis, TARIF["lain"])
    return unit * tarif
