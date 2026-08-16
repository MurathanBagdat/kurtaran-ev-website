# -*- coding: utf-8 -*-
"""
Instagram ilan metinlerinden (caption) yapılandırılmış hayvan bilgisi çıkarır.

Sahiplendirme paylaşımları serbest metin olduğu için burada sezgisel (heuristic)
kurallar var. Çıkarılan her kayıt `taslak` durumunda oluşur; bir yönetici onaylamadan
sitede yayınlanmaz. Böylece yanlış ayrıştırma canlıya yansımaz.

Kendi başına da çalışır:
    python3 tools/caption_parser.py "PAMUK yuva arıyor, 2 yaşında dişi, 18 kg"
"""

from __future__ import annotations

import re
import sys
import unicodedata

# ---------------------------------------------------------------------------
# Sözlükler
# ---------------------------------------------------------------------------
DISI = ("dişi", "disi", "kız", "kiz", "kızımız", "prenses", "hanım", "hanımefendi")
ERKEK = ("erkek", "oğlan", "oglan", "oğlumuz", "delikanlı", "bey", "beyefendi")

KEDI_CINS = [
    "tekir", "sarman", "van kedisi", "ankara kedisi", "british shorthair", "scottish fold",
    "iran kedisi", "persian", "siyam", "siamese", "maine coon", "bengal", "sfenks", "sphynx",
    "smokin", "calico", "üç renkli", "uc renkli", "melez",
]
KOPEK_CINS = [
    "golden retriever", "golden", "labrador", "labrador retriever", "husky", "sibirya kurdu",
    "alman çoban", "alman coban", "german shepherd", "terrier", "jack russell", "pitbull",
    "pit bull", "amerikan bully", "rottweiler", "doberman", "cocker", "beagle", "pointer",
    "setter", "kangal", "akbaş", "akbas", "malaklı", "malakli", "çoban köpeği", "coban kopegi",
    "border collie", "collie", "boxer", "dalmaçyalı", "dalmacyali", "chihuahua", "pomeranian",
    "shih tzu", "maltese", "poodle", "kaniş", "kanis", "melez", "sokak karışımı", "karışık",
]

RENKLER = [
    "siyah", "beyaz", "sarı", "sari", "kahverengi", "gri", "kızıl", "kizil", "krem",
    "tekir", "alacalı", "alacali", "siyah-beyaz", "üç renkli", "uc renkli", "smokin",
]

# Kurtaran Ev gönderilerinde boyut ve cins çoğu zaman hashtag ile veriliyor:
# "#Petit #küçükırk", "#Hera #Doberman", "#Joy #calico"
HASHTAG_BOYUT = {
    "kucukirk": "kucuk", "kucukirk1": "kucuk", "minikirk": "kucuk",
    "ortairk": "orta", "buyukirk": "buyuk", "irikirk": "buyuk",
}

HASHTAG_CINS = {
    "borderterrier": "Border Terrier", "doberman": "Doberman",
    "ankarakedisi": "Ankara Kedisi", "himalayankedi": "Himalaya Kedisi",
    "calico": "Calico", "vankedisi": "Van Kedisi", "tekir": "Tekir",
    "britishshorthair": "British Shorthair", "scottishfold": "Scottish Fold",
    "golden": "Golden Retriever", "labrador": "Labrador",
    "terrier": "Terrier", "husky": "Husky", "kangal": "Kangal",
    "poodle": "Poodle", "chihuahua": "Chihuahua", "beagle": "Beagle",
    "sarman": "Sarman", "smokin": "Smokin",
}

HASHTAG_ATLA = {"sahiplendirme", "yuvaariyor", "kurtaranev", "yavrukedi", "yavrukopek",
                "kedi", "kopek", "adopt", "sahiplen", "acil"}

# Bu parçaları içeren hiçbir hashtag hayvan ismi olamaz (kampanya etiketleri:
# #köpeksahiplendirme, #satinalmasahiplen, #cinsmisin, #adoptdontshop ...)
HASHTAG_ISIM_DEGIL_PARCA = ("sahiplen", "kurtaran", "yuva", "adopt", "kedi", "kopek",
                            "acil", "istanbul", "cinsmisin", "hayvan", "petshop",
                            "pets", "cat", "dog", "insta", "love", "rescue")

KARAKTER = {
    "oyuncu": ["oyuncu", "oyun sever", "enerjik", "hareketli"],
    "sakin": ["sakin", "uysal", "sessiz", "durgun", "efendi"],
    "sevecen": ["sevecen", "sevgi dolu", "kucak sever", "sarılmayı", "cana yakın", "cana yakin"],
    "çekingen": ["çekingen", "cekingen", "utangaç", "utangac", "korkak", "ürkek", "urkek"],
    "meraklı": ["meraklı", "merakli", "araştırmacı"],
    "eğitimli": ["eğitimli", "egitimli", "tuvalet eğitimi", "komut"],
    "koruyucu": ["koruyucu", "bekçi"],
    "sadık": ["sadık", "sadik"],
}

OLUMSUZ_YAKIN = ("değil", "degil", "sevmiyor", "anlaşamıyor", "anlasamiyor",
                 "geçinemiyor", "gecinemiyor", "uygun değil", "olmamalı", "olmamali",
                 "tercih edilmez", "sorun yaşıyor", "yasiyor", "saldırgan", "saldirgan")

# "Kedisiz bir ev daha uygun olacaktır" gibi dolaylı olumsuzlamalar
OLUMSUZ_KALIP = {
    "kedilerleUyum": (r"kedisiz\s+(bir\s+)?ev", r"kedi\s*olmayan", r"kedilerle\s+(arasi\s+)?kotu"),
    "kopeklerleUyum": (r"kopeksiz\s+(bir\s+)?ev", r"tek\s+kopek\s+olarak"),
    "cocuklaUyum": (r"cocuksuz\s+(bir\s+)?ev", r"kucuk\s+cocuk\s+olmayan"),
}

# Yaygın Türkçe isim yanlış-pozitiflerini elemek için
ISIM_DEGIL = {
    "yuva", "sahiplendirme", "sahiplenme", "acil", "yardım", "yardim", "ilan", "duyuru",
    "kurtaran", "ev", "dikkat", "önemli", "onemli", "paylaşım", "paylasim", "lütfen",
    "lutfen", "kedi", "köpek", "kopek", "yavru", "dostumuz", "canımız", "canimiz",
    "merhaba", "arkadaşlar", "arkadaslar", "güncelleme", "guncelleme",
    "yuvalandı", "yuvalandi", "rezerve", "sahiplenildi", "sahiplendirildi",
    "geçici", "gecici", "kalıcı", "kalici", "ömürlük", "omurluk", "yeni",
    "burası", "burasi", "bugün", "bugun", "video",
}


def _tr_lower(s: str) -> str:
    return s.replace("I", "ı").replace("İ", "i").lower()


def _tr_capitalize(s: str) -> str:
    """MISIR -> Mısır. Python'ın capitalize'ı Türkçe I/İ ayrımını bilmiyor."""
    if not s:
        return s
    bas = s[0].replace("i", "İ").upper()
    kalan = _tr_lower(s[1:])
    return bas + kalan


def _sade(s: str) -> str:
    """Aksan/şapka farklarını yok sayarak karşılaştırma için sadeleştirir."""
    s = _tr_lower(s)
    tr = str.maketrans("çğıöşü", "cgiosu")
    s = s.translate(tr)
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


CUMLECIK_SINIRI = re.compile(r"[.!?;,\n•·]")


def _cumlecik(metin: str, konum: int) -> str:
    """Eşleşmenin bulunduğu cümleciği döndürür.

    Olumsuzlamayı ham karakter penceresiyle aramak yanlış sonuç veriyordu:
    "Aşıları yapıldı, henüz kısır değil" cümlesinde 'değil' aşıya bağlanıyordu.
    Bu yüzden nokta/virgül/satır sonu ile sınırlanmış cümleciğe bakıyoruz.
    """
    bas = 0
    for m in CUMLECIK_SINIRI.finditer(metin[:konum]):
        bas = m.end()
    son = CUMLECIK_SINIRI.search(metin, konum)
    return metin[bas: son.start() if son else len(metin)]


def _olumsuz(sade_metin: str, konum: int) -> bool:
    """Eşleşmenin bulunduğu cümlecikte olumsuzlama var mı?

    DİKKAT: konum, `_sade()` uygulanmış metne ait olmalı. _sade() emoji gibi
    ASCII olmayan karakterleri düşürdüğü için ham metinle sade metnin indeksleri
    birbirini tutmuyor; ikisini karıştırmak yanlış cümleciğe bakılmasına yol açar.
    """
    parca = _cumlecik(sade_metin, konum)
    return any(_sade(k) in parca for k in OLUMSUZ_YAKIN)


# ---------------------------------------------------------------------------
# Tekil çıkarıcılar
# ---------------------------------------------------------------------------
def hashtagler(caption: str) -> list[str]:
    return re.findall(r"#(\w+)", caption, re.UNICODE)


def hashtag_boyut(caption: str) -> str | None:
    for h in hashtagler(caption):
        b = HASHTAG_BOYUT.get(_sade(h))
        if b:
            return b
    return None


def hashtag_cins(caption: str) -> str | None:
    for h in hashtagler(caption):
        c = HASHTAG_CINS.get(_sade(h))
        if c:
            return c
    return None


def hashtag_isim(caption: str) -> str | None:
    """İlk hashtag çoğu gönderide hayvanın adı: "#Potter #ortaırk" """
    for h in hashtagler(caption):
        sade_h = _sade(h)
        if sade_h in HASHTAG_ATLA or sade_h in HASHTAG_BOYUT or sade_h in HASHTAG_CINS:
            continue
        if any(parca in sade_h for parca in HASHTAG_ISIM_DEGIL_PARCA):
            continue
        if len(h) < 2 or len(h) > 20 or any(ch.isdigit() for ch in h):
            continue
        return _tr_capitalize(h)
    return None


def isim_bul(caption: str) -> str | None:
    """
    Sırasıyla dener:
      1) "İsmi: Pamuk" / "Adı: Pamuk"
      2) İlk satırdaki BÜYÜK HARFLİ kelime (PAMUK yuva arıyor)
      3) "Pamuk yuva arıyor" kalıbı
    """
    m = re.search(r"(?:ismi|adı|adi|isim|ad)\s*[:\-]\s*([A-Za-zÇĞİÖŞÜçğıöşü]{2,20})", caption, re.I)
    if m:
        return _tr_capitalize(m.group(1).strip())

    ilk_satir = next((s for s in caption.splitlines() if s.strip()), "")
    ilk_satir = re.sub(r"[^\w\sÇĞİÖŞÜçğıöşü]", " ", ilk_satir)
    for kelime in ilk_satir.split():
        if len(kelime) < 2 or len(kelime) > 20:
            continue
        if not kelime.isupper():
            continue
        if _tr_lower(kelime) in ISIM_DEGIL:
            continue
        if any(ch.isdigit() for ch in kelime):
            continue
        return _tr_capitalize(kelime)

    m = re.search(r"([A-ZÇĞİÖŞÜ][a-zçğıöşü]{1,19})\s+(?:yuva|sahiplendir|yuvasını|yuvasini)", caption)
    if m and _tr_lower(m.group(1)) not in ISIM_DEGIL:
        return m.group(1)

    etiket = hashtag_isim(caption)
    if etiket:
        return etiket

    # "Potter, 3 yaşlarında" / "Minnoş 🌻" / "Joy 🧩 #calico" — ilk satırdaki özel ad
    ilk_satir_metni = next((x for x in caption.splitlines() if x.strip()), "")
    ilk = re.match(r"\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]{1,19})(?=$|[\s,.!?])", ilk_satir_metni)
    if ilk and _tr_lower(ilk.group(1)) not in ISIM_DEGIL:
        return _tr_capitalize(ilk.group(1))
    return None


def yas_bul(caption: str) -> tuple[int | None, bool]:
    """(ay, tahmini_mi) döner."""
    d = _sade(caption)
    tahmini = bool(re.search(r"(tahmini|yaklasik|civari|kadar|~)", d))

    m = re.search(r"(\d+)[.,](\d+)\s*(?:yas|yasinda|yasindaki)", d)
    if m:
        yil = int(m.group(1)); kesir = int(m.group(2))
        return yil * 12 + (6 if kesir == 5 else 0), tahmini

    m = re.search(r"(\d{1,2})\s*[-–]\s*(\d{1,2})\s*(?:yas|yasinda)", d)
    if m:  # "2-3 yaşında" → ortalama, tahmini
        return int((int(m.group(1)) + int(m.group(2))) / 2 * 12), True

    m = re.search(r"(\d{1,2})\s*(?:yaslarinda|yaslarindaki|yasinda|yasindaki|yasli|yas\b|yasini)", d)
    if m:
        return int(m.group(1)) * 12, tahmini

    m = re.search(r"(\d{1,2})\s*[-–]\s*(\d{1,2})\s*(?:aylik|ayl|ay\b)", d)
    if m:
        return int((int(m.group(1)) + int(m.group(2))) / 2), True

    m = re.search(r"(\d{1,2})[.,](\d)\s*(?:aylik|ay\b)", d)
    if m:
        return max(1, int(round(float(f"{m.group(1)}.{m.group(2)}")))), tahmini

    m = re.search(r"(\d{1,3})\s*(?:aylik|aylık|ay\b)", d)
    if m:
        ay = int(m.group(1))
        return (ay, tahmini) if ay <= 240 else (None, False)

    m = re.search(r"(\d{1,2})\s*[-–]\s*(\d{1,2})\s*(?:haftalik|hafta\b)", d)
    if m:  # "4-5 haftalık" → ortalama, tahmini
        return max(1, round((int(m.group(1)) + int(m.group(2))) / 2 / 4.3)), True

    m = re.search(r"(\d{1,2})\s*(?:haftalik|hafta\b)", d)
    if m:
        return max(0, int(int(m.group(1)) / 4.3)), tahmini

    if re.search(r"\b(yavru|bebek|enik|kedicik)\b", d):
        return 4, True
    if re.search(r"\b(yasli|kidemli|senior)\b", d):
        return 108, True
    return None, False


def kilo_bul(caption: str) -> tuple[float | None, bool]:
    d = _sade(caption)
    tahmini = bool(re.search(r"(tahmini|yaklasik|civari|~)", d))
    m = re.search(r"(\d{1,3})[.,](\d)\s*(?:kg|kilo)", d)
    if m:
        return float(f"{m.group(1)}.{m.group(2)}"), tahmini
    m = re.search(r"(\d{1,3})\s*(?:kg|kilo)", d)
    if m:
        kilo = float(m.group(1))
        return (kilo, tahmini) if 0 < kilo <= 120 else (None, False)
    return None, False


def cinsiyet_bul(caption: str) -> str | None:
    d = _sade(caption)
    disi = min((d.find(_sade(k)) for k in DISI if _sade(k) in d), default=-1)
    erkek = min((d.find(_sade(k)) for k in ERKEK if _sade(k) in d), default=-1)
    if disi < 0 and erkek < 0:
        return None
    if disi < 0:
        return "erkek"
    if erkek < 0:
        return "disi"
    return "disi" if disi < erkek else "erkek"


def cins_bul(caption: str, tur: str) -> str | None:
    d = _sade(caption)
    liste = KEDI_CINS if tur == "kedi" else KOPEK_CINS
    # en uzun eşleşme kazansın ("golden retriever" > "golden")
    bulunan = [c for c in liste if _sade(c) in d]
    if not bulunan:
        return None
    return " ".join(_tr_capitalize(p) for p in max(bulunan, key=len).split())


def renk_bul(caption: str) -> str | None:
    d = _sade(caption)
    bulunan = [c for c in RENKLER if re.search(rf"\b{re.escape(_sade(c))}\b", d)]
    return _tr_capitalize(max(bulunan, key=len)) if bulunan else None


def evet_hayir_bul(caption: str, anahtarlar: tuple[str, ...]) -> bool | None:
    d = _sade(caption)
    for k in anahtarlar:
        idx = d.find(_sade(k))
        if idx >= 0:
            return not _olumsuz(d, idx)
    return None


def uyum_bul(caption: str, anahtarlar: tuple[str, ...]) -> bool | None:
    """Aynı anahtar birden çok geçebilir; olumsuz geçen varsa o kazanır."""
    d = _sade(caption)
    for k in anahtarlar:
        sade_k = _sade(k)
        idx = d.find(sade_k)
        while idx >= 0:
            if _olumsuz(d, idx):
                return False
            sonraki = d.find(sade_k, idx + 1)
            if sonraki < 0:
                return True
            idx = sonraki
    return None


def _uyum(alan: str, caption: str, anahtarlar: tuple[str, ...]) -> bool | None:
    """Önce dolaylı olumsuz kalıplara bak, sonra normal uyum aramasına düş."""
    d = _sade(caption)
    for kalip in OLUMSUZ_KALIP.get(alan, ()):
        if re.search(kalip, d):
            return False
    return uyum_bul(caption, anahtarlar)


def karakter_bul(caption: str) -> list[str]:
    d = _sade(caption)
    bulunan = []
    for etiket, kelimeler in KARAKTER.items():
        if any(_sade(k) in d for k in kelimeler):
            bulunan.append(etiket)
    return bulunan[:6]


# Sağlık notu kalıpları. İkinci eleman: özel bakım gerektirir mi?
# Aşı/kısırlaştırma bilgisi ayrı alanlarda tutulduğu için burada aranmıyor.
SAGLIK_KALIP = (
    (r"ozel\s+bakim", True),
    (r"engelli", True),
    (r"gor(?:e|u)?m[iu]yor", True),          # göremiyor / görmüyor
    (r"\bkor\b", True),                       # kör
    (r"sagir", True), (r"duym[iu]yor", True),
    (r"felc", True), (r"epilepsi", True),
    (r"protez", True), (r"ilac\s+kullan", True),
    (r"\bfiv\b", True), (r"\bfip\b", True), (r"losemi", True),
    (r"kanser", True), (r"tumor", True),
    (r"tek\s+goz", True), (r"uc\s+ayak", True),
    (r"ameliyat", None), (r"tedavi", None), (r"displazi", None),
)

SAGLIK_CUMLE_SINIRI = re.compile(r"(?<=[.!?])\s+|\n+")


def saglik_bul(caption: str) -> tuple[str | None, bool | None]:
    """Sağlık bilgisi içeren cümleleri ayrı bir nota toplar.

    (saglikNotu, ozelBakim) döner. Cümleler ilan metninden silinmez; not,
    yöneticinin panelde düzenleyeceği bir başlangıç değeridir.
    """
    notlar: list[str] = []
    ozel: bool | None = None
    for cumle in SAGLIK_CUMLE_SINIRI.split(caption or ""):
        s = cumle.strip()
        if not s or s.startswith("#"):
            continue
        sade_c = _sade(s)
        for kalip, agir in SAGLIK_KALIP:
            if re.search(kalip, sade_c):
                temiz = re.sub(r"#\w+", "", s).strip(" -•·")
                if temiz and temiz not in notlar:
                    notlar.append(temiz)
                if agir:
                    ozel = True
                break
    return (" ".join(notlar)[:400] or None), ozel


def konum_bul(caption: str) -> str | None:
    """Bulunduğu yeri (geçici yuva / yaşam alanı) metinden çıkarır."""
    d = _sade(caption)
    semt = next((ad for anahtar, ad in (("hadimkoy", "Hadımköy"), ("besiktas", "Beşiktaş"))
                 if anahtar in d), None)
    # Yalın "geçici yuva" çağrı cümlesi de olabilir ("geçici yuva olabilirsiniz");
    # konum ancak iyelik/bulunma ekiyle anılıyorsa ("geçici yuvamızdaki") güvenilir.
    if re.search(r"gecici\s+yuva(?:m|s?[iu]nda|daki)", d):
        return "Gönüllü geçici yuva"
    if re.search(r"yasam\s+alan(?:im|lar)?[iu]", d):
        return f"{semt} yaşam alanı" if semt else "Yaşam alanı"
    return semt


SAYI_SOZLUK = {
    "bir": 1, "biri": 1, "birisi": 1, "iki": 2, "ikisi": 2,
    "uc": 3, "ucu": 3, "dort": 4, "dordu": 4, "bes": 5, "besi": 5,
}


def coklu_cinsiyet(caption: str) -> list[str]:
    """"ikisi erkek, biri dişi" → ["erkek", "erkek", "disi"].

    Tek eşleşme ("sevgi dolu bir erkek") çoklu ilan sayılmaz; kardeş
    gönderilerinde sayılar her cinsiyet için ayrı verildiğinden toplamın
    2'ye ulaşması gerekir.
    """
    d = _sade(caption)
    sonuc: list[str] = []
    for m in re.finditer(r"\b(bir|biri|birisi|iki|ikisi|uc|ucu|dort|dordu|bes|besi|[1-5])\s+"
                         r"(?:tanesi\s+)?(erkek|disi)\b", d):
        n = SAYI_SOZLUK.get(m.group(1)) or int(m.group(1))
        sonuc += [m.group(2)] * n
    return sonuc if len(sonuc) >= 2 else []


def tur_bul(caption: str, varsayilan: str) -> str:
    d = _sade(caption)
    # Türkçe ekleri de yakala: "kedimiz", "kediciğimiz", "kopekler" ...
    kedi = len(re.findall(r"\bkedi\w*|\bpisi\w*|\btekir\w*", d))
    kopek = len(re.findall(r"\bkopek\w*|\benik\w*|\byavrusu\b", d))
    if kedi > kopek:
        return "kedi"
    if kopek > kedi:
        return "kopek"
    return varsayilan


ILAN_OLUMLU = (
    r"yuva\w*\s+\w*\s?(ariyor|ariyoruz|arayan|bekliyor|olsun)",   # "ömürlük yuvasını arıyoruz"
    r"yuvas\w*\s+(ariyor|ariyoruz|arayan)",
    r"sahiplendir\w*",
    r"sahiplenmek",
    r"kalici\s+yuva",
    r"omurluk\s+yuva",
    r"omur\s+boyu\s+sevecek",
    r"yeni\s+ailesi",
    r"kisirlastirma\s+sarti",
)

ILAN_OLUMSUZ = (
    r"koruyucu\s+mele",           # Koruyucu Melek çağrısı — sahiplendirme değil
    r"yuvasina\s+kavustu",
    r"sahiplendirildi",
    r"yuvalandi",
    r"tesekkur\s+eder",
    r"bagis\s+kampanya",
    r"etkinligimize",
)


def ilan_mi(caption: str) -> bool:
    """Her paylaşım sahiplendirme ilanı değil.

    Gerçek gönderilerde ifade çok çeşitli ("ömürlük yuvasını arıyoruz",
    "yeni ailesinin hayatına...", "kısırlaştırma şartı ile sahiplendirilecektir"),
    bu yüzden sabit kalıp listesi yerine olumlu/olumsuz sinyaller tartılıyor.
    """
    d = _sade(caption)
    olumlu = sum(1 for k in ILAN_OLUMLU if re.search(k, d))
    olumsuz = sum(1 for k in ILAN_OLUMSUZ if re.search(k, d))

    # "🐾 5 Aylık / Dişi / Kısır" künye bloğu güçlü bir ilan işareti
    if re.search(r"(aylik|yasinda|yaslarinda)[^\n]{0,20}\n[^\n]{0,20}(disi|erkek)", d):
        olumlu += 1
    # boyut hashtag'leri yalnızca sahiplendirme gönderilerinde kullanılıyor
    if hashtag_boyut(caption):
        olumlu += 1

    if olumsuz and olumsuz >= olumlu:
        return False
    return olumlu > 0


def yuvalandi_mi(caption: str) -> bool:
    d = _sade(caption)
    return any(k in d for k in ("yuvasina kavustu", "sahiplendirildi", "yuvalandi", "yuvasini buldu"))


def icerik_turu(caption: str) -> str:
    """Gönderiyi sınıflandırır: ilan | koruyucu-melek | yuvalandi | diger.

    Koruyucu Melek çağrıları (örn. Arya) sahiplendirme ilanı değildir ama
    ayrı bir içerik türü olarak tanınır — ileride siteye ayrı bir bölüm
    eklenirse pipeline bunları ayrıştırabilsin diye.
    """
    if ilan_mi(caption):
        return "ilan"
    d = _sade(caption)
    if re.search(r"koruyucu\s+mele", d):
        return "koruyucu-melek"
    if yuvalandi_mi(caption):
        return "yuvalandi"
    return "diger"


def temiz_aciklama(caption: str, limit: int = 600) -> str:
    """Hashtag ve çağrı satırlarını temizleyip okunur bir ilan metni bırakır."""
    satirlar = []
    for satir in caption.splitlines():
        s = satir.strip()
        if not s:
            continue
        sade = _sade(s)
        if s.startswith("#") or sade.count("#") >= 3:
            continue
        if any(k in sade for k in ("dm ", "dm'", "link in bio", "biodaki", "whatsapp",
                                   "iletisime gec", "mesaj at")):
            continue
        s = re.sub(r"#\w+", "", s).strip()
        if s:
            satirlar.append(s)
    metin = " ".join(satirlar)
    metin = re.sub(r"\s{2,}", " ", metin).strip()
    return metin[:limit].rstrip() + ("…" if len(metin) > limit else "")


# ---------------------------------------------------------------------------
# Ana giriş noktası
# ---------------------------------------------------------------------------
def kisir_bul(caption: str) -> bool | None:
    """"Kısırlaştırma şartı ile sahiplendirilecektir" => henüz kısır DEĞİL."""
    d = _sade(caption)
    if re.search(r"kisirlastirma\s+sarti|kisirlastirilmak\s+sarti|kisirlastirma\s+kosulu", d):
        return False
    return evet_hayir_bul(caption, ("kisirlastirildi", "kısırlaştırıldı", "kısır", "kisir",
                                    "kısırlaştırılmış", "kisirlastirilmis"))


def parse(caption: str, varsayilan_tur: str = "kopek") -> dict:
    """Caption metninden animals.py şemasına uygun (kısmî) bir sözlük üretir."""
    caption = caption or ""
    tur = tur_bul(caption, varsayilan_tur)

    yas, yas_tahmini = yas_bul(caption)
    kilo, kilo_tahmini = kilo_bul(caption)
    cins = hashtag_cins(caption) or cins_bul(caption, tur)
    boyut = hashtag_boyut(caption)
    saglik_notu, ozel_bakim = saglik_bul(caption)

    tahmini = []
    if yas is not None and yas_tahmini:
        tahmini.append("yasAy")
    if kilo is not None and kilo_tahmini:
        tahmini.append("kiloKg")

    kayit = {
        "tur": tur,
        "isim": isim_bul(caption),
        "cinsiyet": cinsiyet_bul(caption),
        "cins": cins,
        "boyut": boyut,
        "yasAy": yas,
        "kiloKg": kilo,
        "renk": (lambda r: None if r and cins and _sade(r) == _sade(cins) else r)(renk_bul(caption)),
        "kisir": kisir_bul(caption),
        "asili": evet_hayir_bul(caption, ("aşıları tam", "asilari tam", "aşıları yapıldı",
                                          "asilari yapildi", "aşılı", "asili", "aşıları")),
        "cipli": evet_hayir_bul(caption, ("mikroçip", "mikrocip", "çipli", "cipli", "çip takıldı")),
        "cocuklaUyum": _uyum("cocuklaUyum", caption,
                             ("çocuklarla", "cocuklarla", "çocuk sever", "çocuklu")),
        "kopeklerleUyum": _uyum("kopeklerleUyum", caption,
                                ("köpeklerle", "kopeklerle", "diğer köpekler", "kopege alisik")),
        "kedilerleUyum": _uyum("kedilerleUyum", caption,
                               ("kedilerle", "kedilere", "diğer kediler", "diger kediler")),
        "karakter": karakter_bul(caption),
        "aciklama": temiz_aciklama(caption),
        "saglikNotu": saglik_notu,
        "ozelBakim": ozel_bakim,
        "konum": konum_bul(caption),
        "durum": "taslak",
        "tahmini": tahmini,
    }
    return kayit


def parse_all(caption: str, varsayilan_tur: str = "kopek") -> list[dict]:
    """Tek gönderiden bir ya da birden çok kayıt üretir.

    "Kutu kardeşler … ikisi erkek, biri dişi" gibi kardeş gönderileri
    hayvan başına bir kayda açılır; cinsiyetler metindeki sayılara göre
    dağıtılır, isimler numaralanır ("Kutu 1", "Kutu 2", …).
    """
    taban = parse(caption, varsayilan_tur)
    cinsiyetler = coklu_cinsiyet(caption)
    if not cinsiyetler:
        return [taban]

    kayitlar = []
    for i, cinsiyet in enumerate(cinsiyetler, 1):
        kayit = dict(taban)
        kayit["karakter"] = list(taban["karakter"])
        kayit["tahmini"] = list(taban["tahmini"])
        kayit["cinsiyet"] = cinsiyet
        if taban.get("isim"):
            kayit["isim"] = f"{taban['isim']} {i}"
        kayitlar.append(kayit)
    return kayitlar


def ozet(kayit: dict) -> str:
    dolu = {k: v for k, v in kayit.items()
            if v not in (None, [], "") and k not in ("aciklama", "durum", "tahmini")}
    return ", ".join(f"{k}={v}" for k, v in dolu.items())


if __name__ == "__main__":
    metin = " ".join(sys.argv[1:]) or sys.stdin.read()
    sonuc = parse(metin)
    print("İlan mı :", ilan_mi(metin))
    print("Çıkarım :", ozet(sonuc))
    if sonuc["tahmini"]:
        print("Tahmini :", ", ".join(sonuc["tahmini"]))
