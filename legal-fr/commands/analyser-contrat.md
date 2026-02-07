---
description: Analyser un contrat selon le droit français et le cahier des charges de l'organisation
argument-hint: ""
---

# /analyser-contrat -- Analyse de contrat droit français

Analyse un contrat clause par clause selon le droit français, le Code civil (réforme de 2016), et le cahier des charges de l'organisation. Identifie les écarts, génère des suggestions de modification et évalue l'impact juridique.

**Avertissement** : Cet outil facilite l'analyse mais ne constitue pas un conseil juridique. Toute analyse doit être vérifiée par un avocat qualifié.

## Invocation

```
/analyser-contrat
```

## Workflow

### Étape 1 : Réceptionner le contrat

Accepter le contrat sous tout format : fichier (PDF, DOCX), texte collé, ou lien.

### Étape 2 : Recueillir le contexte

Demander à l'utilisateur :
1. **Votre position** : prestataire, client, concédant, licencié, partenaire
2. **Échéance** : Date limite de finalisation
3. **Points d'attention** : Préoccupations spécifiques (données personnelles, responsabilité, PI, etc.)
4. **Contexte commercial** : Taille du contrat, importance stratégique, relation existante

### Étape 3 : Charger le cahier des charges

Chercher le cahier des charges dans `legal-fr.local.md` ou les fichiers de configuration locaux.

**Si aucun cahier des charges n'est configuré** :
- Informer l'utilisateur
- Proposer de procéder avec les standards du droit français (Code civil, droit des contrats post-réforme 2016)
- Mentionner clairement que l'analyse repose sur le droit commun français

### Étape 4 : Analyse clause par clause

Analyser systématiquement selon le droit français :

| Catégorie de clause | Points de contrôle clés |
|---------------------|------------------------|
| **Formation du contrat** | Capacité, consentement (art. 1128 C. civ.), vices du consentement (erreur, dol, violence) |
| **Objet et contrepartie** | Détermination du contenu (art. 1163), déséquilibre significatif (art. 1171), clauses abusives |
| **Responsabilité contractuelle** | Plafond de responsabilité, clauses limitatives (art. 1231-3), force majeure (art. 1218) |
| **Garanties et assurances** | Garantie des vices cachés, garantie d'éviction, assurance RC Pro |
| **Propriété intellectuelle** | Cession de droits (L.131-3 CPI), licence, œuvres créées dans le cadre du contrat |
| **Données personnelles** | Conformité RGPD, DPA/sous-traitance (art. 28 RGPD), CNIL |
| **Confidentialité** | Durée, périmètre, exceptions, restitution |
| **Durée et résiliation** | Durée déterminée/indéterminée, reconduction tacite (art. L.215-1 C. consom.), résiliation pour faute |
| **Droit applicable et litiges** | Loi applicable, juridiction compétente, clause compromissoire, médiation (art. 750-1 CPC) |
| **Cession du contrat** | Consentement requis (art. 1216 C. civ.), intuitu personae |
| **Imprévision** | Clause de hardship, art. 1195 C. civ. |
| **Clauses pénales** | Art. 1231-5 C. civ., pouvoir modérateur du juge |

### Étape 5 : Classifier les écarts

#### VERT -- Conforme
- Conforme au droit français et au cahier des charges
- Variations mineures commercialement raisonnables

#### JAUNE -- À négocier
- Hors position standard mais dans une marge négociable
- Courant sur le marché mais pas la préférence de l'organisation
- **Inclure** : langage de modification proposé, position de repli, impact commercial

#### ROUGE -- À escalader
- Hors marge acceptable ou illégal au regard du droit français
- Clauses potentiellement réputées non écrites (art. 1171 C. civ.)
- Risque matériel significatif
- **Inclure** : fondement juridique du risque, position du marché, exposition, voie d'escalade

### Étape 6 : Vérification légale française

Pour chaque clause, vérifier la conformité avec :
- **Code civil** (réforme du droit des contrats, ordonnance n°2016-131)
- **Code de commerce** (si B2B, déséquilibre significatif art. L.442-1)
- **Code de la consommation** (si B2C, clauses abusives)
- **RGPD et loi Informatique et Libertés** (données personnelles)
- **Code de la propriété intellectuelle** (PI)
- **Droit du travail** (si applicable)

Utiliser `rechercher_legifrance()` pour vérifier les textes en vigueur si nécessaire.

### Étape 7 : Rapport d'analyse

```
## Analyse de contrat

**Document** : [nom]
**Parties** : [noms et rôles]
**Votre position** : [prestataire/client/etc.]
**Échéance** : [si fournie]
**Base d'analyse** : [Cahier des charges / Droit commun français]

## Synthèse

[Top 3-5 points avec indicateurs de sévérité]

## Analyse clause par clause

### [Catégorie] -- [VERT/JAUNE/ROUGE]
**Le contrat prévoit** : [résumé de la clause]
**Position standard** : [votre standard ou droit commun]
**Fondement juridique** : [articles de loi applicables]
**Écart** : [description]
**Impact** : [conséquences pratiques]
**Modification proposée** : [langage spécifique, si JAUNE ou ROUGE]

## Stratégie de négociation

[Approche recommandée, priorités, concessions possibles]

## Prochaines étapes

[Actions concrètes]
```

## Notes

- Toujours citer les articles du Code civil, Code de commerce, ou textes spéciaux applicables
- Signaler les clauses réputées non écrites au regard de la jurisprudence
- Si le contrat est régi par un droit étranger, le signaler et analyser les implications
- Utiliser `rechercher_legifrance()` et `rechercher_jurisprudence_judilibre()` pour vérifier l'état du droit
