"""Czyta pliki Word z tekstami strony i zapisuje je jako JSON dla generatora.

Każdy fragment w pliku ma identyfikator w nawiasie kwadratowym, np. [home.hero.h1].
Pola .tresc i .podstawa zbierają kolejne akapity aż do następnego identyfikatora.
Akapity na tle (komentarze) i akapity zaczynające się od „UWAGA” są pomijane.
"""
import json
import re
import sys
from pathlib import Path

import docx
from docx.oxml.ns import qn

ID_RE = re.compile(r'^\[([a-z0-9_.\-]+)\]$', re.I)
MULTI = ('.tresc', '.podstawa')


def runs_html(p):
    out = []
    for r in p.runs:
        t = r.text.replace('\u000b', '\n')
        if not t:
            continue
        t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        out.append(f'<strong>{t}</strong>' if r.bold else t)
    return ''.join(out)


def is_comment(p):
    ppr = p._p.pPr
    return ppr is not None and ppr.find(qn('w:shd')) is not None


def parse(path):
    d = docx.Document(path)
    data = {}
    current = None
    for p in d.paragraphs:
        style = p.style.name
        text = p.text.replace('\u000b', '\n').strip()
        if not text or is_comment(p) or text.upper().startswith('UWAGA') or style == 'Title':
            continue
        if style in ('Heading 1', 'Heading 2') :
            current = None
            continue
        first, _, rest = text.partition('\n')
        m = ID_RE.match(first.strip())
        if m:
            key = m.group(1)
            current = key if key.endswith(MULTI) and not key.startswith('wiedza.') else None
            if current:
                data[key] = []
                if rest.strip():
                    data[key].append({'t': 'p', 'h': rest.strip()})
            else:
                data[key] = rest.strip()
            continue
        if current:
            blocks = data[current]
            if style == 'Heading 3':
                blocks.append({'t': 'h3', 'h': text})
            elif style == 'List Bullet':
                html = runs_html(p)
                if blocks and blocks[-1]['t'] == 'ul':
                    blocks[-1]['items'].append(html)
                else:
                    blocks.append({'t': 'ul', 'items': [html]})
            else:
                blocks.append({'t': 'p', 'h': runs_html(p)})
    return data


if __name__ == '__main__':
    lang, out, *files = sys.argv[1:]
    merged = {}
    for f in files:
        part = parse(f)
        dup = set(part) & set(merged)
        for k in dup:
            if part[k] != merged[k]:
                print(f'UWAGA: {k} różni się między plikami, biorę wersję z {Path(f).name}')
        merged.update(part)
    Path(out).write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding='utf-8')
    print(lang, len(merged), 'pól')
