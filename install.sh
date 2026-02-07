#!/bin/bash
# install.sh — Installation du serveur MCP Droit Français + Plugin LEGAL FR
# Compatible macOS (Claude Desktop + Claude Code)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON_BIN="$VENV_DIR/bin/python"
MCP_SERVER="$SCRIPT_DIR/droit_francais_MCP.py"
CLAUDE_DESKTOP_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

echo "=========================================="
echo "  Serveur MCP Droit Français — Installation"
echo "=========================================="
echo ""

# ── 1. Python et venv ──────────────────────────────────
echo "→ Vérification de Python..."
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 non trouvé. Installez Python 3.8+ : https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "  Python $PYTHON_VERSION détecté"

echo "→ Création de l'environnement virtuel..."
python3 -m venv "$VENV_DIR"
echo "  ✓ venv créé dans $VENV_DIR"

echo "→ Installation des dépendances..."
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -e "$SCRIPT_DIR"
echo "  ✓ Dépendances installées (fastmcp, requests, python-dotenv)"

# ── 2. Fichier .env ────────────────────────────────────
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo ""
    echo "→ Configuration des identifiants PISTE"
    echo "  Inscrivez-vous sur https://piste.gouv.fr/ pour obtenir vos identifiants."
    echo "  Abonnez-vous aux API Légifrance et JudiLibre."
    echo ""

    read -rp "  Client ID OAuth 2.0 PISTE : " PISTE_CLIENT_ID
    read -rp "  Client Secret OAuth 2.0 PISTE : " PISTE_CLIENT_SECRET

    cat > "$SCRIPT_DIR/.env" <<ENVEOF
# Identifiants API PISTE (https://piste.gouv.fr/)
PISTE_CLIENT_ID=$PISTE_CLIENT_ID
PISTE_CLIENT_SECRET=$PISTE_CLIENT_SECRET
PISTE_SANDBOX_CLIENT_ID=$PISTE_CLIENT_ID
PISTE_SANDBOX_CLIENT_SECRET=$PISTE_CLIENT_SECRET
ENVEOF

    echo "  ✓ Fichier .env créé"
else
    echo "→ Fichier .env existant conservé"
fi

# ── 3. Test de connexion ───────────────────────────────
echo ""
echo "→ Test de connexion aux API PISTE..."
CONNECTION_OK=$("$PYTHON_BIN" -c "
from api_legifrance import LegifranceAPI
try:
    api = LegifranceAPI(sandbox=False)
    api.get_access_token()
    print('OK')
except Exception as e:
    print(f'FAIL:{e}')
" 2>/dev/null)

if [ "$CONNECTION_OK" = "OK" ]; then
    echo "  ✓ Connexion réussie — Token OAuth obtenu"
else
    echo "  ⚠ Connexion échouée : ${CONNECTION_OK#FAIL:}"
    echo "  Vérifiez vos identifiants dans .env et votre abonnement sur piste.gouv.fr"
    echo "  L'installation continue malgré tout..."
fi

# ── 4. Claude Code ─────────────────────────────────────
echo ""
echo "→ Configuration Claude Code..."
if command -v claude &>/dev/null; then
    # Ajouter le serveur MCP à Claude Code (global)
    claude mcp add droit-francais -s project -- "$PYTHON_BIN" "$MCP_SERVER" 2>/dev/null || true
    echo "  ✓ Serveur MCP ajouté à Claude Code"
else
    echo "  ℹ Claude Code CLI non détecté — le serveur MCP est configuré via .mcp.json"
    echo "    Les outils MCP seront disponibles quand vous lancerez claude dans ce dossier."
fi

# ── 5. Claude Desktop (macOS) ──────────────────────────
echo ""
echo "→ Configuration Claude Desktop (macOS)..."

CLAUDE_DESKTOP_DIR="$(dirname "$CLAUDE_DESKTOP_CONFIG")"

if [ -d "$CLAUDE_DESKTOP_DIR" ] || [ "$(uname)" = "Darwin" ]; then
    mkdir -p "$CLAUDE_DESKTOP_DIR"

    if [ -f "$CLAUDE_DESKTOP_CONFIG" ]; then
        # Fusionner avec la config existante
        "$PYTHON_BIN" -c "
import json, sys

config_path = '$CLAUDE_DESKTOP_CONFIG'
python_bin = '$PYTHON_BIN'
mcp_server = '$MCP_SERVER'

try:
    with open(config_path, 'r') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    config = {}

if 'mcpServers' not in config:
    config['mcpServers'] = {}

config['mcpServers']['droit-francais'] = {
    'command': python_bin,
    'args': [mcp_server]
}

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print('OK')
"
        echo "  ✓ Serveur MCP ajouté à la config Claude Desktop existante"
    else
        # Créer la config
        cat > "$CLAUDE_DESKTOP_CONFIG" <<JSONEOF
{
  "mcpServers": {
    "droit-francais": {
      "command": "$PYTHON_BIN",
      "args": ["$MCP_SERVER"]
    }
  }
}
JSONEOF
        echo "  ✓ Config Claude Desktop créée"
    fi

    echo "  ℹ Redémarrez Claude Desktop pour activer le serveur MCP."
else
    echo "  ℹ Claude Desktop non détecté (pas macOS ou app non installée)"
    echo "  Pour configurer manuellement, ajoutez à :"
    echo "  ~/Library/Application Support/Claude/claude_desktop_config.json"
    echo ""
    echo "  {\"mcpServers\":{\"droit-francais\":{\"command\":\"$PYTHON_BIN\",\"args\":[\"$MCP_SERVER\"]}}}"
fi

# ── 6. Résumé ──────────────────────────────────────────
echo ""
echo "=========================================="
echo "  ✓ Installation terminée"
echo "=========================================="
echo ""
echo "Utilisation :"
echo ""
echo "  Claude Code (local) :"
echo "    cd $SCRIPT_DIR"
echo "    claude"
echo "    > /rechercher-droit responsabilité médicale"
echo "    > /analyser-contrat"
echo "    > /veille-juridique daily"
echo ""
echo "  Claude Desktop (macOS) :"
echo "    1. Redémarrez Claude Desktop"
echo "    2. Les outils Droit Français sont disponibles automatiquement"
echo "    3. Demandez : \"Cherche les articles du Code civil sur le mariage\""
echo ""
echo "  Tests :"
echo "    source venv/bin/activate"
echo "    pytest test_unit_legifrance.py test_unit_judilibre.py -v -m unit"
echo "    pytest test_api_legifrance.py test_api_judilibre.py -v -m integration"
echo ""
