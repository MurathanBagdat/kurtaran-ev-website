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

Varsayılan davranış: ilanlar DOĞRUDAN yayınlanır ("yuva-ariyor"); YUVALANDI
başlıklı gönderiler "yuvalandi" durumuyla gelir. `--taslak` bayrağı verilirse
kayıtlar taslak oluşur ve admin paneli onayı bekler (ihtiyatlı kip).
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
import ai_parser  # noqa: E402
from caption_parser import parse_all, icerik_turu, yuvalandi_mi  # noqa: E402

GRAPH = "https://graph.facebook.com/v21.0"
CONFIG_PATH = animals.ROOT / "tools" / "instagram_config.json"

# RapidAPI "Social Download All In One" — tek bir gönderi bağlantısından
# caption + fotoğrafları verir. Hesabın akışını LİSTELEYEMEZ; o yüzden
# Graph API'nin yerini tutmaz, --link kipiyle yarı otomatik çalışır.
RAPIDAPI_HOST = "social-download-all-in-one.p.rapidapi.com"
RAPIDAPI_URL = f"https://{RAPIDAPI_HOST}/v1/social/autolink"

# RapidAPI "Instagram API - Fast & Reliable Data Scraper" — hesabın gönderi
# AKIŞINI listeleyebilir (/profile → pk, /feed?user_id=pk). Resmî API değildir;
# Instagram'ın kullanım koşulları dışıdır ve her an kırılabilir. Graph API
# jetonu gelene kadar --rapid kipiyle köprü olarak kullanılır.
RAPID_SCRAPER_HOST = "instagram-api-fast-reliable-data-scraper.p.rapidapi.com"

# Hangi hesap hangi türe ait
HESAPLAR = {
    "kurtaranev_kopekleri": "kopek",
    "kurtaranev_kedileri": "kedi",
}

# Hesapların Instagram sayısal kimlikleri (değişmez, herkese açık bilgi).
# Koda sabitlendi ki her çalıştırmada /profile isteği harcanmasın —
# RapidAPI Basic paketinde ayda yalnızca 100 istek hakkı var.
RAPID_PK = {
    "kurtaranev_kopekleri": "42022514534",
    "kurtaranev_kedileri": "23565664304",
}

# Değerlendirilmiş TÜM gönderilerin kalıcı hafızası (karar dahil).
# "İlan değil" denen gönderiler kayıt üretmediği için animals.json'dan
# bilinemez; bu dosya olmasa her çalıştırmada yeniden AI'ya giderlerdi.
GORULEN_PATH = animals.ROOT / "tools" / "gorulen_gonderiler.json"


def gorulenleri_yukle() -> dict:
    if not GORULEN_PATH.exists():
        return {}
    try:
        return json.loads(GORULEN_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def gorulenleri_kaydet(gorulen: dict) -> None:
    GORULEN_PATH.write_text(json.dumps(gorulen, ensure_ascii=False, indent=2,
                                       sort_keys=True) + "\n", encoding="utf-8")


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
    if os.environ.get("RAPIDAPI_KEY"):
        cfg["rapidapi_key"] = os.environ["RAPIDAPI_KEY"]
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
            "6. Jetonu 60 gün dolmadan tazelemek için: python3 tools/instagram_sync.py --jeton-yenile",
            "   (app_id ve app_secret gerektirir; uygulamanın Ayarlar > Temel sayfasında).",
        ],
        "access_token": "BURAYA_UZUN_OMURLU_TOKEN",
        "app_id": "",
        "app_secret": "",
        "rapidapi_key": "",
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


def kip_jeton_yenile(args) -> int:
    """Uzun ömürlü jetonu tazeler (60 günlük ömrü sıfırlar) ve config'e yazar.

    Meta'nın fb_exchange_token akışı: mevcut geçerli uzun ömürlü jeton,
    app_id + app_secret ile yenisiyle değiştirilir. Jeton süresi DOLDUKTAN
    sonra çalışmaz — cron ile örn. ayda bir çalıştırın.
    """
    cfg = config_yukle()
    token = args.token or cfg.get("access_token")
    app_id, app_secret = cfg.get("app_id"), cfg.get("app_secret")
    if not token or token.startswith("BURAYA"):
        print("! Yenilenecek jeton yok. Önce access_token'ı config dosyasına yazın.")
        return 2
    if not app_id or not app_secret:
        print("! app_id ve app_secret gerekli (tools/instagram_config.json).\n"
              "  developers.facebook.com > uygulamanız > Ayarlar > Temel sayfasından alın.")
        return 2

    try:
        veri = _get(f"{GRAPH}/oauth/access_token", {
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": token,
        })
    except RuntimeError as e:
        print(f"! Jeton yenilenemedi: {e}")
        return 1

    yeni = veri.get("access_token")
    if not yeni:
        print(f"! Beklenmedik yanıt: {veri}")
        return 1

    cfg["access_token"] = yeni
    cfg["_jeton_yenileme_tarihi"] = animals.now_iso()
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ Jeton yenilendi ve kaydedildi: {CONFIG_PATH.relative_to(animals.ROOT)}")
    if os.environ.get("IG_ACCESS_TOKEN"):
        print("  Not: IG_ACCESS_TOKEN ortam değişkeni hâlâ ESKİ jetonu taşıyor olabilir;")
        print("  config dosyası kullanılıyorsa sorun yok, değilse değişkeni güncelleyin.")
    return 0


def _jeton_yasi_uyarisi(cfg: dict) -> None:
    """Jeton 50 günden eskiyse hatırlat (uzun ömürlü jeton 60 günde ölür)."""
    tarih = cfg.get("_jeton_yenileme_tarihi")
    if not tarih:
        return
    from datetime import datetime, timezone
    try:
        yas_gun = (datetime.now(timezone.utc) - datetime.fromisoformat(tarih)).days
    except ValueError:
        return
    if yas_gun >= 50:
        print(f"! Jeton {yas_gun} günlük — 60 günde geçersizleşir. "
              f"Yenilemek için: python3 tools/instagram_sync.py --jeton-yenile")


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
ATLAMA_NEDENI = {
    "koruyucu-melek": "Koruyucu Melek çağrısı",
    "yuvalandi": "yuvalanma duyurusu",
    "yuvalandi-duyurusu": "yuvalanma duyurusu",
    "diger": "ilan değil",
}

# ai_parser'ın hayvan sözlüğünden kayda birebir taşınan alanlar
AI_ALANLAR = ("isim", "tur", "cinsiyet", "yasAy", "kiloKg", "cins", "boyut", "renk",
              "kisir", "asili", "cipli", "cocuklaUyum", "kopeklerleUyum",
              "kedilerleUyum", "ozelBakim", "saglikNotu", "konum", "karakter",
              "aciklama", "tahmini",
              # İngilizce karşılıklar — yalnızca AI ayrıştırmasında dolar;
              # kural tabanlı yolda boş kalır, arayüz Türkçesine düşer.
              "cinsEn", "renkEn", "saglikNotuEn", "konumEn", "karakterEn", "aciklamaEn")


def gonderiyi_isle(gonderi: dict, tur: str, kullanici: str, fotograf_cek: bool = True,
                   ai: bool = False, yayinla: bool = True) -> tuple[list[dict], str | None]:
    """Bir gönderiden 0, 1 ya da birden çok (kardeş ilanı) kayıt üretir.

    (kayitlar, atlama_nedeni) döner: gönderi ilan değilse kayıtlar boş,
    neden dolu gelir. ai=True ise ayrıştırma OpenRouter/Gemini'ye yaptırılır;
    model hata verirse kural tabanlı ayrıştırıcıya düşülür.
    """
    caption = gonderi.get("caption") or ""
    kayitlar = None
    yuvalandi = None
    ayristirici = "kural"
    # tur=None gelirse (bağlantıdan hesap anlaşılamadı) ayrıştırıcının
    # metinden çıkardığı tür kullanılır; o da yoksa kopek varsayılır.

    if ai:
        try:
            sonuc = ai_parser.ai_parse(caption)
        except RuntimeError as e:
            print(f"  ! AI ayrıştırılamadı, kural tabanlıya dönüldü: {e}")
        else:
            ayristirici = "ai"
            if sonuc["icerikTuru"] != "ilan":
                return [], ATLAMA_NEDENI.get(sonuc["icerikTuru"], "ilan değil")
            yuvalandi = bool(sonuc.get("yuvalandi"))
            kayitlar = [{alan: h.get(alan) for alan in AI_ALANLAR}
                        for h in sonuc.get("hayvanlar") or []]
            if not kayitlar:
                return [], "ilan ama hayvan bilgisi çıkarılamadı"

    if kayitlar is None:  # kural tabanlı yol (ai kapalı ya da model hatası)
        if icerik_turu(caption) != "ilan":
            return [], ATLAMA_NEDENI.get(icerik_turu(caption), "ilan değil")
        kayitlar = parse_all(caption, varsayilan_tur=tur or "kopek")
        yuvalandi = yuvalandi_mi(caption)

    fotograflar = None
    if fotograf_cek:
        fotograflar = gonderi_fotograflari(gonderi, gonderi.get("id", "x"))

    for sira, kayit in enumerate(kayitlar):
        kayit["tur"] = tur or kayit.get("tur") or "kopek"  # hesap türü biliniyorsa o kazanır
        kayit["durum"] = ("yuvalandi" if yuvalandi
                          else "yuva-ariyor" if yayinla else "taslak")
        kayit["konum"] = kayit.get("konum") or None
        kayit["kaynak"] = {
            "tip": "instagram",
            "hesap": kullanici,
            "gonderiId": gonderi.get("id"),
            "sira": sira,  # aynı gönderiden çıkan kaçıncı kayıt (kardeş ilanları)
            "ayristirici": ayristirici,
            "baglanti": gonderi.get("permalink"),
            "tarih": gonderi.get("timestamp"),
        }
        kayit["olusturma"] = gonderi.get("timestamp") or animals.now_iso()
        if fotograflar is not None:
            kayit["fotograflar"] = list(fotograflar)

    return kayitlar, None


def _kaynak_anahtari(kayit: dict) -> tuple | None:
    """Gönderi + sıra ikilisi: kardeş ilanlarında aynı gönderiden birden çok
    kayıt çıktığı için tek başına gonderiId yetmiyor."""
    kaynak = kayit.get("kaynak") or {}
    if not kaynak.get("gonderiId"):
        return None
    return (kaynak["gonderiId"], kaynak.get("sira") or 0)


def kaydet(yeni_kayitlar: list[dict]) -> tuple[int, int]:
    """Aynı gönderi daha önce alındıysa günceller, yoksa ekler."""
    mevcut = animals.load()
    id_by_post = {
        _kaynak_anahtari(a): a for a in mevcut if _kaynak_anahtari(a)
    }
    eklendi = guncellendi = 0

    for kayit in yeni_kayitlar:
        post_id = (kayit.get("kaynak") or {}).get("gonderiId")
        onceki = id_by_post.get(_kaynak_anahtari(kayit))
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
    _jeton_yasi_uyarisi(cfg)

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
            kayitlar, neden = gonderiyi_isle(g, tur, kullanici,
                                             fotograf_cek=not args.kuru, ai=args._ai,
                                             yayinla=not args.taslak)
            if not kayitlar:
                print(f"  – atlandı ({neden}): {(g.get('caption') or '')[:50]}…")
                continue
            for kayit in kayitlar:
                print(f"  ✓ {kayit.get('isim') or 'İsimsiz'} — {_ozet(kayit)}")
            toplam.extend(kayitlar)

    if args.kuru:
        print(f"\n[kuru çalıştırma] {len(toplam)} ilan işlenirdi, hiçbir şey yazılmadı.")
        return 0

    eklendi, guncellendi = kaydet(toplam)
    print(f"\n{eklendi} yeni ilan eklendi, {guncellendi} ilan güncellendi.")
    print("Taslaklar admin panelinden onay bekliyor: site/admin.html" if args.taslak
          else "İlanlar doğrudan yayınlandı (yuva arıyor).")
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
        kayitlar, neden = gonderiyi_isle(g, tur, kullanici, fotograf_cek=False,
                                         ai=args._ai, yayinla=not args.taslak)
        if not kayitlar:
            print(f"  – atlandı ({neden}): {(g.get('caption') or '')[:50]}…")
            continue
        for kayit in kayitlar:
            # yerel fotoğraf yolları doğrudan kullanılır
            kayit["fotograflar"] = [f for f in (g.get("fotograflar") or [])]
            print(f"  ✓ {kayit.get('isim') or 'İsimsiz'} — {_ozet(kayit)}")
        toplam.extend(kayitlar)

    if args.kuru:
        print(f"\n[kuru çalıştırma] {len(toplam)} ilan işlenirdi.")
        return 0

    eklendi, guncellendi = kaydet(toplam)
    print(f"\n{eklendi} yeni ilan eklendi, {guncellendi} ilan güncellendi.")
    return 0


def _autolink_cek(gonderi_url: str, api_key: str) -> dict:
    """RapidAPI autolink ucundan gönderinin caption + medya listesini alır."""
    govde = json.dumps({"url": gonderi_url}).encode("utf-8")
    istek = urllib.request.Request(RAPIDAPI_URL, data=govde, headers={
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": api_key,
        "Content-Type": "application/json",
        "User-Agent": "KurtaranEv-Sync/1.0",
    })
    try:
        with urllib.request.urlopen(istek, timeout=60) as r:
            veri = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"RapidAPI {e.code}: {e.read().decode('utf-8', 'replace')[:300]}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Ağ hatası: {e.reason}") from e
    if veri.get("error"):
        raise RuntimeError(f"RapidAPI hata döndürdü: {str(veri)[:300]}")
    return veri


def _rapid_get(path: str, params: dict, api_key: str) -> dict:
    """Scraper API'sine GET atar; hız limitine takılırsa bekleyip yeniden dener."""
    import time
    url = f"https://{RAPID_SCRAPER_HOST}{path}?{urllib.parse.urlencode(params)}"
    istek = urllib.request.Request(url, headers={
        "x-rapidapi-host": RAPID_SCRAPER_HOST,
        "x-rapidapi-key": api_key,
        "User-Agent": "KurtaranEv-Sync/1.0",
    })
    for deneme in range(4):
        try:
            with urllib.request.urlopen(istek, timeout=60) as r:
                veri = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and deneme < 3:
                time.sleep(5)
                continue
            raise RuntimeError(f"Scraper API {e.code}: {e.read().decode('utf-8', 'replace')[:200]}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Ağ hatası: {e.reason}") from e
        if isinstance(veri, dict) and veri.get("message") == "Too many requests" and deneme < 3:
            time.sleep(5)
            continue
        return veri
    raise RuntimeError("Scraper API hız limiti: denemeler tükendi")


def _rapid_pk(kullanici: str, api_key: str, cfg: dict) -> str:
    """Hesabın sayısal kimliğini bulur; bulduğunu config'e önbellekler."""
    hesap_cfg = (cfg.get("hesaplar") or {}).get(kullanici) or {}
    if hesap_cfg.get("rapid_pk"):
        return str(hesap_cfg["rapid_pk"])
    if kullanici in RAPID_PK:
        return RAPID_PK[kullanici]
    profil = _rapid_get("/profile", {"username": kullanici}, api_key)
    pk = profil.get("pk")
    if not pk:
        raise RuntimeError(f"Profil bulunamadı: {profil.get('error') or profil}")
    cfg.setdefault("hesaplar", {}).setdefault(kullanici, {})["rapid_pk"] = str(pk)
    if CONFIG_PATH.exists():  # önbelleği yalnızca mevcut config dosyasına yaz
        CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
    return str(pk)


def _rapid_gonderi(item: dict) -> dict:
    """Scraper akış öğesini Graph API gönderi biçimine çevirir."""
    from datetime import datetime, timezone

    def gorsel(m):
        adaylar = (m.get("image_versions2") or {}).get("candidates") or []
        return adaylar[0].get("url") if adaylar else None

    caption = item.get("caption")
    caption = (caption or {}).get("text", "") if isinstance(caption, dict) else (caption or "")
    kod = item.get("code") or str(item.get("pk", ""))
    ts = item.get("taken_at")
    zaman = (datetime.fromtimestamp(ts, timezone.utc).replace(microsecond=0).isoformat()
             if ts else None)

    gonderi = {
        "id": kod,
        "caption": caption,
        "permalink": f"https://www.instagram.com/p/{kod}/",
        "timestamp": zaman,
    }
    if item.get("carousel_media"):
        gonderi["media_type"] = "CAROUSEL_ALBUM"
        gonderi["children"] = {"data": [
            {"media_type": "IMAGE", "media_url": u}
            for u in (gorsel(cm) for cm in item["carousel_media"]) if u
        ]}
    else:
        gonderi["media_type"] = "IMAGE"
        gonderi["media_url"] = gorsel(item)
    return gonderi


def kip_rapid(args) -> int:
    """Her iki hesabın son N gönderisini scraper API ile çekip akışa sokar."""
    import time
    cfg = config_yukle()
    api_key = cfg.get("rapidapi_key")
    if not api_key:
        print("! RapidAPI anahtarı yok. RAPIDAPI_KEY ortam değişkeni ya da "
              "tools/instagram_config.json içindeki rapidapi_key alanı gerekli.")
        return 2

    toplam = []
    hatalar = []
    for kullanici, tur in HESAPLAR.items():
        print(f"\n▸ @{kullanici} ({tur})")
        try:
            pk = _rapid_pk(kullanici, api_key, cfg)
            time.sleep(2)  # ücretsiz katman hız limiti
            akis = _rapid_get("/feed", {"user_id": pk}, api_key)
        except RuntimeError as e:
            print(f"  ! {e}")
            hatalar.append(f"@{kullanici}: {e}")
            continue

        # Sabitlenmiş gönderiler listenin başında ama eski olabilir;
        # tarihe göre sıralayıp gerçekten en yeni N tanesini al.
        items = sorted(akis.get("items") or [], key=lambda x: x.get("taken_at") or 0,
                       reverse=True)[: args.limit]
        print(f"  {len(items)} gönderi alındı (en yeniler)")
        gorulen = gorulenleri_yukle()
        bilinen = {(a.get("kaynak") or {}).get("gonderiId")
                   for a in animals.load() if a.get("kaynak")} | set(gorulen)
        for item in items:
            gonderi = _rapid_gonderi(item)
            # Daha önce değerlendirilen gönderiyi yeniden ayrıştırma — "ilan
            # değil" denenler dahil (AI isteği + indirme tasarrufu).
            # --guncelle ile eski davranışa dönülür: boş alanlar tazelenir.
            if not args.guncelle and gonderi["id"] in bilinen:
                print(f"  = daha önce değerlendirildi, atlandı: {gonderi['id']}")
                continue
            kayitlar, neden = gonderiyi_isle(gonderi, tur, kullanici,
                                             fotograf_cek=not args.kuru, ai=args._ai,
                                             yayinla=not args.taslak)
            if not args.kuru:
                gorulen[gonderi["id"]] = {"hesap": kullanici,
                                          "karar": neden or "ilan",
                                          "tarih": animals.now_iso()}
                gorulenleri_kaydet(gorulen)
            if not kayitlar:
                print(f"  – atlandı ({neden}): {gonderi['caption'][:50]}…")
                continue
            for kayit in kayitlar:
                print(f"  ✓ {kayit.get('isim') or 'İsimsiz'} — {_ozet(kayit)}"
                      + (" [yuvalandı]" if kayit["durum"] == "yuvalandi" else ""))
            toplam.extend(kayitlar)
        time.sleep(2)

    if args.kuru:
        print(f"\n[kuru çalıştırma] {len(toplam)} ilan işlenirdi, hiçbir şey yazılmadı.")
        return 0
    if not toplam:
        _rapor_yaz([], 0, 0, hatalar)
        if hatalar:  # hiçbir şey işlenemedi ve hata var → cron kırmızıya düşsün
            return 1
        # cron için normal bir sonuç: yeni gönderi yoksa iş başarıyla bitmiştir
        print("\nYeni ilan yok.")
        return 0

    eklendi, guncellendi = kaydet(toplam)
    print(f"\n{eklendi} yeni ilan eklendi, {guncellendi} ilan güncellendi.")
    print("Taslaklar admin panelinden onay bekliyor: site/admin.html" if args.taslak
          else "İlanlar doğrudan yayınlandı (yuva arıyor).")
    _rapor_yaz(toplam, eklendi, guncellendi, hatalar)
    return 0


def _rapor_yaz(kayitlar: list[dict], eklendi: int, guncellendi: int,
               hatalar: list[str]) -> None:
    """SYNC_RAPOR ortam değişkeni bir dosya yolu gösteriyorsa markdown rapor yazar.

    GitHub Actions bu dosyayı issue yorumu olarak gönderir → e-posta bildirimi.
    Sessiz çalışmalarda (yeni ilan yok, hata yok) dosya yazılmaz ki mail gitmesin.
    """
    yol = os.environ.get("SYNC_RAPOR")
    if not yol or (not kayitlar and not hatalar):
        return
    from datetime import datetime, timezone
    satirlar = [f"## Instagram senkron raporu — "
                f"{datetime.now(timezone.utc).strftime('%d.%m.%Y %H:%M')} UTC", ""]
    if kayitlar:
        satirlar.append(f"**{eklendi} yeni ilan eklendi, {guncellendi} ilan güncellendi:**")
        satirlar.append("")
        for k in kayitlar:
            baglanti = (k.get("kaynak") or {}).get("baglanti") or ""
            durum = animals.STATUS.get(k.get("durum"), k.get("durum"))
            satirlar.append(f"- [{k.get('isim') or 'İsimsiz'}]({baglanti}) — "
                            f"{_ozet(k)} · {durum}")
        satirlar.append("")
        satirlar.append("Canlı site: https://murathanbagdat.github.io/kurtaran-ev-website/")
    if hatalar:
        satirlar += ["", "### ⚠️ Hatalar", ""] + [f"- {h}" for h in hatalar]
    Path(yol).write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    print(f"Rapor yazıldı: {yol}")


LINK_DESENI = re.compile(r"instagram\.com/(?:([A-Za-z0-9_.]+)/)?(?:p|reel)/([A-Za-z0-9_-]+)")


def kip_link(args) -> int:
    """Gönderi bağlantılarını RapidAPI üzerinden çekip normal akışa sokar.

    Graph API jetonu gelene kadarki ara çözüm: hesap sahibi/yönetici gönderinin
    bağlantısını kopyalar, bu kip caption + fotoğrafları indirir. Kayıtlar yine
    taslak oluşur ve panel onayı bekler.
    """
    cfg = config_yukle()
    api_key = cfg.get("rapidapi_key")
    if not api_key:
        print("! RapidAPI anahtarı yok. RAPIDAPI_KEY ortam değişkeni ya da "
              "tools/instagram_config.json içindeki rapidapi_key alanı gerekli.")
        return 2

    toplam = []
    for url in args.link:
        m = LINK_DESENI.search(url)
        if not m:
            print(f"  ! Gönderi bağlantısı anlaşılamadı: {url}")
            continue
        kullanici, shortcode = m.group(1), m.group(2)
        kullanici = kullanici if kullanici in HESAPLAR else None
        print(f"\n▸ {shortcode}" + (f" (@{kullanici})" if kullanici else ""))

        try:
            veri = _autolink_cek(url, api_key)
        except RuntimeError as e:
            print(f"  ! {e}")
            continue

        # Bağlantıda hesap adı yoksa gönderinin yazarından çıkar
        # ("Kurtaran Ev Kedileri😻" / "Kurtaran Ev Köpekleri 🐶")
        if not kullanici:
            yazar = (veri.get("author") or "").lower()
            if "kedi" in yazar:
                kullanici = "kurtaranev_kedileri"
            elif "köpek" in yazar or "kopek" in yazar:
                kullanici = "kurtaranev_kopekleri"
            if kullanici:
                print(f"  hesap (yazardan): @{kullanici}")

        # Yanıtı Graph API gönderi biçimine çevir ki mevcut akış aynen çalışsın
        resimler = [m2 for m2 in (veri.get("medias") or []) if m2.get("type") == "image"]
        gonderi = {
            "id": shortcode,
            "caption": veri.get("title") or "",
            "permalink": url,
            "media_type": "CAROUSEL_ALBUM",
            "children": {"data": [{"media_type": "IMAGE", "media_url": m2["url"]}
                                  for m2 in resimler if m2.get("url")]},
        }
        tur = HESAPLAR.get(kullanici) or args.tur  # None ise ayrıştırıcı belirler
        kayitlar, neden = gonderiyi_isle(gonderi, tur, kullanici or "instagram",
                                         fotograf_cek=not args.kuru, ai=args._ai,
                                             yayinla=not args.taslak)
        if not kayitlar:
            print(f"  – atlandı ({neden}): {gonderi['caption'][:50]}…")
            continue
        for kayit in kayitlar:
            print(f"  ✓ {kayit.get('isim') or 'İsimsiz'} — {_ozet(kayit)}"
                  + (" [yuvalandı]" if kayit["durum"] == "yuvalandi" else ""))
        toplam.extend(kayitlar)

    if args.kuru:
        print(f"\n[kuru çalıştırma] {len(toplam)} ilan işlenirdi, hiçbir şey yazılmadı.")
        return 0
    if not toplam:
        print("\nİşlenecek ilan çıkmadı.")
        return 1

    eklendi, guncellendi = kaydet(toplam)
    print(f"\n{eklendi} yeni ilan eklendi, {guncellendi} ilan güncellendi.")
    print("Taslaklar admin panelinden onay bekliyor: site/admin.html" if args.taslak
          else "İlanlar doğrudan yayınlandı (yuva arıyor).")
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
    ap.add_argument("--rapid", action="store_true",
                    help="Son gönderileri RapidAPI scraper ile çek (jeton gerekmez, --limit geçerli)")
    ap.add_argument("--link", nargs="+", metavar="URL",
                    help="Instagram gönderi bağlantıları — RapidAPI ile çekilir (jeton gerekmez)")
    ap.add_argument("--tur", choices=("kopek", "kedi"),
                    help="--link için tür (bağlantıdan hesap anlaşılamazsa)")
    ap.add_argument("--kuru", action="store_true", help="Hiçbir şey yazma, sadece ne olacağını göster")
    ap.add_argument("--ornek-config", action="store_true", help="Örnek yapılandırma dosyası oluştur")
    ap.add_argument("--jeton-yenile", action="store_true",
                    help="Uzun ömürlü jetonu tazele ve config dosyasına yaz")
    ap.add_argument("--klasik", action="store_true",
                    help="AI yerine kural tabanlı ayrıştırıcıyı kullan")
    ap.add_argument("--guncelle", action="store_true",
                    help="--rapid: zaten kayıtlı gönderileri de yeniden işle")
    ap.add_argument("--taslak", action="store_true",
                    help="İlanları yayınlamak yerine taslak olarak ekle (panel onayı iste)")
    args = ap.parse_args()

    # OpenRouter anahtarı varsa ayrıştırma varsayılan olarak AI'ya yaptırılır
    cfg = config_yukle()
    args._ai = (not args.klasik) and bool(cfg.get("openrouter_key")
                                          or os.environ.get("OPENROUTER_API_KEY"))
    if args._ai:
        print(f"Ayrıştırıcı: AI ({ai_parser.VARSAYILAN_MODEL})")
    elif not args.klasik:
        print("Ayrıştırıcı: kural tabanlı (OpenRouter anahtarı tanımlı değil)")

    if args.ornek_config:
        ornek_config_yaz()
        return 0
    if args.jeton_yenile:
        return kip_jeton_yenile(args)
    if args.rapid:
        return kip_rapid(args)
    if args.link:
        return kip_link(args)
    if args.dosya:
        return kip_dosya(args)
    return kip_api(args)


if __name__ == "__main__":
    raise SystemExit(main())
