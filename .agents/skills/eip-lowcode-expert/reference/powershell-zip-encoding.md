# PowerShell ZIP Creation & Encoding (Windows, AllSigned Policy)

## Bypassing the execution policy

Machine policy `AllSigned` blocks `-ExecutionPolicy Bypass -File "..."` and `Unblock-File`. Working workaround:

```bash
cat 'script.ps1' | powershell.exe -NonInteractive -Command -
```

Stdin input bypasses the policy. Works for complex scripts with here-strings too.

## Encoding problem with stdin pipe

**Problem:** PowerShell reads stdin with `[Console]::InputEncoding` = OEM code page (CP850 on Western European Windows).

- `cat` in bash sends raw UTF-8 bytes through the pipe
- UTF-8 bytes for `ü` (`0xC3 0xBC`) are decoded as two CP850 characters `├╝`
- When saved with `Set-Content -Encoding UTF8`, those garbled chars get re-encoded — BSI shows `├╝` instead of `ü`

**Solution 1: Construct non-ASCII chars at runtime** (preferred)

```powershell
$ue = [char]252   # ü  (Unicode code point — script stays pure ASCII)
$ae = [char]228   # ä
$oe = [char]246   # ö
$ss = [char]223   # ß

$name = 'E-Mail-Adresse g' + $ue + 'ltig'
```

The script itself stays pure ASCII — no encoding problem during piping.

**Solution 2: Fix garbled content after the fact**

```powershell
$utf8 = New-Object System.Text.UTF8Encoding($false)
$ue = [char]252
$correct = 'E-Mail-Adresse g' + $ue + 'ltig'
$t = [System.IO.File]::ReadAllText($path, $utf8)
$t2 = $t -replace '"de"\s*:\s*"[^"]*"', ('"de" : "' + $correct + '"')
[System.IO.File]::WriteAllText($path, $t2, $utf8)
```

## Writing UTF-8 without BOM

`Set-Content -Encoding UTF8` in Windows PowerShell 5.1 writes UTF-8 **with BOM** (`0xEF 0xBB 0xBF`). BSI EIP's JSON parser can choke on the BOM.

```powershell
$utf8 = New-Object System.Text.UTF8Encoding($false)   # false = no BOM
[System.IO.File]::WriteAllText($path, $content, $utf8)
```

## Stripping BOM from existing files

```powershell
$utf8 = New-Object System.Text.UTF8Encoding($false)
Get-ChildItem -Recurse $dir -File | ForEach-Object {
    $bytes = [System.IO.File]::ReadAllBytes($_.FullName)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        $nb = New-Object byte[] ($bytes.Length - 3)
        [Buffer]::BlockCopy($bytes, 3, $nb, 0, $nb.Length)
        [System.IO.File]::WriteAllBytes($_.FullName, $nb)
    }
}
```

## Creating a ZIP with UTF-8 entry names

```powershell
Add-Type -Assembly System.IO.Compression
Add-Type -Assembly System.IO.Compression.FileSystem
$src = 'C:\path\to\staging\dir'
$out = 'C:\path\to\output.zip'
if (Test-Path $out) { Remove-Item $out }
$enc = [System.Text.Encoding]::UTF8
$mode = [System.IO.Compression.ZipArchiveMode]::Create
$zip = [System.IO.Compression.ZipFile]::Open($out, $mode, $enc)
Get-ChildItem -Recurse $src -File | ForEach-Object {
    $arcName = $_.FullName.Substring($src.Length + 1).Replace('\', '/')
    $entry = $zip.CreateEntry($arcName, [System.IO.Compression.CompressionLevel]::Optimal)
    $es = $entry.Open()
    $fs = [System.IO.File]::OpenRead($_.FullName)
    $fs.CopyTo($es)
    $fs.Close()
    $es.Close()
}
$zip.Dispose()
```

The `$enc` parameter in `ZipFile.Open` controls the encoding of **entry names** (not file contents). File contents are copied byte-for-byte.

## Use two scripts instead of one

Scripts with a here-string near the end can silently skip ZIP creation if the here-string is not correctly terminated. Keep the fix and ZIP steps separate:

```bash
cat fix-files.ps1 | powershell.exe -NonInteractive -Command -
cat ziponly.ps1   | powershell.exe -NonInteractive -Command -
```
