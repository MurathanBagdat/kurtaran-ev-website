#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yeniden paylaşılan hayvanlar: "bu ilanın hayvanı daha yeni bir gönderide var mı?"

Dernek aynı hayvanı aylar sonra yeniden paylaşıyor; yuvalanınca da YUVALANDI
gönderisi atıyor. Geçmişten doldurulan (eski) bir gönderiden çıkan ilan, daha
yeni bir gönderide aynı isim geçiyorsa gereksizdir: ya hayvan zaten yeni
ilanıyla sitede ya da yuvalanmış.

Kural (aynı hesap, daha yeni gönderi):
  a) sitede aynı temel isimli (kardeş numarası hariç) daha yeni bir kayıt var, ya da
  b) bir YUVALANDI gönderisinin BAŞLIĞINDA isim kelime olarak geçiyor. Başlık =
     ilk dolu satır (ayraçlar hariç), o satır YUVALANDI ise bir sonraki satır,
     ve ilk 3 satırdaki hashtag'ler. Daha geniş bakılınca "asıl", "minik",
     "şirin" gibi isimler düz metinde yanlış eşleşiyordu.
İsimsiz/genel adlar (İsimsiz, Yavru Kedi …) eşleşmez.
Aynı isimli iki farklı hayvanda eskisi gizlenir (11.10.2026 kararı: kaçırmak,
yanlışlıkla "yuva arıyor" göstermekten iyidir).

  python3 tools/mukerrer.py --kuru    # geriye doldurulmuş ilanlardan silinecekleri göster
  python3 tools/mukerrer.py           # sil

Gönderi dizini: tools/gonderi_dizini.json (tools/gonderi_dizini.py üretir).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import animals  # noqa: E402
import gonderi_dizini  # noqa: E402
from caption_parser import _sade  # noqa: E402

_AYRAC = re.compile(r"^[\W_]*$")
GENEL_ADLAR = {"", "isimsiz", "yavru", "yavru kedi", "yavru kopek", "kedi", "kopek", "kediler",
               "yavrular", "kardesler"}


def baslik(caption: str) -> list[str]:
    satirlar = [s.strip() for s in _sade(caption or "").splitlines()
                if s.strip() and not _AYRAC.match(s.strip())][:3]
    if not satirlar:
        return []
    parcalar = [satirlar[0]]
    if re.search(r"\byuvalandi", satirlar[0]) and len(satirlar) > 1:
        parcalar.append(satirlar[1])
    parcalar += [e for s in satirlar for e in re.findall(r"#(\w+)", s)]
    return parcalar


def temel_ad(isim: str | None) -> str:
    """'Şirin 3' → 'sirin' (kardeş numarası atılır)."""
    return re.sub(r"\s*\d+$", "", _sade(isim or "").strip())


def daha_yeni_eslesme(kayit: dict, dizin: dict, hayvanlar: list[dict]) -> tuple[str, str] | None:
    """Kaydın hayvanını anan daha yeni gönderi: (kod, "yeni ilan" | "YUVALANDI") ya da None."""
    ad = temel_ad(kayit.get("isim"))
    kaynak = kayit.get("kaynak") or {}
    if ad in GENEL_ADLAR or not kaynak.get("tarih"):
        return None
    for a in hayvanlar:                                   # a) daha yeni kayıt
        k = a.get("kaynak") or {}
        if (k.get("hesap") == kaynak.get("hesap") and k.get("gonderiId") != kaynak.get("gonderiId")
                and (k.get("tarih") or "") > kaynak["tarih"] and temel_ad(a.get("isim")) == ad):
            return k["gonderiId"], "yeni ilan"
    desen = re.compile(r"\b" + re.escape(ad) + r"\b")
    for kod, g in dizin.items():                          # b) daha yeni YUVALANDI gönderisi
        if (g["yuvalandi"] and g["hesap"] == kaynak.get("hesap") and g["tarih"] > kaynak["tarih"]
                and any(desen.search(s) for s in baslik(g["caption"]))):
            return kod, "YUVALANDI"
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Geriye doldurulmuş mükerrer ilanları temizler.")
    ap.add_argument("--kuru", action="store_true", help="Yalnızca göster")
    args = ap.parse_args()
    dizin = gonderi_dizini.yukle()
    hayvanlar = animals.load()
    silinecek = []
    for a in hayvanlar:
        if not (a.get("kaynak") or {}).get("geriye"):
            continue
        eslesme = daha_yeni_eslesme(a, dizin, hayvanlar)
        if eslesme:
            silinecek.append(a["id"])
            print(f"  ✗ {a['kaynak']['tarih'][:10]} {a.get('isim')} ← {eslesme[1]} ({eslesme[0]})")
    print(f"{len(silinecek)} geriye doldurulmuş ilan "
          + ("silinecek (kuru)." if args.kuru else "silindi."))
    if not args.kuru and silinecek:
        animals.save([a for a in hayvanlar if a["id"] not in set(silinecek)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
