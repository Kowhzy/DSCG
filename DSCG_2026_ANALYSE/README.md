# DSCG 2026 — Analyse UE2, UE3, UE5 (annales, rapports du jury, priorités de révision)

Mise à jour : 24/09/2026. Étude réalisée pour Sacha (session DSCG d'octobre 2026).

## Livrables
| Fichier | Contenu |
|---|---|
| `05_rapports/DSCG_2026_UE2.pdf` | UE2 Finance — 24 pages |
| `05_rapports/DSCG_2026_UE3.pdf` | UE3 Management et contrôle de gestion — 24 pages |
| `05_rapports/DSCG_2026_UE5.pdf` | UE5 Management des systèmes d'information — 25 pages |

Chaque PDF est autonome : synthèse exécutive, méthodologie, programme officiel, historique des annales, statistiques, rapports du jury, croisement programme/jury/annales/cours, priorités 2026, analyse thème par thème, annales recommandées, checklist, sources.

## Arborescence
```
00_sources_officielles/
  bulletin_officiel/README_BO.md     statut du programme applicable (arrêté 13/02/2019) et de la réforme 2027
  rapports_jury/                     extraits annotés 2020, 2021, 2024, 2025 + texte intégral 2024 et 2025
01_annales/UE2|UE3|UE5/              texte extrait des sujets (.txt) ; PDF non versionnés (.gitignore)
02_data/UE2|UE3|UE5_dossiers.csv     base de données : 1 ligne = 1 dossier (points, questions, rubriques P/s, compétences, source)
03_analyses/                         statistiques par rubrique, matrices année × rubrique, observations du jury, correspondance cours
04_graphiques/                       carte thermique, fréquences, IPR, poids des parties, taux de réussite
05_rapports/                         les 3 PDF
06_scripts/                          referentiel.py (programme, jury, cours) · contenu.py (textes) · stats.py · build_report.py · qc.py
```

## Sources
- **Niveau 1 (officiel)** : rapports du jury DSCG 2020, 2021, 2024, 2025 (lus intégralement, copies Google Drive) ; sujets 2016-2025 (PDF officiels ou copies FicheBEN des sujets officiels, Drive) ; programme de l'arrêté du 13 février 2019 (rubriques relevées via la page Notion « Programme officiel 2026 »).
- **Niveau 2 (contrôle)** : Compta Online (extraits de recherche : pronostics UE2/UE3/UE5, réforme 2027), notes Drive UE5-01 à UE5-07, base Notion (index uniquement, car héritée d'un modèle).
- Recoupements réalisés : la structure des sujets 2020, 2021, 2024 et 2025 concorde avec la description du rapport du jury correspondant.

## Méthodologie (résumé)
- 10 sessions (2016-2025). Rupture de programme en 2020 : les sessions 2016-2019 sont projetées sur les rubriques actuelles et pèsent moins.
- Chaque dossier est rattaché à des rubriques officielles, en « principal » ou « secondaire ». Une session compte une fois par rubrique. UE2 2022 : deux sujets (épreuve du 25/10/2022 annulée, nouvelle épreuve le 05/01/2023), pondérés ½ chacun.
- **Indice de priorité de révision (IPR, 0-100)** : fréquence 2016-25 (15), fréquence 2020-25 (20), fréquence 2023-25 (10), poids dans le barème (10), citations du jury (15), difficultés signalées par le jury (10), transversalité (10), heures au programme (5), absence récente (5). L'IPR n'est pas une probabilité de tomber.
- Catégories : ≥ 60 maximale ; 45-60 très élevée ; 32-45 élevée ; 20-32 à maîtriser ; < 20 complément. Toute rubrique signalée comme faiblesse par le jury 2025 est classée au moins « très élevée ».

## Limites
- Rapports du jury 2022 et 2023 non consultés : absents du Drive, et sites officiels inaccessibles depuis l'environnement d'analyse (politique réseau).
- Annexe officielle du programme non relue directement. Les intitulés des rubriques viennent de Notion ; les notions détaillées sont un résumé de travail.
- UE2 2024, UE3 2024 et UE5 2024 : PDF scannés. UE2 2024 a été lu en image ; UE3 2024 a été reconstitué d'après le rapport du jury et la page Notion (points non vérifiés) ; UE5 2024 d'après une transcription Drive.
- Le Mac n'était pas accessible (session cloud) : les ressources locales ont été repérées via Notion et Google Drive.
- Les rattachements aux rubriques relèvent d'un jugement d'analyste ; tous sont traçables dans `02_data`.

## Mettre à jour
```bash
pip install reportlab matplotlib pymupdf
# 1. compléter 02_data/*.csv (nouvelle session) et 06_scripts/referentiel.py (nouveau rapport du jury)
python3 06_scripts/stats.py           # statistiques -> 03_analyses
python3 06_scripts/export_jury.py     # tables jury / cours -> 03_analyses
python3 06_scripts/build_report.py    # graphiques + PDF
python3 06_scripts/qc.py              # contrôle de cohérence PDF <-> données
```
