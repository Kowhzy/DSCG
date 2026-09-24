"""Export machine-lisible pour un agent IA de révision : 08_export_agent/UE*.json et UE*.md.
Contenu : programme officiel, priorités (IPR, catégorie, robustesse), statistiques, techniques, observations du jury,
attendus des corrigés (avec alertes), dossiers d'annales, zones à ne pas négliger, consignes d'usage."""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from stats import compute, techniques, sensitivity, SCENARIOS, W, YEARS
from referentiel import RUBRIQUES, JURY, COURS, BO_REF
from contenu import EPREUVE, SYNTHESE, SURPRISES, TROUS, ANNALES

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(BASE, '08_export_agent'); os.makedirs(OUT, exist_ok=True)

CONSIGNES = [
    "L'indice de priorité de révision (IPR, 0-100) hiérarchise l'effort de révision ; ce n'est PAS une probabilité que le thème tombe.",
    "Ne jamais raisonner « tombé en 2025 donc pas en 2026 » : le jury 2025 écrit qu'un point faible peut être réinterrogé dès l'année suivante (rapport 2025, p. 21).",
    "Ne jamais raisonner « absent depuis 5 ans donc il va tomber » : les zones peu interrogées sont signalées comme « à ne pas négliger », sans prédiction.",
    "Aucun point du programme n'est mineur (rapports du jury 2020, 2021, 2022, 2024, 2025) : les catégories basses indiquent un effort minimal, pas une impasse.",
    "Les corrigés sont « indicatifs ». Les entrées marquées ALERTE signalent un corrigé probablement erroné ou dépassé : ne pas faire apprendre ce chiffre ou cette règle sans vérification.",
    "Les valeurs « Non vérifié » ou « n.c. » sont des trous assumés : ne pas les combler par une invention.",
    "Session 2026 = dernière session sur le programme de l'arrêté du 13 février 2019 ; la réforme (arrêté du 4 août 2025) s'applique à partir de 2027.",
]

def read(p):
    return list(csv.DictReader(open(p, encoding='utf-8'), delimiter=';'))

def export(ue):
    rows, res = compute(ue)
    tech = techniques(ue); sens = {x['code']: x for x in sensitivity(ue, res)}
    att = read(os.path.join(BASE, '02_data', f'{ue}_attendus_corriges.csv'))
    dos = read(os.path.join(BASE, '02_data', f'{ue}_dossiers.csv'))
    rub = []
    for r in sorted(res, key=lambda r: -r['ipr']):
        x = sens[r['code']]
        rub.append(dict(
            code=r['code'], partie=r['partie'], intitule=r['titre'], notions_officielles=r['notions'],
            ipr=round(r['ipr'], 1), categorie=r['cat'], regle_jury_2025=bool(r.get('regle')),
            robustesse=dict(rang_reference=x['rank_ref'], rang_min=x['rmin'], rang_max=x['rmax'], scenarios_premier_tiers=f"{x['top_tiers']}/{x['n_scen']}"),
            sessions_principal=[y for y in YEARS if r['years'][y] > 0], sessions_toile_de_fond=[y for y in YEARS if r['yearsA'][y] > 0 and r['years'][y] == 0],
            frequence_2016_2025=round(r['f10'], 3), frequence_2020_2025=round(r['fcur'], 3), frequence_2023_2025=round(r['f3'], 3),
            derniere_apparition=r['last'], poids_bareme_quand_present=round(r['w_when'], 3),
            dossiers=r['dossiers'], jury=[dict(annee=a, page=pg, observation=o, difficulte_candidats=pb, consequence=c) for a, pg, o, pb, c in r['jury']],
            ressources_personnelles=dict(support=COURS[ue].get(r['code'], ('', ''))[0], statut_notion=COURS[ue].get(r['code'], ('', ''))[1]),
            zone_a_ne_pas_negliger=TROUS[ue].get(r['code'])))
    data = dict(
        ue=ue, genere_le='2026-09-24', consignes_agent=CONSIGNES, epreuve=EPREUVE[ue], reference_programme=BO_REF[ue],
        methode_ipr=dict(ponderations=W, seuils={'PRIORITÉ MAXIMALE': 60, 'PRIORITÉ TRÈS ÉLEVÉE': 45, 'PRIORITÉ ÉLEVÉE': 32, 'À MAÎTRISER': 20},
                         regle="une rubrique signalée comme faiblesse par le jury 2025 est au minimum en PRIORITÉ TRÈS ÉLEVÉE",
                         scenarios_sensibilite=list(SCENARIOS)),
        synthese=SYNTHESE[ue], surprises=SURPRISES[ue], rubriques=rub,
        techniques=[dict(technique=t['tech'], libelle=t['label'], sessions_2016_2025=t['s10'], sessions_2020_2025=t['scur'],
                         sessions_2023_2025=t['s3'], derniere=t['last'], dossiers=sorted(t['dossiers'], reverse=True)) for t in tech],
        annales_recommandees=[dict(annale=a, interet=t) for a, t in ANNALES[ue]],
        attendus_corriges=[dict(annee=a['annee'], dossier=a['dossier'], question=a['question'], bareme=a['bareme'], attendus=a['attendus_du_corrige'],
                                pieges=a['pieges_et_vigilance'], alerte='ALERTE' in (a['pieges_et_vigilance'] + a['attendus_du_corrige']), source=a['source']) for a in att],
        dossiers_annales=[{k: d[k] for k in ('annee', 'dossier', 'intitule', 'points', 'total_points', 'questions_resume', 'rubriques_principales',
                                              'rubriques_secondaires', 'techniques', 'nature', 'source')} for d in dos],
        jury_toutes_observations=[dict(annee=a, page=pg, observation=o, rubriques=rb, difficulte_candidats=pb, consequence=c) for a, pg, o, rb, pb, c in JURY[ue]],
        programme_complet=[dict(code=c, partie=p, intitule=t, notions=n) for c, p, t, n, _ in RUBRIQUES[ue]],
    )
    json.dump(data, open(os.path.join(OUT, f'{ue}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # Markdown compact (lecture directe par un agent)
    L = [f"# DSCG 2026 — {ue} — base de révision (générée le 24/09/2026)", "", "## Consignes pour l'agent", *[f"- {c}" for c in CONSIGNES], "",
         f"## Épreuve", EPREUVE[ue], "", "## Constats clés", *[f"- {t}" for t in SYNTHESE[ue]], "",
         "## Priorités (IPR décroissant)", "| Rubrique | Catégorie | IPR | Robustesse (rang min-max, 1er tiers) | Dernière | Notions officielles |", "|---|---|---|---|---|---|"]
    for r in rub:
        rb = r['robustesse']
        L.append(f"| {r['code']} {r['intitule']} | {r['categorie']} | {r['ipr']} | {rb['rang_min']}-{rb['rang_max']}, {rb['scenarios_premier_tiers']} | {r['derniere_apparition'] or 'jamais'} | {r['notions_officielles']} |")
    L += ["", "## Techniques les plus mobilisées", "| Technique | Sessions 2016-25 | Depuis 2020 | Dernière |", "|---|---|---|---|"]
    L += [f"| {t['libelle']} | {t['sessions_2016_2025']:g} | {t['sessions_2020_2025']:g} | {t['derniere']} |" for t in data['techniques']]
    L += ["", "## Zones à ne pas négliger", *[f"- **{c}** — {t}" for c, t in TROUS[ue].items()], "",
          "## Attendus des corrigés officiels (2020-2025)"]
    for a in data['attendus_corriges']:
        L.append(f"- **{a['annee']} D{a['dossier']} — {a['question']}** ({a['bareme']}){' ⚠ ALERTE' if a['alerte'] else ''} : {a['attendus']}" + (f" — *Pièges :* {a['pieges']}" if a['pieges'] else ''))
    L += ["", "## Observations du jury", *[f"- [{o['annee']}, {o['page']}] {o['observation']} → {o['consequence']}" for o in data['jury_toutes_observations']],
          "", "## Annales recommandées", *[f"- **{a['annale']}** — {a['interet']}" for a in data['annales_recommandees']], "",
          "## Dossiers d'annales 2016-2025", "| Session | D | Intitulé | Pts | Rubriques P | Rubriques s | Techniques |", "|---|---|---|---|---|---|---|"]
    L += [f"| {d['annee']} | {d['dossier']} | {d['intitule']} | {d['points'] or 'n.v.'}/{d['total_points'] or 'n.v.'} | {d['rubriques_principales']} | {d['rubriques_secondaires']} | {d['techniques']} |"
          for d in sorted(data['dossiers_annales'], key=lambda d: d['annee'], reverse=True)]
    open(os.path.join(OUT, f'{ue}.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    return len(rub), len(att), len(tech)

if __name__ == '__main__':
    for ue in ('UE2', 'UE3', 'UE5'):
        print(ue, export(ue))
