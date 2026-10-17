# ERVOY - strona www

Strona ERVOY (marka GRUPO VOES, S.A. de C.V.) w trzech wersjach jezykowych: polskiej (adres glowny), hiszpanskiej (`/es/`) i angielskiej (`/en/`).

## Co jest czym

| Plik / katalog | Rola |
|---|---|
| `v2/src/build.py` | generator strony (Jinja2) |
| `v2/src/site_config.py` | adresy podstron, kolejnosc materialow, drobne teksty interfejsu |
| `v2/src/templates/` | szablony HTML |
| `v2/src/static/` | arkusz stylow, skrypt, logo ERVOY i dopiski GRUPO VOES (SVG) |
| `v2/content/*.json` | teksty strony, wyciagniete z plikow Word (`v2/src/extract.py`) |
| `v2/site/` | gotowa strona - to trafia na serwer |
| `assets/` | logotypy marek siostrzanych i obrazek podgladu linku (OG) |
| `favicon*`, `apple-touch-icon.png` | ikony strony (ikona EV) |
| `.htaccess` | przekierowania i kanonizacja domeny |

## Budowanie

```
python v2/src/build.py
```

Wynik trafia do `v2/site/`. Po zmianie tekstow albo szablonow trzeba przebudowac strone i wypchnac `v2/site` razem ze zrodlami.

## Wdrozenie na cPanel

`.cpanel.yml` kopiuje `v2/site/` i `.htaccess` do `$HOME/public_html/grupoervoy.com/` i usuwa z serwera pozostalosci starej strony.

1. cPanel -> **Git Version Control** -> repozytorium.
2. Zakladka **Pull or Deploy** -> **Update from Remote** -> **Deploy HEAD Commit**.

## Identyfikacja

Logo i zasady: ERVOY Brand Guidelines v2.0 (paczka `ERVOY_Brand-Package_v2.0`). Dopisek "Una marca de GRUPO VOES, S.A. de C.V." pochodzi z paczki logo GRUPO VOES. Poprzednia strona (v1) i stara identyfikacja sa w archiwum poza repozytorium.
