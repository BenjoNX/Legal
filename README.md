# Serveur MCP Droit Français

Serveur MCP (Model Context Protocol) pour interroger les API publiques du droit français : **Légifrance** et **JudiLibre**.

Basé sur le projet [DroitFrancaisMCP](https://github.com/jmtanguy/DroitFrancaisMCP) de Jean-Michel Tanguy.

## Fonctionnalités

### Légifrance
- **rechercher_legifrance()** : Recherche multi-critères dans tous les fonds juridiques
- **consulter_legifrance()** : Récupération du texte intégral avec métadonnées

### JudiLibre
- **rechercher_jurisprudence_judilibre()** : Recherche de décisions avec filtres avancés
- **consulter_decision_judilibre()** : Récupération du texte complet d'une décision
- **obtenir_taxonomie_judilibre()** : Accès aux valeurs valides des filtres

## Prérequis

1. Python 3.8+
2. Compte PISTE : s'inscrire sur [piste.gouv.fr](https://piste.gouv.fr/)
3. S'abonner aux API Légifrance et JudiLibre
4. Valider les conditions d'utilisation

## Installation

```bash
# Cloner le repo
git clone <repo-url>
cd Legal

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/macOS

# Installer les dépendances
pip install -e ".[dev]"

# Configurer les identifiants
cp .env.example .env
# Éditer .env avec vos identifiants PISTE
```

## Configuration

Copier `.env.example` vers `.env` et renseigner vos identifiants PISTE :

```
PISTE_CLIENT_ID=votre_client_id
PISTE_CLIENT_SECRET=votre_client_secret
```

## Utilisation avec Claude Desktop

Ajouter dans la configuration MCP de Claude Desktop :

```json
{
  "mcpServers": {
    "droit-francais": {
      "command": "python",
      "args": ["<chemin>/droit_francais_MCP.py"]
    }
  }
}
```

## Tests

```bash
pytest test_api_legifrance.py -v -m integration
pytest test_api_judilibre.py -v -m integration
```

## Licence

MIT License - Copyright (c) 2025 Jean-Michel Tanguy
