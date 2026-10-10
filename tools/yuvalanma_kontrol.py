# -*- coding: utf-8 -*-
"""
"Yuva arıyor" ilanlarının Instagram'da yuvalanıp yuvalanmadığını denetler.

Dernek bir hayvan yuvalanınca gönderinin caption'ını düzenleyip en başa
"YUVALANDI" yazıyor. Bu modül o değişikliği AI kullanmadan yakalar:

  * Gönderi başına istek atılmaz. Hesabın /feed akışı sayfa sayfa gezilir;
    bir sayfa (1 istek) 12 gönderinin GÜNCEL caption'ını verir.
  * Günlük senkronun zaten çektiği ilk sayfalar ücretsiz yeniden kullanılır.
  * Tarama en eski aktif ilanın gönderisine ulaşınca durur — maliyet ilan
    sayısıyla değil, o ilanın akışta ne kadar geride olduğuyla büyür.
  * Günlük alt bütçe GUNLUK_BUTCE istek (genel 350 sınırı da geçerli). Bütçe
    tam taramaya yetmezse kalınan sayfa (imleç) kaydedilir; ertesi gün ilk
    sayfalar yeniden, ardından imleçten itibaren derin sayfalar taranır.
  * Tespit kuralı: caption'ın İLK İKİ dolu satırında kelime olarak
    YUVALANDI / YUVALANDILAR / "yuvasına kavuştu" / "yuvasını buldu" /
    "sahiplendirildi" geçmesi. Metnin içindeki "yuvalandırabiliriz" gibi
    kelimeler bilerek yakalanmaz.
  * Akışta bulunamayan (silinmiş/arşivlenmiş) gönderiler otomatik
    değiştirilmez; raporda "kontrol edin" diye listelenir.
"""

from __future__ import annotations

import json
import re
import time
from datetime import datetime
from pathlib import Path

import animals
import rapidapi_kota
from caption_parser import _sade

GUNLUK_BUTCE = 200
KATEGORI = "yuvalanma"
DURUM_PATH = Path(__file__).resolve().parent / "yuvalanma_kontrol.json"
SAYFA_BEKLEME = 2  # sn, hız limiti

_DESEN = re.compile(r"\byuvalandi(lar)?\b|\byuvasina kavustu|\byuvasini buldu"
                    r"|\bsahiplendirildi(ler)?\b")


def ilk_satirlar(caption: str, n: int = 2) -> list[str]:
    return [s.strip() for s in _sade(caption or "").splitlines() if s.strip()][:n]


def baslikta_yuvalandi(caption: str) -> bool:
    """Caption'ın başında (ilk iki dolu satır) yuvalanma ibaresi var mı?"""
    return any(_DESEN.search(s) for s in ilk_satirlar(caption))


def _caption(item: dict) -> str:
    c = item.get("caption")
    return (c or {}).get("text", "") if isinstance(c, dict) else (c or "")


def _ts(iso: str | None) -> float | None:
    try:
        return datetime.fromisoformat(iso).timestamp() if iso else None
    except ValueError:
        return None


def sonraki_imlec(yanit: dict, pk: str) -> str | None:
    """Sonraki sayfanın imleci. API'nin next_max_id'si, sayfanın son öğesi
    başka hesapla ortak (collab) gönderiyse o hesabın kimliğini taşıyor ve
    akış aylarca ileri atlıyor (denendi: 31 Ağustos → 27 Haziran). Bu yüzden
    imleç, sayfadaki en eski sabitlenmemiş gönderiden kendimiz kuruyoruz."""
    if not yanit.get("more_available"):
        return None
    kendi = [it for it in yanit.get("items") or []
             if not it.get("timeline_pinned_user_ids") and it.get("pk") and it.get("taken_at")]
    if not kendi:
        return yanit.get("next_max_id")
    return f"{min(kendi, key=lambda it: it['taken_at'])['pk']}_{pk}"


def _yukle() -> dict:
    try:
        return json.loads(DURUM_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _kaydet(durum: dict) -> None:
    DURUM_PATH.write_text(json.dumps(durum, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")


def _isaretlenecekler(kayitlar: list[dict], caption: str) -> list[dict]:
    """Aynı gönderiden çıkan birden çok ilan varsa hangileri yuvalandı?
    İlk satırlarda isim geçenler; isim geçmiyorsa (ya da YUVALANDILAR) hepsi."""
    if len(kayitlar) == 1:
        return kayitlar
    bas = " ".join(ilk_satirlar(caption))
    adli = [k for k in kayitlar
            if k.get("isim") and re.search(r"\b" + re.escape(_sade(k["isim"])) + r"\b", bas)]
    return adli or kayitlar


def calistir(rapid_get, hesap_pk: dict[str, str], api_key: str,
             onbellek: dict[str, list[dict]] | None = None, kuru: bool = False) -> dict:
    """Taramayı yapar, yuvalananları işaretler (kuru değilse) ve özet döner.

    rapid_get(path, params, api_key, kategori) — instagram_sync._rapid_get
    hesap_pk — {kullanıcı adı: Instagram pk}
    onbellek — {pk: [o çalıştırmada zaten çekilmiş /feed yanıtları]}
    """
    onbellek = onbellek or {}
    hayvanlar = animals.load()
    durum = _yukle()
    imlecler = durum.setdefault("imlec", {})
    sonuc = {"isaretlenen": [], "bulunamayan": [], "sayfa": {}, "ucretsiz": {},
             "tamamlandi": {}, "hata": None}

    hedefler_tum = [a for a in hayvanlar
                    if a.get("durum") == "yuva-ariyor" and (a.get("kaynak") or {}).get("gonderiId")]
    hesaplar = [h for h in hesap_pk if any(a["kaynak"].get("hesap") == h for a in hedefler_tum)]

    for sira, hesap in enumerate(hesaplar):
        pk = hesap_pk[hesap]
        hedefler: dict[str, list[dict]] = {}
        for a in hedefler_tum:
            if a["kaynak"].get("hesap") == hesap:
                hedefler.setdefault(a["kaynak"]["gonderiId"], []).append(a)
        # Gönderi tarihi bilinmeyen (eski elle eklenmiş) kayıtlar durma noktasını
        # belirlemez; onlar ancak tarama o derinliğe zaten inerse görülür.
        tarihler = [t for t in (_ts(k[0]["kaynak"].get("tarih")) for k in hedefler.values()) if t]
        en_eski = min(tarihler) if tarihler else 0
        # Kalan bütçe, kalan hesaplara eşit bölünür (kullanılmayan pay sonrakine geçer).
        kalan_hesap = len(hesaplar) - sira
        pay = max(0, (GUNLUK_BUTCE - rapidapi_kota.kategori_kullanim(KATEGORI)) // kalan_hesap)

        gorulen: set[str] = set()
        en_derin = None          # taranan en eski (sabitlenmemiş) gönderinin zamanı
        sayfa = ucretsiz = istek = 0
        imlec = None             # bir sonraki sayfanın imleci
        devam_var = True
        atlandi = False          # önceki günün imlecine atlandı mı (tam tarama sayılmaz)

        def isle(yanit: dict) -> None:
            nonlocal en_derin
            for it in yanit.get("items") or []:
                kod = it.get("code")
                if not kod:
                    continue
                gorulen.add(kod)
                if not it.get("timeline_pinned_user_ids") and it.get("taken_at"):
                    en_derin = it["taken_at"] if en_derin is None else min(en_derin, it["taken_at"])
                if kod in hedefler and baslikta_yuvalandi(_caption(it)):
                    for k in _isaretlenecekler(hedefler[kod], _caption(it)):
                        if k["durum"] == "yuva-ariyor":
                            k["durum"] = "yuvalandi"
                            k["guncelleme"] = animals.now_iso()
                            k["kaynak"]["yuvalanma"] = {"tarih": animals.now_iso(),
                                                       "yontem": "instagram-caption"}
                            sonuc["isaretlenen"].append(k)

        def bitti() -> bool:
            return (not devam_var or not imlec
                    or (en_derin is not None and en_derin < en_eski)
                    or all(kod in gorulen for kod in hedefler))

        kayitli_imlec = imlecler.get(hesap)

        def sonraki(yanit: dict) -> None:
            """Sayfadan sonra nereye gidileceği: önceki günden kalan derin tarama
            varsa ilk sayfa(lar)dan sonra oraya atlanır."""
            nonlocal imlec, devam_var, atlandi, kayitli_imlec
            imlec = sonraki_imlec(yanit, pk)
            devam_var = bool(imlec)
            if kayitli_imlec and not bitti():
                imlec, devam_var, atlandi, kayitli_imlec = kayitli_imlec, True, True, None

        # 1) Senkronun zaten çektiği ilk sayfalar — istek harcamaz
        for yanit in onbellek.get(pk) or []:
            isle(yanit)
            sayfa += 1
            ucretsiz += 1
            if yanit is not (onbellek.get(pk) or [])[-1]:
                continue
            sonraki(yanit)

        # 2) Bütçe izin verdikçe sonraki sayfalar (önbellek yoksa en baştan)
        while not (sayfa and bitti()):
            if istek >= pay:
                break
            params = {"user_id": pk}
            if imlec:
                params["next_max_id"] = imlec
            if sayfa:
                time.sleep(SAYFA_BEKLEME)
            try:
                yanit = rapid_get("/feed", params, api_key, KATEGORI)
            except RuntimeError as e:     # KotaAsildi dahil
                sonuc["hata"] = f"@{hesap}: {e}"
                break
            istek += 1
            sayfa += 1
            isle(yanit)
            sonraki(yanit)

        tamam = bool(sayfa) and bitti()
        if tamam:
            imlecler[hesap] = None
        elif sayfa and imlec and not kayitli_imlec:
            imlecler[hesap] = imlec       # yarın buradan devam
        # (hiç sayfa taranamadıysa eski imleç korunur)
        sonuc["sayfa"][hesap] = sayfa
        sonuc["ucretsiz"][hesap] = ucretsiz
        sonuc["tamamlandi"][hesap] = tamam

        # Baştan sona tek seferde taranmışsa: gönderisi akışta olmayan ilanlar
        if tamam and not atlandi:
            for kod, kayitlar in hedefler.items():
                ts = _ts(kayitlar[0]["kaynak"].get("tarih"))
                if kod not in gorulen and ts and en_derin is not None and ts >= en_derin:
                    sonuc["bulunamayan"].extend(kayitlar)
        if sonuc["hata"]:
            break

    if not kuru:
        if sonuc["isaretlenen"]:
            animals.save(hayvanlar)
        durum["sonCalisma"] = animals.now_iso()
        _kaydet(durum)
    sonuc["harcanan"] = rapidapi_kota.kategori_kullanim(KATEGORI)
    return sonuc


def ozet_satiri(sonuc: dict) -> str:
    """Rapor satırı: 'Yuvalanma kontrolü: bugün 12 / 200 istek …'"""
    adlar = {"kurtaranev_kopekleri": "köpek", "kurtaranev_kedileri": "kedi"}
    sayfalar = ", ".join(f"{adlar.get(h, h)} {n} sayfa" for h, n in sonuc["sayfa"].items())
    ucretsiz = sum(sonuc["ucretsiz"].values())
    tamam = all(sonuc["tamamlandi"].values()) if sonuc["tamamlandi"] else True
    durum = "tam tarama tamamlandı" if tamam else "bütçe doldu, kalan sayfalar yarın taranacak"
    return (f"Yuvalanma kontrolü: bugün {sonuc['harcanan']} / {GUNLUK_BUTCE} istek "
            f"({sayfalar or 'aktif ilan yok'}"
            + (f"; {ucretsiz} sayfa senkrondan ücretsiz" if ucretsiz else "")
            + f") · {durum}")
