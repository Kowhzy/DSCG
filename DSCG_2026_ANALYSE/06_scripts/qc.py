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
    att = list(csv.DictReader(open(f'02_data/{ue}_attendus_corriges.csv', encoding='utf-8'), delimiter=';'))
    import re
    norm = lambda x: re.sub(r'\s+', '', x)
    ntxt = norm(txt)
    att_miss = [f"{a['annee']} D{a['dossier']}" for a in att if norm(a['question'])[:25] not in ntxt]
    for k in ('5.5 Robustesse', '5.6 Les techniques', '10.2 Ce qu', '10.3 Corrigés'):
        if k not in txt: print('  section manquante :', k); ok = False
    if att_miss: print('  attendus absents :', att_miss); ok = False
    print(f"{ue}: {d.page_count} p., {len(rows)} rubriques, IPR absents du texte: {miss}, liens: {links}, signets: {len(toc)}, pages quasi vides: {low}")
    ok &= not miss and not low
sys.exit(0 if ok else 1)
