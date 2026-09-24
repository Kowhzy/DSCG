import re,sys
t=open(sys.argv[1]).read().split('\n')
pat=re.compile(r'^\s*((\d{1,2}[\.\)-]\s*(\d{1,2}[\.\)]?)?\s*\S)|(DOSSIER|Dossier|PARTIE|Partie|Travail|TRAVAIL|Question)|.*\bpoints?\b)')
out=[]
for i,l in enumerate(t):
    if pat.match(l) and len(l.strip())>3:
        # join continuation line
        nxt=t[i+1].strip() if i+1<len(t) else ''
        s=l.strip()
        if not s.endswith(('?','.',')')) and nxt and not pat.match(t[i+1]): s+=' '+nxt
        out.append(s[:260])
print('\n'.join(out))
