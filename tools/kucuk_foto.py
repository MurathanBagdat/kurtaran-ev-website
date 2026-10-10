# -*- coding: utf-8 -*-
"""
İlan fotoğraflarının küçük (web) kopyalarını üretir.

  site/assets/img/animals/<ad>.jpg  →  site/assets/img/animals-k/<ad>.webp

Kartlar, küçük resimler ve "diğer yuva arayanlar" bu kopyaları kullanır
(catalog.js / animal.js > kucukFoto); kopya yoksa tarayıcı orijinale düşer.
Orijinaller hiç değiştirilmez.

Kopyası zaten olan dosyalar atlanır; yani her çalıştırmada yalnızca yeni
fotoğraflar işlenir. Pillow gerekir (CI'da `pip install pillow`):

    python3 tools/kucuk_foto.py
"""

from __future__ import annotations

import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent / "site" / "assets" / "img"
KAYNAK = KOK / "animals"
HEDEF = KOK / "animals-k"
GENISLIK = 720       # kart ~360 px × 2 (retina)
KALITE = 74


def main() -> int:
    try:
        from PIL import Image, ImageOps
    except ImportError:
        print("! Pillow yok: pip install pillow")
        return 2
    HEDEF.mkdir(parents=True, exist_ok=True)
    yeni = atlandi = 0
    kaynak_boyut = hedef_boyut = 0
    for dosya in sorted(KAYNAK.iterdir()):
        if dosya.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        cikti = HEDEF / (dosya.stem + ".webp")
        if cikti.exists():   # orijinaller yerinde değişmez; CI'da mtime güvenilmez
            atlandi += 1
            continue
        with Image.open(dosya) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            if im.width > GENISLIK:
                im = im.resize((GENISLIK, round(im.height * GENISLIK / im.width)), Image.LANCZOS)
            im.save(cikti, "WEBP", quality=KALITE, method=6)
        kaynak_boyut += dosya.stat().st_size
        hedef_boyut += cikti.stat().st_size
        yeni += 1
    # Orijinali silinmiş kopyaları temizle
    stemler = {d.stem for d in KAYNAK.iterdir()}
    silinen = 0
    for kopya in HEDEF.glob("*.webp"):
        if kopya.stem not in stemler:
            kopya.unlink()
            silinen += 1
    oran = f" ({kaynak_boyut / 1e6:.1f} MB → {hedef_boyut / 1e6:.1f} MB)" if yeni else ""
    print(f"Küçük fotoğraflar: {yeni} yeni{oran}, {atlandi} güncel, {silinen} silindi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
