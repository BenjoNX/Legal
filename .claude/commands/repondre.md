---
description: Générer une réponse type pour une demande juridique courante
argument-hint: "[type-demande]"
---

# /repondre -- Réponse type juridique

Génère une réponse pour des demandes juridiques courantes en utilisant les modèles configurés. Adapté au droit français (RGPD, Code civil, Code du travail).

## Invocation

```
/repondre [type-demande]
```

Types de demandes :
- `droit-acces` -- Demande d'exercice de droits RGPD (accès, suppression, rectification, portabilité)
- `conservation` -- Avis de conservation de documents (litigation hold)
- `nda` -- Demande de NDA par une équipe métier
- `fournisseur` -- Question juridique d'un fournisseur
- `cnil` -- Réponse à un contrôle ou questionnaire CNIL
- `mise-en-demeure` -- Réponse à une mise en demeure
- `sous-traitant` -- Questions sur le contrat de sous-traitance RGPD

## Workflow

### Étape 1 : Identifier le type de demande

Si ambigu, afficher les catégories disponibles et demander clarification.

### Étape 2 : Vérifier les déclencheurs d'escalade

Avant de générer la réponse, évaluer si la situation nécessite un traitement individualisé :

**Déclencheurs universels** :
- Contentieux potentiel ou enquête réglementaire
- Demande émanant d'une autorité (CNIL, DGCCRF, tribunal)
- Réponse créant un engagement juridique contraignant
- Implication d'un dirigeant
- Médiatisation
- Situation inédite

Si un déclencheur est détecté : alerter l'utilisateur, recommander l'escalade, marquer tout projet de réponse « POUR REVUE JURIDIQUE UNIQUEMENT ».

### Étape 3 : Recueillir les détails

Adapter les questions au type de demande. Pour une demande RGPD par exemple :
- Nom et coordonnées du demandeur
- Type de droit exercé (accès, suppression, rectification, portabilité, opposition)
- Données concernées
- Délai de réponse (30 jours RGPD, prorogeable de 60 jours)

### Étape 4 : Générer la réponse

Utiliser `rechercher_legifrance()` pour vérifier les textes applicables si nécessaire. Respecter :
- Le ton approprié (professionnel, clair)
- Les éléments juridiques requis (références légales, délais)
- Les prochaines étapes pour le destinataire
- Les mentions obligatoires (voies de recours CNIL, etc.)

### Étape 5 : Présenter le projet

```
## Réponse générée : [Type de demande]

**À** : [destinataire]
**Objet** : [objet]

---

[Corps de la réponse]

---

### Vérification d'escalade
[Confirmation qu'aucun déclencheur n'a été détecté, OU déclencheurs signalés]

### Actions de suivi
1. [Action post-envoi]
2. [Rappels à programmer]
3. [Obligations de traçabilité]
```
