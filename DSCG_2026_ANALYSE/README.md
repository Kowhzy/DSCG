# DSCG 2026 — Analyse UE2, UE3, UE5 (annales, rapports du jury, priorités de révision)

Mise à jour : 24/09/2026. Étude réalisée pour Sacha (session DSCG d'octobre 2026).

## Livrables
| Fichier | Contenu |
|---|---|
| `05_rapports/DSCG_2026_UE2.pdf` | UE2 Finance — 33 pages |
| `05_rapports/DSCG_2026_UE3.pdf` | UE3 Management et contrôle de gestion — 31 pages |
| `05_rapports/DSCG_2026_UE5.pdf` | UE5 Management des systèmes d'information — 34 pages |
| `08_export_agent/UE*.json` et `UE*.md` | Base machine-lisible pour un agent IA de révision : consignes, priorités, robustesse, techniques, attendus des corrigés, jury, dossiers |

Chaque PDF est autonome : synthèse exécutive, méthodologie, programme officiel, historique des annales, statistiques, rapports du jury, croisement programme/jury/annales/cours, priorités 2026, analyse thème par thème, annales recommandées, checklist, sources.

## Arborescence
```
00_sources_officielles/
  bulletin_officiel/README_BO.md     statut du programme applicable (arrêté 13/02/2019) et de la réforme 2027
  bulletin_officiel/programme_*.txt  texte officiel des 3 programmes (via Dunod UE2/UE3 et « Programme MSI 19-20 » UE5)
  rapports_jury/                     extraits annotés 2020, 2021, 2022, 2024, 2025 + texte intégral 2022, 2024 et 2025
01_annales/UE2|UE3|UE5/              texte extrait des sujets (.txt) ; PDF non versionnés (.gitignore)
01_annales/corriges/                 texte extrait des corrigés 2020-2025 (UE5 2024 : résumé de lecture du scan)
02_data/UE2|UE3|UE5_dossiers.csv     base de données : 1 ligne = 1 dossier (points, questions, rubriques P/s, compétences, techniques, source)
02_data/UE*_attendus_corriges.csv    attendus des corrigés question par question, pièges, ALERTES (corrigés erronés/dépassés)
03_analyses/                         stats par rubrique, matrices, techniques, sensibilité de l'IPR, journal du reclassement, jury, cours
04_graphiques/                       carte thermique, fréquences, IPR, poids des parties, taux de réussite
05_rapports/                         les 3 PDF
06_scripts/                          extract_pdf.py · referentiel.py · reclassement.py · contenu.py · stats.py · build_report.py · export_agent.py · qc.py
08_export_agent/                     export JSON + Markdown pour l'agent IA
```

## Sources
- **Niveau 1 (officiel)** : rapports du jury DSCG 2020, 2021, 2022, 2024, 2025 (lus intégralement, copies Google Drive) ; sujets 2016-2025 (PDF officiels ou copies FicheBEN des sujets officiels, Drive) ; programme de l'arrêté du 13 février 2019 (texte relu dans sa reproduction Dunod UE2/UE3 et « Programme MSI 19-20 » UE5) ; éléments indicatifs de corrigé 2020-2025 (les 3 UE).
- **Niveau 2 (contrôle)** : Compta Online (extraits de recherche : pronostics UE2/UE3/UE5, réforme 2027), notes Drive UE5-01 à UE5-07, base Notion (index uniquement, car héritée d'un modèle).
- Recoupements réalisés : la structure des sujets 2020, 2021, 2022, 2024 et 2025 concorde avec la description du rapport du jury correspondant.

## Méthodologie (résumé)
- 10 sessions (2016-2025). Rupture de programme en 2020 : les sessions 2016-2019 sont projetées sur les rubriques actuelles et pèsent moins.
- Chaque dossier est rattaché à des rubriques officielles, en « principal » ou « secondaire ». Une session compte une fois par rubrique. UE2 2022 : l'épreuve initiale a été annulée ; seul le sujet de secours composé (2022-S2) compte [Rapport du jury 2022, p. 9], le sujet annulé reste une annale d'entraînement.
- **Indice de priorité de révision (IPR, 0-100)** : fréquence 2016-25 (15), fréquence 2020-25 (20), fréquence 2023-25 (10), poids dans le barème (10), citations du jury (15), difficultés signalées par le jury (10), transversalité (10), heures au programme (5), absence récente (5). L'IPR n'est pas une probabilité de tomber.
- Catégories : ≥ 60 maximale ; 45-60 très élevée ; 32-45 élevée ; 20-32 à maîtriser ; < 20 complément. Toute rubrique signalée comme faiblesse par le jury 2025 est classée au moins « très élevée ».

## Limites
- Rapport du jury 2023 non consulté : absent du Drive, et sites officiels inaccessibles depuis l'environnement d'analyse (politique réseau).
- Annexe du BO non ouverte directement (domaine bloqué) ; son texte a été relu dans les reproductions citées. Les notions affichées en sont un résumé fidèle.
- UE2 2024 et UE5 2024 : corrigés scannés. UE2 2024 a été lu en image ; UE3 2024 : questions vérifiées sur le corrigé officiel, qui reproduit les énoncés (points non communiqués) ; UE5 2024 d'après une transcription Drive.
- Le Mac n'était pas accessible (session cloud) : les ressources locales ont été repérées via Notion et Google Drive.
- Les rattachements aux rubriques relèvent d'un jugement d'analyste ; tous sont traçables dans `02_data`, et les 30 corrections de la passe 2 dans `03_analyses/reclassement_journal.csv`.
- Session 2023 : aucun rapport du jury publié, selon Sacha (non vérifié sur le site officiel, inaccessible). Sujet UE3 2024 non consulté, mais corrigé officiel intégré. Le fichier Drive « 2023 corrigé UE3 dscg.php.pdf » (21 Mo, id 1vu6X1uiyZ0pHs7cSut6-0BmqdELFDg9p) est un corrigé commenté UE3 **2023** (Sup Expertise / Compta Online, pages en image) : source secondaire, non exploitée car le corrigé officiel 2023 est déjà intégré.

## Passe 2 (24/09/2026) — ce qui a changé
- Programmes officiels relus : notions réécrites, volumes horaires par partie (critère « programme » de l'IPR).
- Reclassement de 30 dossiers. Effet majeur en UE3 : la rubrique 2.2 (audit, contrôle interne, risques) n'avait en réalité jamais été interrogée en principal ; 2.5, 2.4, 4.2 et 1.2 montent.
- Nouvelle colonne « techniques » et statistiques par technique (`03_analyses/UE*_techniques.csv`).
- Test de sensibilité de l'IPR sous 7 jeux de pondérations (`03_analyses/UE*_sensibilite.csv`).
- Corrigés 2020-2025 lus question par question (120 entrées, UE3 2024 incluse) ; 7 alertes (erreurs de calcul ou règles dépassées).

## Mettre à jour
```bash
pip install reportlab matplotlib pymupdf
# 1. compléter 02_data/*.csv (nouvelle session) et 06_scripts/referentiel.py (nouveau rapport du jury)
python3 06_scripts/stats.py           # statistiques -> 03_analyses
python3 06_scripts/export_jury.py     # tables jury / cours -> 03_analyses
python3 06_scripts/reclassement.py    # rattachements + techniques (source de vérité des rubriques)
python3 06_scripts/build_report.py    # graphiques + PDF
python3 06_scripts/export_agent.py    # export JSON/Markdown pour l'agent IA
python3 06_scripts/qc.py              # contrôle de cohérence PDF <-> données
```
