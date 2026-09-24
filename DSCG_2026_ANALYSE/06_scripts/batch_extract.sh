#!/bin/bash
# usage: batch_extract.sh ID_RESULTAT... ; nomme d'après le titre Drive (UEx_AAAA_corrige[_Sn] / _sujet)
T=/root/.claude/projects/-home-user-DSCG/4d993102-1692-54ff-91c9-6db77d86df0f/tool-results
S=/tmp/claude-0/-home-user-DSCG/4d993102-1692-54ff-91c9-6db77d86df0f/scratchpad/cor; mkdir -p $S
cd "$(dirname "$0")/.."
for f in "$@"; do
  t=$(jq -r .title $T/mcp-Google_Drive-download_file_content-$f.txt)
  n=$(python3 -c "
import re,sys; t=sys.argv[1]
m=re.search(r'UE ?(\d).*?(\d{4})',t); k='corrige' if re.search('orr',t,re.I) else 'sujet'
s=re.search(r'Sujet (\d)',t); print(f'UE{m.group(1)}_{m.group(2)}_{k}'+(f'_S{s.group(1)}' if s else ''))" "$t")
  echo "$t -> $n"; python3 06_scripts/extract_pdf.py $T/mcp-Google_Drive-download_file_content-$f.txt "01_annales/corriges/$n" $S
done
