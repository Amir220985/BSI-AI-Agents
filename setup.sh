#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$REPO_DIR/.env"
ZSHRC="$HOME/.zshrc"
CLAUDE_DESKTOP_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
MCP_URL="https://bsi-mcp-service-2.kinddune-cc2044ba.northeurope.azurecontainerapps.io/mcp/"

# --- 1. API-Key aus .env lesen -------------------------------------------

if [[ ! -f "$ENV_FILE" ]]; then
  echo "FEHLER: .env nicht gefunden. Bitte .env mit BSI_MCP_API_KEY anlegen."
  echo "Beispiel: echo 'BSI_MCP_API_KEY=dein-key' > .env"
  exit 1
fi

API_KEY=$(grep -E '^BSI_MCP_API_KEY=' "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")

if [[ -z "$API_KEY" ]]; then
  echo "FEHLER: BSI_MCP_API_KEY ist in .env leer oder nicht vorhanden."
  exit 1
fi

echo "API-Key gefunden."

# --- 2. ~/.zshrc setzen (Claude Code CLI) ---------------------------------

if grep -q 'BSI_MCP_API_KEY' "$ZSHRC" 2>/dev/null; then
  # Key aktualisieren falls er sich geändert hat
  sed -i '' "s|^export BSI_MCP_API_KEY=.*|export BSI_MCP_API_KEY=\"$API_KEY\"|" "$ZSHRC"
  echo "BSI_MCP_API_KEY in ~/.zshrc aktualisiert."
else
  echo "export BSI_MCP_API_KEY=\"$API_KEY\"" >> "$ZSHRC"
  echo "BSI_MCP_API_KEY in ~/.zshrc eingetragen."
fi

# --- 3. Claude Desktop App konfigurieren ----------------------------------

if [[ ! -f "$CLAUDE_DESKTOP_CONFIG" ]]; then
  echo "Claude Desktop Config nicht gefunden – überspringe Desktop-Setup."
else
  # Prüfen ob python3 verfügbar ist
  if ! command -v python3 &>/dev/null; then
    echo "WARNUNG: python3 nicht gefunden – Claude Desktop Config muss manuell angepasst werden."
  else
    python3 - <<PYEOF
import json, sys

config_path = """$CLAUDE_DESKTOP_CONFIG"""
mcp_url = """$MCP_URL"""
api_key = """$API_KEY"""

with open(config_path, "r") as f:
    config = json.load(f)

config.setdefault("mcpServers", {})
config["mcpServers"]["azure-knowledge-base"] = {
    "command": "npx",
    "args": [
        "mcp-remote",
        mcp_url,
        "--header",
        f"X-API-KEY:{api_key}"
    ]
}

with open(config_path, "w") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print("Claude Desktop Config aktualisiert.")
PYEOF
  fi
fi

# --- 4. Projekt .claude/settings.json sicherstellen ----------------------

SETTINGS="$REPO_DIR/.claude/settings.json"
if [[ -f "$SETTINGS" ]]; then
  echo ".claude/settings.json bereits vorhanden (Claude Code CLI)."
else
  mkdir -p "$REPO_DIR/.claude"
  cat > "$SETTINGS" <<JSON
{
  "mcpServers": {
    "azure-knowledge-base": {
      "type": "http",
      "url": "$MCP_URL",
      "headers": {
        "X-API-KEY": "\${BSI_MCP_API_KEY}"
      }
    }
  }
}
JSON
  echo ".claude/settings.json angelegt."
fi

# --- Fertig ---------------------------------------------------------------

echo ""
echo "Setup abgeschlossen."
echo "Bitte einmalig ausführen: source ~/.zshrc"
echo "Danach Claude Code / Claude Desktop App neu starten."
