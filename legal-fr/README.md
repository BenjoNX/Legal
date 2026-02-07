# LEGAL FR — Plugin juridique droit français

Plugin Claude Code / Cowork pour le droit français. Adapté du [plugin Legal d'Anthropic](https://github.com/anthropics/knowledge-work-plugins/tree/main/legal), avec intégration du serveur MCP Droit Français (Légifrance + JudiLibre).

## Fonctionnalités

### Commandes (slash commands)

| Commande | Description |
|----------|-------------|
| `/rechercher-droit` | Recherche dans Légifrance et JudiLibre |
| `/analyser-contrat` | Analyse clause par clause selon le droit français |
| `/trier-nda` | Triage rapide d'accords de confidentialité |
| `/veille-juridique` | Briefing (quotidien, thématique, incident) |
| `/repondre` | Réponses types (RGPD, mise en demeure, CNIL) |

### Skills (activés automatiquement)

| Skill | Description |
|-------|-------------|
| `recherche-juridique` | Recherche Légifrance + JudiLibre via MCP |
| `analyse-contrat` | Analyse contractuelle droit français (Code civil réformé 2016) |
| `conformite-rgpd` | RGPD, DPA, CNIL, exercice de droits |
| `evaluation-risques` | Matrice gravité x probabilité, escalade |
| `veille-juridique` | Suivi JORF, jurisprudence, réformes |
| `preparation-reunion` | Briefings et suivi d'actions |

## Installation

### Prérequis

1. Identifiants PISTE (piste.gouv.fr) configurés dans `.env`
2. Serveur MCP Droit Français installé (voir racine du projet)

### Claude Code (local)

```bash
# Ajouter le serveur MCP
claude mcp add droit-francais -- python /chemin/vers/Legal/droit_francais_MCP.py

# Copier les skills dans votre projet
cp -r legal-fr/skills/* .claude/skills/
```

### Claude Desktop / Cowork

Ajouter dans `claude_desktop_config.json` :

```json
{
  "mcpServers": {
    "droit-francais": {
      "command": "python",
      "args": ["/chemin/vers/Legal/droit_francais_MCP.py"]
    }
  }
}
```

## Personnalisation

Créer un fichier `legal-fr.local.md` pour définir les positions de votre organisation :

```markdown
# Cahier des charges juridique

## Positions contractuelles

### Responsabilité
- Position standard : Plafond mutuel à 12 mois de redevances
- Marge acceptable : 6-24 mois
- Escalade : Responsabilité non plafonnée, dommages indirects non exclus

### Données personnelles
- Position standard : DPA obligatoire pour tout traitement
- Exigences : Notification sous-traitants, suppression à la fin, notification violation 48h
- Escalade : Pas de DPA, transfert hors UE sans garanties
```

## Licence

MIT
