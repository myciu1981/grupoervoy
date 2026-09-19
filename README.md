# grupoervoy.com

Strona firmowa Grupo ERVOY w trzech wersjach jezykowych: hiszpanskiej (glowna), angielskiej i polskiej.

## Co jest czym

| Plik / katalog | Rola |
|---|---|
| `index.html` | wersja ES — strona glowna |
| `en/index.html` | wersja EN |
| `pl/index.html` | wersja PL |
| `support.js` | runtime renderujacy strone |
| `ervoy-boot.js` | laduje system projektowy Ervoy |
| `_ds/` | system projektowy: style, fonty, komponenty |
| `assets/` | mapa, logotypy marek, obrazek podgladu (OG) |
| `robots.txt`, `sitemap.xml` | dla wyszukiwarek |
| `*.dc.html` | **pliki zrodlowe do edycji** — nie trafiaja na serwer |

## Wdrozenie na cPanel

Repozytorium zawiera `.cpanel.yml`; sciezka wdrozenia to `$HOME/public_html/grupoervoy.com/` (document root domeny), wiec nic nie trzeba w nim podmieniac.

1. cPanel → **Git Version Control** → Create → wskaz to repozytorium.
2. Zakladka **Pull or Deploy** → **Update from Remote** → **Deploy HEAD Commit**.

Po kazdym `git push` wystarczy powtorzyc krok 2. Automatyczne wdrozenie przy kazdym pushu wymaga dodatkowo webhooka albo klucza SSH — do ustawienia osobno.

Alternatywnie, bez Gita: wgraj przez File Manager do `public_html` katalogi `en`, `pl`, `_ds`, `assets` oraz pliki `index.html`, `support.js`, `ervoy-boot.js`, `robots.txt`, `sitemap.xml`.

## Edycja tresci

Tresc zyje w plikach `index.dc.html`, `en.dc.html`, `pl.dc.html`. Po zmianie trzeba przebudowac odpowiadajace im `index.html`, `en/index.html`, `pl/index.html` — sa to te same pliki z poprawionymi sciezkami, adresami przelacznika jezykow i blokiem `<noscript>` dla robotow.

## Podglad linku (WhatsApp, LinkedIn, Facebook)

Metadane OG siedza w statycznym `<head>`, obrazek to `assets/og-image.png` (1200×630). Po wdrozeniu sprawdz podglad w Facebook Sharing Debugger — pierwszy raz warto wymusic odswiezenie pamieci podrecznej.
