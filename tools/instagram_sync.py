#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kurtaran Ev — Instagram ilan çekme pipeline'ı.

İki çalışma kipi var:

  1) OTOMATİK (Instagram Graph API)
     python3 tools/instagram_sync.py --limit 5
     Çalışması için bir erişim jetonu (access token) gerekir. Instagram, giriş
     yapmadan gönderi içeriği vermiyor; bu yüzden resmî API şart. Kurulum
     adımları README ve to-do.md içinde.

  2) ELLE İÇE AKTARMA (jeton yokken)
     python3 tools/instagram_sync.py --dosya ornek_gonderiler.json
     Gönderi metinlerini ve fotoğraf yollarını bir JSON dosyasına koyup
     ayrıştırıcıdan geçirir. Dernek, API kurulumunu beklemeden çalışabilir.

Her iki kipte de kayıtlar `taslak` durumunda oluşur. Yönetici admin panelinden
onaylayana kadar sitede görünmezler — böylece hatalı ayrıştırma canlıya yansımaz.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import animals  # noqa: E402
from caption_parser import parse, ilan_mi, yuvalandi_mi  # noqa: E402

GRAPH = "https://graph.facebook.com/v21.0"
CONFIG_PATH = animals.ROOT / "tools" / "instagram_config.json"

# Hangi hesap hangi türe ait
HESAPLAR = {
    "kurtaranev_kopekleri": "kopek",
    "kurtaranev_kedileri": "kedi",
}


# ---------------------------------------------------------------------------
# Yapılandırma
# ---------------------------------------------------------------------------
def config_yukle() -> dict:
    """Jetonu önce ortam değişkeninden, sonra config dosyasından okur."""
    cfg = {}
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"! instagram_config.json bozuk: {e}")
    if os.environ.get("IG_ACCESS_TOKEN"):
        cfg["access_token"] = os.environ["IG_ACCESS_TOKEN"]
    return cfg


def ornek_config_yaz() -> None:
    ornek = {
        "_aciklama": "Instagram Graph API bilgileri. Bu dosyayı sürüm kontrolüne EKLEMEYİN.",
        "_kurulum": [
            "1. Her iki Instagram hesabını da İşletme (Business) hesabına çevirin.",
            "2. Hesapları bir Facebook Sayfası ile ilişkilendirin.",
            "3. developers.facebook.com'da bir uygulama oluşturun.",
            "4. instagram_basic ve pages_show_list izinlerini alın.",
            "5. Uzun ömürlü bir access token üretip aşağıya yazın.",
        ],
        "access_token": "BURAYA_UZUN_OMURLU_TOKEN",
        "hesaplar": {
            "kurtaranev_kopekleri": {"ig_user_id": "", "tur": "kopek"},
            "kurtaranev_kedileri": {"ig_user_id": "", "tur": "kedi"},
        },
    }
    CONFIG_PATH.write_text(json.dumps(ornek, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Örnek yapılandırma yazıldı: {CONFIG_PATH.relative_to(animals.ROOT)}")


# ---------------------------------------------------------------------------
# Graph API
# ---------------------------------------------------------------------------
def _get(url: str, params: dict) -> dict:
    tam = f"{url}?{urllib.parse.urlencode(params)}"
    istek = urllib.request.Request(tam, headers={"User-Agent": "KurtaranEv-Sync/1.0"})
    try:
        with urllib.request.urlopen(istek, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        govde = e.read().decode("utf-8", "replace")[:400]
        raise RuntimeError(f"Graph API {e.code}: {govde}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Ağ hatası: {e.reason}") from e


def ig_user_id_bul(token: str, kullanici_adi: str) -> str | None:
    """Bağlı Facebook sayfalarından ilgili Instagram işletme hesabını bulur."""
    sayfalar = _get(f"{GRAPH}/me/accounts",
                    {"access_token": token, "fields": "instagram_business_account{id,username}"})
    for sayfa in sayfalar.get("data", []):
        iba = sayfa.get("instagram_business_account")
        if iba and iba.get("username") == kullanici_adi:
            return iba["id"]
    return None


def gonderileri_cek(token: str, ig_user_id: str, limit: int) -> list[dict]:
    alanlar = "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp,children{media_url,media_type}"
    veri = _get(f"{GRAPH}/{ig_user_id}/media",
                {"access_token": token, "fields": alanlar, "limit": limit})
    return veri.get("data", [])


# ---------------------------------------------------------------------------
# Fotoğraf indirme
# ---------------------------------------------------------------------------
def fotograf_indir(url: str, dosya_adi: str) -> str | None:
    """Fotoğrafı site/assets/img/animals altına indirir, web yolunu döndürür."""
    animals.PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    hedef = animals.PHOTO_DIR / dosya_adi
    if hedef.exists():
        return f"{animals.PHOTO_WEB_PREFIX}/{dosya_adi}"
    try:
        istek = urllib.request.Request(url, headers={"User-Agent": "KurtaranEv-Sync/1.0"})
        with urllib.request.urlopen(istek, timeout=60) as r:
            icerik = r.read()
        if len(icerik) < 1024:
            print(f"  ! fotoğraf çok küçük, atlandı: {dosya_adi}")
            return None
        hedef.write_bytes(icerik)
        return f"{animals.PHOTO_WEB_PREFIX}/{dosya_adi}"
    except Exception as e:  # ağ hataları ilanın tamamını düşürmemeli
        print(f"  ! fotoğraf indirilemedi ({dosya_adi}): {e}")
        return None


def gonderi_fotograflari(gonderi: dict, ig_id: str) -> list[str]:
    yollar = []
    adaylar = []
    if gonderi.get("media_type") == "CAROUSEL_ALBUM":
        for c in (gonderi.get("children", {}).get("data") or []):
            if c.get("media_type") == "IMAGE" and c.get("media_url"):
                adaylar.append(c["media_url"])
    elif gonderi.get("media_url"):
        adaylar.append(gonderi["media_url"])
    elif gonderi.get("thumbnail_url"):
        adaylar.append(gonderi["thumbnail_url"])

    for i, url in enumerate(adaylar[:6]):
        uzanti = ".jpg"
        yol = fotograf_indir(url, f"ig-{ig_id}-{i}{uzanti}")
        if yol:
            yollar.append(yol)
    return yollar


# ---------------------------------------------------------------------------
# Gönderi → kayıt
# ---------------------------------------------------------------------------
def gonderiyi_isle(gonderi: dict, tur: str, kullanici: str, fotograf_cek: bool = True) -> dict | None:
    caption = gonderi.get("caption") or ""
    if not ilan_mi(caption):
        return None

    kayit = parse(caption, varsayilan_tur=tur)
    kayit["tur"] = tur  # hesap hangi türse o kazanır
    kayit["durum"] = "yuvalandi" if yuvalandi_mi(caption) else "taslak"
    kayit["konum"] = kayit.get("konum") or None
    kayit["kaynak"] = {
        "tip": "instagram",
        "hesap": kullanici,
        "gonderiId": gonderi.get("id"),
        "baglanti": gonderi.get("permalink"),
        "tarih": gonderi.get("timestamp"),
    }
    kayit["olusturma"] = gonderi.get("timestamp") or animals.now_iso()

    if fotograf_cek:
        kayit["fotograflar"] = gonderi_fotograflari(gonderi, gonderi.get("id", "x"))

    return kayit


def kaydet(yeni_kayitlar: list[dict]) -> tuple[int, int]:
    """Aynı gönderi daha önce alındıysa günceller, yoksa ekler."""
    mevcut = animals.load()
    id_by_post = {
        (a.get("kaynak") or {}).get("gonderiId"): a
        for a in mevcut if (a.get("kaynak") or {}).get("gonderiId")
    }
    eklendi = guncellendi = 0

    for kayit in yeni_kayitlar:
        post_id = (kayit.get("kaynak") or {}).get("gonderiId")
        onceki = id_by_post.get(post_id)
        if onceki:
            # Yöneticinin elle düzelttiği alanları EZME: yalnızca boş olanları doldur.
            for alan, deger in kayit.items():
                if alan in ("id", "olusturma", "durum"):
                    continue
                if onceki.get(alan) in (None, [], "") and deger not in (None, [], ""):
                    onceki[alan] = deger
            guncellendi += 1
        else:
            kayit["id"] = animals.make_id(kayit["tur"], kayit.get("isim"), post_id or "")
            mevcut.append(kayit)
            eklendi += 1

    normalize_edilmis = []
    for ham in mevcut:
        kayit, hatalar = animals.normalize(ham)
        if hatalar:
            print(f"  ! {ham.get('id')}: {'; '.join(hatalar)}")
        normalize_edilmis.append(kayit)
    animals.save(normalize_edilmis)
    return eklendi, guncellendi


# ---------------------------------------------------------------------------
# Kipler
# ---------------------------------------------------------------------------
def kip_api(args) -> int:
    cfg = config_yukle()
    token = args.token or cfg.get("access_token")
    if not token or token.startswith("BURAYA"):
        print(HATA_JETON_YOK)
        return 2

    toplam = []
    for kullanici, tur in HESAPLAR.items():
        hesap_cfg = (cfg.get("hesaplar") or {}).get(kullanici, {})
        ig_id = hesap_cfg.get("ig_user_id")
        print(f"\n▸ @{kullanici} ({tur})")
        try:
            if not ig_id:
                ig_id = ig_user_id_bul(token, kullanici)
                if not ig_id:
                    print(f"  ! Hesap bulunamadı. İşletme hesabı olduğundan ve "
                          f"Facebook sayfasına bağlı olduğundan emin olun.")
                    continue
                print(f"  ig_user_id: {ig_id}")
            gonderiler = gonderileri_cek(token, ig_id, args.limit)
        except RuntimeError as e:
            print(f"  ! {e}")
            continue

        print(f"  {len(gonderiler)} gönderi alındı")
        for g in gonderiler:
            kayit = gonderiyi_isle(g, tur, kullanici, fotograf_cek=not args.kuru)
            if kayit is None:
                print(f"  – atlandı (ilan değil): {(g.get('caption') or '')[:50]}…")
                continue
            print(f"  ✓ {kayit.get('isim') or 'İsimsiz'} — {_ozet(kayit)}")
            toplam.append(kayit)

    if args.kuru:
        print(f"\n[kuru çalıştırma] {len(toplam)} ilan işlenirdi, hiçbir şey yazılmadı.")
        return 0

    eklendi, guncellendi = kaydet(toplam)
    print(f"\n{eklendi} yeni ilan eklendi, {guncellendi} ilan güncellendi.")
    print("Hepsi TASLAK durumunda — admin panelinden onaylayın: site/admin.html")
    return 0


def kip_dosya(args) -> int:
    """Elle hazırlanmış gönderi listesinden içe aktarır."""
    yol = Path(args.dosya)
    if not yol.is_absolute():
        yol = animals.ROOT / yol
    if not yol.exists():
        print(f"! Dosya yok: {yol}")
        return 2

    gonderiler = json.loads(yol.read_text(encoding="utf-8"))
    if isinstance(gonderiler, dict):
        gonderiler = gonderiler.get("gonderiler", [])

    toplam = []
    for g in gonderiler:
        kullanici = g.get("hesap") or "kurtaranev_kopekleri"
        tur = HESAPLAR.get(kullanici, g.get("tur", "kopek"))
        kayit = gonderiyi_isle(g, tur, kullanici, fotograf_cek=False)
        if kayit is None:
            print(f"  – atlandı (ilan değil): {(g.get('caption') or '')[:50]}…")
            continue
        # yerel fotoğraf yolları doğrudan kullanılır
        kayit["fotograflar"] = [f for f in (g.get("fotograflar") or [])]
        print(f"  ✓ {kayit.get('isim') or 'İsimsiz'} — {_ozet(kayit)}")
        toplam.append(kayit)

    if args.kuru:
        print(f"\n[kuru çalıştırma] {len(toplam)} ilan işlenirdi.")
        return 0

    eklendi, guncellendi = kaydet(toplam)
    print(f"\n{eklendi} yeni ilan eklendi, {guncellendi} ilan güncellendi.")
    return 0


def _ozet(kayit: dict) -> str:
    parcalar = []
    if kayit.get("cinsiyet"):
        parcalar.append(animals.SEX[kayit["cinsiyet"]])
    if kayit.get("yasAy") is not None:
        parcalar.append(animals.yas_metni(kayit["yasAy"]))
    if kayit.get("kiloKg") is not None:
        parcalar.append(f"{kayit['kiloKg']:g} kg")
    if kayit.get("cins"):
        parcalar.append(kayit["cins"])
    return ", ".join(parcalar) or "bilgi yok"


HATA_JETON_YOK = """
────────────────────────────────────────────────────────────────────
Instagram erişim jetonu bulunamadı.

Instagram, giriş yapmadan gönderi metni ve fotoğraflarını PAYLAŞMIYOR.
(Deneyip doğruladık: profil sayfası login duvarına düşüyor, herkese açık
JSON uçları da kapatılmış.) Bu yüzden otomatik akış için resmî
Instagram Graph API şart.

Kurulum:
  1. @kurtaranev_kopekleri ve @kurtaranev_kedileri hesaplarını
     İşletme (Business) hesabına çevirin.
  2. Her ikisini de bir Facebook Sayfası ile ilişkilendirin.
  3. developers.facebook.com üzerinde bir uygulama oluşturun.
  4. instagram_basic + pages_show_list izinlerini alın.
  5. Uzun ömürlü access token üretin.
  6. Jetonu şu iki yoldan biriyle verin:
       export IG_ACCESS_TOKEN="..."
     ya da
       python3 tools/instagram_sync.py --ornek-config
     ile oluşan tools/instagram_config.json dosyasına yazın.

Jeton olmadan da çalışabilirsiniz:
  python3 tools/instagram_sync.py --dosya tools/ornek_gonderiler.json
────────────────────────────────────────────────────────────────────
"""


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Instagram ilanlarını siteye aktarır.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--limit", type=int, default=5, help="Hesap başına gönderi sayısı (varsayılan 5)")
    ap.add_argument("--token", help="Instagram Graph API erişim jetonu")
    ap.add_argument("--dosya", help="Elle hazırlanmış gönderi JSON dosyası")
    ap.add_argument("--kuru", action="store_true", help="Hiçbir şey yazma, sadece ne olacağını göster")
    ap.add_argument("--ornek-config", action="store_true", help="Örnek yapılandırma dosyası oluştur")
    args = ap.parse_args()

    if args.ornek_config:
        ornek_config_yaz()
        return 0
    if args.dosya:
        return kip_dosya(args)
    return kip_api(args)


if __name__ == "__main__":
    raise SystemExit(main())
