"""Contrôle qualité : cohérence PDF ↔ 03_analyses, liens, pages peu remplies."""
import csv, pymupdf, sys
ok = True
for ue in ('UE2', 'UE3', 'UE5'):
    d = pymupdf.open(f'05_rapports/DSCG_2026_{ue}.pdf')
    txt = ' '.join(p.get_text() for p in d).replace('\n', ' ')
    rows = list(csv.DictReader(open(f'03_analyses/{ue}_stats.csv', encoding='utf-8'), delimiter=';'))
    miss = [r['rubrique'] for r in rows if f"IPR {r['IPR'].replace('.', ',')}" not in txt]
    links = sum(1 for p in d for l in p.get_links() if l.get('uri'))
    toc = d.get_toc()
    low = [i + 1 for i, p in enumerate(d) if len(p.get_text()) < 300 and not p.get_images()]
    print(f"{ue}: {d.page_count} p., {len(rows)} rubriques, IPR absents du texte: {miss}, liens: {links}, signets: {len(toc)}, pages quasi vides: {low}")
    ok &= not miss and not low
sys.exit(0 if ok else 1)
