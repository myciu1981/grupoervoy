"""Mapa w hero: korytarz Europa–Meksyk jako jedno skalowalne SVG.

Odwzorowanie Robinsona (λ0 = −40°) na danych Natural Earth 50m. Układ współrzędnych
SVG to 1440 × 740, ten sam co w zatwierdzonym prototypie A z kanwy.
"""
import json
import math
import re
from pathlib import Path

lat_t = list(range(0, 91, 5))
Xt = [1, .9986, .9954, .99, .9822, .973, .96, .9427, .9216, .8962, .8679, .835, .7986, .7597, .7186, .6732, .6213, .5722, .5322]
Yt = [0, .062, .124, .186, .248, .31, .372, .434, .4958, .5571, .6176, .6769, .7346, .7903, .8435, .8936, .9394, .9761, 1]
LON0 = -40.0
W, H = 1440, 740


def interp(x, xs, ys):
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            t = (x - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + t * (ys[i + 1] - ys[i])
    return ys[-1]


def rob(lon, lat):
    X = interp(abs(lat), lat_t, Xt)
    Y = math.copysign(interp(abs(lat), lat_t, Yt), lat)
    return X * (lon - LON0), -1.3523 * Y * 180 / math.pi / 0.8487


S = 9.3
_mx = rob(-101, 23)
LEFT = _mx[0] - 0.175 * W / S
TOP = _mx[1] - 0.70 * H / S


def LL(lon, lat):
    x, y = rob(lon, lat)
    return ((x - LEFT) * S, (y - TOP) * S)


def simplify(pts, mind):
    out = [pts[0]]
    for p in pts[1:]:
        if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) >= mind:
            out.append(p)
    return out


def rings_d(rings, mind=1.0, pad=40):
    ds = []
    for ring in rings:
        q = [LL(lo, la) for lo, la in ring]
        xs = [p[0] for p in q]
        ys = [p[1] for p in q]
        if max(xs) < -pad or min(xs) > W + pad or max(ys) < -pad or min(ys) > H + pad:
            continue
        q = simplify(q, mind)
        if len(q) < 3:
            continue
        ds.append('M' + ' '.join(f'{x:.1f} {y:.1f}' for x, y in q) + 'Z')
    return ''.join(ds)


def catmull(pts, n=10):
    P_ = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(P_) - 2):
        p0, p1, p2, p3 = P_[i - 1], P_[i], P_[i + 1], P_[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def lane(wps, n=10):
    pts = catmull([LL(*w) for w in wps], n)
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    length = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
    return d, length


def dms(lon, lat):
    def f(v, pos, neg):
        a = abs(v)
        d = int(a)
        m = round((a - d) * 60)
        return f"{d}°{m:02d}′{pos if v >= 0 else neg}"
    return f(lat, 'N', 'S') + ' ' + f(lon, 'E', 'W')


NAMES = {
    'pl': dict(gdy='Gdynia', ham='Hamburg', rot='Rotterdam', val='Walencja', mty='Monterrey', cdmx='Meksyk', cdmx_meta='stolica kraju',
               alt='Altamira', ver='Veracruz', hq='Siedziba GRUPO ERVOY', atl='Ocean Atlantycki', title='Mapa tras morskich z Gdyni i Walencji do Veracruz oraz połączeń lądowych do miasta Meksyk i Monterrey'),
    'es': dict(cdmx_m='CDMX', gdy='Gdynia', ham='Hamburgo', rot='Róterdam', val='Valencia', mty='Monterrey', cdmx='Ciudad de México', cdmx_meta='',
               alt='Altamira', ver='Veracruz', hq='Sede de GRUPO ERVOY', atl='Océano Atlántico', title='Mapa de las rutas marítimas de Gdynia y Valencia a Veracruz y de las conexiones terrestres a Ciudad de México y Monterrey'),
    'en': dict(gdy='Gdynia', ham='Hamburg', rot='Rotterdam', val='Valencia', mty='Monterrey', cdmx='Mexico City', cdmx_meta='',
               alt='Altamira', ver='Veracruz', hq='GRUPO ERVOY headquarters', atl='Atlantic Ocean', title='Map of sea routes from Gdynia and Valencia to Veracruz and overland links to Mexico City and Monterrey'),
}

GDY, VAL, VER, ALT = (18.53, 54.52), (-0.33, 39.45), (-96.13, 19.2), (-97.86, 22.4)
MTY, CDMX = (-100.31, 25.67), (-99.13, 19.43)
MAIN = [GDY, (17.0, 55.0), (14.0, 54.85), (11.6, 54.55), (10.2, 54.4), (9.15, 53.9), (7.6, 54.0), (5.6, 53.6),
        (3.4, 52.4), (1.7, 51.15), (-1.5, 50.1), (-5.6, 49.3), (-12, 46.6), (-25, 40.6), (-40, 33.6), (-55, 28.2),
        (-68, 25.8), (-76.5, 25.6), (-80.2, 24.15), (-83.5, 23.9), (-88, 23.2), (-92.5, 21.0), (-95.2, 19.6), VER]
VALW = [VAL, (-0.3, 38.4), (-1.4, 37.4), (-2.6, 36.5), (-5.6, 35.95), (-9.6, 35.4), (-20, 33.2), (-40, 29.8), (-55, 28.2)]
HAMW = [(9.97, 53.55), (9.0, 53.85), (7.6, 54.0)]
ROTW = [(4.1, 51.95), (3.2, 51.75), (1.7, 51.15)]
ALTW = [(-88, 23.2), (-93.5, 23.1), (-96.5, 22.6), ALT]
INLAND = [VER, (-97.0, 18.95), (-98.2, 19.04), CDMX, (-99.8, 20.0), (-100.39, 20.59), (-100.98, 22.15), (-101.0, 25.42), MTY]

_cache = {}


def _geometry(geo_path):
    if 'g' in _cache:
        return _cache['g']
    feats = json.loads(Path(geo_path).read_text(encoding='utf-8'))['features']
    countries = {}
    for f in feats:
        g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        countries.setdefault(f['properties']['ADM0_A3'], []).extend(p[0] for p in polys)
    eu_set = {'DEU', 'NLD', 'BEL', 'ESP'}
    hi_set = {'MEX', 'POL'}
    land, eu, hi = [], [], []
    for code, rings in countries.items():
        d = rings_d(rings)
        if d:
            (hi if code in hi_set else eu if code in eu_set else land).append(d)
    grat = ''.join('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in [LL(lo, la) for lo in range(-140, 61, 2)]) for la in range(0, 81, 15))
    grat += ''.join('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in [LL(lo, la) for la in range(-10, 85, 1)]) for lo in range(-135, 61, 15))
    _cache['g'] = (''.join(land), ''.join(eu), ''.join(hi), grat)
    return _cache['g']


def _rel(d):
    """Ścieżka 'M x y x y ... Z' / 'M x y L x y' na względne 'l' w dziesiątych częściach piksela -
    ten sam kształt co do 0,1 px, plik o ok. 40% mniejszy."""
    out = []
    for sub in re.findall(r'M[^M]+', d):
        closed = sub.rstrip().endswith('Z')
        nums = [round(float(v) * 10) for v in re.findall(r'-?\d+(?:\.\d+)?', sub)]
        pts = list(zip(nums[0::2], nums[1::2]))
        f = lambda v: (f'{v / 10:.1f}'.rstrip('0').rstrip('.') or '0')  # noqa: E731
        seg = [f'M{f(pts[0][0])} {f(pts[0][1])}l']
        seg.append(' '.join(f'{f(x - px)} {f(y - py)}' for (px, py), (x, y) in zip(pts, pts[1:])))
        out.append(''.join(seg) + ('z' if closed else ''))
    return ''.join(out)


def map_svg(geo_path):
    """Podkład mapy (siatka i lądy) jako osobny plik - wspólny dla wszystkich języków, cache'owany
    przez przeglądarkę. Kolory jako atrybuty, bez <style>, żeby nie zależeć od CSP."""
    land, eu, hi, grat = _geometry(geo_path)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
            f'<path fill="none" stroke="#b8c0c7" stroke-opacity=".075" d="{_rel(grat)}"/>'
            f'<g stroke="#0a263c" stroke-width=".8" stroke-linejoin="round">'
            f'<path fill="#11324d" d="{_rel(land)}"/><path fill="#173d5b" d="{_rel(eu)}"/></g>'
            f'<path fill="#1b4868" stroke="#e9edf0" stroke-opacity=".28" stroke-linejoin="round" d="{_rel(hi)}"/></svg>')


CYCLE, START = 15, 3.2


def render(lang, geo_path, map_href):
    N = NAMES[lang]
    i55 = MAIN.index((-55, 28.2))
    d_main, L_main = lane(MAIN)
    d_val, L_val = lane(VALW)
    d_valfull, _ = lane(VALW + MAIN[i55 + 1:])
    d_ham, L_ham = lane(HAMW)
    d_rot, L_rot = lane(ROTW)
    d_alt, L_alt = lane(ALTW)
    d_amb_ham, _ = lane(HAMW + MAIN[MAIN.index((5.6, 53.6)):])
    d_amb_rot, _ = lane(ROTW + MAIN[MAIN.index((1.7, 51.15)) + 1:])
    d_in, L_in = lane(INLAND, 8)
    d_gdl, L_gdl = lane([(-100.39, 20.59), (-101.7, 21.0), (-103.35, 20.67)], 8)
    d_altin, L_altin = lane([ALT, (-99.13, 23.74), MTY], 8)

    gx, gy = LL(*GDY)
    hx, hy = LL(9.97, 53.55)
    rx, ry = LL(4.1, 51.95)
    vx, vy = LL(*VAL)
    ver, alt, mty, cdmx, gdl = LL(*VER), LL(*ALT), LL(*MTY), LL(*CDMX), LL(-103.35, 20.67)
    ax, ay = LL(-45, 41.5)

    def port(x, y):
        return f'<rect class="m-port" x="{x - 4:.1f}" y="{y - 4:.1f}" width="8" height="8"/>'

    def label(x, y, name, meta='', anchor='start'):
        a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
        out = f'<text class="m-name" x="{x:.1f}" y="{y:.1f}"{a}>{name}</text>'
        if meta:
            out += f'<text class="m-meta" x="{x:.1f}" y="{y + 17:.1f}"{a}>{meta}</text>'
        return out

    def draw(cls, d, L, extra=''):
        return f'<path class="{cls} drw{extra}" style="--len:{L + 2:.0f}" d="{d}"/>'

    cdmx_meta = N['cdmx_meta']
    labels = ''.join([
        label(gx - 40, gy - 32, N['gdy'], dms(*GDY)),
        label(hx - 10, hy - 14, N['ham'], anchor='end'),
        label(rx - 12, ry + 10, N['rot'], anchor='end'),
        label(vx + 12, vy - 4, N['val'], dms(*VAL)),
        label(mty[0] - 14, mty[1] - 4, N['mty'], N['hq'], anchor='end'),
        label(cdmx[0] - 14, cdmx[1] + (-4 if cdmx_meta else 5), N['cdmx'], cdmx_meta, anchor='end'),
        label(alt[0] + 10, alt[1] - 12, N['alt']),
        label(ver[0] + 12, ver[1] + 18, N['ver'], dms(*VER)),
    ])
    def mlabel(x, y, name, anchor='start', cls='m-name'):
        a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
        return f'<text class="{cls}" x="{x:.0f}" y="{y:.0f}"{a}>{name}</text>'

    # telefon: mapa przycięta do x 60-1380, y 130-680 (kadr w style.css), nazwy ok. 3 razy większe
    labels_m = ''.join([
        mlabel(gx + 6, gy + 54, N['gdy'], 'middle'),
        mlabel(vx + 14, vy + 46, N['val']),
        mlabel(mty[0] - 30, mty[1] - 28, N['mty'], 'middle'),
        mlabel(ver[0] + 26, ver[1] + 14, N['ver']),
        mlabel(cdmx[0] - 44, cdmx[1] + 88, N.get('cdmx_m', N['cdmx'])),
        mlabel(cdmx[0] - 44, cdmx[1] + 119, cdmx_meta, 'start', 'm-meta') if cdmx_meta else '',
    ])
    svg = f'''<svg class="hero-map" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{N['title']}">
<image href="{map_href}" width="{W}" height="{H}"/>
{draw('m-lane', d_ham, L_ham, ' d1')}{draw('m-lane', d_rot, L_rot, ' d2')}{draw('m-lane', d_alt, L_alt, ' d4')}
{draw('m-lane m-mx', d_in, L_in, ' inl')}{draw('m-lane m-mx', d_gdl, L_gdl, ' inl')}{draw('m-lane m-mx', d_altin, L_altin, ' inl')}
{draw('m-halo', d_val, L_val, ' v')}{draw('m-halo', d_main, L_main)}{draw('m-route', d_val, L_val, ' v')}{draw('m-route', d_main, L_main)}
<path id="p-main" d="{d_main}" fill="none"/><path id="p-val" d="{d_valfull}" fill="none"/><path id="p-in" d="{d_in}" fill="none"/>
<path id="p-ham" d="{d_amb_ham}" fill="none"/><path id="p-rot" d="{d_amb_rot}" fill="none"/>
<text class="m-sea" x="{ax:.1f}" y="{ay:.1f}" text-anchor="middle">{N['atl']}</text>
{''.join(port(*p) for p in [(gx, gy), (hx, hy), (rx, ry), (vx, vy), ver, alt])}
<circle class="m-small" cx="{gdl[0]:.1f}" cy="{gdl[1]:.1f}" r="2.5"/>
<circle class="m-cap" cx="{cdmx[0]:.1f}" cy="{cdmx[1]:.1f}" r="5"/>
<circle class="m-ring" cx="{mty[0]:.1f}" cy="{mty[1]:.1f}" r="6"/>
<circle class="m-hq" cx="{mty[0]:.1f}" cy="{mty[1]:.1f}" r="6"/>
<g class="m-lbl-d">{labels}</g>
<g class="m-lbl-m" aria-hidden="true">{labels_m}</g>
<g class="m-movers" aria-hidden="true">
<rect class="mv-amb" x="-2.5" y="-2.5" width="5" height="5"><animateMotion dur="34s" begin="2s" repeatCount="indefinite"><mpath href="#p-ham"/></animateMotion></rect>
<rect class="mv-amb" x="-2.5" y="-2.5" width="5" height="5"><animateMotion dur="31s" begin="9s" repeatCount="indefinite"><mpath href="#p-rot"/></animateMotion></rect>
<rect class="mv-main" x="-4.5" y="-4.5" width="9" height="9"><animateMotion dur="{CYCLE}s" begin="{START}s" repeatCount="indefinite" calcMode="spline" keyPoints="0;0;1;1" keyTimes="0;0.08;0.62;1" keySplines="0 0 1 1;.5 0 .5 1;0 0 1 1"><mpath href="#p-main"/></animateMotion></rect>
<rect class="mv-main mv-v" x="-3.5" y="-3.5" width="7" height="7"><animateMotion dur="{CYCLE}s" begin="{START + CYCLE / 2:.1f}s" repeatCount="indefinite" calcMode="spline" keyPoints="0;0;1;1" keyTimes="0;0.08;0.62;1" keySplines="0 0 1 1;.5 0 .5 1;0 0 1 1"><mpath href="#p-val"/></animateMotion></rect>
<rect class="mv-main mv-in" x="-3.5" y="-3.5" width="7" height="7"><animateMotion dur="{CYCLE}s" begin="{START}s" repeatCount="indefinite" calcMode="spline" keyPoints="0;0;1;1" keyTimes="0;0.63;0.78;1" keySplines="0 0 1 1;.5 0 .5 1;0 0 1 1"><mpath href="#p-in"/></animateMotion></rect>
</g>
</svg>'''
    return svg


CSS = f'''
.hero-map{{display:block;width:100%;height:100%}}
.m-grat{{fill:none;stroke:rgba(184,192,199,.075);stroke-width:1}}
.m-land{{fill:#11324d;stroke:#0a263c;stroke-width:.8;stroke-linejoin:round}}
.m-eu{{fill:#173d5b}}
.m-hi{{fill:#1b4868;stroke:rgba(233,237,240,.28);stroke-width:1}}
.m-lane{{fill:none;stroke:rgba(255,255,255,.30);stroke-width:1.2;stroke-linecap:round;stroke-linejoin:round}}
.m-mx{{stroke:rgba(255,255,255,.45);stroke-width:1.6}}
.m-halo{{fill:none;stroke:#fff;stroke-opacity:.92;stroke-width:3.8;stroke-linecap:round;stroke-linejoin:round}}
.m-route{{fill:none;stroke:#9f384b;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.m-port{{fill:#fff;stroke:#0a263c;stroke-width:2;paint-order:stroke}}
.m-small{{fill:#b8c0c7}}
.m-cap{{fill:#9f384b;stroke:#fff;stroke-width:2}}
.m-hq{{fill:#9f384b;stroke:#fff;stroke-width:2}}
.m-ring{{fill:none;stroke:#fff;stroke-width:1.5;opacity:0;transform-box:fill-box;transform-origin:center}}
.m-name{{font-family:'Red Hat Display',Arial,sans-serif;font-weight:500;font-size:14px;fill:#fff;paint-order:stroke;stroke:#0a263c;stroke-width:3px;stroke-linejoin:round}}
.m-meta{{font-family:'Red Hat Text',Arial,sans-serif;font-size:12px;fill:#b8c0c7;font-variant-numeric:tabular-nums;paint-order:stroke;stroke:#0a263c;stroke-width:3px;stroke-linejoin:round}}
.m-sea{{font-family:'Red Hat Text',Arial,sans-serif;font-size:13px;letter-spacing:2px;fill:rgba(184,192,199,.55)}}
.mv-amb{{fill:#fff;opacity:.75}}
.mv-main{{fill:#fff;stroke:#9f384b;stroke-width:2;paint-order:stroke}}
@keyframes m-draw{{from{{stroke-dashoffset:var(--len)}}to{{stroke-dashoffset:0}}}}
@keyframes m-fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes m-ring{{0%{{transform:scale(1);opacity:.9}}100%{{transform:scale(3.2);opacity:0}}}}
@media (prefers-reduced-motion:no-preference){{
 .drw{{stroke-dasharray:var(--len) var(--len);animation:m-draw 2.4s cubic-bezier(.45,0,.25,1) both}}
 .m-halo.drw,.m-route.drw{{animation-duration:2.8s;animation-delay:.6s}}
 .m-halo.v,.m-route.v{{animation-delay:1.1s;animation-duration:1.6s}}
 .d1{{animation-delay:.2s}}.d2{{animation-delay:.4s}}.d4{{animation-delay:2.6s;animation-duration:1s}}
 .inl{{animation-delay:3s;animation-duration:1.4s}}
 .m-name,.m-meta,.m-port,.m-cap,.m-hq{{animation:m-fade .6s ease-out 1.6s both}}
 .m-ring{{animation:m-ring 3.2s ease-out 4s infinite}}
}}
@media (prefers-reduced-motion:reduce){{.m-movers{{display:none}}}}
.m-lbl-m{{display:none}}
@media (max-width:1099px){{
 .m-lbl-d,.m-sea{{display:none}}
 .m-lbl-m{{display:inline}}
 .m-lbl-m .m-name{{font-size:20px;stroke-width:5px}}
 .m-lbl-m .m-meta{{font-size:15px;stroke-width:4px}}
 .m-port,.m-cap,.m-hq,.m-small,.mv-main,.mv-amb{{transform-box:fill-box;transform-origin:center;transform:scale(1.4)}}
 .m-halo{{stroke-width:5.5}}.m-route{{stroke-width:2.8}}.m-lane{{stroke-width:1.8}}.m-mx{{stroke-width:2.4}}
}}
@media (max-width:899px){{
 .m-lbl-m .m-name{{font-size:26px;stroke-width:6px}}
 .m-lbl-m .m-meta{{font-size:19px;stroke-width:5px}}
 .m-port,.m-cap,.m-hq,.m-small,.mv-main,.mv-amb{{transform:scale(1.8)}}
 .m-halo{{stroke-width:7}}.m-route{{stroke-width:3.6}}.m-lane{{stroke-width:2.4}}.m-mx{{stroke-width:3}}
}}
@media (max-width:599px){{
 .m-lbl-m .m-name{{font-size:40px;stroke-width:9px}}
 .m-lbl-m .m-meta{{font-size:27px;stroke-width:7px}}
 .m-port,.m-cap,.m-hq,.m-small,.mv-main,.mv-amb{{transform:scale(2.3)}}
 .m-halo{{stroke-width:9}}.m-route{{stroke-width:4.6}}.m-lane{{stroke-width:3}}.m-mx{{stroke-width:3.8}}
 .m-ring{{animation-name:m-ring-m}}
}}
@keyframes m-ring-m{{0%{{transform:scale(2.3);opacity:.9}}100%{{transform:scale(5.5);opacity:0}}}}
'''


def panel_css(rows):
    """Kroki panelu zapalają się w rytm statku (te same CYCLE i START co SMIL)."""
    out = []
    for i, t in enumerate(rows):
        out.append(f"@keyframes pr{i}{{0%,{t}%{{color:#b8c0c7}}{t + 1}%,93%{{color:#fff}}99%,100%{{color:#b8c0c7}}}}"
                   f"@keyframes ps{i}{{0%,{t}%{{background:transparent;border-color:#6b7681}}{t + 1}%,93%{{background:#fff;border-color:#fff}}99%,100%{{background:transparent;border-color:#6b7681}}}}"
                   f"@media (prefers-reduced-motion:no-preference){{.pr{i}{{animation:pr{i} {CYCLE}s linear {START}s infinite}}.pr{i} .sq{{animation:ps{i} {CYCLE}s linear {START}s infinite}}}}")
    return ''.join(out)


PANEL_TIMES = [3, 7, 11, 63, 74]
