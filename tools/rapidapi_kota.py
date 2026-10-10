# -*- coding: utf-8 -*-
"""
RapidAPI scraper için günlük kota bekçisi.

Plan günde 400 istek veriyor; biz kendimize GUNLUK_SINIR (350) koyuyoruz ve
bu sınıra ulaşıldığında istek HİÇ gönderilmez (KotaAsildi). Kullanım iki
kaynaktan izlenir, büyük olan esas alınır:

  1) Kendi sayacımız — her istekten ÖNCE artırılır (yeniden denemeler dahil).
  2) RapidAPI'nin döndürdüğü X-RateLimit-Requests-Limit / -Remaining /
     -Reset başlıkları — lokal ve CI'dan yapılan tüm istekleri kapsar.

Günlük pencere RapidAPI'nin kendi sıfırlanma anına göre işler (gece yarısı
değil): -Reset başlığı "kaç saniye sonra sıfırlanacak" bilgisini verir.
Durum tools/rapidapi_kota.json dosyasında tutulur; CI her çalıştırmada bu
dosyayı commit'ler ki bir sonraki çalıştırma kaldığı yerden devam etsin.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

GUNLUK_SINIR = 350
# Sağlayıcı, planda yazmayan kayan 1 saatlik bir limit uyguluyor (10.10.2026'da
# ~160 istekte 403 "reached requests limit"; pencereden çıkınca kendiliğinden
# açıldı). Altında kalmak için saatte en fazla SAATLIK_SINIR istek; dolarsa
# en eski istek pencereden çıkana kadar beklenir (en fazla BEKLEME_UST sn).
SAATLIK_SINIR = 120
BEKLEME_UST = 75 * 60
_SAAT = 60 * 60
KOTA_PATH = Path(__file__).resolve().parent / "rapidapi_kota.json"
_GUN = 24 * 60 * 60


class KotaAsildi(RuntimeError):
    """Günlük sınıra ulaşıldı; istek gönderilmedi."""


def _yukle() -> dict:
    try:
        return json.loads(KOTA_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _kaydet(durum: dict) -> None:
    durum["sonGuncelleme"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    KOTA_PATH.write_text(json.dumps(durum, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                         encoding="utf-8")


def _pencereyi_tazele(durum: dict, simdi: float) -> dict:
    """Pencere dolmuşsa sayaçları sıfırlar. Bitiş anı bilinmiyorsa geçici
    olarak 24 saat sonrası kabul edilir; ilk yanıtın -Reset başlığı düzeltir."""
    if simdi >= durum.get("pencereBitis", 0):
        durum["pencereBitis"] = int(simdi + _GUN)
        durum["bizimSayac"] = 0
        durum["kalan"] = None
        durum["kategoriler"] = {}
        durum["saglayiciLimiti"] = False
    return durum


def kullanilan(durum: dict) -> int:
    """Bu penceredeki kullanım: kendi sayacımız ile RapidAPI'nin söylediğinin büyüğü."""
    bizim = durum.get("bizimSayac", 0)
    limit, kalan = durum.get("planLimiti"), durum.get("kalan")
    if limit is not None and kalan is not None:
        return max(bizim, limit - kalan)
    return bizim


def izin_al(kategori: str | None = None) -> None:
    """Her istekten hemen önce çağrılır. Sınıra ulaşıldıysa KotaAsildi fırlatır;
    değilse isteği sayaca yazar (istek başarısız olsa bile harcanmış sayılır).
    `kategori` verilirse istek o kategorinin günlük sayacına da yazılır
    (ör. "yuvalanma" — kendi alt bütçesi olan işler için)."""
    durum = _pencereyi_tazele(_yukle(), time.time())
    if durum.get("saglayiciLimiti"):
        _kaydet(durum)
        raise KotaAsildi("API sağlayıcısı bu pencerede 'reached requests limit' döndürdü; "
                         f"istek gönderilmedi. Sıfırlanma: {_saat(durum['pencereBitis'])}")
    if kullanilan(durum) >= GUNLUK_SINIR:
        _kaydet(durum)
        raise KotaAsildi(f"RapidAPI günlük sınırı doldu ({kullanilan(durum)}/{GUNLUK_SINIR}); "
                         f"istek gönderilmedi. Sıfırlanma: {_saat(durum['pencereBitis'])}")
    simdi = time.time()
    son_saat = [t for t in durum.get("sonSaat", []) if t > simdi - _SAAT]
    if len(son_saat) >= SAATLIK_SINIR:
        bekle = min(son_saat) + _SAAT - simdi + 1
        if bekle > BEKLEME_UST:
            raise KotaAsildi(f"Saatlik sınır ({SAATLIK_SINIR}) dolu; {int(bekle)} sn beklemek gerekirdi.")
        print(f"  … saatlik sınır ({SAATLIK_SINIR}) dolu, {int(bekle)} sn bekleniyor")
        time.sleep(bekle)
        simdi = time.time()
        son_saat = [t for t in son_saat if t > simdi - _SAAT]
    durum["sonSaat"] = son_saat + [int(simdi)]
    durum["bizimSayac"] = durum.get("bizimSayac", 0) + 1
    if kategori:
        kat = durum.setdefault("kategoriler", {})
        kat[kategori] = kat.get(kategori, 0) + 1
    _kaydet(durum)


def saglayici_limitine_takildi() -> None:
    """Sağlayıcı (RapidAPI kotasından bağımsız) kendi limitini bildirdi: bu
    pencerenin geri kalanında istek gönderme — her deneme boşa harcanır."""
    durum = _pencereyi_tazele(_yukle(), time.time())
    durum["saglayiciLimiti"] = True
    _kaydet(durum)


def kategori_kullanim(kategori: str) -> int:
    """Bu penceredeki (günlük) o kategoriye ait istek sayısı."""
    durum = _pencereyi_tazele(_yukle(), time.time())
    return (durum.get("kategoriler") or {}).get(kategori, 0)


def yanit_isle(basliklar) -> None:
    """Yanıt başlıklarındaki gerçek kota bilgisini kaydeder (hata yanıtları dahil)."""
    if basliklar is None:
        return

    def sayi(ad):
        deger = basliklar.get(ad)
        try:
            return int(deger) if deger is not None else None
        except ValueError:
            return None

    limit = sayi("X-RateLimit-Requests-Limit")
    kalan = sayi("X-RateLimit-Requests-Remaining")
    sifirlanma = sayi("X-RateLimit-Requests-Reset")
    if limit is None and kalan is None:
        return
    durum = _pencereyi_tazele(_yukle(), time.time())
    if limit is not None:
        durum["planLimiti"] = limit
    if kalan is not None:
        durum["kalan"] = kalan
    if sifirlanma is not None:
        durum["pencereBitis"] = int(time.time() + sifirlanma)
    _kaydet(durum)


def _saat(epoch: int) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%d.%m.%Y %H:%M UTC")


def ozet() -> str:
    """Rapor/log satırı: 'Bugün 12 / 400 istek kullanıldı (kendi sınırımız 350) …'"""
    durum = _pencereyi_tazele(_yukle(), time.time())
    plan = durum.get("planLimiti") or "?"
    return (f"RapidAPI günlük kota: bugün {kullanilan(durum)} / {plan} istek kullanıldı "
            f"(kendi sınırımız {GUNLUK_SINIR}; sıfırlanma {_saat(durum['pencereBitis'])})")


if __name__ == "__main__":
    print(ozet())
