#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geçmiş Instagram ilanlarını siteye aktarır (tek seferlik geriye doldurma).

Günlük senkron yalnızca son gönderilere bakar; takip Ağustos 2026'da başladı.
Bu araç, takipten ÖNCE paylaşılmış ve hâlâ yuva arayan hayvanların
ilanlarını parça parça (varsayılan 30 gün) geriye doğru ekler:

  python3 tools/geriye_doldur.py --kuru        # ne olacağını göster (AI/foto yok)
  python3 tools/geriye_doldur.py               # sonraki 30 günü işle
  python3 tools/geriye_doldur.py --gun 45      # parça boyu
  python3 tools/geriye_doldur.py --durum       # nerede kaldık

  * Başlangıç noktası: hesabın daha önce görülmüş en eski gönderisi. Feed
    imleci ({media_pk}_{hesap_pk}) gönderinin kısa kodundan hesaplanır;
    yeni gönderileri yeniden gezmek için istek harcanmaz.
  * Kaldığı yer tools/geriye_doldurma.json'da; her çalıştırma oradan bir
    parça daha geriye iner, HEDEF_TARIH'e varınca o hesap biter.
  * Caption'ın başında YUVALANDI yazan gönderiler AI'ya gönderilmez,
    fotoğrafı indirilmez; yalnızca "görüldü" kaydedilir. AI de yuvalandı
    derse kayıt eklenmez — yalnızca hâlâ yuva arayanlar gelir.
  * İlan tarihi (olusturma) Instagram paylaşım tarihidir; site bu alana göre
    sıraladığı için eski ilanlar en üstte değil, tarihlerindeki yerde durur.
  * İlan başına en fazla FOTO_SAYISI fotoğraf (depolama: GitHub Pages 1 GB).
  * Kayıtlar kaynak.geriye = true ile işaretlenir.
  * RapidAPI: "geriye" kategorisi, günde en fazla --butce istek (genel
    350/gün ve 120/saat sınırları rapidapi_kota.py'de geçerli).
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

import animals  # noqa: E402
import instagram_sync as sync  # noqa: E402
import rapidapi_kota  # noqa: E402
from yuvalanma_kontrol import baslikta_yuvalandi, sonraki_imlec, _caption  # noqa: E402

HEDEF_TARIH = "2026-04-11"   # 6 ay geriye (11.10.2026'da karar verildi)
FOTO_SAYISI = 3
KATEGORI = "geriye"
DURUM_PATH = Path(__file__).resolve().parent / "geriye_doldurma.json"
SAYFA_BEKLEME = 2  # sn, hız limiti
_GUN = 24 * 60 * 60

# Instagram kısa kodu, gönderi kimliğinin (media pk) base64 yazımıdır;
# kimliğin üst bitleri de milisaniye cinsinden paylaşım zamanıdır.
_ALFABE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
_IG_EPOCH_MS = 1314220021721


def kod_pk(kod: str) -> int:
    n = 0
    for ch in kod[:11]:
        n = n * 64 + _ALFABE.index(ch)
    return n


def kod_zaman(kod: str) -> float:
    return ((kod_pk(kod) >> 23) + _IG_EPOCH_MS) / 1000


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).replace(microsecond=0).isoformat()


def _yukle() -> dict:
    try:
        return json.loads(DURUM_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _kaydet(durum: dict) -> None:
    DURUM_PATH.write_text(json.dumps(durum, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")


def _baslangic(hesap: str, pk: str, gorulen: dict) -> dict:
    """Hesabın daha önce görülmüş en eski gönderisinden bir imleç kurar."""
    kodlar = [k for k, v in gorulen.items() if v.get("hesap") == hesap]
    if not kodlar:
        raise RuntimeError(f"@{hesap}: görülmüş gönderi yok, başlangıç noktası kurulamadı")
    en_eski = min(kodlar, key=kod_pk)
    return {"imlec": f"{kod_pk(en_eski)}_{pk}", "enEski": _iso(kod_zaman(en_eski)),
            "bitti": False}


def _bilinenler(gorulen: dict) -> set[str]:
    return {(a.get("kaynak") or {}).get("gonderiId")
            for a in animals.load() if a.get("kaynak")} | set(gorulen)


def _isle(item: dict, hesap: str, tur: str, args, gorulen: dict, sonuc: dict) -> None:
    """Tek gönderi: yuvalanmışsa atla, değilse ayrıştırıp kaydet."""
    gonderi = sync._rapid_gonderi(item)
    tarih = (gonderi["timestamp"] or "")[:10]
    if baslikta_yuvalandi(gonderi["caption"]):
        karar = "geriye: yuvalanmış"
        kayitlar = []
        print(f"  🏡 {tarih} yuvalanmış, atlandı: {gonderi['caption'][:50]!r}")
    else:
        kayitlar, neden = sync.gonderiyi_isle(
            gonderi, tur, hesap, fotograf_cek=not args.kuru,
            ai=args._ai and not args.kuru, en_fazla_foto=FOTO_SAYISI)
        karar = neden or "ilan"
        if any(k["durum"] == "yuvalandi" for k in kayitlar):
            # Ayrıştırıcı yuvalandı dedi (ör. ibare ilk iki satırda değil)
            kayitlar, karar = [], "geriye: yuvalanmış"
            print(f"  🏡 {tarih} yuvalanmış (ayrıştırıcı), atlandı")
        elif not kayitlar:
            print(f"  – {tarih} atlandı ({neden}): {gonderi['caption'][:50]!r}")
        for k in kayitlar:
            k["kaynak"]["geriye"] = True
            print(f"  ✓ {tarih} {k.get('isim') or 'İsimsiz'} — {sync._ozet(k)}")
    sonuc["yuvalanmis" if karar == "geriye: yuvalanmış" else
          "ilan" if kayitlar else "diger"] += 1
    sonuc["kayitlar"].extend(kayitlar)
    if not args.kuru:
        gorulen[gonderi["id"]] = {"hesap": hesap, "karar": karar,
                                  "tarih": animals.now_iso()}


def hesap_parcasi(hesap: str, tur: str, durum_h: dict, args, api_key: str,
                  gorulen: dict, sonuc: dict) -> None:
    """Hesabın akışında kaldığı yerden --gun gün (en fazla HEDEF_TARIH'e kadar) iner."""
    pk = sync.RAPID_PK[hesap]
    hedef = datetime.fromisoformat(HEDEF_TARIH).replace(tzinfo=timezone.utc).timestamp()
    alt = max(hedef, datetime.fromisoformat(durum_h["enEski"]).timestamp() - args.gun * _GUN)
    print(f"\n▸ @{hesap}: {durum_h['enEski'][:10]} → {_iso(alt)[:10]}")
    sayfa = 0
    while True:
        if rapidapi_kota.kategori_kullanim(KATEGORI) >= args.butce:
            print(f"  ! bugünkü geriye doldurma bütçesi ({args.butce} istek) doldu; kalan yarın")
            break
        if sayfa:
            time.sleep(SAYFA_BEKLEME)
        yanit = sync._rapid_get("/feed", {"user_id": pk, "next_max_id": durum_h["imlec"]},
                                api_key, KATEGORI)
        sayfa += 1
        bilinen = _bilinenler(gorulen)
        kendi = [it for it in yanit.get("items") or []
                 if it.get("taken_at") and not it.get("timeline_pinned_user_ids")]
        for it in sorted(kendi, key=lambda x: x["taken_at"], reverse=True):
            kod = it.get("code") or str(it.get("pk"))
            if it["taken_at"] < hedef or kod in bilinen:
                continue
            _isle(it, hesap, tur, args, gorulen, sonuc)
        if not args.kuru:
            # Her sayfadan sonra yaz: yarıda kesilirse işlenenler kaybolmaz
            if sonuc["kayitlar"]:
                e, g = sync.kaydet(sonuc["kayitlar"])
                sonuc["eklendi"] += e
                sonuc["kayitlar"] = []
            sync.gorulenleri_kaydet(gorulen)
        en_eski = min((it["taken_at"] for it in kendi), default=None)
        imlec = sonraki_imlec(yanit, pk)
        if en_eski is not None:
            durum_h["enEski"] = _iso(min(en_eski, datetime.fromisoformat(durum_h["enEski"]).timestamp()))
        if imlec:
            durum_h["imlec"] = imlec
        if not imlec or (en_eski is not None and en_eski < hedef):
            durum_h["bitti"] = True
            print(f"  ✔ @{hesap} hedef tarihe ({HEDEF_TARIH}) ulaştı")
            break
        if en_eski is not None and en_eski < alt:
            break
    sonuc["sayfa"] += sayfa


def main() -> int:
    ap = argparse.ArgumentParser(description="Geçmiş Instagram ilanlarını parça parça ekler.")
    ap.add_argument("--gun", type=int, default=30, help="Parça boyu, gün (varsayılan 30)")
    ap.add_argument("--butce", type=int, default=40,
                    help="Bugün bu işe en fazla kaç RapidAPI isteği (\"geriye\" kategorisi, varsayılan 40)")
    ap.add_argument("--hesap", choices=list(sync.HESAPLAR), help="Yalnızca bu hesap")
    ap.add_argument("--kuru", action="store_true",
                    help="Hiçbir şey yazma; AI ve fotoğraf yok, kural tabanlı önizleme")
    ap.add_argument("--durum", action="store_true", help="Nerede kalındığını göster")
    args = ap.parse_args()

    cfg = sync.config_yukle()
    api_key = cfg.get("rapidapi_key")
    args._ai = bool(cfg.get("openrouter_key"))
    gorulen = sync.gorulenleri_yukle()
    durum = _yukle()
    durum.setdefault("hedefTarih", HEDEF_TARIH)
    hesaplar = durum.setdefault("hesaplar", {})
    for hesap in sync.HESAPLAR:
        if hesap not in hesaplar:
            hesaplar[hesap] = _baslangic(hesap, sync.RAPID_PK[hesap], gorulen)

    if args.durum:
        for h, d in hesaplar.items():
            print(f"@{h}: {'bitti' if d['bitti'] else 'devam'} — en eski {d['enEski'][:10]}"
                  f" (hedef {HEDEF_TARIH})")
        print(rapidapi_kota.ozet())
        return 0
    if not api_key:
        print("! RapidAPI anahtarı yok (tools/instagram_config.json > rapidapi_key)")
        return 2
    if not args._ai and not args.kuru:
        print("! OpenRouter anahtarı yok; geçmiş ilanlar AI olmadan eklenmez.")
        return 2
    print("Kuru çalıştırma: hiçbir şey yazılmayacak, AI çağrılmayacak." if args.kuru
          else f"Ayrıştırıcı: AI · ilan başına en fazla {FOTO_SAYISI} fotoğraf")

    sonuc = {"ilan": 0, "yuvalanmis": 0, "diger": 0, "kayitlar": [], "eklendi": 0, "sayfa": 0}
    hata = None
    for hesap, tur in sync.HESAPLAR.items():
        if (args.hesap and hesap != args.hesap) or hesaplar[hesap]["bitti"]:
            continue
        # Kuru çalıştırma durumu ilerletmesin
        durum_h = dict(hesaplar[hesap]) if args.kuru else hesaplar[hesap]
        try:
            hesap_parcasi(hesap, tur, durum_h, args, api_key, gorulen, sonuc)
        except RuntimeError as e:      # KotaAsildi dahil
            hata = f"@{hesap}: {e}"
            print(f"  ! {hata}")
            break
        finally:
            if not args.kuru:
                durum.setdefault("parcalar", []).append({
                    "zaman": animals.now_iso(), "hesap": hesap,
                    "enEski": durum_h["enEski"], "bitti": durum_h["bitti"]})
                _kaydet(durum)

    print(f"\nSonuç: {sonuc['ilan']} ilan gönderisi"
          + (f" → {sonuc['eklendi']} kayıt eklendi" if not args.kuru else " (kuru: eklenmedi)")
          + f", {sonuc['yuvalanmis']} yuvalanmış, {sonuc['diger']} ilan değil · {sonuc['sayfa']} sayfa")
    print(rapidapi_kota.ozet())
    if not args.kuru and sonuc["eklendi"]:
        print("Sonraki adım: python tools/kucuk_foto.py (Pillow gerekir), sonra commit + PR.")
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
