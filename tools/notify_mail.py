# -*- coding: utf-8 -*-
"""
Senkron raporunu Gmail SMTP ile e-postalar.

Kullanım (GitHub Actions içinde):
    python3 tools/notify_mail.py sync_rapor.md

GMAIL_ADDRESS ve GMAIL_APP_PASSWORD ortam değişkenleri gerekir (Gmail
"uygulama şifresi" — normal hesap şifresi değil). Alıcı REPORT_EMAIL ile
değiştirilebilir. instagram-to-youtube reposundaki notify.py düzeneğinin
aynısı.
"""

from __future__ import annotations

import os
import re
import smtplib
import sys
from email.mime.text import MIMEText
from pathlib import Path

DEFAULT_RECIPIENT = "murathanbagdat@hotmail.com"


def _duz_metin(markdown: str) -> str:
    """Raporu e-postada okunur düz metne çevirir: [ad](url) → ad: url"""
    metin = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 → \2", markdown)
    metin = re.sub(r"^#+\s*", "", metin, flags=re.M)
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", metin)


def send_email(subject: str, body: str) -> bool:
    address = os.environ.get("GMAIL_ADDRESS")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    recipient = os.environ.get("REPORT_EMAIL", DEFAULT_RECIPIENT)
    if not address or not password:
        print("E-posta yapılandırılmamış (GMAIL_ADDRESS/GMAIL_APP_PASSWORD yok); atlandı.")
        return False

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = address
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
        smtp.login(address, password)
        smtp.sendmail(address, [recipient], msg.as_string())
    print(f"E-posta gönderildi → {recipient}: {subject}")
    return True


def main() -> int:
    if len(sys.argv) < 2 or not Path(sys.argv[1]).exists():
        print("Rapor dosyası yok; e-posta gönderilmedi.")
        return 0
    rapor = Path(sys.argv[1]).read_text(encoding="utf-8")
    hata_var = "Hatalar" in rapor
    konu = ("⚠️ Kurtaran Ev senkron HATASI" if hata_var
            else "🐾 Kurtaran Ev — yeni ilanlar sitede")
    return 0 if send_email(konu, _duz_metin(rapor)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
