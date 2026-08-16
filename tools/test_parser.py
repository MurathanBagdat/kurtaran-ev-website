# -*- coding: utf-8 -*-
"""
Caption ayrıştırıcı için regresyon testleri.
Çalıştırma: python3 tools/test_parser.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from caption_parser import parse, parse_all, ilan_mi, yuvalandi_mi, icerik_turu  # noqa: E402

VAKALAR = [
    (
        "emoji + karışık olumluluk",
        "🐶 PAMUK yuva arıyor!\nYaklaşık 2 yaşında, dişi, 18 kg. Melez.\n"
        "Kısırlaştırıldı ✅ Aşıları tam ✅\n"
        "Çocuklarla çok iyi anlaşıyor, diğer köpeklerle de sorunsuz. Kedilerle anlaşamıyor.\n"
        "#sahiplendirme",
        {"isim": "Pamuk", "cinsiyet": "disi", "yasAy": 24, "kiloKg": 18.0,
         "kisir": True, "asili": True, "cocuklaUyum": True,
         "kopeklerleUyum": True, "kedilerleUyum": False, "tur": "kopek"},
    ),
    (
        "aynı cümlede olumsuzlama",
        "Tekir kedimiz MISIR 8 aylık erkek, 3,5 kg. Aşıları yapıldı, henüz kısır değil. Yuva arıyor.",
        {"isim": "Mısır", "cinsiyet": "erkek", "yasAy": 8, "kiloKg": 3.5,
         "kisir": False, "asili": True, "tur": "kedi", "cins": "Tekir"},
    ),
    (
        "İsmi: kalıbı + yaş aralığı",
        "İsmi: Zeytin. 3-4 yaşlarında, yaklaşık 22 kilo, Golden Retriever karışımı. Yuvasını arıyor.",
        {"isim": "Zeytin", "yasAy": 42, "kiloKg": 22.0, "cins": "Golden Retriever"},
    ),
    (
        "ondalık yaş",
        "BULUT 1,5 yaşında erkek köpek. Yuva arıyor.",
        {"isim": "Bulut", "yasAy": 18, "cinsiyet": "erkek", "tur": "kopek"},
    ),
    (
        "haftalık yavru",
        "10 haftalık yavru kedimiz LİMON yuva arıyor. Çok oyuncu.",
        {"isim": "Limon", "yasAy": 2, "tur": "kedi", "karakter": ["oyuncu"]},
    ),
    (
        "bilgi yok — alanlar boş kalmalı",
        "Bu güzelliğe yuva arıyoruz. Detaylar için mesaj atın.",
        {"yasAy": None, "kiloKg": None, "cinsiyet": None, "cins": None},
    ),
    (
        "sağlık notu + özel bakım",
        "BONCUK yuva arıyor. Tek gözü görmüyor, özel bakım gerekiyor ama sevgisi eksiksiz.",
        {"isim": "Boncuk", "ozelBakim": True,
         "saglikNotu": "Tek gözü görmüyor, özel bakım gerekiyor ama sevgisi eksiksiz."},
    ),
    (
        "konum — gönüllü geçici yuva",
        "#Lily #küçükırk\nGönüllü geçici yuvamızdaki Lily, 3-4 yaşlarında, kısır bir kız.\n"
        "Lily'nin ömürlük yuvasını arıyoruz.",
        {"isim": "Lily", "konum": "Gönüllü geçici yuva", "kisir": True},
    ),
    (
        "konum — semtli yaşam alanı",
        "DUMAN yuva arıyor. Hadımköy yaşam alanımızda kalıyor, 2 yaşında erkek.",
        {"isim": "Duman", "konum": "Hadımköy yaşam alanı", "yasAy": 24},
    ),
    (
        "sağlık bilgisi yoksa alanlar boş",
        "PAMUK yuva arıyor, 2 yaşında dişi.",
        {"saglikNotu": None, "ozelBakim": None, "konum": None},
    ),
    (
        "YUVALANDI / Geçici yuva satırları isim sanılmamalı — isim hashtag'ten gelmeli",
        "YUVALANDI 🥳\n#Köfte #ortaırk\nDünyanın en uslu köpeği Köfte🥰 2-3 yaşlarında, "
        "erkek. Köfte'ye yeni yuvasını arıyoruz.\n"
        "🐾 Sahiplenemiyorsanız geçici yuva olabilirsiniz 🙏\n"
        "🐾 Geçici yuva olamıyorsanız, ilanı paylaşabilirsiniz 🙏",
        {"isim": "Köfte", "cinsiyet": "erkek", "yasAy": 30, "boyut": "orta",
         "konum": None},  # çağrı cümlesindeki "geçici yuva" konum değildir
    ),
]

KUTU_KARDESLER = (
    "Kutu kardeşler ✨\n"
    "Küçücük bir kutunun içinde terk edildiler 🥺\n"
    "Özel olarak beslenip büyütüldüler şimdi ise kalıcı yuvalarını arıyorlar 😻\n\n"
    "🐾 4-5 haftalık\n"
    "🐾 ikisi erkek, biri dişi\n"
    "🐾 kısırlaştırma şartı ile sahiplendirilecektir.\n\n"
    "Bu miniklerden birini ya da üçünü birden hayatınıza dahil edebilirsiniz."
)

ARYA = (
    "Arya 10 yaşında. Ve göremiyor 😔\n"
    "Onun Koruyucu Meleği olarak mama, bakım ve sağlık giderlerinin "
    "karşılanmasına katkı sağlayabilirsiniz."
)

ILAN_MI = [
    ("PAMUK yuva arıyor!", True),
    ("Sahiplendirme ilanı: Boncuk", True),
    ("🎉 Boncuk yuvasına kavuştu! Teşekkürler.", False),
    ("Bağış kampanyamıza destek olun.", False),
]


def main() -> int:
    hata = 0
    for baslik, caption, beklenen in VAKALAR:
        sonuc = parse(caption)
        for alan, deger in beklenen.items():
            if sonuc.get(alan) != deger:
                print(f"  ✗ [{baslik}] {alan}: beklenen {deger!r}, gelen {sonuc.get(alan)!r}")
                hata += 1
        else:
            pass
        if all(sonuc.get(a) == d for a, d in beklenen.items()):
            print(f"  ✓ {baslik}")

    for caption, beklenen in ILAN_MI:
        if ilan_mi(caption) != beklenen:
            print(f"  ✗ ilan_mi({caption[:40]!r}): beklenen {beklenen}")
            hata += 1
    if all(ilan_mi(c) == b for c, b in ILAN_MI):
        print("  ✓ ilan/ilan değil ayrımı")

    if not yuvalandi_mi("Boncuk yuvasına kavuştu"):
        print("  ✗ yuvalandi_mi çalışmıyor")
        hata += 1
    else:
        print("  ✓ yuvalandı tespiti")

    # Çoklu hayvan: tek gönderiden üç kayıt, cinsiyetler dağıtılmış
    kardesler = parse_all(KUTU_KARDESLER, varsayilan_tur="kedi")
    beklenen_cinsiyet = ["erkek", "erkek", "disi"]
    if len(kardesler) != 3:
        print(f"  ✗ kutu kardeşler: 3 kayıt beklenirdi, {len(kardesler)} geldi")
        hata += 1
    elif [k["cinsiyet"] for k in kardesler] != beklenen_cinsiyet:
        print(f"  ✗ kutu kardeşler cinsiyetleri: {[k['cinsiyet'] for k in kardesler]}")
        hata += 1
    elif not all(k["kisir"] is False and k["tur"] == "kedi" for k in kardesler):
        print("  ✗ kutu kardeşler: kisir=False / tur=kedi beklenirdi")
        hata += 1
    elif len({k["isim"] for k in kardesler}) != 3:
        print(f"  ✗ kutu kardeşler isimleri benzersiz değil: {[k['isim'] for k in kardesler]}")
        hata += 1
    else:
        print("  ✓ çoklu hayvan (kardeş) ilanı → 3 kayıt")

    # Tekil ilan "bir erkek" yüzünden çoklaşmamalı
    tekil = parse_all("POTTER yuva arıyor. Çok iyi huylu bir erkek, 3 yaşında.")
    if len(tekil) != 1:
        print(f"  ✗ tekil ilan çoklaştı: {len(tekil)} kayıt")
        hata += 1
    else:
        print("  ✓ tekil ilan tek kayıt kaldı")

    # İçerik türü sınıflandırması
    for metin, beklenen in ((ARYA, "koruyucu-melek"),
                            (KUTU_KARDESLER, "ilan"),
                            ("🎉 Boncuk yuvasına kavuştu! Teşekkürler.", "yuvalandi"),
                            ("Bağış kampanyamıza destek olun.", "diger")):
        if icerik_turu(metin) != beklenen:
            print(f"  ✗ icerik_turu({metin[:30]!r}): beklenen {beklenen!r}, "
                  f"gelen {icerik_turu(metin)!r}")
            hata += 1
    else:
        if all(icerik_turu(m) == b for m, b in ((ARYA, "koruyucu-melek"),
                                                (KUTU_KARDESLER, "ilan"))):
            print("  ✓ içerik türü sınıflandırması")

    print()
    print("TÜM TESTLER GEÇTİ" if hata == 0 else f"{hata} TEST BAŞARISIZ")
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
