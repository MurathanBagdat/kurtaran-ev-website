# -*- coding: utf-8 -*-
"""
Kurtaran Ev — mevcut ilanların İngilizce alanlarını tamamlar.

Instagram senkronu artık her yeni ilanı iki dilde üretiyor (bkz. ai_parser.py).
Bu betik, o değişiklikten önce kaydedilmiş ya da elle girilmiş kayıtların boş
kalan "...En" alanlarını aynı modele doldurtur. Türkçe alanlara dokunmaz.

    python3 tools/translate_en.py            # eksikleri tamamla
    python3 tools/translate_en.py --deneme   # neyin çevrileceğini yaz, kaydetme
    python3 tools/translate_en.py --hepsi    # dolu olanları da yeniden çevir
    python3 tools/translate_en.py --id kopek-pamuk-ab12cd
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ai_parser  # noqa: E402
import animals  # noqa: E402


def eksik_alanlar(kayit: dict) -> list[str]:
    """Türkçesi dolu ama İngilizcesi boş olan alan adları."""
    return [tr for tr, en in animals.EN_ESLESME.items()
            if kayit.get(tr) and not kayit.get(en)]


def main() -> int:
    ap = argparse.ArgumentParser(description="İlanların İngilizce alanlarını tamamlar")
    ap.add_argument("--deneme", action="store_true", help="Kaydetme, yalnızca ne yapılacağını yaz")
    ap.add_argument("--hepsi", action="store_true", help="İngilizcesi dolu kayıtları da yeniden çevir")
    ap.add_argument("--id", action="append", default=[], help="Yalnızca bu id'ler (birden çok kez verilebilir)")
    args = ap.parse_args()

    hayvanlar = animals.load()
    if not hayvanlar:
        print("animals.json boş — çevrilecek kayıt yok.")
        return 0

    hedefler = [h for h in hayvanlar if not args.id or h.get("id") in args.id]
    if args.id:
        bulunamayan = set(args.id) - {h.get("id") for h in hedefler}
        for eksik in sorted(bulunamayan):
            print(f"  ! kayıt bulunamadı: {eksik}")

    yapilacak = [h for h in hedefler if args.hepsi or eksik_alanlar(h)]
    print(f"{len(hayvanlar)} kayıttan {len(yapilacak)} tanesinin İngilizcesi eksik.")
    if not yapilacak:
        return 0

    cevrilen = 0
    for kayit in yapilacak:
        etiket = f"{kayit.get('isim')} ({kayit.get('id')})"
        eksik = eksik_alanlar(kayit) or list(animals.EN_ESLESME)
        if args.deneme:
            print(f"  · {etiket}: {', '.join(eksik)}")
            continue
        try:
            en = ai_parser.ai_translate(kayit)
        except RuntimeError as e:
            print(f"  ! {etiket}: çevrilemedi — {e}")
            continue
        kayit.update(en)
        cevrilen += 1
        print(f"  ✓ {etiket}: {', '.join(eksik)}")

    if args.deneme:
        print("Deneme kipi — hiçbir şey kaydedilmedi.")
        return 0

    if cevrilen:
        # normalize + JSON/JS/şema dosyalarını birlikte tazeler
        animals.save([animals.normalize(h)[0] for h in hayvanlar])
        print(f"{cevrilen} kayıt güncellendi → animals.json, animals.js")
    return 0 if cevrilen == len(yapilacak) else 1


if __name__ == "__main__":
    raise SystemExit(main())
