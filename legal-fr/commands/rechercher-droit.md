---
description: Rechercher dans les sources officielles du droit français (Légifrance, JudiLibre)
argument-hint: "[termes de recherche]"
---

# /rechercher-droit -- Recherche juridique française

Recherche dans les bases officielles du droit français via le serveur MCP Droit Français : Légifrance (codes, lois, décrets, ordonnances) et JudiLibre (jurisprudence).

**Avertissement** : Cet outil facilite la recherche juridique mais ne constitue pas un conseil juridique. Toute analyse doit être vérifiée par un professionnel du droit qualifié.

## Invocation

```
/rechercher-droit [termes de recherche]
```

## Workflow

### Étape 1 : Comprendre la demande

Analyser la demande de l'utilisateur pour déterminer :
1. **Type de recherche** : Texte législatif, jurisprudence, ou les deux
2. **Termes de recherche** : Mots-clés, références d'articles, numéros de décision
3. **Périmètre** : Fonds spécifique (Code civil, JORF, etc.), juridiction, période

### Étape 2 : Recherche dans Légifrance

Si la demande concerne des textes législatifs ou réglementaires, utiliser l'outil MCP `rechercher_legifrance()` :

- **Codes** : `fond="CODE_ETAT"`, avec le nom du code (`code="Code civil"`)
- **Lois et décrets** : `fond="LODA_ETAT"` ou `fond="JORF"`
- **Jurisprudence Légifrance** : `fond="JURI"` (judiciaire), `fond="CETAT"` (Conseil d'État), `fond="CONSTIT"` (Conseil constitutionnel)
- **Conventions collectives** : `fond="KALI"`
- **Recherche transversale** : `fond="ALL"`

Pour obtenir le texte intégral d'un résultat, utiliser `consulter_legifrance(id)`.

### Étape 3 : Recherche dans JudiLibre

Si la demande concerne la jurisprudence, utiliser `rechercher_jurisprudence_judilibre()` :

- **Juridiction** : `cc` (Cour de cassation), `ca` (cours d'appel), `tj` (tribunaux judiciaires), `tcom` (tribunaux de commerce)
- **Chambre** : `civ1`, `civ2`, `civ3`, `comm`, `soc`, `cr` (criminelle), `pl` (plénière)
- **Localisation** : `ca_paris`, `ca_lyon`, etc.
- **Filtres** : type de décision, solution, thème, dates

Pour obtenir le texte intégral d'une décision, utiliser `consulter_decision_judilibre(id)`.

Pour connaître les valeurs valides des filtres, utiliser `obtenir_taxonomie_judilibre()`.

### Étape 4 : Présenter les résultats

Structurer les résultats :

```
## Résultats de recherche : [termes]

### Sources législatives (Légifrance)
| Réf. | Titre | Date | Fonds | ID |
|------|-------|------|-------|----|
| [ref] | [titre] | [date] | [fonds] | [id pour consultation] |

### Jurisprudence (JudiLibre)
| Juridiction | Chambre | Date | Solution | Thème | ID |
|-------------|---------|------|----------|-------|----|
| [jur] | [ch] | [date] | [sol] | [thème] | [id] |

### Analyse
[Synthèse des résultats pertinents, articulation entre les textes et la jurisprudence]

### Pour approfondir
- Consulter le texte intégral : `consulter_legifrance("[id]")`
- Consulter la décision : `consulter_decision_judilibre("[id]")`
```

## Notes

- Toujours croiser les sources législatives et jurisprudentielles quand c'est pertinent
- Indiquer les articles en vigueur vs abrogés
- Signaler les évolutions législatives récentes sur le sujet
- Si les résultats sont trop nombreux, proposer des filtres pour affiner
