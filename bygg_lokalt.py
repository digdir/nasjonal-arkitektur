import os
import subprocess
import shutil
import sys

def main():
    print("Starter lokal bygging av dokumentasjon...")
    
    model_path = "model/Nasjonal Arkitektur kapabilitetsmodell-2026-05-20.archimate"
    if not os.path.exists(model_path):
        print(f"Feil: Finner ikke modellfilen: {model_path}")
        sys.exit(1)
        
    print("\n[1/3] Konverterer ArchiMate til YAML...")
    result = subprocess.run(["python", "scripts/convert_archimate_to_yaml.py", model_path, "data/nasjonal-arkitektur.yaml"])
    if result.returncode != 0:
        print("Feil under konvertering til YAML.")
        sys.exit(1)
        
    print("\n[2/3] Genererer Markdown-dokumentasjon...")
    result = subprocess.run(["python", "scripts/generate_docs.py"])
    if result.returncode != 0:
        print("Feil under generering av dokumentasjon.")
        sys.exit(1)
        
    print("\n[3/3] Kopierer kilde- og datafiler til docs-mappen for nedlasting...")
    os.makedirs("docs", exist_ok=True)
    shutil.copy2("data/nasjonal-arkitektur.yaml", "docs/nasjonal-arkitektur.yaml")
    shutil.copy2(model_path, "docs/Nasjonal Arkitektur kapabilitetsmodell.archimate")
    
    print("\nFerdig! Dokumentasjonen er bygget lokalt i docs-mappen.")
    print("Du kan nå committe endringene og pushe til GitHub.")

if __name__ == "__main__":
    main()
