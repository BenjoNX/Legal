# Serveur MCP Droit Français + Plugin LEGAL FR

## Projet

Serveur MCP interrogeant les API publiques du droit français (Légifrance et JudiLibre) via PISTE, accompagné d'un plugin "LEGAL FR" adapté au droit français.

## Serveur MCP — Outils disponibles

Les outils suivants sont exposés via le serveur MCP `droit-francais` :

### Légifrance (textes législatifs et réglementaires)
- `rechercher_legifrance(recherche, fond, type_champ, type_recherche, code, date_debut, date_fin, page, page_taille, tri, operateur)` — Recherche multi-critères
- `consulter_legifrance(id)` — Texte intégral par ID (LEGIARTI, LEGITEXT, JURITEXT, etc.)

### JudiLibre (jurisprudence)
- `rechercher_jurisprudence_judilibre(recherche, juridiction, localisation, chambre, type_decision, theme, solution, date_debut, date_fin, tri, ordre, nombre_resultats, page)` — Recherche de décisions
- `consulter_decision_judilibre(decision_id)` — Texte intégral d'une décision
- `obtenir_taxonomie_judilibre(taxonomy_id, key, value, context_value)` — Valeurs valides des filtres

## Commandes slash

- `/rechercher-droit [termes]` — Recherche dans les sources officielles
- `/analyser-contrat` — Analyse clause par clause selon le droit français
- `/trier-nda` — Triage d'accord de confidentialité
- `/veille-juridique [daily|theme|incident] [sujet]` — Briefing juridique
- `/repondre [type]` — Réponse type juridique

## Configuration

- Identifiants PISTE dans `.env` (jamais committé)
- Serveur MCP configuré dans `.mcp.json`
- Skills dans `.claude/skills/`
- Commandes dans `.claude/commands/`

## Lancer le serveur MCP

```bash
source venv/bin/activate
python droit_francais_MCP.py
```

## Tests

```bash
# Tests unitaires (pas besoin de réseau)
pytest test_unit_legifrance.py test_unit_judilibre.py -v -m unit

# Tests d'intégration (nécessitent des identifiants PISTE valides)
pytest test_api_legifrance.py test_api_judilibre.py -v -m integration
```
