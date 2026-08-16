# -*- coding: utf-8 -*-
"""
Caption ayrıştırıcı için regresyon testleri.
Çalıştırma: python3 tools/test_parser.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from caption_parser import parse, ilan_mi, yuvalandi_mi  # noqa: E402

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
]

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

    print()
    print("TÜM TESTLER GEÇTİ" if hata == 0 else f"{hata} TEST BAŞARISIZ")
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
