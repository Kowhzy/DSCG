"""Reclassement des dossiers sur le texte officiel des programmes (passe 2, 24/09/2026) + étiquettes « techniques ».

Pourquoi : la 1re passe rattachait les dossiers à des définitions de rubriques supposées. Le texte officiel du programme
(00_sources_officielles/bulletin_officiel/programme_*.txt) montre notamment qu'en UE3 la rubrique 2.2 porte sur l'audit,
le contrôle interne et les risques (et non sur les coûts), que les prix de cession interne relèvent de 2.4, les coûts
cachés/dysfonctionnements de 3.2, les tableaux de bord sociaux et la masse salariale de 4.1, la RSE vue par le contrôle de
gestion de 1.2 ; en UE2 que les offres publiques (OPR) relèvent de 6.3 et la notation de 2.2 ; en UE5 que le BYOD et les
référentiels relèvent de 1.3 et la notion de PCA de 4.2.

Les techniques (facteur rare, coûts/marges/seuil, écarts…) ne sont pas toutes nommées par le programme : ce sont des
prérequis du DCG que les sujets mobilisent. Elles sont donc suivies à part, dans une colonne « techniques ».

Entrée/sortie : 02_data/UE*_dossiers.csv (colonnes rubriques_principales, rubriques_secondaires réécrites ; colonne
techniques ajoutée ou mise à jour). Journal : 03_analyses/reclassement_journal.csv (ancien → nouveau, justification).
Le script est idempotent.
"""
import csv, os

BASE = os.path.join(os.path.dirname(__file__), '..')

# (ue, annee, dossier) : (principales, secondaires, techniques, justification du changement ou '')
NEW = {
 # ---------------- UE2 ----------------
 ('UE2','2025','1'): ('1.2|4.1','4.3|1.1','MEDAF_beta|CMPC|VAN_TRI|flux_projet',''),
 ('UE2','2025','2'): ('6.3','4.2|4.3','LBO|tableau_amortissement',''),
 ('UE2','2025','3'): ('6.5|4.2|6.1','2.2','crowdfunding|dividende_theories|gouvernance',''),
 ('UE2','2024','1'): ('3.1|3.2|1.2','6.3|3.3','MEDAF_beta|DCF_FTD|multiples|prime_offre_publique',"OPR = « offres publiques » : 6.3 et non 6.2 (programme officiel 6.3)"),
 ('UE2','2024','2'): ('6.3|2.2','6.2|1.1','prime_offre_publique|droits_de_vote|gouvernance',"OPR/retrait obligatoire = offres publiques (6.3) ; 6.2 conservé en secondaire (opérations sur le capital)"),
 ('UE2','2024','3'): ('2.2','1.1','RSE_ESG|parties_prenantes|societe_a_mission',''),
 ('UE2','2023','1'): ('4.1','5.2|1.1','Black_Scholes|option_reelle',''),
 ('UE2','2023','2'): ('2.2|3.1|3.2|1.2','3.3|4.3','gouvernance|CMPC|covariance_risque|DCF_FTD|multiples|fonds_de_commerce',''),
 ('UE2','2023','3'): ('2.2|5.2','','RSE_ESG|notation|couverture_taux',''),
 ('UE2','2022-S1','1'): ('2.1','4.3','diagnostic_ratios',''),
 ('UE2','2022-S1','2'): ('2.2|6.1','1.1','RSE_ESG|gouvernance|dividende_theories',''),
 ('UE2','2022-S1','3'): ('6.3|6.1','','parite_fusion|BPA_relution|dividende_theories',''),
 ('UE2','2022-S2','1'): ('2.1','','diagnostic_ratios',''),
 ('UE2','2022-S2','2'): ('2.2','1.1','gouvernance',''),
 ('UE2','2022-S2','3'): ('1.1','','efficience_finance_comportementale',''),
 ('UE2','2022-S2','4'): ('2.2','','RSE_ESG|parties_prenantes',''),
 ('UE2','2021','1'): ('1.2|4.1|4.2','1.3|3.3','covariance_risque|MEDAF_beta|capital_investissement|immobilier|VAN_TRI|annuite_equivalente',''),
 ('UE2','2021','2'): ('6.3','','parite_fusion',''),
 ('UE2','2021','3'): ('5.2|6.5','','blockchain_crypto|couverture_change',''),
 ('UE2','2020','1'): ('2.2|1.3|4.2','1.2|6.5|6.1','EVA|CMPC|obligations_duration|crowdfunding',''),
 ('UE2','2020','2'): ('5.2|5.1','6.5','couverture_taux|netting_cash_pooling|blockchain_crypto',''),
 ('UE2','2020','3'): ('3.3','4.2','start_up_VC',''),
 ('UE2','2019','1'): ('2.1|3.1|5.2','1.2|4.3|6.4|2.2','diagnostic_ratios|TFT|notation|CMPC|DCF_FTD|obligations_duration|couverture_taux',"notation = 2.2 (« la notation et le scoring ») ajoutée en secondaire"),
 ('UE2','2019','2'): ('6.3|6.4','4.3','LBO|dissertation',''),
 ('UE2','2018','1'): ('1.2|2.1','1.3','covariance_risque|MEDAF_beta|diagnostic_ratios',''),
 ('UE2','2018','2'): ('4.2|6.5','','capital_investissement|dissertation',''),
 ('UE2','2017','1'): ('6.2|3.1|4.2','3.2','IPO|DCF_FTD|multiples',''),
 ('UE2','2017','2'): ('5.2','','couverture_change|dissertation',''),
 ('UE2','2016','1'): ('2.1|1.2|3.1','4.3|6.3','diagnostic_ratios|MEDAF_beta|CMPC|DCF_FTD',''),
 ('UE2','2016','2'): ('6.3','','fusions_acquisitions|dissertation',''),
 # ---------------- UE3 ----------------
 ('UE3','2025','1'): ('2.5|2.6|1.2','3.3','RSE|ecarts|parties_prenantes|note_synthese',"RSE vue par le CG = 1.2 (programme : « place du CG dans le DD et la RSE ») ; 3.3 passe en secondaire"),
 ('UE3','2025','2'): ('4.1|4.2','2.1','diagnostic_ressources_competences|competences|masse_salariale',''),
 ('UE3','2025','3'): ('2.4','2.1|2.2|2.6','PCI|integration_verticale|couts_transaction',"prix de cession interne/transfert = 2.4 (programme) ; 2.2 (risques, dont fiscal) en secondaire"),
 ('UE3','2024','1'): ('2.1|2.3|2.5','2.4','Porter_5F|tarification|previsions_resultat|strategies_generiques|note_synthese',"2.2 retiré : la grille de prix relève de 2.3 (tarification) et les prévisions de 2.5"),
 ('UE3','2024','2'): ('2.5|2.3|2.4','3.3|2.1','ecarts|facteur_rare|digital|franchise_plateforme|PESTEL',"2.2 retiré : facteur rare = technique de DCG mobilisée pour un choix de programme (2.5), pas une notion de 2.2"),
 ('UE3','2023','1'): ('2.1','','PESTEL|Porter_5F|scenarios|note_synthese',"2.5 retiré : aucune question de planification"),
 ('UE3','2023','2'): ('2.5|2.4|2.6','','ecarts|faire_faire_faire|parties_prenantes|note_synthese',"2.2 retiré : relocalisation/internalisation = gestion du périmètre (2.4) ; écarts = 2.5"),
 ('UE3','2023','3'): ('4.2|4.1|3.2','','competences|formation|QVT_attractivite|couts_caches|TBS',"coûts cachés = « analyse des dysfonctionnements » (3.2) ; TBS = 4.1"),
 ('UE3','2022','1'): ('2.1|2.3','','PESTEL|Porter_5F|strategies_generiques|marketing|digital',"2.5 retiré : aucune question de planification (corrigé)"),
 ('UE3','2022','2'): ('4.1|4.2','3.2|1.1','GEPP|KM|TBS|masse_salariale|couts_caches',"coûts cachés = 3.2 (secondaire) ; 3.3 retiré"),
 ('UE3','2022','3'): ('2.6','1.2','parties_prenantes|gouvernance|RSE',"RSE/DD = 1.2 plutôt que 3.3"),
 ('UE3','2021','1'): ('2.1','','SWOT|ocean_bleu',"2.5 retiré"),
 ('UE3','2021','2'): ('2.1|2.5','2.3','business_model',"business model = 2.1 (notion) et 2.5 (« analyser un business model »)"),
 ('UE3','2021','3'): ('4.1|4.2','1.1','integration_fidelisation|cout_turnover|seuil_rentabilite',"1.1 en secondaire (management libéré) ; 4.2 (rémunération, fidélisation) en principal"),
 ('UE3','2021','4'): ('1.2|2.5|4.2','3.3','remuneration|previsions_resultat|outils_CG',"BSPCE = rémunération (4.2) ; CA/rentabilité prévisionnels = 2.5"),
 ('UE3','2020','1'): ('2.1|2.3|2.5','','diagnostic_strategique|couts_marges_seuil|tarification|valeur_client|note_synthese',"2.2 retiré : tarification dynamique = 2.3 ; coûts/marges/seuil = technique mobilisée en 2.5"),
 ('UE3','2020','2'): ('3.2|3.3','3.1|2.2','diagnostic_processus|couts_caches|conduite_projet|tableau_de_bord|performance_globale',"audit interne vs diagnostic = 2.2 en secondaire"),
 ('UE3','2019','1'): ('1.1|1.2','3.3|2.6','Mintzberg|entreprise_liberee|RSE',"RSE/ISO 26000 = 1.2"),
 ('UE3','2019','2'): ('2.1|4.2','2.2','strategies_generiques|chaine_valeur|diagnostic_ressources_competences|competences|risques',''),
 ('UE3','2019','3'): ('2.4|2.5','2.1','modes_developpement|franchise_plateforme|ecarts|couts_marges_seuil',"2.2 remplacé par 2.1 (modalités de développement)"),
 ('UE3','2018','1'): ('2.1|2.6|3.2','1.2|3.3|3.1','strategies_generiques|parties_prenantes|RSE|couts_caches',"coûts cachés = 3.2 ; RSE = 1.2"),
 ('UE3','2018','2'): ('3.1|3.2','4.2|2.7','conduite_changement|progres_continu|apprentissage_organisationnel|rentabilite_actions',''),
 ('UE3','2017','1'): ('2.1','','PESTEL|SWOT',''),
 ('UE3','2017','2'): ('1.1|2.1','2.4|2.7','Mintzberg|Greiner|modes_developpement',"croissance internationale = modalités de développement (2.1)"),
 ('UE3','2017','3'): ('4.1','','masse_salariale|ecarts',"écarts de masse salariale = 4.1 (programme : « calculer les écarts et les effets de la masse salariale »)"),
 ('UE3','2016','1'): ('2.1|1.1|2.6','3.3','diagnostic_ressources_competences|strategies_generiques|Mintzberg|parties_prenantes',''),
 ('UE3','2016','2'): ('3.1|2.5','1.2|3.2','conduite_projet|valeur_acquise|ecarts|outils_CG',''),
 # ---------------- UE5 ----------------
 ('UE5','2025','1'): ('6.1|1.2|6.2','1.1|1.3|2.2','alignement_strategique|referentiels_COBIT_ITIL_ISO|methodologie_audit|Gantt|organisation_DSI',''),
 ('UE5','2025','2'): ('5.3|5.2','5.1|4.2|1.3','PSSI_DIC|PCA_PRA|Zero_Trust|BYOD_ShadowIT|IAM_MFA',"PCA = notion de 4.2 ; BYOD = 1.3 (programme) en secondaire"),
 ('UE5','2025','3'): ('1.4|6.4','1.1|2.5','BI_decisionnel|gouvernance_donnees|RGPD',''),
 ('UE5','2024','1'): ('1.3|3.2|2.4','3.1|2.2','urbanisation_strates|conduite_changement',''),
 ('UE5','2024','2'): ('1.2|4.1','1.1','alignement_strategique|indicateurs_SI',''),
 ('UE5','2024','3'): ('2.2|1.3','5.3|1.1|2.1|2.4|5.2','BYOD_ShadowIT|erreurs_gestion_projet|note_synthese',"BYOD = 1.3 (programme : « Bring Your Own Device ») ; 5.3 en secondaire"),
 ('UE5','2023','1'): ('3.1','5.2','GED|RGPD|conservation_legale|workflow',''),
 ('UE5','2023','2'): ('2.2|3.2','1.3|2.1','COPIL|methodes_projet|Gantt|urbanisation_strates',''),
 ('UE5','2023','3'): ('5.2|5.3','3.1|1.3','facturation_electronique|securite_SI|RGPD',''),
 ('UE5','2022','1'): ('1.1|1.3|5.1','2.1','gouvernance_SI|schema_architecture|FCS_projet',''),
 ('UE5','2022','2'): ('3.1|2.2','5.2','workflow|methodes_projet|facturation_electronique',''),
 ('UE5','2022','3'): ('2.1|5.2','3.1|4.5|5.1','SaaS_OnPremise|RGPD',''),
 ('UE5','2021','1'): ('1.1|1.2|4.3','4.1','organisation_DSI|schema_directeur|indicateurs_couts_SI',''),
 ('UE5','2021','2'): ('2.1|2.2|2.4','','FCS_projet|methodes_projet|Gantt',''),
 ('UE5','2021','3'): ('3.1|5.2','5.3|4.2','conservation_legale|workflow|dematerialisation|RGPD|PCA_PRA',"PCA/PRA = 4.2 en secondaire"),
 ('UE5','2020','1'): ('5.2','4.2','RGPD',''),
 ('UE5','2020','2'): ('5.3|5.2','2.5|4.2','PCA_PRA|securite_SI|RGPD',"PCA = 4.2 en secondaire"),
 ('UE5','2020','3'): ('3.1|3.2|2.2','5.3','ERP|conduite_changement|securite_SI',''),
 ('UE5','2019','1'): ('1.3','','urbanisation_strates',''),
 ('UE5','2019','2'): ('1.2|3.1|4.1','2.1','alignement_strategique|ERP|SaaS_OnPremise|indicateurs_SI',''),
 ('UE5','2019','3'): ('2.2','2.4','conduite_changement|Gantt',''),
 ('UE5','2018','1'): ('3.2|2.2','2.1','COPIL|FCS_projet|ERP',''),
 ('UE5','2018','2'): ('2.2','2.4','PERT|Gantt',''),
 ('UE5','2018','3'): ('5.2|5.3','5.1','securite_SI|chiffrement_VPN',''),
 ('UE5','2017','1'): ('1.2|1.4','1.1|6.4','alignement_strategique|BI_decisionnel',''),
 ('UE5','2017','2'): ('5.1|4.2|4.3','6.2|1.3','architecture_cloud|SLA|TCO|referentiels_COBIT_ITIL_ISO',"référentiel ITIL = 1.3 en secondaire"),
 ('UE5','2017','3'): ('2.1|4.1','2.5','indicateurs_SI',''),
 ('UE5','2016','1'): ('1.2|1.1|1.3','','alignement_strategique|organisation_DSI|urbanisation_strates',''),
 ('UE5','2016','2'): ('3.2|2.2|4.5','5.1|1.3','ERP|methodes_projet|referentiels_COBIT_ITIL_ISO|SaaS_OnPremise',"référentiels = 1.3 en secondaire"),
 ('UE5','2016','3'): ('5.2|6.2|6.3','6.1','chiffrement_VPN|audit_informatise',''),
}

# Libellés lisibles des techniques (pour les rapports)
LABELS = {
 'MEDAF_beta':'MEDAF, bêta (désendetté/réendetté)','CMPC':'CMPC','VAN_TRI':'VAN, TRI, conflits de critères','flux_projet':'Flux d\'un projet (BFR, IS, valeur de reprise)',
 'LBO':'Montage LBO','tableau_amortissement':'Tableaux d\'amortissement / annuités','crowdfunding':'Crowdfunding','dividende_theories':'Politique de dividende (théories)',
 'gouvernance':'Gouvernance (codes, agence, administrateurs)','DCF_FTD':'DCF / flux de trésorerie disponibles','multiples':'Multiples (comparables)',
 'prime_offre_publique':'Prime et fourchette d\'une offre publique','droits_de_vote':'Structure d\'actionnariat, droits de vote','RSE_ESG':'RSE / ESG / extra-financier',
 'parties_prenantes':'Parties prenantes','societe_a_mission':'Société à mission','Black_Scholes':'Black-Scholes','option_reelle':'Options réelles',
 'covariance_risque':'Covariance, variance, risque de portefeuille','fonds_de_commerce':'Évaluation d\'un fonds de commerce','notation':'Notation (financière / extra-financière)',
 'couverture_taux':'Couverture du risque de taux (swap, collar…)','diagnostic_ratios':'Diagnostic par ratios (ROCE, ROE, gearing…)','parite_fusion':'Parité d\'échange, fusion',
 'BPA_relution':'BPA : relution / dilution','efficience_finance_comportementale':'Efficience et finance comportementale','capital_investissement':'Capital-investissement',
 'immobilier':'Finance immobilière','annuite_equivalente':'Annuité équivalente / horizon commun','blockchain_crypto':'Blockchain, crypto-actifs','couverture_change':'Couverture du risque de change',
 'EVA':'EVA / création de valeur','obligations_duration':'Obligations (taux, duration, sensibilité)','netting_cash_pooling':'Netting / centralisation de trésorerie',
 'start_up_VC':'Évaluation de start-up (VC method)','TFT':'Tableau de flux de trésorerie','dissertation':'Dissertation (format pré-2020)','IPO':'Introduction en bourse',
 'fusions_acquisitions':'Fusions-acquisitions (qualitatif)',
 'RSE':'RSE / DD','ecarts':'Analyse d\'écarts','note_synthese':'Note de synthèse','diagnostic_ressources_competences':'Diagnostic ressources / compétences',
 'competences':'Gestion des compétences','masse_salariale':'Masse salariale (effets niveau/masse/report)','PCI':'Prix de cession interne / de transfert',
 'integration_verticale':'Intégration verticale','couts_transaction':'Coûts de transaction','Porter_5F':'5 (+1) forces de Porter','tarification':'Tarification / grille de prix',
 'previsions_resultat':'Prévisions de CA / résultat','facteur_rare':'Optimisation sous contrainte (facteur rare)','digital':'Marketing digital',
 'franchise_plateforme':'Franchise / plateforme','PESTEL':'PESTEL','scenarios':'Scénarios','faire_faire_faire':'Faire ou faire-faire (relocalisation)',
 'formation':'Plan de formation','QVT_attractivite':'QVT, attractivité','couts_caches':'Coûts cachés (Savall-Zardet)','TBS':'Tableau de bord social',
 'strategies_generiques':'Stratégies génériques','marketing':'Marketing stratégique / mix','GEPP':'GEPP / GPEC','KM':'Knowledge management (SECI)',
'SWOT':'SWOT','ocean_bleu':'Océan bleu','business_model':'Business model (canvas)','integration_fidelisation':'Intégration, fidélisation',
 'cout_turnover':'Coût du turnover','seuil_rentabilite':'Seuil de rentabilité d\'une décision','remuneration':'Rémunération (dont BSPCE)','outils_CG':'Outils de contrôle de gestion',
 'diagnostic_strategique':'Diagnostic stratégique (démarche)','couts_marges_seuil':'Coûts, marges, seuil de rentabilité','valeur_client':'Valeur client / offre',
 'diagnostic_processus':'Diagnostic des processus','conduite_projet':'Conduite de projet','tableau_de_bord':'Tableau de bord de pilotage','performance_globale':'Performance globale',
 'Mintzberg':'Configurations de Mintzberg','entreprise_liberee':'Entreprise libérée','chaine_valeur':'Chaîne de valeur','risques':'Risques',
 'modes_developpement':'Modes de développement','conduite_changement':'Conduite du changement','progres_continu':'Progrès continu',
 'apprentissage_organisationnel':'Apprentissage organisationnel','rentabilite_actions':'Rentabilité d\'un plan d\'actions','Greiner':'Modèle de Greiner','valeur_acquise':'Valeur acquise (projet)',
 'alignement_strategique':'Alignement stratégique','referentiels_COBIT_ITIL_ISO':'Référentiels (COBIT, ITIL, ISO)','methodologie_audit':'Méthodologie d\'audit SI',
 'Gantt':'Gantt','organisation_DSI':'Organisation de la DSI','PSSI_DIC':'PSSI (DIC)','PCA_PRA':'PCA / PRA (RTO, RPO)','Zero_Trust':'Zero Trust',
 'BYOD_ShadowIT':'BYOD / Shadow IT','IAM_MFA':'IAM, MFA, MDM','BI_decisionnel':'BI / décisionnel','gouvernance_donnees':'Gouvernance des données','RGPD':'RGPD',
 'urbanisation_strates':'Urbanisation, strates du SI','indicateurs_SI':'Indicateurs de performance/qualité du SI','erreurs_gestion_projet':'Diagnostic d\'un projet (erreurs)',
 'GED':'GED','conservation_legale':'Conservation légale des documents','workflow':'Workflow (facture)','COPIL':'Comité de pilotage','methodes_projet':'Méthodes de projet (V, agile)',
 'facturation_electronique':'Facturation électronique','securite_SI':'Sécurité du SI','gouvernance_SI':'Gouvernance du SI','schema_architecture':'Schéma d\'architecture',
 'FCS_projet':'FCS / risques d\'un projet','SaaS_OnPremise':'SaaS vs On Premise','schema_directeur':'Schéma directeur','indicateurs_couts_SI':'Indicateurs de coût du SI',
 'dematerialisation':'Dématérialisation (copie fiable)','ERP':'ERP / PGI','PERT':'PERT','chiffrement_VPN':'Chiffrement, VPN','architecture_cloud':'Architecture, cloud, virtualisation',
 'SLA':'SLA / contrat de service','TCO':'TCO','audit_informatise':'Audit en milieu informatisé',
}

def run():
    journal = []
    for ue in ('UE2', 'UE3', 'UE5'):
        p = os.path.join(BASE, '02_data', f'{ue}_dossiers.csv')
        rows = list(csv.DictReader(open(p, encoding='utf-8'), delimiter=';'))
        fields = list(rows[0].keys())
        if 'techniques' not in fields:
            fields.insert(fields.index('competences') + 1, 'techniques')
        seen = set()
        for r in rows:
            k = (ue, r['annee'], r['dossier'])
            assert k in NEW, f'dossier non reclassé : {k}'
            seen.add(k)
            P, S, T, why = NEW[k]
            for t in T.split('|'):
                assert t in LABELS, f'technique sans libellé : {t}'
            if (r['rubriques_principales'], r['rubriques_secondaires']) != (P, S):
                journal.append([ue, r['annee'], r['dossier'], r['rubriques_principales'], r['rubriques_secondaires'], P, S,
                                (why.replace(' ; ', ' · ')) or 'ajustement mineur de cohérence avec le programme officiel'])
            r['rubriques_principales'], r['rubriques_secondaires'], r['techniques'] = P, S, T
        assert seen == {k for k in NEW if k[0] == ue}, 'clés NEW sans dossier'
        with open(p, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fields, delimiter=';')
            w.writeheader(); w.writerows(rows)
    jp = os.path.join(BASE, '03_analyses', 'reclassement_journal.csv')
    if journal or not os.path.exists(jp):
        with open(jp, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f, delimiter=';')
            w.writerow(['ue', 'annee', 'dossier', 'P_avant', 'S_avant', 'P_apres', 'S_apres', 'justification'])
            w.writerows(journal)
    print(len(journal), 'dossiers modifiés')

if __name__ == '__main__':
    run()
