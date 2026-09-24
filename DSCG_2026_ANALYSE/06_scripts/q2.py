import re,sys
L=[l.rstrip() for l in open(sys.argv[1])]
out=[];i=0
while i<len(L):
    s=L[i].strip()
    if re.match(r'^(DOSSIER|PARTIE|Dossier|Partie|SOUS-DOSSIER|Sous-dossier)\b',s) or re.match(r'^(Question\s*)?\d{1,2}(\.\d{1,2})*[\.\)]?(\s|$)',s):
        buf=s;j=i+1
        while j<len(L) and len(buf)<300 and L[j].strip() and not re.match(r'^(\d{1,2}(\.\d)*[\.\)]?\s|DOSSIER|PARTIE|Annexe|ANNEXE)',L[j].strip()):
            buf+=' '+L[j].strip(); j+=1
            if buf.endswith(('?','.')) and len(buf)>60: break
        if not re.match(r'^[\d\s,\.%€]+$',buf): out.append(buf[:300])
    i+=1
print('\n'.join(out))
