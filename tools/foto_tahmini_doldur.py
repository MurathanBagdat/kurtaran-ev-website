# -*- coding: utf-8 -*-
"""
Mevcut köpek ilanlarında boş kalan boyut, kilo ve cinsi ilk fotoğraftan doldurur
(geriye doldurma, Ekim 2026 — feedback AD-19…AD-21).

Gönderi metinleri zaten ayrıştırıldı; bu alanlar boşsa metinde bilgi yoktu demektir.
Bu yüzden modele yalnızca ilk fotoğraf ve kayıttaki bilinen bilgiler (isim, yaş,
metinden gelen boyut/cins) verilir. Yalnızca BOŞ alanlar doldurulur (panelden elle
girilen değerlere dokunulmaz), doldurulanlar `tahmini` işaretlenir. Model emin
değilse alan boş kalır.

    python3 tools/foto_tahmini_doldur.py --kuru --sinir 3   # yazmadan dene
    python3 tools/foto_tahmini_doldur.py                     # tüm köpekler

Her 10 ilanda bir kaydeder; yarıda kesilirse yeniden çalıştırmak kaldığı yerden
sürer (yalnızca boş alanı olan köpekler seçilir; modelin emin olmadığı ilanlar da
yeniden denenir).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import animals  # noqa: E402
import ai_parser  # noqa: E402

SEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "boyut":   {"type": ["string", "null"], "enum": ["kucuk", "orta", "buyuk", None]},
        "kiloMin": {"type": ["number", "null"]},
        "kiloMax": {"type": ["number", "null"]},
        "cins":    {"type": ["string", "null"]},
        "cinsEn":  {"type": ["string", "null"]},
    },
    "required": ["boyut", "kiloMin", "kiloMax", "cins", "cinsEn"],
}

SISTEM = """Kurtaran Ev, sahipsiz kedi ve köpekleri kurtaran bir Türk hayvan derneğidir.
Sana bir sahiplendirme ilanındaki köpeğin ilk fotoğrafı ve ilanda bilinen bilgiler
verilecek. İlanın metninde boyut, kilo ve (belirtilmişse) cins bilgisi YOKTU; yalnızca
"istenen" alanları fotoğraftan tahmin et.

- kilo her zaman ARALIK (kiloMin < kiloMax), en fazla ~6 kg genişliğinde.
- boyut: kucuk = 12 kg altı, orta = 12–25 kg, buyuk = 25 kg üstü. Boyutu kilo aralığının
  ORTA NOKTASINA göre seç. Bilinen boyut verildiyse kilo aralığı onunla tutarlı olmalı.
- cins: belirgin bir ırk görünüyorsa adını yaz ("Labrador Retriever melezi"); yoksa "Melez".
  cinsEn: İngilizcesi ("Labrador Retriever mix", "Mixed breed").
- Bilinen cins verildiyse kilo ve boyut tahmininde onu da göz önüne al.
- EMİN DEĞİLSEN null bırak. Fotoğraftan tahmin YAPMA: köpek net görünmüyor, kısmen kadrajda
  ya da ölçek verecek bir şey (insan, eşya) yok; birden fazla hayvan var ve ilandaki köpeğin
  hangisi olduğu belli değil (kardeş ilanında tahmin hepsine uymalı); fotoğraf yazı/kolaj
  ağırlıklı. 6 aydan küçük yavrunun boyutu null kalır (kilo aralığı verilebilir).
- İstenmeyen alanları null bırak.

Yalnızca şemaya uygun JSON döndür."""


def tahmin_et(kayit: dict, istenen: list[str], kardes: int) -> dict:
    foto = animals.ROOT / "site" / kayit["fotograflar"][0]
    bilinen = {
        "isim": kayit.get("isim"),
        "yasAy": kayit.get("yasAy"),
        "boyut (metinden)": kayit.get("boyut"),
        "cins (metinden)": kayit.get("cins"),
        "aynı gönderideki hayvan sayısı": kardes,
        "istenen": istenen,
    }
    icerik = [{"type": "text", "text": json.dumps(bilinen, ensure_ascii=False)},
              ai_parser._foto_icerigi(str(foto))]
    return ai_parser._cagir(SISTEM, icerik, SEMA, "foto_tahmini", None, ai_parser.VARSAYILAN_MODEL)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kuru", action="store_true", help="yalnızca göster, kaydetme")
    ap.add_argument("--sinir", type=int, default=0, help="en fazla bu kadar ilan (0 = hepsi)")
    args = ap.parse_args()

    hayvanlar = animals.load()
    kardes = {}
    for h in hayvanlar:
        pid = (h.get("kaynak") or {}).get("gonderiId")
        kardes[pid] = kardes.get(pid, 0) + 1

    adaylar = []
    for h in hayvanlar:
        if h["tur"] != "kopek" or not h.get("fotograflar"):
            continue
        istenen = [a for a, bos in (("boyut", not h.get("boyut")), ("kilo", h.get("kiloKg") is None),
                                    ("cins", not h.get("cins"))) if bos]
        if istenen:
            adaylar.append((h, istenen))
    if args.sinir:
        adaylar = adaylar[:args.sinir]
    print(f"{len(adaylar)} köpek ilanında boş alan var")

    sayac = {"boyut": 0, "kilo": 0, "cins": 0, "hata": 0}
    for i, (h, istenen) in enumerate(adaylar, 1):
        try:
            t = tahmin_et(h, istenen, kardes.get((h.get("kaynak") or {}).get("gonderiId"), 1))
        except RuntimeError as e:
            sayac["hata"] += 1
            print(f"  ! {h['id']}: {e}")
            continue
        degisti = []
        tahmini = h.setdefault("tahmini", [])
        if "kilo" in istenen and t.get("kiloMin") is not None:
            kmin, kmax = t["kiloMin"], t.get("kiloMax")
            h["kiloKg"], h["kiloKgMax"] = kmin, (kmax if kmax and kmax > kmin else None)
            degisti.append(f"kilo {kmin:g}–{kmax:g}" if h["kiloKgMax"] else f"kilo {kmin:g}")
            tahmini.append("kiloKg")
            sayac["kilo"] += 1
        if "boyut" in istenen and t.get("boyut"):
            h["boyut"] = t["boyut"]
            degisti.append(f"boyut {t['boyut']}")
            tahmini.append("boyut")
            sayac["boyut"] += 1
        if "cins" in istenen and t.get("cins"):
            h["cins"], h["cinsEn"] = t["cins"], t.get("cinsEn") or h.get("cinsEn")
            degisti.append(f"cins {t['cins']}")
            tahmini.append("cins")
            sayac["cins"] += 1
        h["tahmini"] = list(dict.fromkeys(tahmini))
        if degisti:
            h["guncelleme"] = animals.now_iso()
        print(f"  [{i}/{len(adaylar)}] {h['isim']}: {', '.join(degisti) or 'emin değil, boş kaldı'}", flush=True)
        if not args.kuru and i % 10 == 0:
            animals.save(hayvanlar)

    print(f"Doldurulan: boyut {sayac['boyut']}, kilo {sayac['kilo']}, cins {sayac['cins']}; hata {sayac['hata']}")
    if not args.kuru:
        animals.save(hayvanlar)
        print("animals.json / animals.js kaydedildi")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
