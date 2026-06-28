# Plan détaillé du Manuel Qualité — STE MEZZALUNA SARL
*Produit par : architecte-manuel — Étape 4 du pipeline*
*Croise le plan-type réglementaire (`referentiel-et-plan-type.md`) et l'inventaire des sources (`inventaire-documentaire.md`).*

> **⚠️ POINT DE CONTRÔLE UTILISATEUR :** ce plan détaillé **doit être validé explicitement avant le lancement de la rédaction**. Voir la note finale et les arbitrages demandés.

**Légende sources :** `MQ` = Manuel_Qualite.docx ; `AD` = Analyse_des_dangers ; `P-Trac/P-Stock/P-Bat/P-Dechets` = procédures ; `Pol` = Politique ; `Diag` = Diagramme fabrication ; `Org` = Organigramme ; `EqHACCP` = tableau équipe HACCP ; `Conv-*` = conventions ; `FDS/FT` = fiches produits N&D ; `ENR-*` = formulaires d'enregistrement.
**Légende couverture :** 🟢 source complète · 🟡 source partielle · 🔴 à créer/obtenir.

---

## CHAPITRE 0 — Pages de garde & gestion documentaire

| ID | Titre | Objectif | Sources | Manque | Exig. grille |
|---|---|---|---|---|---|
| 0.1 | Identification de l'entreprise | Identifier juridiquement l'établissement et l'objet du manuel | 🟢 MQ §1 ; Conv-* (MF, adresses) | RNE/statuts, n° agrément éventuel | Plans/identité |
| 0.2 | Objet, champ d'application, exclusions | Délimiter ce que couvre le manuel (site Menzel Temime, gamme pâtes fraîches) | 🟢 MQ §1 ; AD §1 | — | Cadre général |
| 0.3 | Gestion documentaire (versions, approbation, diffusion) | Tableau de gestion : rédacteur/vérificateur/approbateur, indices de révision | 🟡 gabarits ENR (cartouches) | Noms/dates/visas réels | Maîtrise documentaire |
| 0.4 | Glossaire & abréviations | Définir PMS, BPH/BPF, CCP, PRP/PRPo, DLC, MAP, MP/PF/PSF… | 🟢 dispersé dans MQ, P-Trac, P-Stock | — | Lisibilité instructeur |

## CHAPITRE 1 — Cadre réglementaire & engagement de la direction *(chapitre NOUVEAU — corrige la lacune majeure)*

| ID | Titre | Objectif | Sources | Manque | Exig. grille |
|---|---|---|---|---|---|
| 1.1 | Politique sécurité des aliments & engagement direction | Reprendre la politique signée (FR + AR) | 🟢 Pol ; MQ §5 | Date/version à jour | Engagement direction |
| 1.2 | Référentiel réglementaire tunisien | Lister Loi 2019-25, décret 2024-716, arrêté Santé 11/03/2025, arrêté Agriculture 26/05/2006, NT 09.14 | 🟢 referentiel-et-plan-type §4 | Confirmation textes (cf. note incertitude) | Base légale |
| 1.3 | Autorités compétentes (INSSPA, ANCSEP/ANER, DGSV) | Décrire les rôles respectifs et le circuit | 🟢 referentiel §2-3 | Autorité d'agrément à confirmer | Autorité compétente |
| 1.4 | Référentiels d'appui (Codex, ISO 22000, UE, FCD) | Distinguer réglementation opposable vs référentiels volontaires | 🟢 MQ (refs existantes) ; referentiel §4 | — | Distinction normative |
| 1.5 | Statut administratif visé (notification + agrément) | Décrire la démarche : notification INSSPA + agrément sanitaire POA/pêche | 🟡 referentiel §3 ; Conv-KM (mission agrément) | Récépissé notification, n° agrément | Notification + agrément |

## CHAPITRE 2 — Présentation de l'établissement & des produits

| ID | Titre | Objectif | Sources | Manque | Exig. grille |
|---|---|---|---|---|---|
| 2.1 | Description de l'établissement et des activités | Site 250 m², zones, capacité 20–100 kg/j | 🟢 MQ §1 ; P-Bat §4 | Plan de masse coté | Présentation |
| 2.2 | Gamme de produits | Lister pâtes farcies (5 ravioli, 2 tortellini), gnocchi, tagliatelle, lasagne, linguine + codes produits | 🟢 AD §1 ; P-Trac (préfixes lot) | — | Description produits |
| 2.3 | Caractéristiques produits, MAP, double pasteurisation, DLC | Fiches produits : composition, MAP, barèmes, DLC | 🟡 AD ; Diag ; P-Stock (DLC) | Fiches techniques produits FT01–FT11, DLC validées | Caractérisation HACCP |
| 2.4 | Usage prévu & populations cibles | Préciser usage (produit réfrigéré à cuire/RTE), populations | 🟡 AD §1 | Usage prévu précis par produit | HACCP usage prévu |

## CHAPITRE 3 — Système de management (SMSDA)

| ID | Titre | Objectif | Sources | Manque | Exig. grille |
|---|---|---|---|---|---|
| 3.1 | Organigramme, responsabilités, équipe sécurité des aliments | Organigramme + équipe HACCP (8 membres) | 🟢 Org ; EqHACCP ; AD T4 | Fiches de poste signées | Responsabilités |
| 3.2 | Maîtrise documentaire et des enregistrements | Système de codification (ENR-*, DEC-*, durées d'archivage) | 🟢 P-Trac T14 ; P-Dechets T18 | Tableau maître unifié | Maîtrise documentaire |
| 3.3 | Communication interne/externe (dont INSSPA) | Modalités de communication, notification autorités | 🟡 Pol ; P-Trac §7 | Procédure communication INSSPA | Communication |
| 3.4 | Gestion des urgences, retrait/rappel | Procédure retrait/rappel, notification <24h | 🟢 MQ §5 (retrait/rappel) ; P-Trac §7 | Mettre à jour « ANCSEP »→autorité correcte | Retrait/rappel |
| 3.5 | Revue de direction, amélioration continue | Périodicité, entrées/sorties de revue | 🟡 Pol ; MQ §5 | Comptes-rendus de revue | Amélioration |

## CHAPITRE 4 — Programmes prérequis (BPH/BPF)

| ID | Titre | Objectif | Sources | Manque | Exig. grille |
|---|---|---|---|---|---|
| 4.1 | Conception/implantation des locaux ; marche en avant | Zones par niveau de risque, flux, marche en avant | 🟢 P-Bat (T6/T7/T9) ; MQ §2 | Plan des locaux coté + plan des flux | Locaux / marche en avant |
| 4.2 | Hygiène du personnel & formation | Tenue, lavage mains, santé, comportement, visiteurs | 🟢 MQ §2 (Hygiène) ; FT RC MANO SEPT | Harmoniser « 12 vs 13 étapes » lavage mains | BPH personnel |
| 4.3 | Nettoyage et désinfection | Plan N&D : zones, produits, fréquences, contrôle efficacité | 🟡 P-Dechets T13 ; FDS/FT (ARVO 21 SR, ARVO DERM, INDAL PERACID, RC MANO SEPT) | **Plan N&D global (PRO-N&D-001) à reconstruire** ; FT TRICHLORID 90% manquante ; preuves contrôle efficacité | BPH N&D |
| 4.4 | Lutte contre les nuisibles | Plan dératisation/désinsectisation, sous-traitant Delta Hygiène | 🟢 MQ §2 (Nuisibles) | Contrat Delta Hygiène, plan d'appâtage, rapports | BPH nuisibles |
| 4.5 | Maintenance & étalonnage (pasteurisateurs, sondes, MAP) | Plan maintenance préventive + étalonnage | 🟢 P-Bat §7/T10 ; ENR-MAI-001 | Certificats d'étalonnage des sondes/pasteurisateurs | Maîtrise CCP / métrologie |
| 4.6 | Eau, air, énergie ; déchets & sous-produits animaux | Eau potable, vapeur, gestion déchets D-01→D-05 | 🟢 P-Bat §8/T11 ; P-Dechets ; Conv-déchets | Analyses eau SONEDE/MULTILAB, BSD | Eau / déchets / SPA |
| 4.7 | Chaîne du froid | T° par zone, relevés 3×/j, actions si écart | 🟢 P-Stock T7/T9 ; ENR-TMP-* | Enregistrements réels | Chaîne du froid |
| 4.8 | Gestion des allergènes | Plan allergènes (gluten, œuf, lait, poisson, crustacés) | 🔴 AD (mentions éparses) | **Plan allergènes dédié à créer** (présent en filigrane, pas formalisé) | Allergènes |
| 4.9 | Matériaux & objets au contact (films/barquettes MAP) | Conformité contact alimentaire | 🟡 ENR réception emballages (CE 10/2011) | Déclarations de conformité emballages | Matériaux contact |
| 4.10 | Maîtrise des approvisionnements (fournisseurs POA/pêche agréés) | Sélection/évaluation fournisseurs | 🟢 MQ §4 | Liste fournisseurs + n° agrément POA | Fournisseurs agréés |

## CHAPITRE 5 — Traçabilité & gestion des fournisseurs

| ID | Titre | Objectif | Sources | Manque | Exig. grille |
|---|---|---|---|---|---|
| 5.1 | Système de traçabilité amont/interne/aval | 3 niveaux, exercices simulés 2×/an <4h | 🟢 P-Trac (complet) | — | Traçabilité |
| 5.2 | Identification des lots, gestion MAP | Format lot AAXXAJJMMYY, préfixes produits | 🟢 P-Trac T8 | — | Identification lots |
| 5.3 | Évaluation des fournisseurs de POA et produits de la pêche | Agrément fournisseurs sensibles | 🟡 MQ §4 | Justificatifs agrément fournisseurs | Fournisseurs POA |

## CHAPITRE 6 — Étude HACCP

| ID | Titre | Objectif | Sources | Manque | Exig. grille |
|---|---|---|---|---|---|
| 6.1 | Champ et équipe HACCP | Périmètre, équipe, supervision externe | 🟢 AD T4 ; EqHACCP | Validation/signatures équipe | HACCP équipe |
| 6.2 | Descriptions produits & diagrammes | Diagrammes farcis/non farcis/gnocchi vérifiés | 🟢 Diag ; AD §3 | Vérification terrain des diagrammes datée | HACCP diagrammes |
| 6.3 | Analyse des dangers (B/C/P) | 20 étapes, focus Listeria, C. botulinum (MAP), Salmonella, histamine | 🟢 AD (T7–T… complet) | Renfort danger C. botulinum/MAP & histamine pêche | HACCP dangers |
| 6.4 | Détermination & justification des CCP | CCP1 refroid., CCP2/CCP3 pasteurisation | 🟢 AD ; Diag ; P-Trac T9 | **Réconcilier CCP2 : >45°C (Diag) vs >74°C (texte)** | CCP |
| 6.5 | Limites critiques, surveillance, actions correctives | Barèmes, fréquences, responsables, fiches CCP | 🟢 AD ; ENR (CCP) | Fiches ENR-CCP-001/002/003 modèles | Surveillance CCP |
| 6.6 | Validation & vérification (barèmes, challenge tests) | Justifier scientifiquement barèmes pasteurisation + MAP | 🔴 — | **Validation barèmes + challenge tests Listeria/Clostridium à fournir** | Validation procédé |

## CHAPITRE 7 — Plan d'auto-surveillance & contrôles

| ID | Titre | Objectif | Sources | Manque | Exig. grille |
|---|---|---|---|---|---|
| 7.1 | Plan d'analyses (produits, surfaces, eau) | Programme MULTILAB : microbio PF/MP, surfaces, aflatoxines | 🟢 Conv-MULTILAB (annexe) | Fréquences à figer, planning rempli | Auto-surveillance |
| 7.2 | Critères & interprétation | Critères microbiologiques et seuils | 🟡 Conv-MULTILAB ; FCD 2025 | Tableau critères/seuils consolidé | Critères microbio |
| 7.3 | Contrôles à réception & libération des lots | Réception MP/emballages, décision, libération PF | 🟢 MQ §4 ; ENR réception | — | Contrôle réception |
| 7.4 | Métrologie | Étalonnage instruments de mesure | 🟡 P-Bat T10 | Certificats étalonnage | Métrologie |

## CHAPITRE 8 — Étiquetage & information du consommateur

| ID | Titre | Objectif | Sources | Manque | Exig. grille |
|---|---|---|---|---|---|
| 8.1 | Mentions obligatoires, allergènes, DLC, conservation | Définir l'étiquetage conforme | 🔴 P-Stock (DLC) ; P-Trac (lot) | **Maquettes d'étiquettes à fournir** | Étiquetage |
| 8.2 | Conformité étiquetage (NT + Codex) | Vérifier conformité réglementaire | 🔴 — | NT étiquetage applicable | Étiquetage conforme |

## CHAPITRE 9 — Gestion des non-conformités & amélioration

| ID | Titre | Objectif | Sources | Manque | Exig. grille |
|---|---|---|---|---|---|
| 9.1 | Non-conformités produits/process | Procédure NC (mineure/majeure/critique) | 🟢 MQ §5 ; ENR 14.1 | Harmoniser format n° NC (NCI-JJMMAA vs NC-AAAA-MM-XX) | Gestion NC |
| 9.2 | Réclamations, retrait/rappel | Traitement réclamations (48h), retrait/rappel | 🟢 MQ §5 ; Pol | Registre réclamations | Réclamations |
| 9.3 | Audits internes, actions correctives/préventives | Programme d'audit interne, AC/AP, suivi efficacité | 🟡 MQ §5 ; P-Dechets (KPI) | Programme d'audit + rapports | Audit interne |

## ANNEXES (numérotation à figer en mise en forme)

| ID | Annexe | Source | Manque |
|---|---|---|---|
| A1 | Organigramme | 🟢 Org | — |
| A2 | Diagrammes de fabrication | 🟢 Diag | Vérification terrain datée |
| A3 | Plan de masse / plan des locaux / plan des flux | 🔴 | **À fournir (absent)** |
| A4 | Tableau équipe HACCP | 🟢 EqHACCP | Signatures |
| A5 | Fiches techniques produits (FT01–FT11) | 🔴 | À fournir |
| A6 | Plan HACCP détaillé + fiches CCP | 🟢 AD | Fiches CCP modèles |
| A7 | Plan N&D + FDS/FT produits | 🟡 FDS/FT (4) | Plan N&D global ; FT TRICHLORID |
| A8 | Plan de lutte contre les nuisibles | 🟡 MQ §2 | Contrat Delta Hygiène + plan appâtage |
| A9 | Conventions (KM Consulting, MULTILAB, déchets) | 🟢 Conv-* | — |
| A10 | Modèles d'enregistrements | 🟢 ENR-* (11) | Corriger collisions de codes (2.3 ×2 ; Bon d'entrée mal titré) |
| A11 | Résultats d'analyses (eau, microbio, personnel) | 🔴 | À fournir (PV) |
| A12 | Attestations/certificats (ANGED, étalonnages, alimentarité, formations) | 🔴 | À fournir |
| A13 | Copie des textes réglementaires applicables | 🟡 referentiel §10 | Joindre textes |

---

## Note finale — exigences réglementaires NON rattachées à une source disponible (à signaler avant validation)

Ces exigences de la grille de conformité **ne peuvent pas être entièrement rédigées** faute de source : elles seront balisées `[À COMPLÉTER]` dans le brouillon et consolidées dans `liste-informations-manquantes.md`.

1. **Autorité d'agrément exacte** (INSSPA vs DGSV vs guichet conjoint) — *décision/confirmation administration requise* (referentiel §7).
2. **Validation des barèmes de double pasteurisation + MAP** et **challenge tests Listeria/Clostridium botulinum** (6.6) — preuves scientifiques absentes.
3. **Plan des locaux coté / plan des flux** (A3, 2.1, 4.1) — annexe obligatoire absente.
4. **Plan N&D global PRO-N&D-001 détaillé** (4.3, A7) — section vide dans le manuel + FT TRICHLORID manquante.
5. **Plan allergènes formalisé** (4.8) — présent en filigrane uniquement.
6. **Maquettes d'étiquetage** (8.1-8.2) — absentes.
7. **Preuves** : analyses eau potable, rapports MULTILAB, analyses corpo-parasitologiques personnel, certificats d'étalonnage, attestations de formation, agrément ANGED prestataire, déclarations d'alimentarité emballages (A11-A12).
8. **Tableau de gestion documentaire renseigné** (0.3) — noms/dates/visas réels.

## Décisions d'arbitrage demandées à l'utilisateur (avant rédaction)

- **D1 — Périmètre du manuel :** conformité réglementaire tunisienne **seule**, ou **+ ISO 22000 / exigences clients FCD** ? (le plan est compatible avec les deux ; cela change le niveau de détail de certains chapitres).
- **D2 — Restructuration :** le manuel existant a 7 sections ; le plan proposé en a **10 (0–9)** pour insérer le **Chapitre 1 réglementaire** et formaliser allergènes/auto-surveillance/étiquetage. **Confirmez-vous cette nouvelle structure** (recommandée) ou préférez-vous **conserver la numérotation des 7 sections** existantes ?
- **D3 — Incohérences détectées :** dois-je les **harmoniser d'office** dans la rédaction (12/13 étapes lavage mains ; code 2.3 dupliqué ; format n° NC ; CCP2 >45/>74°C ; orthographe Gabsi ; fichier « Bon d'entrée » mal titré), ou les **laisser et seulement les signaler** ?
- **D4 — Langue :** manuel en **français** (politique reprise aussi en arabe), conforme au prompt — confirmez-vous ?

> **Ce plan détaillé doit être validé par l'utilisateur avant le lancement de la rédaction** (point de contrôle géré par le fil principal).
