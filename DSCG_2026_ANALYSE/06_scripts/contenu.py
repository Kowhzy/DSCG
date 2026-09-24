"""Contenu rédigé (analyse) par UE. Toute donnée chiffrée citée ici est recalculée/contrôlée dans build_report.py
à partir de 02_data et 03_analyses (fonction de contrôle `controles`)."""

TITRES = {
 'UE2': "DSCG 2026 — UE2 Finance — Analyse des annales, rapports du jury et priorités de révision",
 'UE3': "DSCG 2026 — UE3 Management et contrôle de gestion — Analyse des annales, rapports du jury et priorités de révision",
 'UE5': "DSCG 2026 — UE5 Management des systèmes d'information — Analyse des annales, rapports du jury et priorités de révision",
}

EPREUVE = {
 'UE2': "Écrit de 3 heures, coefficient 1 ; calculatrice en mode examen autorisée ; 3 dossiers indépendants depuis 2020 (sujets 2023-2024 notés sur 20, 2025 sur 50) [DSCG UE2 2023-2025, page de garde]. Date 2026 : non vérifiée dans les sources consultées.",
 'UE3': "Écrit de 4 heures (coefficient 1,5 en 2019 selon la page de garde du sujet ; coefficient 2026 : non vérifié) ; 2 à 4 dossiers ; 2025 : 3 dossiers sur 20 points (8/6/6) [DSCG UE3 2025, page de garde]. Date 2026 : non vérifiée.",
 'UE5': "Écrit de 3 heures, coefficient 1, aucun document ni matériel (calculatrice interdite) ; 3 dossiers ; noté sur 40 points depuis 2024 (14/14/12 en 2024, 18/12/10 en 2025) [DSCG UE5 2024-2025]. Date de l'épreuve : jeudi 22 octobre 2026, 9h30-12h30 selon ta convocation (note Drive « UE5-01-cadrage-et-programme »).",
}

SYNTHESE = {
 'UE2': [
  "Référentiel applicable : programme de l'arrêté du 13 février 2019 (1re session en 2020). La réforme du 4 août 2025 ne s'applique qu'à partir de la session 2027 : la session d'octobre 2026 est la dernière sur le programme 2019.",
  "Socle calculatoire quasi systématique : « la valeur et le risque » (bêta, MEDAF, CMPC) est présent dans chacune des trois dernières sessions (2023, 2024, 2025) et dans 6 sessions sur 10 depuis 2016. En 2025, le coût du capital d'une société non cotée par comparables reprend exactement la mécanique du sujet 2016.",
  "La gouvernance et l'extra-financier (RSE/ESG, parties prenantes, agence, Copé-Zimmermann, société à mission) sont la rubrique la plus présente depuis la réforme (4 sessions sur 6 en principal ; en 2025 seulement en toile de fond). Le jury 2024 en fait un attendu explicite : « la performance durable de l'entreprise est autant à prendre en considération que les performances financière et économique ».",
  "Depuis 2020, la « question de réflexion » (25 % des points) a disparu : elle est remplacée par de petites questions de cours insérées dans le cas [Rapport du jury 2020, p. 7]. Chaque sujet combine désormais un dossier calculatoire et des questions de restitution argumentée.",
  "Le jury 2025 rappelle que les acquis du DCG (VAN, TRI, annuités constantes, tableaux d'amortissement) « peuvent légitimement faire l'objet de questions ». Il déplore la faible maîtrise du LBO et un dossier 3 (crowdfunding, dividende) sacrifié faute de temps.",
  "Session très volatile : taux de réussite de 14,75 % (2023) à 52,49 % (2022), et 43,00 % en 2025 [Rapports du jury 2024 et 2025, p. 18-19]. Le pic de 2022 s'explique par le sujet de secours « conçu sans besoin de faire de calculs », une « exception » selon le jury [Rapport du jury 2022, p. 9]. Le socle technique est discriminant.",
 ],
 'UE3': [
  "Référentiel applicable : programme de 2019 (1re session en 2020 ; selon le jury, le contenu de l'UE3 « n'a pas été profondément modifié avec la réforme ») ; la réforme de 2025 ne vaut qu'à partir de 2027.",
  "Le diagnostic stratégique (PESTEL, Porter, SWOT, ressources/compétences, business model) est présent dans 9 sessions sur 10 depuis 2016 (en toile de fond seulement en 2025). Le jury 2024 relève cependant des erreurs de choix d'outil : PESTEL ou SWOT au lieu des 5 forces pour le micro-environnement.",
  "Rupture 2024-2025 : le contrôle de gestion « fait part égale avec le management » [Rapport du jury 2024, p. 24 ; confirmé en 2025, p. 28]. Les calculs (écarts, facteur rare, masse salariale, prix de cession interne) sont redevenus centraux.",
  "Faiblesse n°1 signalée par le jury 2025 : « la décomposition des écarts et [l]es différents effets de la masse salariale ». La masse salariale était déjà ratée en 2022 : « pas compliqué mais peu de candidat[s] ont réussi » [Rapport du jury 2022, p. 10]. Les écarts figurent dans chacune des trois dernières sessions (2023, 2024, 2025) ; la masse salariale est calculée en 2017, 2022 et 2025 et la gestion des RH est en principal dans 5 sessions sur 10.",
  "Pilotage et performance : les techniques sont fréquentes (coûts cachés dans 4 sessions : 2018, 2020, 2022, 2023 ; tableau de bord social en 2022 et 2023), mais le programme les range en 3.2 (dysfonctionnements) et 4.1 (TBS). La rubrique 3.3 (KPI, tableaux de bord stratégiques, performance globale) n'est en principal qu'en 2020.",
  "Correction par rapport à la 1re version de cette étude : selon le texte officiel, la rubrique 2.2 porte sur l'audit, le contrôle interne et les risques ; elle n'a jamais été interrogée en principal. Les calculs de coûts (facteur rare en 2024 ; coûts, marges et seuil en 2019-2020) sont des techniques du DCG mobilisées au service de 2.5 (planification, choix de programme) et de 2.3 (tarification). Ils restent à maîtriser : voir le tableau des techniques (section 5.6).",
  "Le marketing (notamment digital) est la partie la plus abandonnée selon le jury 2022 : « La partie marketing n'est pas maîtrisée et souvent abandonnée » [Rapport du jury 2022, p. 10]. La rubrique 2.3 est en principal en 2020, 2022 et 2024 (en toile de fond en 2021).",
  "Chute du taux de réussite : de 50,14 % en 2024 à 17,28 % en 2025, avec une moyenne de 7,08 [Rapport du jury 2025, p. 10 et 19]. Le niveau technique et la contextualisation sont devenus discriminants.",
 ],
 'UE5': [
  "Référentiel applicable : programme de 2019 (140 h ; 1re session en 2020) ; la réforme de 2025 (Zero Trust, NIS2, IA, Green IT, MiCA) ne s'applique qu'à partir de la session 2027. Le sujet 2025 montre toutefois une lecture extensive du programme de 2019 (Zero Trust, RTO/RPO, BI).",
  "La conduite de projet SI est le thème le plus constant : en principal dans 8 sessions sur 10, et un diagramme de Gantt (ou un PERT) est demandé en 2018, 2019, 2021, 2023 et 2025.",
  "Droit et sécurité de l'information (RGPD/DPO, conservation, dématérialisation, cryptographie) : 7 sessions sur 10 ; le RGPD est mobilisé dans chacune des 5 sessions 2020-2023 et en 2025. Surveillance et prévention (PSSI, PCA/PRA, Shadow IT, Zero Trust) figure dans chacune des 3 dernières sessions (en principal en 2023 et 2025, en toile de fond en 2024).",
  "Alignement stratégique et schéma directeur : 6 sessions sur 10, et c'est la notion que le jury critique le plus (2024 et 2025) : copies « sans fondements théoriques solides », alignement « réduit à un choix technique ».",
  "2025 ouvre de nouveaux champs : audit du SI (COBIT, ISO 27001, méthodologie de mission) comme « socle structurant », Zero Trust et BI/Data Science. Le jury rappelle qu'un point faible une année peut être réinterrogé dès l'année suivante [Rapport du jury 2025, p. 21].",
  "Changements de format : notation sur 40 points depuis 2024, calculatrice interdite, formats imposés (note de 20 lignes). Le taux de réussite chute de 57,85 % (2024) à 38,87 % (2025).",
 ],
}

SURPRISES = {
 'UE2': [
  "2022 : l'épreuve du 25 octobre 2022 a été annulée et repassée le 5 janvier 2023 (arrêté publié au BO ESR n°46 de 2022, référence ESRS2233990A, repérée par recherche web, non ouverte). Le rapport du jury 2022 (p. 9) tranche : « le sujet de secours a été activé » ; c'est le sujet Energy+ en 4 parties égales, « conçu sans besoin de faire de calculs » par exception. C'est lui qui compte pour la session 2022 ; le sujet initial (Sopra Steria, 2022-S1) reste une annale d'entraînement, exclue des statistiques.",
  "2023 : taux de réussite de 14,75 % et médiane de 6/20, les plus bas de la période [Rapport du jury 2024, p. 10 et 18]. Le sujet combinait options réelles (Black-Scholes), CMPC/covariance, DCF, multiples et swap de taux. Le rapport 2023 n'a pas été consulté : l'explication officielle n'est pas vérifiée.",
  "Fraude et blanchiment (5.3) n'a jamais été interrogé en UE2 sur la période (le blanchiment est apparu en UE1 en 2024 [Rapport du jury 2024, p. 20]). La structure de financement (4.3) n'apparaît qu'en toile de fond (CMPC, levier).",
 ],
 'UE3': [
  "Rubriques jamais interrogées en principal sur 10 ans : 1.3 (contrôle de gestion et systèmes d'information), 2.2 (contrôle de gestion face à l'audit, au contrôle interne et aux risques) et 2.7 (contrôle de gestion et changement organisationnel). Le management du changement (3.1) n'est plus apparu depuis 2018, alors que les jurys 2020 et 2021 en font un « point majeur ».",
  "2025 : format resserré à 20 points (8/6/6) et sujet jugé « court » ; le candidat est placé dans l'entreprise, et non plus en cabinet comme en 2024.",
  "La rubrique « gestion du périmètre » (internalisation/relocalisation, franchise, marketplace, prix de transfert) est présente dans chacune des 3 dernières sessions.",
 ],
 'UE5': [
  "La partie 4 « gestion de la performance informationnelle » (30 h sur 140 au programme officiel) est peu interrogée depuis 2020 hors indicateurs (2024) : contrats de services, budgets et évaluation des projets n'y ont jamais été interrogés en principal ; coûts seulement en 2021 (indicateurs de coût). La notion de PCA relève officiellement de 4.2 : elle a été mobilisée en 2020, 2021 et 2025.",
  "Maintenance (2.3), gestion des connaissances (2.5) et audit assisté (6.3, dernière apparition en 2016) forment les zones du programme jamais ou très rarement évaluées.",
  "2025 : le jury juge le sujet « tout à fait conforme au programme officiel » tout en y intégrant Zero Trust, RTO/RPO et BI, des notions absentes de ton cours de sécurité selon ta note Drive « UE5-07 sécurité moderne ».",
 ],
}

TROUS = {
 'UE2': {
  '6.2': "IPO en 2017 (ancien programme) ; l'OPR de 2024 relève des offres publiques (6.3). Rachats d'actions, opérations sur le nombre d'actions, APA et scission : jamais interrogés sur la période. Fiche mécanismes et effets (BPA, signal).",
  '5.3': "Jamais interrogé en UE2 depuis 2016. Rubrique courte : vigilance, TRACFIN, déclaration de soupçon, signaux d'alerte. Une question de cours de 1 à 2 points reste possible ; 30 min de fiche suffisent.",
  '6.4': "Seulement dans la réflexion 2019 (ancien programme). Titrisation et défaisance : définitions, intérêts, risques.",
  '4.3': "Jamais interrogé seul, mais sous-jacent à tout calcul de CMPC et de levier (2016, 2019, 2023, 2025). Théories de Modigliani-Miller, du compromis et du financement hiérarchique : mobilisables en question de réflexion.",
  '5.1': "Seulement 2020 (netting). Centralisation de trésorerie et cash pooling à connaître.",
  '1.3': "Obligations (duration, sensibilité) en 2020, EVA en 2020 ; gestion de portefeuille et patrimoine absents depuis 2018.",
  '3.3': "Start-up (2020), fonds de commerce (2023, en toile de fond) ; immobilier cité par les jurys 2019-2020 comme « nouveauté » (vu en investissement en 2021).",
 },
 'UE3': {
  '1.3': "Jamais interrogé : ERP, mégadonnées, circulation de l'information au service du contrôle de gestion.",
  '2.7': "Jamais interrogé en principal, alors que les jurys 2020-2021 citent « la mise en œuvre stratégique et la gestion du changement et des transformations ».",
  '3.1': "Absent depuis 2018 (conduite du changement, styles, résistances, progrès continu vs projet). Les annales 2016 D2 et 2018 D2 sont les meilleures ressources.",
  '2.2': "Jamais en principal : positionner le contrôle de gestion face à l'audit (interne/externe, légal/contractuel) et au contrôle interne, identifier les risques de l'entité, communication financière. Seulement en toile de fond (2019 D2-D3 : risques ; 2020 D2 : audit vs diagnostic ; 2025 D3 : risque fiscal). Fiche de définitions et de liens CG/audit/CI.",
  '3.2': "Coûts cachés et dysfonctionnements : 2018 D1, 2020 D2, 2023 D3 (et 2022 D2 en toile de fond). Coûts cibles et analyse de la valeur, pourtant cités par le programme, n'ont jamais été interrogés sur la période.",
  '1.2': "En principal en 2019 D1 (RSE), 2021 D4 (rôle du contrôleur en start-up) et 2025 D1 (RSE et redevance de pollution) : la RSE vue par le contrôle de gestion est revenue en 2025.",
 },
 'UE5': {
  '4.2': "Contrat de services (SLA, infogérance, réversibilité) : seulement 2017 (ancien programme). Pourtant, les environnements « externalisation, cloud, contractualisation des prestataires » sont cités par le jury 2020.",
  '4.3': "Coûts du SI / TCO : 2017 (TCO) et 2021 (indicateurs de coût). Une question de coût complet ou de TCO sans calculatrice reste plausible sous forme qualitative.",
  '4.4': "Budgets du SI : jamais interrogés sur la période.",
  '4.5': "Évaluation des projets (ROI, coûts-avantages) : seulement 2016 et, en toile de fond, 2022 (SaaS vs On Premise).",
  '2.3': "Maintenance (corrective, évolutive, TMA) : jamais interrogée en principal.",
  '2.5': "Gestion des connaissances : jamais en principal (seulement en toile de fond en 2017, 2020 et 2025).",
  '6.3': "Audit assisté par ordinateur : 2016 uniquement.",
 },
}

ANNALES = {
 'UE2': [
  ("2025 (sujet entier, 3 h)", "À refaire absolument en conditions réelles : coût du capital d'une société non cotée par comparables, VAN/TIR et conflit de critères, LBO (holding, dettes senior/junior, annuités constantes), crowdfunding, neutralité du dividende. Couvre les trois faiblesses citées par le jury 2025."),
  ("2024 D1 + D2", "Enchaînement MEDAF → DCF (FTD) → multiples → prime et fourchette d'OPR ; gouvernance post-OPR (droits de vote, Copé-Zimmermann, signal). Le jury 2024 relève des lacunes sur les FTD."),
  ("2024 D3 + 2022-S2 D4", "RSE/ESG, parties prenantes (Freeman), société à mission, matérialité : rédaction courte et contextualisée."),
  ("2023 D2", "Gouvernance (mécanismes, administrateurs indépendants) + CMPC, covariance, DCF, multiples, fonds de commerce : le dossier le plus complet sur l'évaluation."),
  ("2023 D1 + D3", "Options réelles (Black-Scholes) et swap de taux : dossiers techniques de la session la plus difficile (14,75 % de réussite)."),
  ("2022-S1 D3 (sujet annulé, entraînement)", "OPE : parité, prime, dividende exceptionnel, transfert de richesse, BPA relutif/dilutif."),
  ("2021 D1 + D3", "Bêta/MEDAF, capital-investissement, VAN, annuité équivalente, horizon commun ; change (terme vs option) et crypto-actifs."),
  ("2020 (sujet entier)", "EVA, duration/sensibilité, crowdfunding, collar, netting, blockchain, Venture Capital Method : le panorama le plus large des « nouveautés » 2019."),
  ("2016 Partie 1 (ancien programme)", "Bêta d'activité de comparables → bêta des CP → CMPC → DCF : même mécanique que 2025 D1, excellent entraînement technique."),
  ("2022-S2 D2 + D3", "Efficience (Fama), finance comportementale, AFEP-MEDEF : théorie pure, en réponse à la critique « concepts théoriques fondamentaux » (jury 2024-2025)."),
 ],
 'UE3': [
  ("2025 (sujet entier, 4 h)", "À refaire absolument : schéma d'écarts à construire (redevance), effets sur la masse salariale, compétences distinctives, prix de transfert, parties prenantes. Ce sont les faiblesses n°1 du jury 2025."),
  ("2024 (sujet entier)", "Porter pour le micro-environnement (et non PESTEL), grille tarifaire, écarts de CA, facteur rare, marketing digital, marketplace, franchise ; TPE de services."),
  ("2023 D2", "Écarts sur marge (volume, prix/coût), gain d'une relocalisation (analyse différentielle), cartographie des parties prenantes."),
  ("2023 D3 + 2022 D2", "Compétences, formation, GEPP, knowledge management, coûts cachés, tableau de bord social, masse salariale."),
  ("2017 D3 (ancien programme)", "Masse salariale : variation par catégorie, écarts de salaire/composition/effectif, effets de niveau, de masse et de report. La référence technique sur les effets."),
  ("2019 D3 (ancien programme)", "Décomposition des écarts de marge de production, contributions par canal, franchise."),
  ("2020 D2 + D1 partie B", "Diagnostic des processus, coût des dysfonctionnements, tableau de bord et indicateurs de performance globale ; coûts, seuil, valeur client."),
  ("2018 D2 + 2016 D2", "Conduite du changement, styles, progrès continu ; pilotage de projet par la valeur acquise et les écarts. Zones peu interrogées récemment."),
  ("2021 D2 + D4", "Business model canvas, outils de contrôle de gestion en start-up (rôle du contrôleur)."),
 ],
 'UE5': [
  ("2025 (sujet entier, 3 h)", "À refaire absolument : alignement stratégique, COBIT vs ISO 27001, méthodologie d'audit avec Gantt, PSSI (DIC), PCA/PRA (RTO/RPO), Zero Trust, BI (ETL, entrepôt), rôle de la DSI."),
  ("2024 (sujet entier)", "Strates du SI, choix d'un CRM après acquisition, résistance au changement, alignement (modèle à citer), indicateurs de performance et de qualité, BYOD et Shadow IT, erreurs de conduite de projet."),
  ("2023 D2 + D1", "COPIL, méthode de projet, Gantt d'un programme de bascule, urbanisation ; GED (indexation, conservation), RGPD."),
  ("2021 (sujet entier)", "Organisation de la DSI, schéma directeur, indicateurs de coût, FCS/risques, deux méthodes de projet, Gantt, SI achats et RGPD."),
  ("2022 (sujet entier)", "Gouvernance SI, architecture cible, workflow facture, Factur-X, SaaS vs On Premise, mutualisation du DPO."),
  ("2020 Q1-Q15", "RGPD complet : DPO, AIPD, registre, consentement, sous-traitants, continuité et formation."),
  ("2018 D2 + D3", "PERT/chemin critique ; VPN et clés de chiffrement : seul entraînement « cryptographie » récent."),
  ("2017 D2", "SLA/ITIL, TCO, virtualisation : le seul dossier sur la partie « performance informationnelle » (zone peu interrogée)."),
  ("2016 D3", "Audit en environnement informatisé et audit assisté par ordinateur (6.2/6.3)."),
 ],
}

METHODE_COMMUNE = [
 ("Question directrice", "Compte tenu du programme officiel, des attentes du jury, des annales et de tes ressources, quelles compétences maîtriser en priorité pour la session 2026 ? L'étude ne prédit pas le sujet : elle hiérarchise l'effort de révision."),
 ("Période", "Sessions 2016 à 2025 (10 sessions). Rupture : le programme de l'arrêté du 13 février 2019 s'applique depuis la session 2020 [Rapport du jury 2020, p. 6-9]. Les sessions 2016-2019 (ancien programme) sont projetées sur les rubriques actuelles à titre indicatif et pèsent moins dans l'indice (voir critères). La session 2026 est la dernière sur le programme 2019 : la réforme du 4 août 2025 (BO ESR du 28 août 2025) s'applique à partir de 2027 (sources secondaires concordantes : Compta Online, note Drive ; texte officiel non ouvert)."),
 ("Unité d'analyse", "Le dossier (ou bloc de questions pour UE5 2020). Chaque dossier est rattaché à une ou plusieurs rubriques officielles : « principale » (P) si une question au moins la mobilise directement, « secondaire » (s) si elle n'intervient qu'en toile de fond. Un dossier peut donc compter pour plusieurs rubriques."),
 ("Fréquences", "Une session compte 1 pour une rubrique si au moins un dossier la mobilise en principal (plusieurs dossiers de la même session ne comptent qu'une fois). Fréquence sur 10 sessions (2016-2025), sur le programme actuel (6 sessions 2020-2025), sur les 5 et les 3 dernières. UE2 2022 : seul le sujet de secours réellement composé (2022-S2) est compté ; le sujet annulé (2022-S1) est conservé comme entraînement, avec un poids nul."),
 ("Poids", "Part du barème : points du dossier / total du sujet, répartis à parts égales entre les rubriques principales du dossier. « Poids quand présent » = part moyenne du barème les années où la rubrique est présente (2020-2025). UE3 2024 : points non disponibles, les deux parties sont réputées « d'égale importance » (jury)."),
 ("Indice de priorité de révision (IPR, 0-100)", "Somme pondérée de 9 critères normalisés entre 0 et 1 : fréquence 2016-2025 (15) ; fréquence 2020-2025 (20) ; fréquence 2023-2025 (10) ; poids quand présent, plafonné à 50 % du barème (10) ; nombre de rapports du jury citant la rubrique (15) ; nombre de difficultés de candidats signalées par le jury (10) ; transversalité, c'est-à-dire le nombre de rubriques co-mobilisées depuis 2020 (10) ; poids dans le programme officiel (5 ; volume horaire de la partie divisé par son nombre de rubriques) ; « zone à ne pas négliger » = absente des 3 dernières sessions (5). L'IPR n'est PAS une probabilité de tomber."),
 ("Catégories", "IPR ≥ 60 : priorité maximale ; 45-60 : très élevée ; 32-45 : élevée ; 20-32 : à maîtriser ; < 20 : complément. Règle correctrice : une rubrique signalée comme faiblesse par le jury 2025 n'est jamais classée sous « très élevée », car le jury écrit qu'« un point retenu pour une session qui présente un niveau trop faible peut être retenu dès l'année suivante » [Rapport du jury 2025, p. 21]."),
 ("Raisonnements écartés", "« Tombé en 2025 donc pas en 2026 » est explicitement contredit par le jury 2025. « Absent depuis 5 ans donc il va tomber » n'est pas une preuve : l'absence récente ne pèse que 5 points sur 100 et sert à signaler des zones à ne pas négliger."),
 ("Rattachement aux rubriques (passe 2)", "Chaque dossier a été reclassé sur le texte officiel des rubriques (notions et contenus) ; 30 rattachements ont été corrigés par rapport à la 1re version (journal : 03_analyses/reclassement_journal.csv). Les techniques mobilisées (écarts, facteur rare, MEDAF, Gantt, RGPD…) sont suivies à part (colonne « techniques »), car le programme ne les nomme pas toutes : ce sont souvent des prérequis du DCG."),
 ("Robustesse", "Le classement a été recalculé sous 7 jeux de pondérations (référence, égalitaire, fréquences seules, jury renforcé, récence renforcée, sans « zone à ne pas négliger », barème renforcé). Pour chaque rubrique, on donne son rang minimal et maximal (section 5.5). Une priorité est jugée robuste si elle reste dans le premier tiers dans tous les scénarios."),
 ("Corrigés", "Les éléments indicatifs de corrigé 2020-2025 ont été lus question par question pour les 3 UE ; les attendus, pièges et erreurs repérées sont reportés en section 10 et dans 02_data/UE*_attendus_corriges.csv. Les chiffres des corrigés ont été recalculés quand c'était possible : les écarts constatés sont signalés comme « ALERTE »."),
 ("Limites", "Pas de rapport du jury pour la session 2023 : selon toi, aucun n'a été publié (information non vérifiée sur le site officiel, inaccessible depuis l'environnement d'analyse) ; les résultats 2023 proviennent des tableaux pluriannuels du rapport 2024. Rapport 2022 lu intégralement. Annexe officielle du programme non ouverte directement (domaine bloqué) : son texte a été relu dans sa reproduction en tête des manuels Dunod UE2 et UE3 et dans le document « Programme MSI 19-20 » (UE5) ; les notions affichées sont un résumé fidèle de ce texte. Sujets : copies FicheBEN des sujets officiels (filigrane) ou PDF texte du Drive. UE3 2024 : sujet non consulté, mais questions vérifiées sur le corrigé officiel, qui reproduit les énoncés ; points non communiqués. UE5 2024 et UE2 2024 : corrigés scannés, lus en image. Les rattachements aux rubriques relèvent d'un jugement d'analyste ; ils sont tous traçables dans 02_data. Ton Mac n'était pas accessible : tes ressources ont été repérées via Notion et Google Drive."),
]
