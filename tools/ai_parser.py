# -*- coding: utf-8 -*-
"""
Kurtaran Ev — yapay zekâ ile gönderi ayrıştırma (OpenRouter / Gemini Flash).

caption_parser.py'deki kural tabanlı ayrıştırıcının yerine geçebilen katman:
gönderi metnini modele verir, yapılandırılmış (JSON şemalı) cevap alır.
Model her ilanı Türkçe alanlarla birlikte İngilizce karşılıklarıyla ('...En'
ekli alanlar) döndürür; site iki dilde yayınlanıyor.
Yalnızca metin gönderilir — fotoğraflar modele verilmez (şimdilik bilinçli
karar; maliyet ve basitlik).

Temel ilke: modele "bilmediğini boş bırak" talimatı verilir; metinde
yazmayan hiçbir alan doldurulmaz, tahminî değerler `tahmini` listesinde
işaretlenir. Kayıtlar yine taslak oluşur, panel onayı olmadan yayına çıkmaz.

Anahtar: tools/instagram_config.json içindeki `openrouter_key` alanı ya da
OPENROUTER_API_KEY ortam değişkeni.

Tek başına deneme:
    python3 tools/ai_parser.py "PAMUK yuva arıyor, 2 yaşında dişi, 18 kg"
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://openrouter.ai/api/v1/chat/completions"
VARSAYILAN_MODEL = "google/gemini-3.6-flash"

# Tek hayvanın alanları — animals.py şemasının ayrıştırılabilir kısmı.
_HAYVAN_SEMASI = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "isim":           {"type": ["string", "null"], "description": "Hayvanın adı"},
        "tur":            {"type": ["string", "null"], "enum": ["kopek", "kedi", None]},
        "cinsiyet":       {"type": ["string", "null"], "enum": ["disi", "erkek", None]},
        "yasAy":          {"type": ["integer", "null"], "description": "Yaş, AY cinsinden (2 yaş = 24)"},
        "kiloKg":         {"type": ["number", "null"]},
        "cins":           {"type": ["string", "null"], "description": "Irk, örn. 'Border Terrier'"},
        "boyut":          {"type": ["string", "null"], "enum": ["kucuk", "orta", "buyuk", None]},
        "renk":           {"type": ["string", "null"]},
        "kisir":          {"type": ["boolean", "null"]},
        "asili":          {"type": ["boolean", "null"], "description": "Aşıları tam mı"},
        "cipli":          {"type": ["boolean", "null"], "description": "Mikroçipli mi"},
        "cocuklaUyum":    {"type": ["boolean", "null"]},
        "kopeklerleUyum": {"type": ["boolean", "null"]},
        "kedilerleUyum":  {"type": ["boolean", "null"]},
        "ozelBakim":      {"type": ["boolean", "null"], "description": "Özel bakım gerektiriyor mu"},
        "saglikNotu":     {"type": ["string", "null"], "description": "Sağlık durumu cümleleri"},
        "konum":          {"type": ["string", "null"], "description": "Bulunduğu yer (geçici yuva / yaşam alanı)"},
        "karakter":       {"type": "array", "items": {"type": "string"},
                           "description": "Karakter etiketleri: oyuncu, sakin, sevecen..."},
        "aciklama":       {"type": ["string", "null"],
                           "description": "Hashtag'siz, çağrısız, temiz ilan metni"},
        "tahmini":        {"type": "array", "items": {"type": "string"},
                           "description": "Tahminî olan alan adları, örn. ['yasAy']"},

        # --- İngilizce karşılıklar (sitenin EN kipi için) -------------------
        # Yalnızca serbest metin alanlarının çevirisi tutulur; tur/cinsiyet/boyut
        # gibi seçimlik alanlar zaten dilden bağımsız anahtarlardır ve arayüzde
        # çevrilir. Türkçesi null olan alanın İngilizcesi de null olmalıdır.
        "cinsEn":         {"type": ["string", "null"], "description": "cins alanının İngilizcesi"},
        "renkEn":         {"type": ["string", "null"], "description": "renk alanının İngilizcesi"},
        "saglikNotuEn":   {"type": ["string", "null"], "description": "saglikNotu alanının İngilizcesi"},
        "konumEn":        {"type": ["string", "null"], "description": "konum alanının İngilizcesi"},
        "karakterEn":     {"type": "array", "items": {"type": "string"},
                           "description": "karakter etiketlerinin İngilizcesi, aynı sıra ve sayıda"},
        "aciklamaEn":     {"type": ["string", "null"], "description": "aciklama alanının İngilizcesi"},
    },
    "required": ["isim", "tur", "cinsiyet", "yasAy", "kiloKg", "cins", "boyut",
                 "renk", "kisir", "asili", "cipli", "cocuklaUyum", "kopeklerleUyum",
                 "kedilerleUyum", "ozelBakim", "saglikNotu", "konum", "karakter",
                 "aciklama", "tahmini",
                 "cinsEn", "renkEn", "saglikNotuEn", "konumEn", "karakterEn", "aciklamaEn"],
}

SEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "icerikTuru": {
            "type": "string",
            "enum": ["ilan", "koruyucu-melek", "yuvalandi-duyurusu", "diger"],
            "description": "Gönderinin türü",
        },
        "yuvalandi": {
            "type": "boolean",
            "description": "İlandaki hayvan yuvalandı olarak işaretlenmiş mi (örn. başında YUVALANDI yazıyor)",
        },
        "hayvanlar": {
            "type": "array",
            "items": _HAYVAN_SEMASI,
            "description": "Yalnızca icerikTuru 'ilan' ise dolu; hayvan başına bir öğe",
        },
    },
    "required": ["icerikTuru", "yuvalandi", "hayvanlar"],
}

SISTEM = """Kurtaran Ev, sahipsiz kedi ve köpekleri kurtaran bir Türk hayvan derneğidir.
Sana derneğin Instagram gönderilerinden birinin metni verilecek. İki görevin var:

1) SINIFLANDIR:
   - "ilan": belirli hayvan(lar)ın sahiplendirilmesi için yazılmış ilan.
   - "koruyucu-melek": bir hayvana düzenli bağışçı (Koruyucu Melek) arayan çağrı — sahiplendirme değildir.
   - "yuvalandi-duyurusu": yalnızca bir hayvanın yuvalandığını kutlayan gönderi (ilan bilgisi içermeyen).
   - "diger": kampanya, teşekkür, tanıtım, ziyaret videosu, genel bilgilendirme vb.
   Dikkat: "sahiplenmek için bağlantıya tıklayın" gibi genel çağrılar içeren tanıtım
   gönderileri İLAN DEĞİLDİR; ilan sayılması için belirli bir hayvan tanıtılıyor olmalı.
   Başında "YUVALANDI" yazan ama hayvanın tüm ilan bilgilerini içeren gönderiler
   "ilan" sayılır ve yuvalandi=true işaretlenir.

2) İLANSA BİLGİLERİ ÇIKAR — hayvan başına bir kayıt:
   - Kardeş/çoklu ilanlarda ("ikisi erkek, biri dişi") her hayvan için ayrı kayıt üret;
     isimleri yoksa ortak addan numaralandır ("Kutu 1", "Kutu 2"...).
   - EN ÖNEMLİ KURAL: yalnızca metinde AÇIKÇA yazan bilgiyi doldur. Yazmıyorsa null bırak.
     Fotoğraf göremiyorsun; renk, boyut, cins gibi bilgileri ASLA uydurma.
   - "yaklaşık", "tahmini", "3-4 yaşlarında", "1 yaş civarı" gibi ifadelerde değeri doldur
     (aralıklarda ortalama) ve alan adını "tahmini" listesine ekle.
   - yasAy her zaman AY cinsindendir: "2 yaşında" → 24, "5 aylık" → 5, "4-5 haftalık" → 1.
   - "kısırlaştırma şartı ile sahiplendirilecektir" → kisir=false (henüz kısır değil).
   - "Kedisiz bir ev daha uygun" gibi dolaylı ifadeler → ilgili uyum alanı false.
   - saglikNotu: sağlıkla ilgili cümleleri (körlük, ameliyat, tedavi, engel...) buraya al;
     ciddi/kalıcı bir durum varsa ozelBakim=true. Aşı/kısırlık bilgisi buraya YAZILMAZ.
   - konum: yalnızca hayvanın NEREDE OLDUĞU yazıyorsa doldur ("gönüllü geçici yuvamızdaki X").
     "Geçici yuva olabilirsiniz" gibi çağrılar konum DEĞİLDİR.
   - aciklama: hashtag'ler, DM/bağlantı çağrıları ve tekrarlar atılmış, akıcı bir ilan metni.
   - karakter: metindeki mizaç ifadelerini kısa etiketlere çevir (oyuncu, sakin, sevecen,
     çekingen, meraklı, eğitimli, koruyucu, sadık gibi).

3) İNGİLİZCESİNİ DE ÜRET — site hem Türkçe hem İngilizce yayınlanıyor:
   - Serbest metin alanlarının İngilizce karşılığını "En" ekli alanlara yaz:
     cins→cinsEn, renk→renkEn, saglikNotu→saglikNotuEn, konum→konumEn,
     karakter→karakterEn, aciklama→aciklamaEn.
   - Türkçesi null olan alanın İngilizcesi de null olur; karakter boşsa karakterEn de boştur.
     ÇEVİRİRKEN YENİ BİLGİ EKLEME — İngilizce metin Türkçesiyle birebir aynı bilgiyi taşımalı.
   - karakterEn, karakter ile AYNI SIRADA ve AYNI SAYIDA öğe içerir
     (oyuncu→playful, sakin→calm, sevecen→affectionate, çekingen→shy,
      meraklı→curious, eğitimli→trained, koruyucu→protective, sadık→loyal).
   - Hayvanın adı çevrilmez, olduğu gibi kalır (isim alanı tektir).
   - aciklamaEn: kelime kelime değil, akıcı ve doğal İngilizce bir ilan metni olsun;
     Türkçe metnin tonunu ve tüm bilgilerini koru. Türkiye'ye özgü terimleri anlaşılır
     çevir ("geçici yuva" → "foster home", "barınak" → "shelter",
     "kısırlaştırma şartıyla" → "on the condition of neutering/spaying").
   - cinsEn: ırk adlarının yerleşik İngilizcesini kullan ("Melez" → "Mixed breed",
     "Sokak kedisi" → "Domestic shorthair", "Golden Retriever" → "Golden Retriever").

Yalnızca şemaya uygun JSON döndür."""


def _anahtar_bul() -> str | None:
    if os.environ.get("OPENROUTER_API_KEY"):
        return os.environ["OPENROUTER_API_KEY"]
    cfg_yolu = Path(__file__).resolve().parent / "instagram_config.json"
    if cfg_yolu.exists():
        try:
            return json.loads(cfg_yolu.read_text(encoding="utf-8")).get("openrouter_key")
        except json.JSONDecodeError:
            pass
    return None


def _cagir(sistem: str, kullanici: str, sema: dict, sema_adi: str,
           api_key: str | None, model: str) -> dict:
    """OpenRouter'a JSON şemalı tek bir istek atar, çözülmüş sözlüğü döner."""
    api_key = api_key or _anahtar_bul()
    if not api_key:
        raise RuntimeError("OpenRouter anahtarı yok (openrouter_key / OPENROUTER_API_KEY)")

    govde = json.dumps({
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": sistem},
            {"role": "user", "content": kullanici or ""},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": sema_adi, "strict": True, "schema": sema},
        },
    }).encode("utf-8")

    istek = urllib.request.Request(API_URL, data=govde, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://kurtaranev.org",
        "X-Title": "Kurtaran Ev Instagram Sync",
    })
    try:
        with urllib.request.urlopen(istek, timeout=120) as r:
            cevap = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"OpenRouter {e.code}: {e.read().decode('utf-8', 'replace')[:300]}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Ağ hatası: {e.reason}") from e

    try:
        return json.loads(cevap["choices"][0]["message"]["content"])
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Model cevabı çözülemedi: {str(cevap)[:300]}") from e


def ai_parse(caption: str, api_key: str | None = None,
             model: str = VARSAYILAN_MODEL) -> dict:
    """Gönderi metnini modele ayrıştırtır.

    Dönen sözlük: {"icerikTuru": ..., "yuvalandi": bool, "hayvanlar": [...]}
    Her hayvan sözlüğü Türkçe alanların yanında İngilizce karşılıklarını da
    ("...En" ekli alanlar) taşır. Hata durumunda RuntimeError fırlatır —
    çağıran taraf kural tabanlı ayrıştırıcıya düşebilir.
    """
    sonuc = _cagir(SISTEM, caption, SEMA, "gonderi_ayristirma", api_key, model)

    # asgari doğrulama — şemaya güvenme, çağıranın beklediği yapıyı garanti et
    if not isinstance(sonuc, dict) or "icerikTuru" not in sonuc:
        raise RuntimeError(f"Beklenmedik model çıktısı: {str(sonuc)[:300]}")
    sonuc.setdefault("yuvalandi", False)
    sonuc.setdefault("hayvanlar", [])
    for hayvan in sonuc["hayvanlar"]:
        if isinstance(hayvan, dict):
            _en_tutarla(hayvan)
    return sonuc


# ---------------------------------------------------------------------------
# Türkçe kayıttan İngilizce alanları üretme (eski kayıtları tamamlamak için)
# ---------------------------------------------------------------------------

# Türkçesi → İngilizcesi eşlenen serbest metin alanları
CEVIRI_ALANLARI = {
    "cins": "cinsEn",
    "renk": "renkEn",
    "saglikNotu": "saglikNotuEn",
    "konum": "konumEn",
    "karakter": "karakterEn",
    "aciklama": "aciklamaEn",
}

_CEVIRI_SEMASI = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "cinsEn":       {"type": ["string", "null"]},
        "renkEn":       {"type": ["string", "null"]},
        "saglikNotuEn": {"type": ["string", "null"]},
        "konumEn":      {"type": ["string", "null"]},
        "karakterEn":   {"type": "array", "items": {"type": "string"}},
        "aciklamaEn":   {"type": ["string", "null"]},
    },
    "required": list(CEVIRI_ALANLARI.values()),
}

CEVIRI_SISTEMI = """Kurtaran Ev, sahipsiz kedi ve köpekleri kurtaran bir Türk hayvan derneğidir.
Sitesi hem Türkçe hem İngilizce yayınlanıyor. Sana bir sahiplendirme ilanının Türkçe
alanları JSON olarak verilecek; aynı alanların İngilizcesini üret.

Kurallar:
- cins→cinsEn, renk→renkEn, saglikNotu→saglikNotuEn, konum→konumEn,
  karakter→karakterEn, aciklama→aciklamaEn.
- Türkçesi null ya da boş olan alanın İngilizcesi de null olur; karakter boşsa
  karakterEn de boş dizidir.
- YENİ BİLGİ EKLEME, bilgi ÇIKARMA. İngilizce metin Türkçesiyle birebir aynı bilgiyi taşımalı.
- karakterEn, karakter ile aynı sırada ve aynı sayıda öğe içerir.
- Hayvanın adı çevrilmez.
- aciklamaEn kelime kelime değil, akıcı ve doğal İngilizce olsun; Türkçe metnin tonunu koru.
  Türkiye'ye özgü terimleri anlaşılır çevir ("geçici yuva" → "foster home",
  "barınak" → "shelter", "kısırlaştırma şartıyla" → "on the condition of neutering/spaying").
- cinsEn'de ırk adlarının yerleşik İngilizcesini kullan ("Melez" → "Mixed breed").

Yalnızca şemaya uygun JSON döndür."""


def _en_tutarla(hayvan: dict) -> dict:
    """Türkçesi boş olan alanın İngilizcesini de boşaltır, karakterEn'i hizalar.

    Model kurala uymayıp uydurursa arayüzde iki dil arasında fark oluşmasın diye
    son bir güvenlik kemeri.
    """
    for tr_alan, en_alan in CEVIRI_ALANLARI.items():
        if tr_alan == "karakter":
            continue
        if not hayvan.get(tr_alan):
            hayvan[en_alan] = None
    if not hayvan.get("karakter"):
        hayvan["karakterEn"] = []
    else:
        en = hayvan.get("karakterEn") or []
        # sayı tutmuyorsa çeviriyi güvenilir eşleyemeyiz — Türkçesine düş
        if len(en) != len(hayvan["karakter"]):
            hayvan["karakterEn"] = list(hayvan["karakter"])
    return hayvan


def ai_translate(kayit: dict, api_key: str | None = None,
                 model: str = VARSAYILAN_MODEL) -> dict:
    """Türkçe alanları dolu bir ilan kaydının İngilizce alanlarını üretir.

    Yalnızca "...En" alanlarını içeren bir sözlük döner; kaydı değiştirmez.
    Çevrilecek Türkçe içerik yoksa istek atmadan boş karşılıklar döner.
    """
    girdi = {alan: kayit.get(alan) for alan in CEVIRI_ALANLARI}
    if not any(girdi.values()):
        return {en: ([] if tr == "karakter" else None)
                for tr, en in CEVIRI_ALANLARI.items()}

    girdi["isim"] = kayit.get("isim")  # ada göre cinsiyet/ton tutturabilsin
    sonuc = _cagir(CEVIRI_SISTEMI, json.dumps(girdi, ensure_ascii=False),
                   _CEVIRI_SEMASI, "ilan_cevirisi", api_key, model)
    if not isinstance(sonuc, dict):
        raise RuntimeError(f"Beklenmedik çeviri çıktısı: {str(sonuc)[:300]}")

    birlesik = dict(kayit)
    birlesik.update({en: sonuc.get(en) for en in CEVIRI_ALANLARI.values()})
    _en_tutarla(birlesik)
    return {en: birlesik.get(en) for en in CEVIRI_ALANLARI.values()}


if __name__ == "__main__":
    metin = " ".join(sys.argv[1:]) or sys.stdin.read()
    print(json.dumps(ai_parse(metin), ensure_ascii=False, indent=2))
