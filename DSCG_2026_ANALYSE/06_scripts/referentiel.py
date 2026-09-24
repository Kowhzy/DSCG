"""Référentiel de travail : programme officiel DSCG (arrêté du 13 février 2019, annexe II — applicable à la session 2026),
observations des rapports du jury, correspondance avec les ressources personnelles de Sacha.

Sources et niveau de vérification (voir README) :
- Parties, rubriques, notions et volumes horaires : texte officiel du programme (annexe de l'arrêté du 13 février 2019),
  relu via sa reproduction dans les manuels Dunod UE2/UE3 et le document « Programme MSI 19-20 » (UE5) ; l'annexe du BO
  elle-même n'a pas pu être ouverte depuis l'environnement d'analyse (domaine bloqué).
- Passe 2 (24/09/2026) : notions réécrites sur le texte officiel ; dossiers reclassés (06_scripts/reclassement.py,
  journal 03_analyses/reclassement_journal.csv).
"""

BO_REF = {
    'UE2': "Annexe II de l'arrêté du 13 février 2019 (BO ESR n°25 du 20 juin 2019), UE2 Finance, p. 6-10 de l'annexe",
    'UE3': "Annexe II de l'arrêté du 13 février 2019 (BO ESR n°25 du 20 juin 2019), UE3 Management et contrôle de gestion, p. 10-15 de l'annexe",
    'UE5': "Annexe II de l'arrêté du 13 février 2019 (BO ESR n°25 du 20 juin 2019), UE5 Management des systèmes d'information, p. 18-25 de l'annexe",
}

# (code, partie, intitulé officiel de la rubrique, notions et contenus officiels (résumé fidèle du programme), poids BO = heures moyennes par rubrique)
# Poids BO = volume horaire de la partie / nombre de rubriques de la partie (le programme ne donne pas d'heures par rubrique).
def _h(h, n): return round(h / n, 2)
RUBRIQUES = {
 'UE2': [
  ('1.1','1. La valeur (20 h)','La valeur en finance',"marchés financiers et financement de l'économie, efficience (hypothèse, formes), hypothèses des modèles, aspects psychologiques et humains (finance comportementale), regard critique sur la finance classique",_h(20,3)),
  ('1.2','1. La valeur (20 h)','La valeur et le risque',"MEDAF (fondements, usage pratique, limites), modèle de Fama et French et dérivés, mesure des primes de risque",_h(20,3)),
  ('1.3','1. La valeur (20 h)','La valeur et la performance',"cours boursiers et gestion de portefeuille, placements financiers et gestion patrimoniale, introduction à la finance immobilière, performance boursière, modèles d'actualisation des dividendes",_h(20,3)),
  ('2.1','2. Diagnostic approfondi (20 h)','Analyse financière des comptes consolidés',"diagnostic selon le modèle économique, comptes consolidés/combinés, activité, structure financière, rentabilité économique et des capitaux propres, flux de trésorerie",_h(20,2)),
  ('2.2','2. Diagnostic approfondi (20 h)','Analyse extra-financière',"gouvernance d'entreprise, RSE et critères extra-financiers, création de valeur et sa répartition (EVA), notation et scoring",_h(20,2)),
  ('3.1','3. Évaluation de l\'entreprise (20 h)','Évaluation par les flux',"flux revenant aux apporteurs de capitaux / aux actionnaires, business plan, rôle de l'actualisation",_h(20,3)),
  ('3.2','3. Évaluation de l\'entreprise (20 h)','Évaluation par approche comparative',"choix des inducteurs, échantillon de comparables, effets des paramètres sous-jacents, avantages et limites",_h(20,3)),
  ('3.3','3. Évaluation de l\'entreprise (20 h)','Autres évaluations particulières et spécifiques',"ANR et goodwill, approche immobilière, start-up, approches sectorielles",_h(20,3)),
  ('4.1','4. Investissement et financement (30 h)','Investissement et désinvestissement',"critères de sélection (projets exclusifs, liés), rationnement du capital, désinvestissement, défaillance et liquidation",_h(30,3)),
  ('4.2','4. Investissement et financement (30 h)','Modalités de financement',"fonds propres et quasi-fonds propres, financements bancaires, obligataires, court terme (euro PP), capital-investissement, financements publics",_h(30,3)),
  ('4.3','4. Investissement et financement (30 h)','Le choix d\'une structure de financement',"arbitrage capitaux propres / dettes, déterminants de la structure financière, théories du choix de financement",_h(30,3)),
  ('5.1','5. La trésorerie (20 h)','La gestion des flux de trésorerie au sein d\'un groupe',"centralisation de trésorerie, opérations intragroupe, supports de financement et de placement",_h(20,3)),
  ('5.2','5. La trésorerie (20 h)','La gestion des risques',"couverture change et taux (marchés organisés, gré à gré), options et Black-Scholes, swaps, forward, futures, structure des taux",_h(20,3)),
  ('5.3','5. La trésorerie (20 h)','La fraude et le blanchiment des capitaux',"réglementation financière, fraude comptable et financière, Tracfin, éthique et déontologie",_h(20,3)),
  ('6.1','6. Ingénierie financière (30 h)','La politique de dividende',"théories et déterminants de la politique de dividende, effets informationnels, impacts fiscaux",_h(30,5)),
  ('6.2','6. Ingénierie financière (30 h)','La gestion de la valeur de l\'action',"rachats d'actions, opérations sur le nombre d'actions, restructurations (APA, scission), introductions en bourse",_h(30,5)),
  ('6.3','6. Ingénierie financière (30 h)','Les fusions et acquisitions',"synergies, holdings, opérations à effet de levier (LBO), offres publiques",_h(30,5)),
  ('6.4','6. Ingénierie financière (30 h)','Les opérations sur les dettes et sur les créances',"defeasance, titrisation",_h(30,5)),
  ('6.5','6. Ingénierie financière (30 h)','Les innovations financières',"fintechs, crowdfunding, systèmes privés d'échange de titres, blockchains, cryptomonnaies, analyse par les réseaux et les données",_h(30,5)),
 ],
 'UE3': [
  ('1.1','1. Modèles d\'organisation et contrôle de gestion (30 h)','Évolution des modèles d\'organisation',"formes structurelles, structures par projet, réseaux, transversalité et processus, entreprise virtuelle, hybridation public/privé",_h(30,3)),
  ('1.2','1. Modèles d\'organisation et contrôle de gestion (30 h)','Le positionnement du contrôle de gestion et l\'identification du métier comme aide à la stratégie',"rôle et place du CG selon les structures, travail d'information du contrôleur, CG et DD/RSE, éthique et déontologie",_h(30,3)),
  ('1.3','1. Modèles d\'organisation et contrôle de gestion (30 h)','Le contrôle de gestion et les systèmes d\'information et de communication',"PGI, transmission électronique de l'information, mégadonnées",_h(30,3)),
  ('2.1','2. Management stratégique (80 h)','Analyse et choix stratégiques',"diagnostic et chaîne de valeur, business model, risques, critères de performance, segmentation/DAS, stratégies génériques, recentrage/diversification, croissance interne/externe, alliances",_h(80,7)),
  ('2.2','2. Management stratégique (80 h)','Place et rôle du contrôle de gestion stratégique',"CG face à l'audit et au contrôle interne, risques de l'entité, formes et champs de l'audit, communication financière, dimension culturelle des outils",_h(80,7)),
  ('2.3','2. Management stratégique (80 h)','Approche du marketing stratégique',"leviers du marketing, communication multicanale, e-réputation, digitalisation et fidélisation, B to B, B to C, tarification dynamique (yield), big data",_h(80,7)),
  ('2.4','2. Management stratégique (80 h)','La gestion du périmètre de l\'entité',"extension (acquisitions, fusions), réduction, coopération, réseau, prix de cession interne et de transfert",_h(80,7)),
  ('2.5','2. Management stratégique (80 h)','La planification et le diagnostic stratégique',"CG et diagnostic, planification, plans prévisionnels (activité, financement, business plan), analyse d'un business model, intérêts et limites de la gestion budgétaire",_h(80,7)),
  ('2.6','2. Management stratégique (80 h)','Analyse des parties prenantes et structures de gouvernance',"cartographie des parties prenantes, attentes et jeux de pouvoir, types de gouvernance, communication vers les parties prenantes",_h(80,7)),
  ('2.7','2. Management stratégique (80 h)','Contrôle de gestion et changement organisationnel',"CG interface stratégie/organisation, aide à l'évolution de la structure",_h(80,7)),
  ('3.1','3. Conduite du changement (40 h)','Le management du changement',"types et diagnostic du changement, styles et leviers, management en mode projet, suivi des projets, ordonnancement",_h(40,3)),
  ('3.2','3. Conduite du changement (40 h)','Management et pilotage par les processus',"cartographie des processus, progrès continu, coûts cibles, analyse de la valeur, dysfonctionnements organisationnels, usage des rapports d'audit",_h(40,3)),
  ('3.3','3. Conduite du changement (40 h)','Le contrôle de gestion et le pilotage stratégique',"performance globale, FCS, KPI, tableaux de bord stratégiques",_h(40,3)),
  ('4.1','4. Management des ressources humaines et des compétences (30 h)','La gestion des ressources humaines',"tableaux de bord sociaux, bilan social, écarts et effets de la masse salariale, GPEC, gestion de crise (négociation, médiation…)",_h(30,2)),
  ('4.2','4. Management des ressources humaines et des compétences (30 h)','La gestion des compétences',"identification des compétences, formation, carrières, politique de rémunération, gestion des connaissances, apprentissage organisationnel",_h(30,2)),
 ],
 'UE5': [
  ('1.1','1. Gouvernance des SI (30 h)','Position de la fonction SI au sein de l\'organisation',"DSI : missions, fonctions, rôles, ressources, types d'organisation, tableau de bord de la DSI",_h(30,4)),
  ('1.2','1. Gouvernance des SI (30 h)','La stratégie SI',"alignement stratégique, schéma directeur, agilité",_h(30,4)),
  ('1.3','1. Gouvernance des SI (30 h)','Évolution des systèmes d\'information',"urbanisation et cartographie, SI inter-organisationnels, open data/innovation, BYOD, référentiels (ITIL, COBIT, ISO)",_h(30,4)),
  ('1.4','1. Gouvernance des SI (30 h)','Management stratégique des données (Big Data-Mégadonnées)',"big data, analyse et sécurité des données, plateformes, datacenter et cloud computing",_h(30,4)),
  ('2.1','2. La gestion de projets SI (30 h)','Les enjeux d\'un projet',"place du projet dans la stratégie, agilité, organisation du projet, MOA/MOE, faire/faire-faire face au cloud (SaaS, IaaS, PaaS), régie/forfait",_h(30,5)),
  ('2.2','2. La gestion de projets SI (30 h)','La mise en œuvre d\'un projet',"cahier des charges, parties prenantes, cycle de vie, planification et ordonnancement, qualité (ISO, CMMI), suivi des coûts et délais (écarts), tests et recette, déploiement, formation",_h(30,5)),
  ('2.3','2. La gestion de projets SI (30 h)','Maintenance',"maintenance corrective et évolutive, contrat de maintenance, TMA et niveau de service",_h(30,5)),
  ('2.4','2. La gestion de projets SI (30 h)','Gestion des risques du projet',"analyse et gestion des risques, intégration des risques dans les contrats",_h(30,5)),
  ('2.5','2. La gestion de projets SI (30 h)','Gestion des connaissances',"capitalisation des savoirs, outils collaboratifs et de KM, text mining",_h(30,5)),
  ('3.1','3. Les systèmes d\'entreprise (15 h)','La place des systèmes d\'entreprise (SE)',"intégration, PGI-ERP, couverture fonctionnelle, open source, SaaS, évolutions réglementaires",_h(15,2)),
  ('3.2','3. Les systèmes d\'entreprise (15 h)','Le cycle de vie des systèmes d\'entreprise (SE)',"mise en place, déploiement, renouvellement, exploitation et évaluation",_h(15,2)),
  ('4.1','4. Gestion de la performance informationnelle (30 h)','Définition d\'indicateurs',"indicateurs de performance et de qualité (données, sécurité, fiabilité…)",_h(30,5)),
  ('4.2','4. Gestion de la performance informationnelle (30 h)','Le contrat de services',"niveaux de service (SLA), infogérance, facturation interne, responsabilité du prestataire, plan de continuité d'activité",_h(30,5)),
  ('4.3','4. Gestion de la performance informationnelle (30 h)','Les coûts',"coûts de la fonction SI, TCO, coût d'opportunité, externalisation, open source, mutualisation, tarifications du cloud",_h(30,5)),
  ('4.4','4. Gestion de la performance informationnelle (30 h)','Les budgets',"budget de la fonction SI, facturation interne, pay per licence / per use",_h(30,5)),
  ('4.5','4. Gestion de la performance informationnelle (30 h)','Évaluation des projets de SI',"bilan coûts/avantages, critères de sélection, ROI pré et post projet, réversibilité, analyse post mortem",_h(30,5)),
  ('5.1','5. Architecture et sécurité des SI (15 h)','Architecture technique',"client-serveur, middleware, transactionnel, intégration, portail",_h(15,3)),
  ('5.2','5. Architecture et sécurité des SI (15 h)','Mise en place d\'une architecture de confiance',"PKI, certificat, signature électronique, droit de l'information (RGPD, conservation, dématérialisation)",_h(15,3)),
  ('5.3','5. Architecture et sécurité des SI (15 h)','Surveillance et prévention',"surveillance des processus, prévention, continuité, protection juridique, assurances et garanties",_h(15,3)),
  ('6.1','6. Audit du SI, conseil et reporting (20 h)','Audit du système d\'information',"missions d'audit (interne, externe, stratégique), documentation d'audit, conseils et recommandations",_h(20,4)),
  ('6.2','6. Audit du SI, conseil et reporting (20 h)','Gouvernance d\'entreprise et environnement spécifique pour l\'auditeur ou le conseil',"normes professionnelles, comptes d'entités informatisées, risques d'audit et de conseil, ITIL, COBIT, cartographie applicative, obligations légales",_h(20,4)),
  ('6.3','6. Audit du SI, conseil et reporting (20 h)','Audit et conseils assistés',"étapes et outils de l'audit assisté, progiciels d'aide aux missions",_h(20,4)),
  ('6.4','6. Audit du SI, conseil et reporting (20 h)','Contrôle et reporting',"projets de reporting, entrepôt de données, visualisation, qualité et intégration des données",_h(20,4)),
 ],
}
PARTIES_NOTE = {
 'UE2': "Parties, rubriques et volumes horaires : programme officiel UE2 (140 h, 15 ECTS), reproduit en tête du manuel Dunod UE2 (00_sources_officielles/bulletin_officiel/programme_UE2_via_Dunod.txt).",
 'UE3': "Parties, rubriques et volumes horaires : programme officiel UE3 (180 h, 20 ECTS), reproduit en tête du manuel Dunod UE3 (programme_UE3_via_Dunod.txt).",
 'UE5': "Parties, rubriques et volumes horaires : programme officiel UE5 (140 h, 15 ECTS), transcription du document « Programme MSI 19-20 » (programme_UE5_transcription.txt).",
}

# Observations des jurys : (année, page, observation (paraphrase fidèle ou verbatim entre guillemets), rubriques, problème candidats (bool), conséquence)
JURY = {
 'UE2': [
  (2020,'p. 7',"Format modifié : la question de réflexion (25 % des points) est remplacée par de petites questions de cours insérées dans le sujet.",'',False,"S'entraîner aux questions de cours courtes intégrées au cas, pas à la dissertation."),
  (2020,'p. 7',"Seule vraie nouveauté du programme dans le sujet : la question sur la blockchain.",'6.5',False,"Connaître définitions et usages de la blockchain en finance/trésorerie."),
  (2020,'p. 7',"Rappel du rapport 2019 : extra-financier et gouvernance, innovations financières (blockchain, fintech, ICO), réglementation financière, évaluation des patrimoines/immobilier sont « des points majeurs » ; « il n'est plus envisageable d'en faire l'impasse ».",'2.2|6.5|1.3|3.3',False,"Couvrir les « nouveautés » 2019 même hors calcul."),
  (2021,'p. 7',"Sujet « complet » : bêta, VAN, option de change / contrat à terme + questions de restitution du cours (immobilier, crypto-actifs).",'1.2|4.1|5.2|6.5',False,"Les fondamentaux calculatoires restent le socle ; la restitution de cours rapporte des points."),
  (2021,'p. 7-8',"Nouveautés à maîtriser : finance environnementale, gouvernance, régulation, indicateurs extra-financiers, fintech, finance comportementale.",'2.2|6.5|1.1',False,"Fiches synthétiques sur chacun de ces thèmes."),
  (2021,'p. 3-4',"Taux de réussite UE2 = 23,86 % ; 30,1 % des copies < 6.",'',True,"UE à fort taux d'élimination : sécuriser le socle calculatoire."),
  (2024,'p. 22',"D1 « classique, essentiellement calculatoire » : MEDAF puis trois méthodes d'évaluation pour une fourchette de négociation (OPR Bel).",'1.2|3.1|3.2|6.3',False,"Savoir enchaîner MEDAF → DCF → multiples → fourchette."),
  (2024,'p. 22',"Gouvernance après OPR : loi Copé-Zimmermann, théorie de l'agence ; D3 RSE/ESG, parties prenantes, société à mission, actionnariat salarié.",'2.2|6.3',False,"Gouvernance et RSE = tiers du sujet ou plus."),
  (2024,'p. 23',"Candidats sans connaissances de base « (FTD ; RSE/ESG, etc.) », réponses non contextualisées, concepts théoriques fondamentaux non maîtrisés.",'3.1|2.2|1.1',True,"Retravailler le calcul des FTD et les définitions RSE/ESG ; contextualiser."),
  (2024,'p. 23-24',"« la performance durable de l'entreprise est autant à prendre en considération que les performances financière et économique » ; articuler cours, théorie et exemples ; tableaux (TFT).",'2.2|1.1',False,"Intégrer systématiquement une dimension ESG dans les conseils."),
  (2025,'p. 25',"D1 : coût du capital d'une société non cotée par le MEDAF (comparables) ; VAN/TIR de projets exclusifs et divergences.",'1.2|4.1',False,"Maîtriser bêta désendetté/réendetté et conflit VAN/TRI."),
  (2025,'p. 26',"Questions de niveau DCG (VAN, TRI, annuités constantes, tableaux d'amortissement) jugées légitimes : « les acquis du DCG constituent un préalable indispensable ».",'4.1|4.2',False,"Revoir les mathématiques financières du DCG."),
  (2025,'p. 26',"« la faible maîtrise […] de certains mécanismes du LBO, en particulier le calcul des annuités constantes ».",'6.3|4.2',True,"Refaire un montage LBO complet (holding, dette senior/junior, remontée de dividendes)."),
  (2025,'p. 26',"D3 (crowdfunding, dividende, grands auteurs) insuffisamment traité par mauvaise gestion du temps malgré un barème élevé.",'6.5|6.1|4.2',True,"Réserver du temps au dernier dossier rédactionnel."),
  (2025,'p. 26-27',"Méconnaissance des concepts théoriques fondamentaux « notamment en finance d'entreprise » ; posture d'analyste et de conseiller ; tableaux systématiques.",'1.1|6.1',True,"Fiches auteurs/théories (MM, agence, signal, Fama, Gordon)."),
 ],
 'UE3': [
  (2020,'p. 7',"Sujet long : « Le critère de bonne gestion du temps des analyses est devenu récurrent sur le sujet UE3 ».",'',True,"S'entraîner en temps réel (4 h) avec beaucoup d'annexes."),
  (2020,'p. 7-8',"Points majeurs : extra-financier, investissements immatériels et humains, mise en œuvre stratégique, gestion du changement, « calculs de coûts/performances fondamentaux », incertitude, choix entre options, scénarios.",'3.3|4.1|4.2|3.1|2.7|2.5',False,"Couvrir changement + RH + calculs de coûts ; raisonner en scénarios."),
  (2020,'p. 8',"Épreuve « plus axée sur une réflexion ancrée sur des cas réels […] que sur des calculs bruts et des définitions non contextualisées ».",'',False,"Toujours appliquer l'outil au cas."),
  (2021,'p. 8',"Sujet start-up en 4 dossiers (diagnostic, business model, RH, rôle du contrôleur) ; « assez long » ; contenu du programme UE3 « pas […] profondément modifié avec la réforme ».",'2.1|2.3|4.1|1.2',False,"Les annales antérieures à 2020 restent exploitables en UE3."),
  (2024,'p. 24',"« le contrôle de gestion fait part égale avec le management » ; compétences de haut niveau (analyser, évaluer, créer).",'2.5',False,"Le contrôle de gestion chiffré pèse désormais la moitié du barème."),
  (2024,'p. 25',"Réponses descriptives, récitation, « fréquent manque de contextualisation » ; méconnaissance des TPE et des services.",'',True,"Contextualiser ; s'entraîner sur des TPE et des services."),
  (2024,'p. 26',"« de nombreux candidats ont utilisé le PESTEL ou SWOT au lieu des forces de Porter pour analyser le micro-environnement ».",'2.1',True,"Choisir l'outil selon le niveau d'analyse (macro vs micro)."),
  (2024,'p. 26',"« peu de candidats ont compris qu'il fallait utiliser la méthode du facteur rare ».",'2.5',True,"Refaire des exercices d'optimisation sous contrainte."),
  (2025,'p. 28',"Rééquilibrage CG/management « confirmé » ; concevoir un schéma d'analyse d'écarts, analyser masse salariale et prix de transfert ; RSE traitée par le double prisme.",'2.5|4.1|2.4|1.2',False,"Savoir construire soi-même une décomposition d'écarts."),
  (2025,'p. 29',"Consignes non respectées (concepts non définis alors que demandé) ; récitation « comme en 2024 ».",'',True,"Définir chaque concept demandé avant de l'appliquer."),
  (2025,'p. 29-30',"« De nombreux candidats ne maîtrisent pas les techniques de base, qu'il s'agisse de la décomposition des écarts et des différents effets de la masse salariale » ; calcul d'une redevance à partir d'une formule simple raté.",'2.5|4.1',True,"PRIORITÉ : écarts (y compris réinterprétés) et effets niveau/masse/report."),
  (2025,'p. 30',"Conseils 2026 : maîtriser et réinterpréter les techniques ; exploiter calculs et concepts dans une argumentation ; articuler management et CG.",'2.5|2.4',False,"Chaque calcul doit déboucher sur une analyse et une préconisation."),
  (2025,'p. 18-19',"Taux de réussite UE3 : 50,14 % (2024) → 17,28 % (2025) ; moyenne 9,65 → 7,08.",'',True,"Session 2025 très sélective : le niveau technique est discriminant."),
 ],
 'UE5': [
  (2020,'p. 9',"Nouvelle maquette : cas en cabinet, ~20 questions de 0,5 à 2 points ; sécurité, DPO, RGPD, migration vers un ERP en SaaS ; « tendance qui devrait être celle des épreuves à venir ».",'5.2|5.3|3.1|3.2',False,"RGPD/sécurité et ERP en contexte cabinet."),
  (2020,'p. 9',"Environnement : télétravail, continuité de service, externalisation et cloud, contractualisation des prestataires ; plutôt que « la conception ex nihilo ».",'5.3|4.2|2.1',False,"Prestataires, cloud, continuité."),
  (2021,'p. 9',"D1 schéma directeur « assez technique » ; indicateurs de coût ; D2 FCS, risques, deux méthodes, Gantt ; D3 RGPD et SI achats, résilience.",'1.2|4.3|2.1|2.4|2.2|5.2|5.3',False,"Schéma directeur, indicateurs de coût, méthodes et Gantt."),
  (2021,'p. 10',"« Cette UE5 continue sa transformation vers de moins en moins de questions liées aux techniques et à l'informatique ».",'',False,"Posture de manager/conseil plutôt que technicien."),
  (2024,'p. 29',"D1 : décision CRM après acquisition, accompagnement du changement ; le jury regrette des « morceaux de cours » non reliés au contexte.",'3.2|2.2|1.3',True,"Argumenter en situation."),
  (2024,'p. 29',"D2 : alignement stratégique ; références explicites au modèle valorisées ; « de nombreuses copies manquent de fondements théoriques solides » ; indicateurs de performance et de qualité.",'1.2|4.1',True,"Connaître et citer le modèle d'alignement."),
  (2024,'p. 30',"D3 : SI fantômes et BYOD (note de synthèse), erreurs de gestion de projet ; « L'ensemble du programme doit être maîtrisé ».",'5.3|2.2|1.3',False,"Notes de synthèse courtes et structurées."),
  (2025,'p. 35',"Nouvelle orientation « niveau master » ; D1 audit et convergence = « socle structurant » : alignement, COBIT vs ISO 27001, méthodologie d'audit.",'6.1|6.2|1.2',False,"Méthodologie de mission d'audit SI + référentiels."),
  (2025,'p. 36',"D1 : « un nombre significatif de copies a présenté des développements génériques, peu contextualisés » ; alignement stratégique « parfois réduit à un choix technique basique ou à une simple standardisation logicielle ».",'1.2|6.1',True,"Analyser les dimensions organisationnelles/managériales."),
  (2025,'p. 36',"D2 sécurité et Zero Trust « discriminant » : DIC, PCA vs PRA (RTO/RPO), Zero Trust comme cadre, BYOD, IAM/MFA/MDM ; confusions référentiels/normes/solutions.",'5.3|5.2|4.2|1.3',True,"Fiche sécurité moderne (manquante dans le cours selon tes notes Drive)."),
  (2025,'p. 36',"D3 BI : chaîne de valeur (collecte, ETL, entrepôt, restitution), compétences, rôle de la DSI ; BI réduite à un outil dans les copies faibles.",'1.4|6.4|1.1',True,"Chaîne décisionnelle et gouvernance des données."),
  (2025,'p. 36-37',"Trois difficultés persistantes : corpus théorique peu mobilisé, argumentation descriptive, rédaction ; « La simple restitution de connaissances techniques ne saurait suffire ».",'1.2|6.2',True,"Citer explicitement modèles et référentiels."),
  (2025,'p. 18-19',"Taux de réussite UE5 : 57,85 % (2024) → 38,87 % (2025).",'',True,"Épreuve en durcissement."),
 ],
}

# Correspondance avec les ressources de Sacha (page Notion « Programme officiel 2026 — couverture et preuves » ; statut déclaré I/A/U)
COURS = {
 'UE2': {
  '1.1':('F1 (INTEC Cours 1 « La valeur ») ch.4 p.98, 102','I'), '1.2':('F1 ch.3 IV p.84','A'), '1.3':('F1 ch.2 p.50, ch.3 p.69 ; F2 p.74','A'),
  '2.1':('F4 (INTEC Cours 4) ch.1 p.9-33','A'), '2.2':('F4 ch.2 p.38-49','A'), '3.1':('F2 (INTEC Cours 2) ch.2 p.67-74','A'),
  '3.2':('F2 ch.3 p.76-78','A'), '3.3':('F2 ch.4 p.82-87, ch.5 p.90-91','I'), '4.1':('F2 ch.1 p.9-31','A'),
  '4.2':('F2 ch.2 p.43-46','A'), '4.3':('F2 ch.2 III p.59','A'), '5.1':('F4 partie 6 ch.1 p.53-61','I'),
  '5.2':('F4 partie 6 ch.2 p.64-95','A'), '5.3':('F4 partie 6 ch.3 p.114-116','I'), '6.1':('F3 (INTEC Cours 3) ch.1 p.9-24','I'),
  '6.2':('F3 ch.2 p.27-54','I'), '6.3':('F3 ch.3 p.61-70','U (limité)'), '6.4':('F3 ch.4 p.90-91','I'), '6.5':('F3 ch.5 p.92-94','I'),
 },
 'UE3': {
  '1.1':('M (Dunod MCG) ch.1 p.1 ; cours prof. séance 3','A'), '1.2':('M ch.2 p.32 ; séances 1/5','I/A'), '1.3':('M ch.3 p.63','I'),
  '2.1':('M ch.4 p.112, ch.5 p.134','A'), '2.2':('M ch.6 p.158 ; séance 4','I'), '2.3':('M ch.7 p.188','A'),
  '2.4':('M ch.8 p.211','A'), '2.5':('M ch.9 p.234','A'), '2.6':('M ch.10 p.253 ; séance 6','A'), '2.7':('M ch.12 p.318','I'),
  '3.1':('M ch.12 p.318','I'), '3.2':('M ch.11 p.290','A'), '3.3':('M ch.13 p.345','A'), '4.1':('M ch.14 p.372','U (limité)'), '4.2':('M ch.15 p.398','I'),
 },
 'UE5': {
  '1.1':('S1 Position fonction informatique (10 p.)','I/A'), '1.2':('S2 Stratégie et gouvernance informatique (13 p.)','A'), '1.3':('S3 Urbanisation des SI (10 p.)','I/A'),
  '1.4':('SE (Expert DSCG UE5) p.79, 82, 209','A/I'), '2.1':('S4 Gestion de projets de SI (43 p.) ; S6','A/U'), '2.2':('S4 ; SE p.247, 254-257','A'),
  '2.3':('S6 Contrats de service (18 p.)','I'), '2.4':('S4/S6','A'), '2.5':('S12 Outils collaboratifs p.1','I'),
  '3.1':('S5 Progiciels de gestion intégrée (30 p.)','A/I'), '3.2':('S5','I'), '4.1':('S7 Gestion de la performance informatique (29 p.)','A'),
  '4.2':('S6 ; SE p.125','A'), '4.3':('S7','I'), '4.4':('S7','I'), '4.5':('S7','I'), '5.1':('S8 Architectures techniques','I/A'),
  '5.2':('SE p.160-163 ; fiche ACD13','A'), '5.3':('S9 Sécurité des SI ; note Drive UE5-07 « sécurité moderne »','A'),
  '6.1':('S10 Audit et gouvernance ; SE p.242-244 ; ACD11','I'), '6.2':('S10, S2','I'), '6.3':('SE p.292-305','I'), '6.4':('SE p.79, 296 ; ACD12','I'),
 },
}
COURS_NOTE = ("Supports : F1-F4 = fascicules INTEC UE212 2025/2026 (Drive, dossier « COURS 1-4 », aussi sous /Users/sacha/Documents/DSCG/UE 2 - Finance/Cours INTEC/) ; "
 "M = Livre Dunod MCG UE3 (/Users/sacha/Documents/DSCG/UE 3 - MCG/Ressources/) ; S1-S12 = cours/fiches de l'enseignante UE5 (/Users/sacha/Documents/DSCG/UE 5 - MSI/) ; "
 "SE = Expert DSCG UE5 (Drive « Expert DSCG UE 5.pdf »). Pages = pagination des sommaires relevée lors d'une session antérieure (Notion), non relue intégralement ici. "
 "Statut déclaré (Notion) : I = inconnu/pas de preuve, A = aidé/exposé, U = autonome sur une tâche précise.")
