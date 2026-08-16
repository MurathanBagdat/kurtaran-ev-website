#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Örnek ilan kayıtları oluşturur.

NEDEN VAR: Instagram, giriş yapmadan gönderi içeriği vermediği için gerçek
ilanlar otomatik çekilemedi. Katalog arayüzünün, filtrelerin ve admin panelinin
çalıştığını görebilmeniz için bu kayıtlar üretiliyor.

Bunların hepsi `ornek: true` olarak işaretlidir; sitede "ÖRNEK KAYIT" rozetiyle
ve sayfa başında bir uyarı bandıyla gösterilirler. Gerçek ilanlar geldiğinde
tek tıkla temizlenebilirler:

    python3 tools/seed.py --sil
    (ya da admin panelinden "Örnek kayıtları sil")

Bazı kayıtların bilerek fotoğrafı ve eksik alanları yok — arayüzün "bilgi yok"
durumunu da doğru gösterdiğini kontrol edebilmek için.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import animals  # noqa: E402

F = animals.PHOTO_WEB_PREFIX

ORNEKLER = [
    # --- KÖPEKLER ---------------------------------------------------------
    {
        "tur": "kopek", "isim": "Zeytin", "cinsiyet": "disi", "cins": "Melez",
        "yasAy": 24, "kiloKg": 17.0, "renk": "Sarı",
        "kisir": True, "asili": True, "cipli": True,
        "cocuklaUyum": True, "kopeklerleUyum": True, "kedilerleUyum": None,
        "karakter": ["oyuncu", "sevecen", "meraklı"],
        "konum": "Hadımköy Yaşam Alanı", "durum": "yuva-ariyor",
        "aciklama": "Zeytin, iki yıl önce Hadımköy çevresinde bulunduğunda çok ürkekti. "
                    "Bugün kapıda karşılayan, tasması takılınca sevinçten zıplayan bir köpek. "
                    "Günde iki yürüyüş yapabilecek, sabırlı bir aile arıyoruz.",
        "fotograflar": [f"{F}/ornek-sari-kopek.jpg"],
        "tahmini": ["yasAy"],
    },
    {
        "tur": "kopek", "isim": "Kevok", "cinsiyet": "erkek", "cins": "Amerikan Bully",
        "yasAy": 84, "kiloKg": 32.0, "renk": "Beyaz",
        "kisir": True, "asili": True, "cipli": True,
        "cocuklaUyum": True, "kopeklerleUyum": False, "kedilerleUyum": False,
        "ozelBakim": False,
        "karakter": ["sakin", "sadık", "eğitimli"],
        "konum": "Hadımköy Yaşam Alanı", "durum": "yuvalandi",
        "saglikNotu": "Kalça displazisi hafif düzeyde; ağır egzersiz önerilmiyor.",
        "aciklama": "Irkı ve yaşı yüzünden yıllarca gözden kaçan Kevok, onu gerçekten gören "
                    "insanla tanıştı. Artık her sabah sahilde yürüyor.",
        "fotograflar": [f"{F}/ornek-beyaz-kopek.jpg"],
    },
    {
        "tur": "kopek", "isim": "Karabaş", "cinsiyet": "erkek", "cins": "Çoban Köpeği",
        "yasAy": 36, "kiloKg": 28.0, "renk": "Siyah-beyaz",
        "kisir": True, "asili": True, "cipli": None,
        "cocuklaUyum": True, "kopeklerleUyum": True, "kedilerleUyum": None,
        "karakter": ["koruyucu", "sadık", "sakin"],
        "konum": "Hadımköy Yaşam Alanı", "durum": "yuva-ariyor",
        "aciklama": "Bahçeli bir ev ve gün içinde yanında olabilecek bir aile arıyor. "
                    "Apartman yaşamı ona göre değil.",
        "fotograflar": [f"{F}/ornek-siyahbeyaz-kopek.jpg"],
        "tahmini": ["yasAy", "kiloKg"],
    },
    {
        "tur": "kopek", "isim": "Lucy", "cinsiyet": "disi", "cins": "Melez",
        "yasAy": 96, "kiloKg": 14.0,
        "kisir": True, "asili": True,
        "cocuklaUyum": True, "kopeklerleUyum": True, "kedilerleUyum": True,
        "ozelBakim": True,
        "karakter": ["sakin", "sevecen"],
        "konum": "Hadımköy Yaşam Alanı", "durum": "yuvalandi",
        "saglikNotu": "Kanser tedavisi sürüyor; düzenli kontrol gerekiyor.",
        "aciklama": "Tedavisi devam ederken bir aile ona yalnızca evini değil, bütün kalbini açtı.",
        "fotograflar": [f"{F}/ornek-acik-kopek.jpg"],
    },
    {
        "tur": "kopek", "isim": "Fındık", "cinsiyet": "disi",
        "yasAy": 5,
        "asili": False, "kisir": False,
        "cocuklaUyum": True, "kopeklerleUyum": True,
        "karakter": ["oyuncu", "meraklı"],
        "konum": "Hadımköy Yaşam Alanı", "durum": "yuva-ariyor",
        "aciklama": "Beş aylık. Cinsi ve yetişkin boyu bilinmiyor; anne melez, orta boy bir köpekti. "
                    "Aşı takvimi sürüyor, kısırlaştırma yaşı geldiğinde yapılacak.",
        "fotograflar": [],
        "tahmini": ["yasAy"],
    },
    {
        "tur": "kopek", "isim": "Duman", "cinsiyet": "erkek",
        "kiloKg": 22.0,
        "kisir": True, "asili": True,
        "kopeklerleUyum": True,
        "karakter": ["çekingen"],
        "konum": "Hadımköy Yaşam Alanı", "durum": "yuva-ariyor",
        "aciklama": "Yaşı bilinmiyor, veteriner tahmini 4-6 yaş aralığında. İnsanlara alışması "
                    "zaman aldı; sabırlı, sakin bir yuvada çok iyi olacak.",
        "fotograflar": [],
    },
    {
        "tur": "kopek", "isim": "Pamuk", "cinsiyet": "disi", "cins": "Golden Retriever",
        "yasAy": 18, "kiloKg": 25.0, "renk": "Krem",
        "kisir": True, "asili": True, "cipli": True,
        "cocuklaUyum": True, "kopeklerleUyum": True, "kedilerleUyum": True,
        "karakter": ["oyuncu", "sevecen", "eğitimli"],
        "konum": "Hadımköy Yaşam Alanı", "durum": "rezerve",
        "aciklama": "Temel komutları biliyor, tasmada güzel yürüyor. Ön görüşmesi tamamlandı, "
                    "ev ziyareti bekleniyor.",
        "fotograflar": [],
    },

    # --- KEDİLER ----------------------------------------------------------
    {
        "tur": "kedi", "isim": "Mırnav", "cinsiyet": "disi", "cins": "Tekir",
        "yasAy": 30, "kiloKg": 4.2,
        "kisir": True, "asili": True, "cipli": True,
        "cocuklaUyum": True, "kedilerleUyum": True, "kopeklerleUyum": None,
        "karakter": ["meraklı", "sevecen"],
        "konum": "Beşiktaş Kedi Sahiplendirme Alanı", "durum": "yuva-ariyor",
        "aciklama": "Pencere kenarını çok seviyor. Kucağa alışması birkaç gün sürüyor ama "
                    "alıştıktan sonra dizinizden inmiyor. Balkon teli şart.",
        "fotograflar": [f"{F}/ornek-tekir.jpg"],
    },
    {
        "tur": "kedi", "isim": "Limon", "cinsiyet": "erkek", "cins": "Sarman",
        "yasAy": 3, "kiloKg": 1.1,
        "kisir": False, "asili": False,
        "cocuklaUyum": True, "kedilerleUyum": True,
        "karakter": ["oyuncu"],
        "konum": "Kedi Yaşam Alanı", "durum": "yuva-ariyor",
        "aciklama": "Üç aylık, kardeşiyle birlikte bulundu. İkisinin birlikte sahiplenilmesini "
                    "tercih ediyoruz. Aşı takvimi yeni başladı.",
        "fotograflar": [],
        "tahmini": ["yasAy", "kiloKg"],
    },
    {
        "tur": "kedi", "isim": "Zeytin", "cinsiyet": "erkek", "cins": "Sarman",
        "yasAy": 3, "kiloKg": 1.2,
        "kisir": False, "asili": False,
        "cocuklaUyum": True, "kedilerleUyum": True,
        "karakter": ["oyuncu", "çekingen"],
        "konum": "Kedi Yaşam Alanı", "durum": "yuva-ariyor",
        "aciklama": "Limon'un kardeşi. Ondan biraz daha çekingen; birlikte sahiplenilmeleri "
                    "uyum sürecini çok kolaylaştırır.",
        "fotograflar": [],
        "tahmini": ["yasAy", "kiloKg"],
    },
    {
        "tur": "kedi", "isim": "Boncuk", "cinsiyet": "disi", "cins": "Van Kedisi",
        "yasAy": 108,
        "kisir": True, "asili": True, "ozelBakim": True,
        "kedilerleUyum": False, "cocuklaUyum": None,
        "karakter": ["sakin"],
        "konum": "Dumankaya Kedi Tedavi Alanı", "durum": "yuva-ariyor",
        "saglikNotu": "Böbrek değerleri takip ediliyor, özel mama kullanıyor.",
        "aciklama": "Kıdemli bir hanımefendi. Tek kedi olarak yaşamayı tercih ediyor. "
                    "Kilosu tartılamadı; sakin bir evde huzurlu bir emeklilik hak ediyor.",
        "fotograflar": [],
    },
    {
        "tur": "kedi", "isim": "İsimsiz", "cinsiyet": None,
        "durum": "taslak",
        "konum": "Kedi Yaşam Alanı",
        "aciklama": "Yeni geldi, henüz muayene edilmedi. Bilgiler tamamlanınca yayınlanacak.",
        "fotograflar": [],
    },
]


def ekle() -> int:
    mevcut = animals.load()
    var_olan_ornek = {a.get("id") for a in mevcut if a.get("ornek")}
    if var_olan_ornek:
        print(f"  {len(var_olan_ornek)} örnek kayıt zaten var; önce siliniyor.")
        mevcut = [a for a in mevcut if not a.get("ornek")]

    for ham in ORNEKLER:
        ham = dict(ham)
        ham["ornek"] = True
        ham["kaynak"] = {"tip": "ornek", "not": "Örnek kayıt — gerçek bir ilan değildir."}
        kayit, hatalar = animals.normalize(ham)
        if hatalar:
            print(f"  ! {ham.get('isim')}: {'; '.join(hatalar)}")
        mevcut.append(kayit)

    animals.save(mevcut)
    return len(ORNEKLER)


def sil() -> int:
    mevcut = animals.load()
    kalan = [a for a in mevcut if not a.get("ornek")]
    silinen = len(mevcut) - len(kalan)
    animals.save(kalan)
    return silinen


def main() -> int:
    ap = argparse.ArgumentParser(description="Örnek ilan kayıtlarını ekler veya siler.")
    ap.add_argument("--sil", action="store_true", help="Örnek kayıtları temizle")
    args = ap.parse_args()

    if args.sil:
        n = sil()
        print(f"{n} örnek kayıt silindi.")
        return 0

    n = ekle()
    toplam = animals.load()
    kopek = sum(1 for a in toplam if a["tur"] == "kopek")
    kedi = sum(1 for a in toplam if a["tur"] == "kedi")
    print(f"{n} örnek kayıt eklendi. Toplam: {len(toplam)} ilan ({kopek} köpek, {kedi} kedi).")
    print("Hepsi 'ÖRNEK KAYIT' rozetiyle işaretli. Silmek için: python3 tools/seed.py --sil")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
