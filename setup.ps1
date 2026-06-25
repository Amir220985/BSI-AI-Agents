# BSI AI Development — Einrichtungsskript für Windows
# Ausführen mit: powershell -ExecutionPolicy Bypass -File setup.ps1

$ErrorActionPreference = "Stop"

$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$EnvFile = Join-Path $RepoDir ".env"
$Profile = $PROFILE.CurrentUserAllHosts
$ClaudeDesktopConfig = "$env:APPDATA\Claude\claude_desktop_config.json"
$McpUrl = "https://bsi-mcp-service-2.kinddune-cc2044ba.northeurope.azurecontainerapps.io/mcp/"

# --- 1. API-Key aus .env lesen -------------------------------------------

if (-not (Test-Path $EnvFile)) {
    Write-Error "FEHLER: .env nicht gefunden. Bitte .env mit BSI_MCP_API_KEY anlegen.`nBeispiel: echo 'BSI_MCP_API_KEY=dein-key' > .env"
    exit 1
}

$ApiKey = Get-Content $EnvFile | Where-Object { $_ -match '^BSI_MCP_API_KEY=' } |
    ForEach-Object { ($_ -split '=', 2)[1].Trim('"').Trim("'") } |
    Select-Object -First 1

if (-not $ApiKey) {
    Write-Error "FEHLER: BSI_MCP_API_KEY ist in .env leer oder nicht vorhanden."
    exit 1
}

Write-Host "API-Key gefunden."

# --- 2. PowerShell-Profil setzen (Claude Code CLI) -----------------------

$EnvLine = "`$env:BSI_MCP_API_KEY = `"$ApiKey`""

if (-not (Test-Path $Profile)) {
    New-Item -ItemType File -Path $Profile -Force | Out-Null
}

$ProfileContent = Get-Content $Profile -Raw -ErrorAction SilentlyContinue
if ($ProfileContent -match 'BSI_MCP_API_KEY') {
    $ProfileContent = $ProfileContent -replace '\$env:BSI_MCP_API_KEY\s*=\s*"[^"]*"', $EnvLine
    Set-Content $Profile $ProfileContent
    Write-Host "BSI_MCP_API_KEY im PowerShell-Profil aktualisiert."
} else {
    Add-Content $Profile "`n$EnvLine"
    Write-Host "BSI_MCP_API_KEY im PowerShell-Profil eingetragen."
}

# Direkt in aktuelle Session laden
$env:BSI_MCP_API_KEY = $ApiKey

# --- 3. Claude Desktop App konfigurieren ----------------------------------

$ClaudeDir = Split-Path $ClaudeDesktopConfig
if (-not (Test-Path $ClaudeDir)) {
    Write-Host "Claude Desktop Config-Verzeichnis nicht gefunden – überspringe Desktop-Setup."
} else {
    if (-not (Test-Path $ClaudeDesktopConfig)) {
        '{}' | Set-Content $ClaudeDesktopConfig
    }

    $Config = Get-Content $ClaudeDesktopConfig -Raw | ConvertFrom-Json

    if (-not $Config.mcpServers) {
        $Config | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value ([PSCustomObject]@{})
    }

    $McpEntry = [PSCustomObject]@{
        command = "npx"
        args    = @(
            "mcp-remote",
            $McpUrl,
            "--header",
            "X-API-KEY:$ApiKey"
        )
    }

    $Config.mcpServers | Add-Member -MemberType NoteProperty -Name "azure-knowledge-base" -Value $McpEntry -Force

    $Config | ConvertTo-Json -Depth 10 | Set-Content $ClaudeDesktopConfig
    Write-Host "Claude Desktop Config aktualisiert."
}

# --- 4. Projekt .claude/settings.json sicherstellen ----------------------

$SettingsDir = Join-Path $RepoDir ".claude"
$SettingsFile = Join-Path $SettingsDir "settings.json"

if (Test-Path $SettingsFile) {
    Write-Host ".claude/settings.json bereits vorhanden (Claude Code CLI)."
} else {
    New-Item -ItemType Directory -Path $SettingsDir -Force | Out-Null
    @"
{
  "mcpServers": {
    "azure-knowledge-base": {
      "type": "http",
      "url": "$McpUrl",
      "headers": {
        "X-API-KEY": "`${BSI_MCP_API_KEY}"
      }
    }
  }
}
"@ | Set-Content $SettingsFile
    Write-Host ".claude/settings.json angelegt."
}

# --- Fertig ---------------------------------------------------------------

Write-Host ""
Write-Host "Setup abgeschlossen."
Write-Host "Bitte Claude Code / Claude Desktop App neu starten."
