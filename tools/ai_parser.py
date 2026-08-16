# -*- coding: utf-8 -*-
"""
Kurtaran Ev — yapay zekâ ile gönderi ayrıştırma (OpenRouter / Gemini Flash).

caption_parser.py'deki kural tabanlı ayrıştırıcının yerine geçebilen katman:
gönderi metnini modele verir, yapılandırılmış (JSON şemalı) cevap alır.
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
    },
    "required": ["isim", "tur", "cinsiyet", "yasAy", "kiloKg", "cins", "boyut",
                 "renk", "kisir", "asili", "cipli", "cocuklaUyum", "kopeklerleUyum",
                 "kedilerleUyum", "ozelBakim", "saglikNotu", "konum", "karakter",
                 "aciklama", "tahmini"],
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


def ai_parse(caption: str, api_key: str | None = None,
             model: str = VARSAYILAN_MODEL) -> dict:
    """Gönderi metnini modele ayrıştırtır.

    Dönen sözlük: {"icerikTuru": ..., "yuvalandi": bool, "hayvanlar": [...]}
    Hata durumunda RuntimeError fırlatır — çağıran taraf kural tabanlı
    ayrıştırıcıya düşebilir.
    """
    api_key = api_key or _anahtar_bul()
    if not api_key:
        raise RuntimeError("OpenRouter anahtarı yok (openrouter_key / OPENROUTER_API_KEY)")

    govde = json.dumps({
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": SISTEM},
            {"role": "user", "content": caption or ""},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "gonderi_ayristirma", "strict": True, "schema": SEMA},
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
        icerik = cevap["choices"][0]["message"]["content"]
        sonuc = json.loads(icerik)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Model cevabı çözülemedi: {str(cevap)[:300]}") from e

    # asgari doğrulama — şemaya güvenme, çağıranın beklediği yapıyı garanti et
    if not isinstance(sonuc, dict) or "icerikTuru" not in sonuc:
        raise RuntimeError(f"Beklenmedik model çıktısı: {str(sonuc)[:300]}")
    sonuc.setdefault("yuvalandi", False)
    sonuc.setdefault("hayvanlar", [])
    return sonuc


if __name__ == "__main__":
    metin = " ".join(sys.argv[1:]) or sys.stdin.read()
    print(json.dumps(ai_parse(metin), ensure_ascii=False, indent=2))
