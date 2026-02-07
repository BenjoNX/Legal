---
description: Briefing juridique (veille quotidienne, recherche thématique, ou alerte incident)
argument-hint: "[daily|theme|incident] [sujet]"
---

# /veille-juridique -- Briefing juridique

Génère des briefings contextuels pour le travail juridique. Trois modes : veille quotidienne, recherche thématique, et alerte incident.

**Avertissement** : Cet outil facilite la veille mais ne constitue pas un conseil juridique.

## Invocation

```
/veille-juridique daily                    # Veille quotidienne
/veille-juridique theme [sujet]            # Recherche thématique
/veille-juridique incident [description]   # Alerte incident
```

## Mode : Veille quotidienne

Résumé matinal de ce qu'un juriste doit savoir. Utiliser `rechercher_legifrance(fond="JORF")` pour les publications récentes au Journal Officiel, et `rechercher_jurisprudence_judilibre()` pour les décisions récentes.

```
## Veille juridique -- [Date]

### Urgent / Action requise
[Éléments nécessitant une attention immédiate]

### Publications au Journal Officiel
[Lois, décrets, arrêtés récents pertinents]

### Jurisprudence notable
[Décisions récentes de la Cour de cassation, cours d'appel]

### Contrats en cours
[Revues en attente, échéances proches]

### Agenda du jour
[Réunions à préparer]

### Échéances de la semaine
[Délais, renouvellements, prescriptions]
```

## Mode : Recherche thématique

Recherche approfondie sur un sujet juridique. Utiliser `rechercher_legifrance()` et `rechercher_jurisprudence_judilibre()` pour croiser textes et jurisprudence.

```
## Recherche thématique : [Sujet]

### Synthèse
[Résumé exécutif en 2-3 phrases]

### Textes applicables
[Codes, lois, règlements en vigueur — via Légifrance]

### Jurisprudence
[Décisions clés — via JudiLibre]

### Doctrine / Position CNIL
[Si applicable]

### Points de vigilance
[Risques, questions ouvertes]

### Recommandations
[Actions à entreprendre]
```

## Mode : Alerte incident

Briefing rapide pour une situation nécessitant une attention juridique immédiate (violation de données, contentieux, contrôle CNIL, etc.).

```
## Alerte incident : [Sujet]
**Préparé** : [horodatage]
**Gravité** : [évaluation]

### Résumé de la situation
[Ce qui est connu]

### Obligations légales immédiates
[Notifications CNIL 72h, mise en demeure, prescription, etc.]

### Textes applicables
[Via rechercher_legifrance() si nécessaire]

### Contrats concernés
[Clauses pertinentes : indemnisation, assurance, force majeure]

### Actions immédiates recommandées
1. [Action la plus urgente]
2. [Priorité suivante]

### Informations manquantes
[Ce qu'il faut encore déterminer]
```
