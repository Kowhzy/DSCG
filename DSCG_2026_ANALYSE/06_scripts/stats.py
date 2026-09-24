"""Calcule les statistiques par rubrique officielle et l'Indice de Priorité de Révision (IPR).
Entrées : 02_data/UE*_dossiers.csv, referentiel.py. Sorties : 03_analyses/UE*_stats.csv, 03_analyses/UE*_matrice.csv"""
import csv, os, sys, json
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from referentiel import RUBRIQUES, JURY

BASE = os.path.join(os.path.dirname(__file__), '..')
YEARS = list(range(2016, 2026))
CUR = [y for y in YEARS if y >= 2020]           # programme actuel (arrêté 2019, 1re session 2020)
LAST5 = [y for y in YEARS if y >= 2021]
LAST3 = [y for y in YEARS if y >= 2023]

# Pondérations de l'IPR (somme = 100) — voir méthodologie
W = dict(f_hist=15, f_cur=20, f_rec=10, poids=10, jury=15, diff=10, transv=10, bo=5, gap=5)

def year_of(a):
    return int(str(a)[:4])

def load(ue):
    rows = list(csv.DictReader(open(os.path.join(BASE, '02_data', f'{ue}_dossiers.csv'), encoding='utf-8'), delimiter=';'))
    # poids de sujet : 2022-S1 / 2022-S2 (UE2) = 0,5 chacun (lequel a été composé : non vérifié)
    subj = defaultdict(set)
    for r in rows:
        subj[year_of(r['annee'])].add(r['annee'])
    for r in rows:
        y = year_of(r['annee']); r['y'] = y
        r['w_subject'] = 1 / len(subj[y])
        r['P'] = [c for c in r['rubriques_principales'].split('|') if c]
        r['S'] = [c for c in r['rubriques_secondaires'].split('|') if c]
    # part des points de chaque dossier dans son sujet
    by_subject = defaultdict(list)
    for r in rows:
        by_subject[r['annee']].append(r)
    for a, rs in by_subject.items():
        if all(r['points'] and r['total_points'] for r in rs):
            for r in rs: r['share'] = float(r['points']) / float(r['total_points'])
        else:  # points inconnus (UE3 2024) : parties d'égale importance selon le jury
            for r in rs: r['share'] = 1 / len(rs)
    return rows

def compute(ue):
    rows = load(ue)
    codes = [c for c, *_ in RUBRIQUES[ue]]
    sessP = {c: defaultdict(float) for c in codes}   # présence (0..1) par année, en principal
    sessA = {c: defaultdict(float) for c in codes}   # présence principal ou secondaire
    weight = {c: defaultdict(float) for c in codes}  # part du barème attribuée
    ndos = defaultdict(int); cooc = defaultdict(set); dossiers = defaultdict(list)
    for r in rows:
        y, w = r['y'], r['w_subject']
        for c in set(r['P']):
            sessP[c][y] = min(1.0, sessP[c][y] + w) if sessP[c][y] < w * 2 else sessP[c][y]
            weight[c][y] += w * r['share'] / len(r['P'])
            ndos[c] += 1
            dossiers[c].append(f"{r['annee']} D{r['dossier']}")
        for c in set(r['P']) | set(r['S']):
            sessA[c][y] = max(sessA[c][y], w) if y in sessA[c] else w
            if y >= 2020:
                cooc[c] |= (set(r['P']) | set(r['S'])) - {c}
    # correction : présence par année = somme des poids de sujets où la rubrique apparaît (max 1)
    for c in codes:
        for y in YEARS:
            s = sum(r['w_subject'] for r in {id(r): r for r in rows}.values() if r['y'] == y and c in r['P'])
            # une rubrique présente dans 2 dossiers du même sujet ne compte qu'une fois : dédoublonnage par sujet
            subjects = {r['annee']: r['w_subject'] for r in rows if r['y'] == y and c in r['P']}
            sessP[c][y] = min(1.0, sum(subjects.values()))
            subjectsA = {r['annee']: r['w_subject'] for r in rows if r['y'] == y and (c in r['P'] or c in r['S'])}
            sessA[c][y] = min(1.0, sum(subjectsA.values()))
    jury_years = defaultdict(set); diff = defaultdict(int); jury_txt = defaultdict(list)
    for (an, page, obs, rub, pb, cons) in JURY[ue]:
        for c in [x for x in rub.split('|') if x]:
            jury_years[c].add(an); jury_txt[c].append((an, page, obs, pb, cons))
            if pb: diff[c] += 1
    bo = {c: b for c, _, _, _, b in RUBRIQUES[ue]}
    res = []
    maxco = max((len(cooc[c]) for c in codes), default=1) or 1
    maxj = max((len(jury_years[c]) for c in codes), default=1) or 1
    maxd = max((diff[c] for c in codes), default=1) or 1
    for c, partie, titre, notions, b in RUBRIQUES[ue]:
        f10 = sum(sessP[c][y] for y in YEARS) / len(YEARS)
        fcur = sum(sessP[c][y] for y in CUR) / len(CUR)
        f5 = sum(sessP[c][y] for y in LAST5) / len(LAST5)
        f3 = sum(sessP[c][y] for y in LAST3) / len(LAST3)
        fa_cur = sum(sessA[c][y] for y in CUR) / len(CUR)
        present = [y for y in YEARS if sessP[c][y] > 0]
        last = max(present) if present else None
        presentA = [y for y in YEARS if sessA[c][y] > 0]
        lastA = max(presentA) if presentA else None
        w_cur = sum(weight[c][y] for y in CUR) / len(CUR)          # poids moyen par session (programme actuel)
        n_cur = sum(1 for y in CUR if sessP[c][y] > 0)
        w_when = (sum(weight[c][y] for y in CUR) / sum(sessP[c][y] for y in CUR)) if n_cur else 0
        gap = 1.0 if (last is None or last <= 2022) else 0.0  # absent des 3 dernières sessions
        bo_n = (b / max(x[4] for x in RUBRIQUES[ue])) if b else 0.5
        comp = dict(f_hist=f10, f_cur=fcur, f_rec=f3, poids=min(1.0, w_when / 0.5), jury=len(jury_years[c]) / maxj,
                    diff=diff[c] / maxd, transv=len(cooc[c]) / maxco, bo=bo_n, gap=gap)
        ipr = sum(W[k] * comp[k] for k in W)
        res.append(dict(code=c, partie=partie, titre=titre, notions=notions,
            sessions_10=round(sum(sessP[c][y] for y in YEARS), 1), sessions_cur=round(sum(sessP[c][y] for y in CUR), 1),
            f10=f10, fcur=fcur, f5=f5, f3=f3, fa_cur=fa_cur, n_dossiers=ndos[c], last=last, lastA=lastA,
            since=(2026 - last) if last else None, w_cur=w_cur, w_when=w_when, jury_n=len(jury_years[c]), diff_n=diff[c],
            transv=len(cooc[c]), gap=gap, ipr=ipr, dossiers=dossiers[c],
            years={y: sessP[c][y] for y in YEARS}, yearsA={y: sessA[c][y] for y in YEARS}, jury=jury_txt[c], comp=comp))
    # catégories (seuils fixes sur l'IPR + règle jury 2025)
    for r in res:
        s = r['ipr']
        cat = 'PRIORITÉ MAXIMALE' if s >= 60 else 'PRIORITÉ TRÈS ÉLEVÉE' if s >= 45 else 'PRIORITÉ ÉLEVÉE' if s >= 32 else 'À MAÎTRISER' if s >= 20 else 'COMPLÉMENT'
        # règle : une rubrique explicitement signalée comme faiblesse par le jury 2025 ne descend pas sous « très élevée »
        j25 = any(an == 2025 and pb for an, _, _, pb, _ in r['jury'])
        if j25 and cat in ('PRIORITÉ ÉLEVÉE', 'À MAÎTRISER', 'COMPLÉMENT'):
            cat = 'PRIORITÉ TRÈS ÉLEVÉE'; r['regle'] = 'relevée par la règle « faiblesse signalée par le jury 2025 »'
        r['cat'] = cat
    return rows, res

def write(ue, rows, res):
    out = os.path.join(BASE, '03_analyses')
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, f'{ue}_stats.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['rubrique', 'partie', 'intitule', 'sessions_2016_2025', 'freq_10', 'sessions_2020_2025', 'freq_prog_actuel',
                    'freq_5_dernieres', 'freq_3_dernieres', 'freq_avec_transversal_2020_2025', 'nb_dossiers', 'derniere_apparition',
                    'annees_depuis', 'poids_moyen_par_session_2020_2025', 'poids_moyen_quand_present', 'nb_annees_jury',
                    'nb_difficultes_jury', 'transversalite', 'IPR', 'categorie', 'dossiers'])
        for r in sorted(res, key=lambda r: -r['ipr']):
            w.writerow([r['code'], r['partie'], r['titre'], r['sessions_10'], f"{r['f10']:.2f}", r['sessions_cur'], f"{r['fcur']:.2f}",
                        f"{r['f5']:.2f}", f"{r['f3']:.2f}", f"{r['fa_cur']:.2f}", r['n_dossiers'], r['last'] or '', r['since'] or '',
                        f"{r['w_cur']:.3f}", f"{r['w_when']:.3f}", r['jury_n'], r['diff_n'], r['transv'], f"{r['ipr']:.1f}", r['cat'],
                        ', '.join(r['dossiers'])])
    with open(os.path.join(out, f'{ue}_matrice.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['rubrique'] + YEARS)
        for r in res:
            w.writerow([r['code']] + [('P' if r['years'][y] >= 1 else 'P½' if r['years'][y] > 0 else 's' if r['yearsA'][y] > 0 else '') for y in YEARS])

if __name__ == '__main__':
    for ue in ('UE2', 'UE3', 'UE5'):
        rows, res = compute(ue)
        write(ue, rows, res)
        print(ue, len(rows), 'dossiers')
        for r in sorted(res, key=lambda r: -r['ipr']):
            print(f"  {r['code']:4} {r['ipr']:5.1f} {r['cat']:22} f10={r['f10']:.2f} fcur={r['fcur']:.2f} f3={r['f3']:.2f} last={r['last']} jury={r['jury_n']} diff={r['diff_n']} tr={r['transv']} w={r['w_when']:.2f}  {r['titre'][:45]}")
