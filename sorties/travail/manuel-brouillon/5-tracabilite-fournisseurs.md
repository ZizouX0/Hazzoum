# Chapitre 5 — Traçabilité & gestion des fournisseurs

## 5.1 Système de traçabilité amont / interne / aval

Le système de traçabilité couvre toute la chaîne, de la réception des matières premières à la livraison des produits finis, et garantit l'identification des MP et emballages d'un lot de PF ainsi que la destination de chaque lot expédié **en moins de 4 heures**.

| Niveau | Portée | Documents |
|---|---|---|
| **Amont** (fournisseurs → usine) | MP, emballages, produits chimiques | Fiche réception MP (ENR-REC-001), Fiche réception emballages (1.2), rapports MULTILAB |
| **Interne** (usine → PF) | Lien MP → CCP → lot PF | Fiche de production (ENR-PRD-001), fiches CCP (ENR-CCP-001/002/003) |
| **Aval** (PF → client) | Expéditions, clients | BL client signé, registre des expéditions (ENR-TRP-001) |

**Exercices de traçabilité simulée** : 2 par an (1 amont + 1 aval), objectif 100 % des lots retrouvés en < 4 h ; résultats présentés en revue de direction.

**Référentiels** : ISO 22000:2018 ; Codex CAC/RCP 1-1969 ; (référence d'appui) Règlement (CE) 178/2002 art. 18/19 (une étape en amont / une étape en aval).

## 5.2 Identification des lots et gestion MAP

Le numéro de lot PF suit le format **AAXXAJJMMYY** (11 caractères), décomposé comme suit :

| Position | Champ | Contenu | Exemple `RR11D100426` |
|---|---|---|---|
| 1-2 (AA) | Préfixe produit | 2 lettres (RR, RF, RS, RP, RB, TS, TF, GN, TA, LZ, LG) | `RR` = ravioli ricotta-épinard |
| 3-5 (XXA) | Code interne | Code recette/ligne | `11D` |
| 6-7 (JJ) | Jour | Jour de production | `10` |
| 8-9 (MM) | Mois | Mois de production | `04` |
| 10-11 (YY) | Année | Année (2 chiffres) | `26` (2026) |

Soit `RR11D100426` = ravioli ricotta-épinard, recette/ligne `11D`, produit le **10 avril 2026** (un autre lot du même produit fabriqué le 04 mai 2026 porterait `RR11D040526`).

> *Correction apportée (E-10) : décomposition champ par champ ajoutée pour rendre le format auto-démontrable.* **[À COMPLÉTER : signification exacte du segment central « 11D » (code recette, ligne ou poste) à préciser par l'entreprise.]**

Le numéro de lot est imprimé sur le produit (convoyeur dateur) et reporté sur toutes les fiches de production et les emballages. La fiche de production relie le lot PF aux numéros de lots des MP utilisées et aux enregistrements CCP1/CCP2/CCP3, au N&D du jour et, le cas échéant, au rapport d'analyse MULTILAB.

## 5.3 Évaluation des fournisseurs de POA et de produits de la pêche

Les fournisseurs d'ingrédients d'origine animale et de la pêche (viande/volaille, fromages/ricotta, ovoproduits, saumon, crevettes) font l'objet d'une vigilance renforcée : vérification de leur agrément sanitaire, des certificats sanitaires accompagnant les lots, et de la chaîne du froid à réception (voir § 4.10 et § 7.3).

> **[À COMPLÉTER : liste des fournisseurs de POA/pêche avec numéros d'agrément et copies des certificats sanitaires.]**

### Informations à fournir par l'entreprise
- Justificatifs d'agrément des fournisseurs de POA/pêche (5.3).
- Rapports des derniers exercices de traçabilité simulée (5.1).
