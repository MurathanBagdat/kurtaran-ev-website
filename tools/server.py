#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kurtaran Ev — yerel geliştirme sunucusu ve admin API'si.

Çalıştırma:
    python3 tools/server.py
    → http://127.0.0.1:8000          (site)
    → http://127.0.0.1:8000/admin.html (yönetim paneli)

Yalnızca 127.0.0.1'e bağlanır; dışarıdan erişilemez. Admin şifresi:
    export KE_ADMIN_SIFRE="kendi-sifreniz"
Verilmezse varsayılan kullanılır ve açılışta uyarı basılır.

NOT: Bu sunucu yerel çalışma içindir. Canlıda admin paneli için gerçek bir
kimlik doğrulama (oturum, HTTPS, hız sınırı) gerekir — to-do.md'ye bakın.
"""

from __future__ import annotations

import base64
import json
import mimetypes
import os
import re
import secrets
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import animals  # noqa: E402

SITE_DIR = animals.ROOT / "site"
VARSAYILAN_SIFRE = "kurtaranev"
SIFRE = os.environ.get("KE_ADMIN_SIFRE", VARSAYILAN_SIFRE)
PORT = int(os.environ.get("KE_PORT", "8000"))

MAX_GOVDE = 12 * 1024 * 1024          # 12 MB — fotoğraf yüklemesi için
IZINLI_FOTO = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}

_jetonlar: set[str] = set()
_kilit = threading.Lock()


class Handler(SimpleHTTPRequestHandler):
    server_version = "KurtaranEv/1.0"

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(SITE_DIR), **kw)

    # --- yardımcılar ------------------------------------------------------
    def _json(self, govde, kod: int = 200):
        ham = json.dumps(govde, ensure_ascii=False).encode("utf-8")
        self.send_response(kod)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(ham)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(ham)

    def _govde_oku(self) -> dict:
        uzunluk = int(self.headers.get("Content-Length") or 0)
        if uzunluk <= 0:
            return {}
        if uzunluk > MAX_GOVDE:
            raise ValueError("İstek gövdesi çok büyük")
        try:
            return json.loads(self.rfile.read(uzunluk).decode("utf-8"))
        except json.JSONDecodeError as e:
            raise ValueError(f"Geçersiz JSON: {e}")

    def _yetkili(self) -> bool:
        baslik = self.headers.get("Authorization") or ""
        jeton = baslik.removeprefix("Bearer ").strip()
        with _kilit:
            return bool(jeton) and jeton in _jetonlar

    def _yetki_gerek(self) -> bool:
        if self._yetkili():
            return True
        self._json({"hata": "Yetkisiz. Lütfen giriş yapın."}, 401)
        return False

    def log_message(self, bicim, *args):
        if "/api/" in (self.path or ""):
            sys.stderr.write(f"  {self.command} {self.path}\n")

    # --- yönlendirme ------------------------------------------------------
    def do_GET(self):
        yol = urlparse(self.path).path
        if yol.startswith("/api/"):
            return self._api_get(yol)
        if yol == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        yol = urlparse(self.path).path
        if not yol.startswith("/api/"):
            return self._json({"hata": "Bulunamadı"}, 404)
        try:
            return self._api_post(yol)
        except ValueError as e:
            return self._json({"hata": str(e)}, 400)
        except Exception as e:  # sunucu çökmesin
            return self._json({"hata": f"Sunucu hatası: {e}"}, 500)

    def do_DELETE(self):
        yol = urlparse(self.path).path
        m = re.fullmatch(r"/api/hayvanlar/([\w\-]+)", yol)
        if not m:
            return self._json({"hata": "Bulunamadı"}, 404)
        if not self._yetki_gerek():
            return
        silindi = animals.delete(m.group(1))
        return self._json({"silindi": silindi}, 200 if silindi else 404)

    # --- API --------------------------------------------------------------
    def _api_get(self, yol: str):
        if yol == "/api/durum":
            return self._json({
                "calisiyor": True,
                "girisYapildi": self._yetkili(),
                "sayi": len(animals.load()),
            })
        if yol == "/api/hayvanlar":
            if not self._yetki_gerek():
                return
            return self._json({"hayvanlar": animals.load()})
        if yol == "/api/sema":
            return self._json({
                "alanlar": animals.FIELDS,
                "durumlar": animals.STATUS,
                "yasGruplari": animals.AGE_GROUPS,
                "tahminEdilebilir": list(animals.ESTIMABLE),
            })
        return self._json({"hata": "Bulunamadı"}, 404)

    def _api_post(self, yol: str):
        govde = self._govde_oku()

        if yol == "/api/giris":
            if secrets.compare_digest(str(govde.get("sifre", "")), SIFRE):
                jeton = secrets.token_urlsafe(24)
                with _kilit:
                    _jetonlar.add(jeton)
                return self._json({"jeton": jeton})
            return self._json({"hata": "Şifre hatalı."}, 401)

        if yol == "/api/cikis":
            baslik = (self.headers.get("Authorization") or "").removeprefix("Bearer ").strip()
            with _kilit:
                _jetonlar.discard(baslik)
            return self._json({"cikildi": True})

        if not self._yetki_gerek():
            return

        if yol == "/api/hayvanlar":
            try:
                kayit = animals.upsert(govde)
            except ValueError as e:
                return self._json({"hata": str(e)}, 400)
            return self._json({"hayvan": kayit})

        if yol == "/api/fotograf":
            return self._foto_yukle(govde)

        if yol == "/api/instagram-sync":
            return self._instagram_sync(govde)

        if yol == "/api/ornekleri-sil":
            kalan = [a for a in animals.load() if not a.get("ornek")]
            silinen = len(animals.load()) - len(kalan)
            animals.save(kalan)
            return self._json({"silinen": silinen})

        return self._json({"hata": "Bulunamadı"}, 404)

    def _foto_yukle(self, govde: dict):
        veri_url = govde.get("veri") or ""
        m = re.match(r"data:([\w/+.-]+);base64,(.+)$", veri_url, re.S)
        if not m:
            raise ValueError("Fotoğraf data-URL biçiminde olmalı.")
        mime, b64 = m.group(1), m.group(2)
        if mime not in IZINLI_FOTO:
            raise ValueError(f"Desteklenmeyen görsel türü: {mime}. JPEG, PNG veya WebP kullanın.")
        try:
            ham = base64.b64decode(b64, validate=True)
        except Exception:
            raise ValueError("Fotoğraf çözümlenemedi.")
        if len(ham) > 8 * 1024 * 1024:
            raise ValueError("Fotoğraf 8 MB'tan büyük olamaz.")

        animals.PHOTO_DIR.mkdir(parents=True, exist_ok=True)
        ad = f"{animals.slugify(govde.get('isim') or 'foto')}-{secrets.token_hex(4)}{IZINLI_FOTO[mime]}"
        (animals.PHOTO_DIR / ad).write_bytes(ham)
        return self._json({"yol": f"{animals.PHOTO_WEB_PREFIX}/{ad}"})

    def _instagram_sync(self, govde: dict):
        komut = [sys.executable, str(animals.ROOT / "tools" / "instagram_sync.py"),
                 "--limit", str(int(govde.get("limit") or 5))]
        if govde.get("kuru"):
            komut.append("--kuru")
        try:
            sonuc = subprocess.run(komut, capture_output=True, text=True, timeout=180,
                                   cwd=str(animals.ROOT))
        except subprocess.TimeoutExpired:
            return self._json({"hata": "Instagram senkronu zaman aşımına uğradı."}, 504)
        return self._json({
            "kod": sonuc.returncode,
            "cikti": (sonuc.stdout or "") + (sonuc.stderr or ""),
        })

    def guess_type(self, path):
        # .js dosyaları için doğru MIME (bazı sistemlerde text/plain dönüyor)
        tur, _ = mimetypes.guess_type(path)
        if str(path).endswith(".js"):
            return "application/javascript; charset=utf-8"
        if str(path).endswith(".json"):
            return "application/json; charset=utf-8"
        if str(path).endswith(".html"):
            return "text/html; charset=utf-8"
        if str(path).endswith(".css"):
            return "text/css; charset=utf-8"
        return tur or "application/octet-stream"


def main() -> int:
    if not (SITE_DIR / "index.html").exists():
        print(f"! site/ klasörü bulunamadı: {SITE_DIR}")
        return 1
    if not animals.JSON_PATH.exists():
        print("  animals.json yok — boş veri dosyası oluşturuluyor.")
        animals.save([])

    sunucu = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print("─" * 62)
    print("  Kurtaran Ev — yerel sunucu")
    print(f"  Site        : http://127.0.0.1:{PORT}")
    print(f"  Admin paneli: http://127.0.0.1:{PORT}/admin.html")
    print(f"  Kayıt sayısı: {len(animals.load())}")
    if SIFRE == VARSAYILAN_SIFRE:
        print()
        print(f"  ⚠ Admin şifresi varsayılan: \"{VARSAYILAN_SIFRE}\"")
        print("    Değiştirmek için:  export KE_ADMIN_SIFRE=\"...\"")
    print("─" * 62)
    print("  Durdurmak için Ctrl+C")
    try:
        sunucu.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu durduruldu.")
    finally:
        sunucu.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
