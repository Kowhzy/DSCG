"""Décode un résultat JSON (download_file_content) en PDF, extrait le texte, rend les pages en PNG si scan."""
import json, base64, sys, pymupdf, os
src, out = sys.argv[1], sys.argv[2]           # out = chemin sans extension
data = json.load(open(src))
open(out + '.pdf', 'wb').write(base64.b64decode(data['content']))
d = pymupdf.open(out + '.pdf')
txt = '\n'.join(f'=== PAGE {i+1} ===\n' + p.get_text() for i, p in enumerate(d))
open(out + '.txt', 'w').write(txt)
n = sum(len(p.get_text().strip()) for p in d)
print(f'{out}: {d.page_count} pages, {n} caractères de texte')
if n < 300 * d.page_count:
    sp = sys.argv[3] if len(sys.argv) > 3 else '/tmp'
    for i, p in enumerate(d):
        p.get_pixmap(dpi=90).save(os.path.join(sp, os.path.basename(out) + f'_p{i+1}.png'))
    print('scan probable : pages rendues en PNG')
