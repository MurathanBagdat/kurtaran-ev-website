#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
İki hesabın gönderi dizini: bugünden --bas tarihine kadar her gönderinin
güncel caption'ı (ilk 600 karakter), tarihi ve "yuvalandı" bilgisi.

Neden: aynı hayvan aylar sonra yeniden paylaşılıyor; eski gönderiden çıkan
ilan, yeni gönderide YUVALANDI yazsa bile "yuva arıyor" kalıyordu. Mükerrer
temizliği (tools/mukerrer.py) bu dizinle "daha yeni gönderide aynı isim var
mı?" sorusunu istek harcamadan yanıtlar.

  python3 tools/gonderi_dizini.py --bas 2026-01-01    # ~1 istek / 12 gönderi

Çıktı: tools/gonderi_dizini.json  {kod: {hesap, tarih, yuvalandi, caption}}
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import instagram_sync as sync  # noqa: E402
import rapidapi_kota  # noqa: E402
from yuvalanma_kontrol import baslikta_yuvalandi, sonraki_imlec, _caption  # noqa: E402

DIZIN_PATH = Path(__file__).resolve().parent / "gonderi_dizini.json"
KATEGORI = "dizin"


def yukle() -> dict:
    try:
        return json.loads(DIZIN_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--bas", default="2026-01-01", help="Bu tarihe kadar geriye (YYYY-AA-GG)")
    args = ap.parse_args()
    api_key = sync.config_yukle().get("rapidapi_key")
    bas = datetime.fromisoformat(args.bas).replace(tzinfo=timezone.utc).timestamp()
    dizin = yukle()
    for hesap, pk in sync.RAPID_PK.items():
        params, sayfa = {"user_id": pk}, 0
        while True:
            if sayfa:
                time.sleep(2)
            yanit = sync._rapid_get("/feed", params, api_key, KATEGORI)
            sayfa += 1
            for it in yanit.get("items") or []:
                if not it.get("code") or not it.get("taken_at"):
                    continue
                cap = _caption(it)
                dizin[it["code"]] = {
                    "hesap": hesap,
                    "tarih": datetime.fromtimestamp(it["taken_at"], timezone.utc).isoformat(),
                    "yuvalandi": baslikta_yuvalandi(cap),
                    "caption": cap[:600],
                }
            kendi = [it["taken_at"] for it in yanit.get("items") or []
                     if it.get("taken_at") and not it.get("timeline_pinned_user_ids")]
            imlec = sonraki_imlec(yanit, pk)
            if not imlec or (kendi and min(kendi) < bas):
                break
            params = {"user_id": pk, "next_max_id": imlec}
        print(f"@{hesap}: {sayfa} sayfa")
    DIZIN_PATH.write_text(json.dumps(dict(sorted(dizin.items(), key=lambda kv: kv[1]["tarih"],
                                                 reverse=True)),
                                     ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(dizin)} gönderi → {DIZIN_PATH.name}")
    print(rapidapi_kota.ozet())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
