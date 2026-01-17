import os

def clear_screen():
    """Membersihkan layar terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def konversi_nilai_ke_label(nilai):
    """Mengubah nilai angka menjadi huruf (A-E)"""
    if nilai >= 85: return 'A'
    elif nilai >= 80: return 'A-'
    elif nilai >= 70: return 'B+'
    elif nilai >= 65: return 'B-'
    elif nilai >= 60: return 'C+'
    elif nilai >= 55: return 'C'
    elif nilai >= 45: return 'D'
    else: return 'E'

def konversi_label_ke_bobot(label):
    """Mengubah label huruf menjadi nilai bobot desimal"""
    bobot_map = {'A':4,'A-':3.75,'B+':3.5,'B':3,'B-':2.75,'C+':2.5,'C':2,'D':1,'E':0}
    return bobot_map.get(label.upper(), 0.0)

def hitung_total_sks(list_sks):
    return sum(list_sks)

def hitung_total_nilai(list_sks, list_nilai):
    total = 0
    for i in range(len(list_sks)):
        label = konversi_nilai_ke_label(list_nilai[i])
        bobot = konversi_label_ke_bobot(label)
        total += (list_sks[i] * bobot)
    return total

def hitung_ips(total_nilai, total_sks):
    if total_sks == 0: return 0.0
    return total_nilai / total_sks