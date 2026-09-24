"""Exporte les observations du jury et la correspondance cours en CSV (03_analyses)."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from referentiel import JURY, COURS, RUBRIQUES
B = os.path.join(os.path.dirname(__file__), '..', '03_analyses')
for ue in JURY:
    with open(os.path.join(B, f'{ue}_jury.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';'); w.writerow(['annee', 'page', 'observation', 'rubriques', 'probleme_candidats', 'consequence_revision'])
        for r in JURY[ue]: w.writerow([r[0], r[1], r[2], r[3], 'oui' if r[4] else 'non', r[5]])
    with open(os.path.join(B, f'{ue}_correspondance_cours.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';'); w.writerow(['rubrique', 'partie', 'intitule_officiel', 'support_cours', 'statut_declare_notion'])
        for c, pa, t, n, b in RUBRIQUES[ue]:
            cs, stt = COURS[ue].get(c, ('', '')); w.writerow([c, pa, t, cs, stt])
print('ok')
