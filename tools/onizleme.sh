#!/usr/bin/env bash
# Önizleme ortamı: bulunulan dalın site/ klasörünü Cloudflare Pages'e yükler.
#
#   tools/onizleme.sh            # bulunulan dal
#   tools/onizleme.sh <dal-adi>  # başka bir ad altında
#
# Adres: https://onizleme.kurtaranev.org — her zaman EN SON önizlenen dalı gösterir
#   (hangi dal olduğu: /_onizleme.txt). *.pages.dev adresleri Türkiye'de erişime
#   kapalı olduğu için dal başına adres yerine tek, özel alan adı kullanılıyor.
#   /                       tam prototip (GitHub Pages'teki sitenin aynısı)
#   /ilanlar/kopekler       ilan modu (ilanlar.kurtaranev.org/kopekler'in aynısı)
#   /ilanlar/en/kediler     ilan modu, İngilizce
#   /ilanlar/ilan?id=…      ilan detayı
#
# Canlıya hiçbir şey dokunmaz: ayrı Pages projesi (kurtaranev-onizleme), ayrı adres.
# Merge'den ÖNCE arayüzü değiştiren her PR bu adreste test edilir (bkz. CLAUDE.md).
# Yükleme artımlıdır: fotoğraflar ilk seferden sonra yeniden gönderilmez.
# Gereken: wrangler girişi (wrangler login) — GitHub sırrı gerekmez.
set -euo pipefail

PROJE=kurtaranev-onizleme
KOK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DAL="${1:-$(git -C "$KOK" rev-parse --abbrev-ref HEAD)}"
KOMIT="$(git -C "$KOK" rev-parse --short HEAD)"
if ! git -C "$KOK" diff --quiet -- site; then
  echo "! site/ altında commit'lenmemiş değişiklik var; önizleme bunları da içerir." >&2
fi

GECICI="$(mktemp -d)"
trap 'rm -rf "$GECICI"' EXIT
# APFS'te cp -c dosyaları kopyalamadan klonlar (291 MB anında)
cp -Rc "$KOK/site/." "$GECICI/" 2>/dev/null || cp -R "$KOK/site/." "$GECICI/"
# Ekip paneli önizlemede yok: kapısı (şifre, GitHub vekili) yalnızca admin.kurtaranev.org'da
rm -f "$GECICI/admin.html" "$GECICI/assets/js/admin.js" "$GECICI/assets/js/admin-github.js"

printf 'dal: %s\nkomit: %s\ntarih: %s\n' "$DAL" "$KOMIT" "$(date -u +%FT%TZ)" > "$GECICI/_onizleme.txt"

cat > "$GECICI/_headers" <<'EOF'
/*
  X-Robots-Tag: noindex, nofollow
  Cache-Control: no-cache
EOF
cat > "$GECICI/_redirects" <<'EOF'
/ilanlar            /ilanlar/kopekler     302
/ilanlar/           /ilanlar/kopekler     302
/ilanlar/en         /ilanlar/en/kopekler  302
/ilanlar/en/        /ilanlar/en/kopekler  302
EOF

# Projenin üretim dalına (main) yüklenir: özel alan adı yalnızca üretim dalını gösterir
wrangler pages deploy "$GECICI" --project-name "$PROJE" --branch main \
  --commit-hash "$KOMIT" --commit-message "önizleme: $DAL" --commit-dirty=true

ADRES="https://onizleme.kurtaranev.org"
echo
echo "Önizleme ($DAL @ $KOMIT):"
echo "  Tam site:   $ADRES/"
echo "  İlan modu:  $ADRES/ilanlar/kopekler   ·   $ADRES/ilanlar/kediler"
echo "  İngilizce:  $ADRES/ilanlar/en/kopekler"
