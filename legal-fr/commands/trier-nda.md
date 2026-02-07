---
description: Pré-filtrage rapide d'un accord de confidentialité (NDA) selon le droit français
argument-hint: ""
---

# /trier-nda -- Triage d'accord de confidentialité

Triage rapide d'un accord de confidentialité (NDA) entrant. Classifie selon trois niveaux : VERT (approbation standard), JAUNE (revue par un juriste), ROUGE (problèmes significatifs).

**Avertissement** : Cet outil facilite le triage mais ne constitue pas un conseil juridique.

## Invocation

```
/trier-nda
```

## Workflow

### Étape 1 : Réceptionner le NDA

Accepter le NDA sous tout format (fichier, texte, lien).

### Étape 2 : Grille de contrôle

| Critère | Vérification |
|---------|-------------|
| **Réciprocité** | Obligations mutuelles ? Si unilatéral, est-ce adapté ? |
| **Définition des informations confidentielles** | Périmètre raisonnable ? Pas trop large ? |
| **Exceptions standard** | Information publique, connue antérieurement, développée indépendamment, reçue d'un tiers, obligation légale |
| **Durée** | Accord : 1-3 ans standard. Survie : 2-5 ans (secrets d'affaires : plus long) |
| **Divulgation autorisée** | Salariés, sous-traitants, conseils ayant besoin d'en connaître |
| **Restitution/destruction** | À la fin du contrat, avec exception pour obligations légales/archivage |
| **Non-sollicitation** | Ne doit PAS figurer dans un NDA |
| **Non-concurrence** | Ne doit PAS figurer dans un NDA |
| **Clause résiduelle** | Absente ou strictement limitée à la mémoire non assistée |
| **Droit applicable** | Droit français ou juridiction commerciale raisonnable |
| **Clause pénale** | Montant proportionné (pouvoir modérateur du juge, art. 1231-5 C. civ.) |
| **Conformité RGPD** | Si échange de données personnelles : mention des obligations RGPD |

### Étape 3 : Classification

#### VERT -- Approbation standard
Tous les critères remplis. NDA conforme aux standards du marché français.

#### JAUNE -- Revue juriste nécessaire
Écarts mineurs mais gérables (définition large, durée plus longue, juridiction acceptable mais non préférée, exception manquante facilement ajoutée).

#### ROUGE -- Problèmes significatifs
Unilatéral inadapté, exceptions critiques manquantes, clauses de non-concurrence ou non-sollicitation, durée déraisonnable, clause résiduelle large, juridiction problématique, clauses commerciales cachées.

### Étape 4 : Rapport

```
## Rapport de triage NDA

**Classification** : [VERT / JAUNE / ROUGE]
**Parties** : [noms]
**Type** : [Mutuel / Unilatéral]
**Durée** : [durée]
**Droit applicable** : [juridiction]

## Grille de contrôle

| Critère | Statut | Notes |
|---------|--------|-------|
| Réciprocité | [OK/ALERTE/KO] | [détails] |
| ... | | |

## Problèmes identifiés

### [Problème 1 -- JAUNE/ROUGE]
**Constat** : [description]
**Risque** : [conséquences]
**Fondement juridique** : [articles applicables]
**Correction proposée** : [langage ou approche]

## Recommandation

[Action : approuver / envoyer pour revue / refuser et contre-proposer]
```
