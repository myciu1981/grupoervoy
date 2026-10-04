"""Generator strony grupoervoy.com (v2).

Użycie:  python src/build.py            -> buduje wszystkie języki, dla których jest content/<lang>.json
Wynik trafia do katalogu site/. Teksty pochodzą z plików Word (zob. extract.py).
"""
import hashlib
import html
import json
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup

sys.path.insert(0, str(Path(__file__).parent))
import hero  # noqa: E402
from site_config import (ARTICLES, BING_VERIFY, DEFAULT, INDEXNOW_KEY, HREFLANG, HTML_LANG, X_DEFAULT, LANGS, OG_LOCALE, PREFIX, RESOURCES, ROUTES,  # noqa: E402
                         SERVICES, SITE, UI, UPDATES, WHATSAPP)

ROOT = Path(__file__).resolve().parent.parent
ORG_ID = SITE + '/#organization'
SRC = ROOT / 'src'
OUT = ROOT / 'site'
REPO = ROOT.parent

FLAGS = {
    'pl': '<svg viewBox="0 0 20 14" aria-hidden="true"><rect width="20" height="7" fill="#fff"/><rect y="7" width="20" height="7" fill="#dc143c"/></svg>',
    'es': '<svg viewBox="0 0 20 14" aria-hidden="true"><rect width="20" height="14" fill="#fff"/><rect width="6.67" height="14" fill="#006847"/><rect x="13.33" width="6.67" height="14" fill="#ce1126"/><circle cx="10" cy="7" r="1.8" fill="#8c5a2b"/></svg>',
    'en': '<svg viewBox="0 0 20 14" aria-hidden="true"><rect width="20" height="14" fill="#012169"/><path d="M0 0l20 14M20 0 0 14" stroke="#fff" stroke-width="2.6"/><path d="M0 0l20 14M20 0 0 14" stroke="#c8102e" stroke-width="1.2"/><path d="M10 0v14M0 7h20" stroke="#fff" stroke-width="4"/><path d="M10 0v14M0 7h20" stroke="#c8102e" stroke-width="2.2"/></svg>',
}
ICON_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3z" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8.6 7.8c.3-.6.6-.6.9-.6h.6c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.4 0 .6l-.5.7c-.1.2-.2.3 0 .6.6 1 1.4 1.8 2.5 2.4.3.1.4.1.6-.1l.7-.8c.2-.2.4-.2.6-.1l1.8.9c.3.1.4.3.4.5 0 .5-.2 1.4-1.1 1.9-.8.4-1.9.5-3.7-.3a10 10 0 0 1-4.4-4.2c-.7-1.4-.6-2.5-.1-3.3z" fill="currentColor"/></svg>'


def slug(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').replace('ł', 'l')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def digits(s):
    return re.sub(r'\D', '', s)


def short_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def blocks_html(blocks):
    out = []
    for b in blocks or []:
        if b['t'] == 'p':
            out.append(f"<p>{b['h']}</p>")
        elif b['t'] == 'h3':
            out.append(f"<h2>{html.escape(b['h'])}</h2>")
        elif b['t'] == 'ul':
            out.append('<ul>' + ''.join(f'<li>{i}</li>' for i in b['items']) + '</ul>')
    return '\n'.join(out)


class Lang:
    def __init__(self, code, data):
        self.code = code
        self.d = data
        self.missing = set()

    def t(self, key):
        v = self.d.get(key)
        if v is None:
            self.missing.add(key)
            return f'[[{key}]]'
        return v

    def url(self, key, lang=None):
        lang = lang or self.code
        return '/' + PREFIX[lang] + ROUTES[key][lang]


def service_body(L, n):
    pre = f'u{n}.'
    skip = {'seo.tytul', 'seo.opis', 'label', 'h1', 'lead'}
    out, items = [], []

    def flush():
        if items:
            out.append('<ul>' + ''.join(f'<li>{html.escape(i)}</li>' for i in items) + '</ul>')
            items.clear()
    for k, v in L.d.items():
        if not k.startswith(pre):
            continue
        rest = k[len(pre):]
        if rest in skip:
            continue
        if re.match(r'.*\.lista\.\d+$', rest):
            items.append(v)
            continue
        flush()
        if rest.startswith('h2.'):
            out.append(f'<h2>{html.escape(v)}</h2>')
        else:
            out.append(f'<p>{html.escape(v)}</p>')
    flush()
    return '\n'.join(out)


PL_MONTHS = {'sty': 1, 'lut': 2, 'mar': 3, 'kwi': 4, 'maj': 5, 'cze': 6, 'lip': 7, 'sie': 8, 'wrz': 9,
             'paź': 10, 'paz': 10, 'lis': 11, 'gru': 12}


def fair_end(termin):
    """Ostatni dzień targów z polskiego terminu, np. '13–15 paź 2026', 'kwiecień/maj 2027', 'co roku 2027'.
    Gdy brak dnia - koniec miesiąca, gdy brak miesiąca - koniec roku."""
    y = re.search(r'20\d\d', termin)
    if not y:
        return None
    year = int(y.group(0))
    head = termin[:y.start()].lower()
    found = [(m.start(), PL_MONTHS[m.group(1)[:3]]) for m in re.finditer(r'([a-ząćęłńóśźż]{3,})', head)
             if m.group(1)[:3] in PL_MONTHS]
    if not found:
        return date(year, 12, 31)
    pos, month = found[-1]
    days = re.findall(r'\d+', head[:pos])
    if days:
        return date(year, month, int(days[-1]))
    nxt = date(year + (month == 12), month % 12 + 1, 1)
    return date.fromordinal(nxt.toordinal() - 1)


_PL_CONTENT = None

PL_MONTHS_GEN = {'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4, 'maja': 5, 'czerwca': 6, 'lipca': 7, 'sierpnia': 8,
                 'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12}


def pl_content():
    global _PL_CONTENT
    if _PL_CONTENT is None:
        _PL_CONTENT = json.loads((ROOT / 'content' / 'pl.json').read_text(encoding='utf-8'))
    return _PL_CONTENT


def iso_updated(key):
    """Data aktualizacji artykułu w ISO 8601, czytana z wersji polskiej (np. '4 października 2026')."""
    m = re.match(r'(\d+)\s+(\w+)\s+(20\d\d)', pl_content().get(f'{key}.aktualizacja', ''))
    if not m or m.group(2) not in PL_MONTHS_GEN:
        return None
    return date(int(m.group(3)), PL_MONTHS_GEN[m.group(2)], int(m.group(1))).isoformat()


def page_title(title):
    """Google ucina tytuły po ok. 60 znakach - przy długich tytułach pomijamy dopisek z nazwą firmy."""
    suffix = ' | GRUPO ERVOY'
    return title[:-len(suffix)] if len(title) > 65 and title.endswith(suffix) else title


def fairs(L, today=None):
    """Wiersze kalendarza targów. Imprezy, które już się skończyły, są pomijane -
    termin czytamy z wersji polskiej, bo numeracja targów jest wspólna dla języków."""
    today = today or date.today()
    rows, cats = [], {}
    n = 0
    while f'zas.targi.{n + 1}.nazwa' in L.d:
        n += 1
        end = fair_end(pl_content().get(f'zas.targi.{n}.termin', ''))
        if end and end < today:
            continue
        g = lambda f: L.d.get(f'zas.targi.{n}.{f}', '')  # noqa: E731
        termin = g('termin')
        m = re.match(r'^(.*?)\s+(20\d\d.*)$', termin)
        d1, d2 = (m.group(1), m.group(2)) if m else (termin, '')
        city, _, venue = g('miejsce').partition(' · ')
        tags = [x.strip() for x in g('branza').split(',') if x.strip()]
        for tg in tags:
            cats.setdefault(slug(tg), tg)
        url = g('link')
        rows.append(dict(name=g('nazwa'), url=url, host=re.sub(r'^https?://(www\.)?', '', url).rstrip('/'),
                         d1=d1, d2=d2, city=city, venue=venue, tags=tags, cat_keys=' '.join(slug(x) for x in tags),
                         desc=g('opis'), rec=g('polecamy').strip().lower() in ('tak', 'sí', 'si', 'yes')))
    order = [r['city'] for r in rows]
    cities = sorted(set(order), key=lambda c: (-order.count(c), c))
    return rows, sorted([dict(key=k, label=v) for k, v in cats.items()], key=lambda c: slug(c['label'])), cities


def glossary(L):
    items = []
    for b in L.d.get('zas.slownik.tresc', []):
        if b['t'] != 'ul':
            continue
        for it in b['items']:
            m = re.match(r'<strong>(.*?)</strong>\s*[–-]\s*(.*)$', it, re.S)
            if not m:
                continue
            term, definition = html.unescape(m.group(1)), html.unescape(m.group(2)).strip()
            definition = definition[:1].upper() + definition[1:]
            items.append(dict(term=term, def_=definition))
    groups = {}
    for e in sorted(items, key=lambda e: slug(e['term'])):
        L0 = slug(e['term'])[:1].upper()
        groups.setdefault(L0, []).append(dict(term=e['term'], **{'def': e['def_']}, id='h-' + slug(e['term']),
                                              search=e['term'] + ' ' + e['def_']))
    intro = [b for b in L.d.get('zas.slownik.tresc', []) if b['t'] == 'p']
    return sorted(groups.items()), intro


def llms_txt(built):
    """Plik /llms.txt (llmstxt.org): zwięzły opis firmy i spis stron dla modeli językowych, w Markdownie."""
    E = built.get('en') or next(iter(built.values()))
    u = lambda L, k: SITE + L.url(k)  # noqa: E731
    out = ['# GRUPO ERVOY', '',
           '> GRUPO ERVOY, S.A. de C.V. is a Mexican company based in Monterrey, Nuevo León, that helps European '
           'manufacturers prepare their products for sale in Mexico and enter the Mexican market: market research, '
           'Mexican NOM standards and labelling, local representation, import and logistics, distributors and trade shows. '
           'The team works in Spanish, English and Polish. The first consultation is free.', '',
           f'- Address: Cambridge 103, 64349 Monterrey, N.L., Mexico',
           f"- Email: {E.t('kontakt.firma.email')}",
           f"- Contact: {u(E, 'kontakt')}",
           f"- Own brands in Mexico: {E.t('marki.smb.nazwa')} (https://{E.t('marki.smb.link')}), "
           f"{E.t('marki.polaca.nazwa')} (https://{E.t('marki.polaca.link')})",
           '- Languages of this site: Polish (default, https://grupoervoy.com/), Spanish (https://grupoervoy.com/es/), '
           'English (https://grupoervoy.com/en/)', '', '## Services', '']
    out += [f"- [{E.t(f'home.uslugi.{i}.tytul')}]({u(E, k)}): {E.t(f'{k}.seo.opis')}" for i, k in enumerate(SERVICES, 1)]
    out += ['', '## Knowledge base', '']
    out += [f"- [{E.t(f'{k}.tytul')}]({u(E, k)}): {E.t(f'{k}.zapowiedz')}" for k in ARTICLES + UPDATES]
    out += [f"- [{E.t(f'{k}.tytul')}]({u(E, k)}): {E.t(f'{k}.zapowiedz')}" for k in RESOURCES]
    out += ['', '## Company', '',
            f"- [{E.t('menu.o-nas')}]({u(E, 'onas')})", f"- [{E.t('menu.jak-pracujemy')}]({u(E, 'proces')})",
            f"- [{E.t('menu.marki')}]({u(E, 'marki')})", '']
    for code, title in (('es', 'Español'), ('pl', 'Polski')):
        if code in built:
            L = built[code]
            out += [f'## {title}', '', f"- [{L.t('home.seo.tytul')}]({u(L, 'home')}): {L.t('home.seo.opis')}"]
            out += [f"- [{L.t(f'home.uslugi.{i}.tytul')}]({u(L, k)})" for i, k in enumerate(SERVICES, 1)]
            out += [f"- [{L.t('menu.baza-wiedzy')}]({u(L, 'wiedza')})", f"- [{L.t('menu.kontakt')}]({u(L, 'kontakt')})", '']
    return '\n'.join(out)


def build(langs):
    env = Environment(loader=FileSystemLoader(SRC / 'templates'), autoescape=True, undefined=StrictUndefined,
                      trim_blocks=True, lstrip_blocks=True)
    env.filters['nl'] = lambda s: Markup('<br>'.join(html.escape(x) for x in s.split('\n')))
    env.filters['digits'] = digits

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / 'assets').mkdir(parents=True)
    css = SRC / 'static' / 'style.css'
    js = SRC / 'static' / 'site.js'
    css_hash, js_hash = short_hash(css), short_hash(js)
    shutil.copy(css, OUT / 'assets' / f'style.{css_hash}.css')
    shutil.copy(js, OUT / 'assets' / f'site.{js_hash}.js')
    for f in (SRC / 'static').glob('*.svg'):
        shutil.copy(f, OUT / 'assets' / f.name)
    for f in ['smb-mx.png', 'polaca-foods.png', 'smb-mx-icon.svg', 'polaca-foods-sygnet.png', 'og-image.png']:
        shutil.copy(REPO / 'assets' / f, OUT / 'assets' / f)
    for f in ['favicon.svg', 'favicon.ico', 'favicon-32x32.png', 'apple-touch-icon.png', 'google0df9b290c98199fd.html']:
        shutil.copy(REPO / f, OUT / f)

    map_doc = hero.map_svg(SRC / 'data' / 'ne50.geojson').encode('utf-8')
    map_href = f"/assets/map.{hashlib.sha256(map_doc).hexdigest()[:8]}.svg"
    (OUT / map_href.lstrip('/')).write_bytes(map_doc)

    built = {code: Lang(code, json.loads((ROOT / 'content' / f'{code}.json').read_text(encoding='utf-8'))) for code in langs}
    pages_for_sitemap = []

    for code, L in built.items():
        ui = UI[code]
        wa_key = WHATSAPP[code]
        wa_num = digits(L.t(wa_key + '.telefon'))
        whatsapp = f"https://wa.me/{wa_num}?text={quote(L.t('cta.whatsapp.wiadomosc'))}"
        nav = [('uslugi', L.t('menu.uslugi')), ('proces', L.t('menu.jak-pracujemy')), ('wiedza', L.t('menu.baza-wiedzy')),
               ('marki', L.t('menu.marki')), ('onas', L.t('menu.o-nas')), ('kontakt', L.t('menu.kontakt'))]
        hero_svg = hero.render(code, SRC / 'data' / 'ne50.geojson', map_href)

        def render(key, template, section=None, seo=None, **ctx):
            path = ROUTES[key][code]
            title, desc = seo or (L.t(f'{key}.seo.tytul'), L.t(f'{key}.seo.opis'))
            title = page_title(title)
            canonical = SITE + L.url(key)
            alternates = [dict(hreflang=HREFLANG[c], href=SITE + L.url(key, c)) for c in LANGS if c in built]
            if X_DEFAULT in built:
                alternates.append(dict(hreflang='x-default', href=SITE + L.url(key, X_DEFAULT)))
            lang_links = [dict(code=c, name=ui['lang_names'][c], flag=FLAGS[c], href=L.url(key, c), current=c == code) for c in LANGS]
            jsonld = ctx.pop('jsonld', [])
            if key != 'home':
                crumbs_ld = [dict(name=ui['home'], url=SITE + L.url('home'))] + [dict(name=c['label'], url=SITE + c['href']) for c in ctx.get('crumbs', [])] + [dict(name=ctx.get('h1', title), url=canonical)]
                jsonld.append(json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                    {'@type': 'ListItem', 'position': i + 1, 'name': c['name'], 'item': c['url']} for i, c in enumerate(crumbs_ld)]}, ensure_ascii=False))
            base = dict(bing_verify=BING_VERIFY, t=L.t, url=L.url, ui=ui, html_lang=HTML_LANG[code], og_locale=OG_LOCALE[code], site=SITE,
                        og_locale_alt=[OG_LOCALE[c] for c in LANGS if c != code and c in built],
                        seo_title=title, seo_desc=desc, og_title=title, og_desc=desc, canonical=canonical, alternates=alternates,
                        og_type='website', noindex=False, nav=nav, section=section, lang_links=lang_links, whatsapp=whatsapp,
                        css_hash=css_hash, js_hash=js_hash, services=SERVICES, icon_wa=Markup(ICON_WA), jsonld=[Markup(j) for j in jsonld],
                        dark_header=False, no_band=False, band_h2=None, band_text=None)
            base.update(ctx)
            out_path = OUT / PREFIX[code] / path / 'index.html'
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(env.get_template(template).render(**base), encoding='utf-8')
            pages_for_sitemap.append((key, code))

        kb = L.url('wiedza')
        kb_crumb = [dict(label=L.t('menu.baza-wiedzy'), href=kb)]
        tabs = lambda cur: [dict(label=L.t(f'wiedza.dzial.{i}.nazwa'), href=L.url(k), count=n, current=k == cur)  # noqa: E731
                            for i, (k, n) in enumerate([('wiedza', len(ARTICLES)), ('wiedza.akt', len(UPDATES)), ('wiedza.zas', len(RESOURCES))], 1)]

        org = {'@context': 'https://schema.org', '@type': 'Organization', '@id': ORG_ID, 'name': 'GRUPO ERVOY',
               'legalName': 'GRUPO ERVOY, S.A. de C.V.', 'alternateName': ['Grupo Ervoy', 'ERVOY'], 'url': SITE + L.url('home'),
               'description': L.t('home.seo.opis'), 'logo': SITE + '/apple-touch-icon.png', 'image': SITE + '/assets/og-image.png',
               'email': L.t('kontakt.firma.email'), 'telephone': '+' + digits(L.t('kontakt.osoba2.telefon')),
               'areaServed': [{'@type': 'Country', 'name': 'Mexico'}, {'@type': 'Place', 'name': 'European Union'}],
               'knowsLanguage': ['es', 'pl', 'en'],
               'brand': [{'@type': 'Brand', 'name': L.t('marki.smb.nazwa'), 'url': 'https://' + L.t('marki.smb.link')},
                         {'@type': 'Brand', 'name': L.t('marki.polaca.nazwa'), 'url': 'https://' + L.t('marki.polaca.link')}],
               'address': {'@type': 'PostalAddress', 'streetAddress': 'Cambridge 103', 'postalCode': '64349', 'addressLocality': 'Monterrey',
                           'addressRegion': 'Nuevo León', 'addressCountry': 'MX'},
               'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'sales', 'name': L.t(p + '.imie'), 'telephone': '+' + digits(L.t(p + '.telefon')),
                                 'email': L.t(p + '.email')} for p in ('kontakt.osoba1', 'kontakt.osoba2')]}

        # strona główna
        frows, _, _ = fairs(L)
        render('home', 'home.html', seo=(L.t('home.seo.tytul'), L.t('home.seo.opis')), dark_header=True,
               paths=[['u1'], ['u2', 'u4', 'u3'], ['u5', 'u6']], next_fairs=frows[:3],
               hero_svg=Markup(hero_svg), map_href=map_href, hero_css=Markup(hero.CSS), panel_css=Markup(hero.panel_css(hero.PANEL_TIMES)),
               teaser=ARTICLES[:3], jsonld=[json.dumps(org, ensure_ascii=False), json.dumps(
                   {'@context': 'https://schema.org', '@type': 'WebSite', '@id': SITE + L.url('home') + '#website', 'url': SITE + L.url('home'),
                    'name': 'GRUPO ERVOY', 'alternateName': ['Grupo Ervoy', 'ERVOY'], 'inLanguage': HTML_LANG[code],
                    'publisher': {'@id': ORG_ID}}, ensure_ascii=False)])

        # usługi
        render('uslugi', 'cards.html', section='uslugi', label=L.t('uslugi.label'), h1=L.t('uslugi.h1'),
               leads=[L.t('uslugi.lead'), L.t('uslugi.lead2')], crumbs=[], crumb_here='', updated=None, tabs=None,
               cards=[dict(href=L.url(k), num=f'0{i}', title=L.t(f'home.uslugi.{i}.tytul'), text=L.t(f'home.uslugi.{i}.tekst')) for i, k in enumerate(SERVICES, 1)],
               steps=None, kb_items=None, extra=None, faq=None, faq_title='', disclaimer=None)
        for i, k in enumerate(SERVICES, 1):
            render(k, 'blocks.html', section='uslugi', label=L.t(f'{k}.label'), h1=L.t(f'{k}.h1'), leads=[L.t(f'{k}.lead')],
                   crumbs=[dict(label=L.t('menu.uslugi'), href=L.url('uslugi'))], crumb_here=L.t(f'home.uslugi.{i}.tytul'),
                   updated=None, tabs=None, body=Markup(service_body(L, i)), legal=None, legal_title='', disclaimer=None,
                   jsonld=[json.dumps({'@context': 'https://schema.org', '@type': 'Service', 'name': L.t(f'home.uslugi.{i}.tytul'),
                                       'description': L.t(f'{k}.seo.opis'), 'url': SITE + L.url(k), 'inLanguage': HTML_LANG[code],
                                       'provider': {'@id': ORG_ID}, 'areaServed': {'@type': 'Country', 'name': 'Mexico'}},
                                      ensure_ascii=False)])

        # jak pracujemy
        extra = f"<h2>{html.escape(L.t('proces.h2.partnerzy'))}</h2><p>{html.escape(L.t('proces.partnerzy.p1'))}</p><p>{html.escape(L.t('proces.partnerzy.p2'))}</p>"
        render('proces', 'cards.html', section='proces', label=L.t('proces.label'), h1=L.t('proces.h1'), leads=[L.t('proces.lead')],
               crumbs=[], crumb_here='', updated=None, tabs=None, cards=None, kb_items=None,
               steps=[dict(title=L.t(f'proces.{i}.tytul'), text=L.t(f'proces.{i}.tekst')) for i in range(1, 7)],
               extra=Markup(extra), faq=None, faq_title='', disclaimer=None)

        # baza wiedzy
        faq = []
        i = 1
        while f'faq.{i}.pytanie' in L.d:
            faq.append(dict(q=L.t(f'faq.{i}.pytanie'), a=L.t(f'faq.{i}.odpowiedz')))
            i += 1
        faq_ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': q['a']}} for q in faq]}, ensure_ascii=False)

        def kb_items(keys):
            return [dict(href=L.url(k), num=f'{j:02d}', title=L.t(f'{k}.tytul'), text=L.t(f'{k}.zapowiedz'), updated=L.d.get(f'{k}.aktualizacja'))
                    for j, k in enumerate(keys, 1)]
        common_kb = dict(label=L.t('wiedza.label'), h1=L.t('wiedza.h1'), leads=[L.t('wiedza.lead')], updated=None,
                         cards=None, steps=None, extra=None, crumb_here='')
        render('wiedza', 'cards.html', section='wiedza', crumbs=[], tabs=tabs('wiedza'), kb_items=kb_items(ARTICLES),
               faq=faq, faq_title=L.t('faq.h2'), disclaimer=L.t('wiedza.zastrzezenie'), jsonld=[faq_ld], **common_kb)
        render('wiedza.akt', 'cards.html', section='wiedza', crumbs=[], tabs=tabs('wiedza.akt'), kb_items=kb_items(UPDATES),
               faq=None, faq_title='', disclaimer=None,
               seo=(f"{L.t('wiedza.dzial.2.nazwa')} | GRUPO ERVOY", L.t('wiedza.dzial.2.opis')), **common_kb)
        render('wiedza.zas', 'cards.html', section='wiedza', crumbs=[], tabs=tabs('wiedza.zas'), kb_items=kb_items(RESOURCES),
               faq=None, faq_title='', disclaimer=None,
               seo=(f"{L.t('wiedza.dzial.3.nazwa')} | GRUPO ERVOY", L.t('wiedza.dzial.3.opis')), **common_kb)

        for group, dz in ((ARTICLES, 1), (UPDATES, 2)):
            for k in group:
                title = L.t(f'{k}.tytul')
                art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': title, 'description': L.t(f'{k}.zapowiedz'),
                       'inLanguage': HTML_LANG[code], 'image': SITE + '/assets/og-image.png',
                       'author': {'@type': 'Organization', '@id': ORG_ID, 'name': 'GRUPO ERVOY', 'url': SITE + L.url('onas')},
                       'publisher': {'@type': 'Organization', '@id': ORG_ID, 'name': 'GRUPO ERVOY',
                                     'logo': {'@type': 'ImageObject', 'url': SITE + '/apple-touch-icon.png'}},
                       'mainEntityOfPage': SITE + L.url(k)}
                if iso_updated(k):
                    art['datePublished'] = art['dateModified'] = iso_updated(k)
                art_ld = json.dumps(art, ensure_ascii=False)
                render(k, 'blocks.html', section='wiedza', seo=(f'{title} | GRUPO ERVOY', L.t(f'{k}.zapowiedz')),
                       label=L.t(f'wiedza.dzial.{dz}.nazwa'), h1=title, leads=[L.t(f'{k}.zapowiedz')],
                       crumbs=kb_crumb + ([dict(label=L.t('wiedza.dzial.2.nazwa'), href=L.url('wiedza.akt'))] if dz == 2 else []),
                       crumb_here=title, updated=L.d.get(f'{k}.aktualizacja'), tabs=None,
                       body=Markup(blocks_html(L.d.get(f'{k}.tresc'))), legal=Markup(blocks_html(L.d.get(f'{k}.podstawa'))),
                       legal_title=L.t('wiedza.et.podstawa'), disclaimer=L.t('wiedza.zastrzezenie'),
                       band_h2=L.t('wiedza.et.cta.h2'), band_text=L.t('wiedza.et.cta.tekst'), og_type='article', jsonld=[art_ld])

        zas_crumbs = kb_crumb + [dict(label=L.t('wiedza.dzial.3.nazwa'), href=L.url('wiedza.zas'))]
        rows, cats, cities = fairs(L)
        render('zas.targi', 'fairs.html', section='wiedza', seo=(f"{L.t('zas.targi.tytul')} | GRUPO ERVOY", L.t('zas.targi.zapowiedz')),
               label=L.t('wiedza.dzial.3.nazwa'), h1=L.t('zas.targi.tytul'), leads=[L.t('zas.targi.wstep')],
               crumbs=zas_crumbs, crumb_here=L.t('zas.targi.tytul'), updated=L.d.get('zas.targi.aktualizacja'), tabs=None,
               fairs=rows, fair_cats=cats, fair_cities=cities, outro=L.d.get('zas.targi.przygotowanie'))
        groups, intro = glossary(L)
        render('zas.slownik', 'glossary.html', section='wiedza', seo=(f"{L.t('zas.slownik.tytul')} | GRUPO ERVOY", L.t('zas.slownik.zapowiedz')),
               label=L.t('wiedza.dzial.3.nazwa'), h1=L.t('zas.slownik.tytul'), leads=[re.sub('<[^>]+>', '', b['h']) for b in intro],
               crumbs=zas_crumbs, crumb_here=L.t('zas.slownik.tytul'), updated=L.d.get('zas.slownik.aktualizacja'), tabs=None,
               groups=groups, letters={g for g, _ in groups}, alphabet=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
               legal=Markup(blocks_html(L.d.get('zas.slownik.podstawa'))), legal_title=L.t('wiedza.et.podstawa'))

        # marki, o nas, kontakt, polityka
        render('marki', 'brands.html', section='marki', label=L.t('marki.label'), h1=L.t('marki.h1'), leads=[L.t('marki.lead')],
               crumbs=[], crumb_here='', updated=None, tabs=None,
               brands=[dict(name=L.t('marki.smb.nazwa'), text=L.t('marki.smb.tekst'), link=L.t('marki.smb.link'), img='smb-mx.png'),
                       dict(name=L.t('marki.polaca.nazwa'), text=L.t('marki.polaca.tekst'), link=L.t('marki.polaca.link'), img='polaca-foods.png')])
        about = ''.join([f"<p>{html.escape(L.t('onas.p2'))}</p>", f"<h2>{html.escape(L.t('onas.h2.monterrey'))}</h2>",
                         f"<p>{html.escape(L.t('onas.monterrey.p1'))}</p>", f"<h2>{html.escape(L.t('onas.h2.zasady'))}</h2>",
                         f"<p>{html.escape(L.t('onas.zasady.p1'))}</p>", f"<p>{html.escape(L.t('onas.zasady.p2'))}</p>"])
        render('onas', 'about.html', section='onas', label=L.t('onas.label'), h1=L.t('onas.h1'), leads=[L.t('onas.p1')],
               crumbs=[], crumb_here='', updated=None, tabs=None)
        people = []
        for p in ('kontakt.osoba1', 'kontakt.osoba2'):
            tel = L.t(p + '.telefon')
            people.append(dict(name=L.t(p + '.imie'), role=L.t(p + '.stanowisko'), langs=L.t(p + '.jezyki'), tel=tel, tel_raw='+' + digits(tel), email=L.t(p + '.email'),
                               wa=f"https://wa.me/{digits(tel)}?text={quote(L.t('cta.whatsapp.wiadomosc'))}"))
        render('kontakt', 'contact.html', section='kontakt', label=L.t('kontakt.label'), h1=L.t('kontakt.h1'), leads=[L.t('kontakt.lead')],
               crumbs=[], crumb_here='', updated=None, tabs=None, people=people,
               jsonld=[json.dumps(dict(org, employee=[{'@type': 'Person', 'name': x['name'], 'jobTitle': x['role'], 'email': x['email'],
                                                       'telephone': x['tel_raw']} for x in people]), ensure_ascii=False)])
        render('polityka', 'blocks.html', seo=(f"{ui['privacy_h1']} | GRUPO ERVOY", ui['privacy_h1']), label=None, h1=ui['privacy_h1'], leads=[],
               crumbs=[], crumb_here='', updated=None, tabs=None, body=Markup(f"<p>{html.escape(ui['privacy_pending'])}</p>"),
               legal=None, legal_title='', disclaimer=None, noindex=True)

        if code == DEFAULT:
            (OUT / '404.html').write_text(env.get_template('error.html').render(
                t=L.t, url=L.url, ui=ui, html_lang=HTML_LANG[code], og_locale=OG_LOCALE[code], site=SITE, seo_title=L.t('404.seo.tytul'),
                seo_desc=L.t('404.tekst'), og_title=L.t('404.seo.tytul'), og_desc=L.t('404.tekst'), canonical=SITE + '/404.html', alternates=[],
                og_type='website', noindex=True, nav=nav, section=None,
                lang_links=[dict(code=c, name=ui['lang_names'][c], flag=FLAGS[c], href=L.url('home', c), current=c == code) for c in LANGS],
                whatsapp=whatsapp, css_hash=css_hash, js_hash=js_hash, services=SERVICES, icon_wa=Markup(ICON_WA), jsonld=[],
                dark_header=False, no_band=True, band_h2=None, band_text=None), encoding='utf-8')

        if L.missing:
            print(f'[{code}] BRAK PÓL:', ', '.join(sorted(L.missing)))

    # sitemap i robots. lastmod zmienia się tylko, gdy zmieni się treść strony (odcisk w content/lastmod.json) -
    # Google ignoruje lastmod, jeśli przy każdym wydaniu wszystkie strony mają dzisiejszą datę.
    today = date.today().isoformat()
    lm_path = ROOT / 'content' / 'lastmod.json'
    lastmod = json.loads(lm_path.read_text(encoding='utf-8')) if lm_path.exists() else {}
    urls = []
    for key, code in pages_for_sitemap:
        if key == 'polityka':
            continue
        L = built[code]
        loc = SITE + L.url(key)
        page = (OUT / PREFIX[code] / ROUTES[key][code] / 'index.html').read_text(encoding='utf-8')
        page = re.sub(r'(style|site|map)\.[0-9a-f]{8}\.', '', page)
        digest = hashlib.sha256(page.encode('utf-8')).hexdigest()[:16]
        if lastmod.get(loc, [None])[0] != digest:
            lastmod[loc] = [digest, today]
        alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{HREFLANG[c]}" href="{SITE + L.url(key, c)}"/>' for c in LANGS if c in built)
        alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE + L.url(key, X_DEFAULT)}"/>'
        urls.append(f'<url><loc>{loc}</loc><lastmod>{lastmod[loc][1]}</lastmod>{alts}</url>')
    lm_path.write_text(json.dumps(dict(sorted(lastmod.items())), indent=0, ensure_ascii=False) + '\n', encoding='utf-8')
    (OUT / 'llms.txt').write_text(llms_txt(built), encoding='utf-8')
    (OUT / 'BingSiteAuth.xml').write_text(f'<?xml version="1.0"?>\n<users>\n\t<user>{BING_VERIFY}</user>\n</users>\n', encoding='utf-8')
    (OUT / f'{INDEXNOW_KEY}.txt').write_text(INDEXNOW_KEY, encoding='utf-8')
    (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                                     'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(urls) + '\n</urlset>\n', encoding='utf-8')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n', encoding='utf-8')
    print('zbudowano:', len(pages_for_sitemap), 'stron w', ', '.join(built))


if __name__ == '__main__':
    langs = [c for c in LANGS if (ROOT / 'content' / f'{c}.json').exists()]
    build(langs)
