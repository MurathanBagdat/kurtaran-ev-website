# -*- coding: utf-8 -*-
"""
Kurtaran Ev — hayvan ilanı veri modeli ve deposu.

Tek doğruluk kaynağı: site/assets/data/animals.json
Ondan türetilen:      site/assets/data/animals.js  (tarayıcı file:// ile de okuyabilsin diye)

Tasarım kararı: cins, yaş, kilo gibi alanların HİÇBİRİ zorunlu değildir. Bilinmeyen alan
`null` bırakılır; tahmin edilen alanlar `tahmini` listesinde işaretlenir ve arayüzde
"~2 yaş (tahmini)" biçiminde gösterilir.
"""

from __future__ import annotations

import json
import hashlib
import os
import re
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "site" / "assets" / "data"
JSON_PATH = DATA_DIR / "animals.json"
JS_PATH = DATA_DIR / "animals.js"
PHOTO_DIR = ROOT / "site" / "assets" / "img" / "animals"
PHOTO_WEB_PREFIX = "assets/img/animals"

SPECIES = ("kopek", "kedi")

# İlan durumları
STATUS = {
    "taslak": "Taslak (yayında değil)",
    "yuva-ariyor": "Yuva arıyor",
    "rezerve": "Rezerve",
    "yuvalandi": "Yuvalandı",
}
PUBLIC_STATUS = ("yuva-ariyor", "rezerve", "yuvalandi")

SEX = {"disi": "Dişi", "erkek": "Erkek"}
SIZE = {"kucuk": "Küçük", "orta": "Orta", "buyuk": "Büyük"}

# Tahmin edilebilen / arayüzde "tahmini" rozetiyle gösterilebilen alanlar
ESTIMABLE = ("yasAy", "kiloKg", "boyut", "cins")

# Alan şeması: admin formunu, doğrulamayı ve filtreleri bu tablo besler.
GRUPLAR = {
    "temel":     "Temel bilgiler",
    "fiziksel":  "Fiziksel özellikler",
    "saglik":    "Sağlık",
    "uyum":      "Uyum",
    "icerik":    "İlan içeriği",
}

# Alan şeması: admin formunu, doğrulamayı ve filtreleri bu tablo besler.
# Buraya yeni bir alan eklemek admin panelinde de otomatik olarak görünür.
FIELDS = {
    "isim":        {"tip": "metin",  "etiket": "İsim", "grup": "temel"},
    "tur":         {"tip": "secim",  "etiket": "Tür", "grup": "temel",
                    "secenekler": {"kopek": "Köpek", "kedi": "Kedi"}},
    "cinsiyet":    {"tip": "secim",  "etiket": "Cinsiyet", "grup": "temel", "secenekler": SEX},
    "durum":       {"tip": "secim",  "etiket": "Durum", "grup": "temel", "secenekler": STATUS},
    "konum":       {"tip": "metin",  "etiket": "Bulunduğu yer", "grup": "temel"},

    "cins":        {"tip": "metin",  "etiket": "Cins / ırk", "grup": "fiziksel"},
    "yasAy":       {"tip": "sayi",   "etiket": "Yaş (ay)", "grup": "fiziksel", "min": 0, "max": 360,
                    "ipucu": "36 = 3 yaşında. Bilinmiyorsa boş bırakın."},
    "kiloKg":      {"tip": "ondalik","etiket": "Kilo (kg)", "grup": "fiziksel", "min": 0, "max": 120},
    "boyut":       {"tip": "secim",  "etiket": "Boyut", "grup": "fiziksel", "secenekler": SIZE,
                    "ipucu": "Boş bırakılırsa kilodan tahmin edilir."},
    "renk":        {"tip": "metin",  "etiket": "Renk / desen", "grup": "fiziksel"},

    "kisir":       {"tip": "uclu",   "etiket": "Kısırlaştırıldı", "grup": "saglik"},
    "asili":       {"tip": "uclu",   "etiket": "Aşıları tam", "grup": "saglik"},
    "cipli":       {"tip": "uclu",   "etiket": "Mikroçipli", "grup": "saglik"},
    "ozelBakim":   {"tip": "uclu",   "etiket": "Özel bakım gerekiyor", "grup": "saglik"},
    "saglikNotu":  {"tip": "uzunmetin", "etiket": "Sağlık notu", "grup": "saglik"},

    "cocuklaUyum": {"tip": "uclu",   "etiket": "Çocuklarla uyumlu", "grup": "uyum"},
    "kopeklerleUyum": {"tip": "uclu","etiket": "Köpeklerle uyumlu", "grup": "uyum"},
    "kedilerleUyum":  {"tip": "uclu","etiket": "Kedilerle uyumlu", "grup": "uyum"},

    "karakter":    {"tip": "etiketler", "etiket": "Karakter etiketleri", "grup": "icerik",
                    "ipucu": "Virgülle ayırın: oyuncu, sakin, sevecen"},
    "aciklama":    {"tip": "uzunmetin", "etiket": "İlan metni", "grup": "icerik"},
}

TEXT_FIELDS = {k for k, v in FIELDS.items() if v["tip"] in ("metin", "uzunmetin")}
BOOL_FIELDS = {k for k, v in FIELDS.items() if v["tip"] == "uclu"}
NUM_FIELDS = {k for k, v in FIELDS.items() if v["tip"] in ("sayi", "ondalik")}


# ---------------------------------------------------------------------------
# Yardımcılar
# ---------------------------------------------------------------------------
def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(text: str) -> str:
    if not text:
        return "isimsiz"
    tr = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    text = text.translate(tr)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "isimsiz"


def make_id(tur: str, isim: str | None, tohum: str = "") -> str:
    h = hashlib.sha1(f"{tur}|{isim}|{tohum}|{now_iso()}".encode()).hexdigest()[:6]
    return f"{tur}-{slugify(isim or 'isimsiz')}-{h}"


def yas_metni(ay: int | None) -> str | None:
    """Ay cinsinden yaşı okunur Türkçeye çevirir."""
    if ay is None:
        return None
    if ay < 1:
        return "Yenidoğan"
    if ay < 12:
        return f"{ay} aylık"
    yil = ay // 12
    kalan = ay % 12
    if kalan == 0:
        return f"{yil} yaşında"
    if kalan >= 6:
        return f"{yil},5 yaşında"
    return f"{yil} yaşında"


def yas_grubu(tur: str, ay: int | None) -> str | None:
    """Filtreleme için yaş grubu."""
    if ay is None:
        return None
    if ay < 12:
        return "yavru"
    if ay < 84:
        return "yetiskin"
    return "kidemli"


AGE_GROUPS = {"yavru": "Yavru (0–1 yaş)", "yetiskin": "Yetişkin (1–7 yaş)", "kidemli": "Kıdemli (7+ yaş)"}


def boyut_tahmini(tur: str, kilo: float | None) -> str | None:
    if kilo is None:
        return None
    if tur == "kedi":
        return "kucuk"
    if kilo < 12:
        return "kucuk"
    if kilo < 25:
        return "orta"
    return "buyuk"


# ---------------------------------------------------------------------------
# Normalizasyon / doğrulama
# ---------------------------------------------------------------------------
def bos_kayit(tur: str = "kopek") -> dict:
    kayit = {"id": None, "tur": tur}
    for alan, tanim in FIELDS.items():
        if alan == "tur":
            continue
        kayit[alan] = [] if tanim["tip"] == "etiketler" else None
    kayit.update({
        "durum": "taslak",
        "fotograflar": [],
        "tahmini": [],
        "ornek": False,
        "kaynak": None,
        "olusturma": None,
        "guncelleme": None,
    })
    return kayit


def _to_bool(v):
    if v is None or v == "" or v == "bilinmiyor":
        return None
    if isinstance(v, bool):
        return v
    return str(v).lower() in ("true", "evet", "1", "var", "yes")


def _to_num(v, ondalik=False):
    if v is None or v == "":
        return None
    try:
        n = float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return None
    return round(n, 1) if ondalik else int(round(n))


def normalize(ham: dict) -> tuple[dict, list[str]]:
    """Gelen sözlüğü şemaya oturtur. (kayit, hatalar) döner."""
    hatalar = []
    tur = (ham.get("tur") or "kopek").strip()
    if tur not in SPECIES:
        hatalar.append(f"Geçersiz tür: {tur}")
        tur = "kopek"

    kayit = bos_kayit(tur)

    for alan, tanim in FIELDS.items():
        if alan == "tur":
            continue
        deger = ham.get(alan)
        tip = tanim["tip"]
        if tip in ("metin", "uzunmetin"):
            deger = (str(deger).strip() or None) if deger not in (None, "") else None
        elif tip == "sayi":
            deger = _to_num(deger)
        elif tip == "ondalik":
            deger = _to_num(deger, ondalik=True)
        elif tip == "uclu":
            deger = _to_bool(deger)
        elif tip == "secim":
            deger = deger if deger in tanim["secenekler"] else None
        elif tip == "etiketler":
            if isinstance(deger, str):
                deger = [p.strip() for p in deger.split(",") if p.strip()]
            deger = [str(p).strip() for p in (deger or []) if str(p).strip()][:8]
        kayit[alan] = deger

    # sayısal sınırlar
    for alan in NUM_FIELDS:
        v = kayit.get(alan)
        if v is None:
            continue
        tanim = FIELDS[alan]
        if v < tanim["min"] or v > tanim["max"]:
            hatalar.append(f"{tanim['etiket']} aralık dışı: {v}")
            kayit[alan] = None

    if not kayit.get("isim"):
        kayit["isim"] = "İsimsiz"

    kayit["durum"] = kayit.get("durum") or "taslak"
    kayit["fotograflar"] = [str(f) for f in (ham.get("fotograflar") or []) if str(f).strip()][:12]
    kayit["tahmini"] = [f for f in (ham.get("tahmini") or []) if f in ESTIMABLE]
    kayit["ornek"] = bool(ham.get("ornek"))
    kayit["kaynak"] = ham.get("kaynak") or None
    kayit["id"] = ham.get("id") or make_id(tur, kayit["isim"])
    kayit["olusturma"] = ham.get("olusturma") or now_iso()
    kayit["guncelleme"] = now_iso()

    # boyut bilinmiyorsa kilodan türet ve tahmini işaretle
    if kayit["boyut"] is None:
        tahmin = boyut_tahmini(tur, kayit["kiloKg"])
        if tahmin:
            kayit["boyut"] = tahmin
            if "boyut" not in kayit["tahmini"]:
                kayit["tahmini"].append("boyut")

    # arayüzün hazır kullanacağı türetilmiş alanlar
    kayit["yasMetni"] = yas_metni(kayit["yasAy"])
    kayit["yasGrubu"] = yas_grubu(tur, kayit["yasAy"])
    kayit["arama"] = " ".join(filter(None, [
        kayit.get("isim"), kayit.get("cins"), kayit.get("renk"),
        kayit.get("konum"), kayit.get("aciklama"), kayit.get("saglikNotu"),
        " ".join(kayit.get("karakter") or []),
    ])).lower()

    return kayit, hatalar


# ---------------------------------------------------------------------------
# Depo
# ---------------------------------------------------------------------------
def load() -> list[dict]:
    if not JSON_PATH.exists():
        return []
    try:
        veri = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"animals.json okunamadı: {e}")
    return veri.get("hayvanlar", [])


def _atomic_write(path: Path, icerik: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(icerik)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def save(hayvanlar: list[dict]) -> None:
    """JSON'u ve tarayıcının okuduğu JS dosyasını birlikte yazar."""
    hayvanlar = sorted(hayvanlar, key=lambda a: a.get("olusturma") or "", reverse=True)
    govde = {"guncelleme": now_iso(), "sayi": len(hayvanlar), "hayvanlar": hayvanlar}
    _atomic_write(JSON_PATH, json.dumps(govde, ensure_ascii=False, indent=2) + "\n")

    js = (
        "/* Otomatik üretildi — bu dosyayı elle düzenlemeyin.\n"
        "   Kaynak: assets/data/animals.json · Üreten: tools/animals.py */\n"
        "window.KE_DATA = " + json.dumps(govde, ensure_ascii=False, indent=2) + ";\n"
    )
    _atomic_write(JS_PATH, js)


def upsert(kayit: dict) -> dict:
    hayvanlar = load()
    kayit, hatalar = normalize(kayit)
    if hatalar:
        raise ValueError("; ".join(hatalar))
    for i, mevcut in enumerate(hayvanlar):
        if mevcut.get("id") == kayit["id"]:
            kayit["olusturma"] = mevcut.get("olusturma") or kayit["olusturma"]
            hayvanlar[i] = kayit
            break
    else:
        hayvanlar.append(kayit)
    save(hayvanlar)
    return kayit


def delete(animal_id: str) -> bool:
    hayvanlar = load()
    kalan = [a for a in hayvanlar if a.get("id") != animal_id]
    if len(kalan) == len(hayvanlar):
        return False
    save(kalan)
    return True


def get(animal_id: str) -> dict | None:
    return next((a for a in load() if a.get("id") == animal_id), None)


def rebuild() -> int:
    """JSON'daki kayıtları yeniden normalize edip JS dosyasını tazeler."""
    hayvanlar = []
    for ham in load():
        kayit, hatalar = normalize(ham)
        if hatalar:
            print(f"  ! {ham.get('id')}: {'; '.join(hatalar)}")
        hayvanlar.append(kayit)
    save(hayvanlar)
    return len(hayvanlar)


if __name__ == "__main__":
    n = rebuild()
    print(f"{n} kayıt yeniden yazıldı → {JSON_PATH.name}, {JS_PATH.name}")
