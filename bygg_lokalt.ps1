# Skript for å bygge dokumentasjonen lokalt før man pusher til GitHub
Write-Host "Starter lokal bygging av dokumentasjon..." -ForegroundColor Cyan

# Sjekk at modellfilen finnes
$modelPath = "model/Nasjonal Arkitektur kapabilitetsmodell-2026-05-20.archimate"
if (!(Test-Path $modelPath)) {
    Write-Host "Finner ikke modellfilen: $modelPath. Vennligst sjekk stien." -ForegroundColor Red
    Pause
    exit
}

# 1. Konverter ArchiMate til YAML
Write-Host "`n[1/3] Konverterer ArchiMate til YAML..." -ForegroundColor Yellow
python scripts/convert_archimate_to_yaml.py $modelPath "data/nasjonal-arkitektur.yaml"
if ($LASTEXITCODE -ne 0) { Write-Host "Feil under konvertering." -ForegroundColor Red; Pause; exit }

# 2. Generer Markdown-filer fra YAML og kopierer inn HTML-rapport bilder
Write-Host "`n[2/3] Genererer Markdown-dokumentasjon..." -ForegroundColor Yellow
python scripts/generate_docs.py
if ($LASTEXITCODE -ne 0) { Write-Host "Feil under generering." -ForegroundColor Red; Pause; exit }

# 3. Kopier råfiler til docs-mappen slik at de kan lastes ned fra forsiden
Write-Host "`n[3/3] Kopierer kilde- og datafiler til docs-mappen for nedlasting..." -ForegroundColor Yellow
Copy-Item "data/nasjonal-arkitektur.yaml" -Destination "docs/" -Force
Copy-Item $modelPath -Destination "docs/Nasjonal Arkitektur kapabilitetsmodell.archimate" -Force

Write-Host "`nFerdig! Dokumentasjonen er bygget lokalt i docs-mappen." -ForegroundColor Green
Write-Host "Du kan nå sjekke resultatet lokalt (ved å kjøre 'mkdocs serve') eller legge til filene i git, committe og pushe." -ForegroundColor Cyan
Pause
