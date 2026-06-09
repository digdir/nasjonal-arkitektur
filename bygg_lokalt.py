import os
import subprocess
import shutil
import sys

def main():
    print("Starter lokal bygging av dokumentasjon...")
    
    import glob
    
    archimate_files = glob.glob("model/*.archimate")
    if not archimate_files:
        print("Feil: Finner ingen .archimate-filer i model/-mappen.")
        sys.exit(1)
        
    # Sorterer filene alfabetisk (noe som fungerer perfekt for YYYY-MM-DD datoformatet)
    archimate_files.sort()
    model_path = archimate_files[-1]
    print(f"Fant nyeste modell: {model_path}")
    print("\n[1/4] Konverterer ArchiMate til YAML...")
    result = subprocess.run(["python", "scripts/convert_archimate_to_yaml.py", model_path, "data/nasjonal-arkitektur.yaml"])
    if result.returncode != 0:
        print("Feil under konvertering til YAML.")
        sys.exit(1)
        
    print("\n[2/4] Konverterer ArchiMate til TTL...")
    result = subprocess.run(["python", "scripts/archimate2ttl.py", model_path, "data/nasjonal-arkitektur.ttl"])
    if result.returncode != 0:
        print("Feil under konvertering til TTL.")
        sys.exit(1)
        
    print("\n[3/4] Genererer Markdown-dokumentasjon...")
    result = subprocess.run(["python", "scripts/generate_docs.py"])
    if result.returncode != 0:
        print("Feil under generering av dokumentasjon.")
        sys.exit(1)
        
    print("\n[4/4] Kopierer kilde- og datafiler til docs-mappen for nedlasting...")
    os.makedirs("docs", exist_ok=True)
    shutil.copy2("data/nasjonal-arkitektur.yaml", "docs/nasjonal-arkitektur.yaml")
    shutil.copy2("data/nasjonal-arkitektur.ttl", "docs/nasjonal-arkitektur.ttl")
    shutil.copy2(model_path, "docs/Nasjonal Arkitektur kapabilitetsmodell.archimate")
    
    print("\nFerdig! Dokumentasjonen er bygget lokalt i docs-mappen.")
    print("Du kan nå committe endringene og pushe til GitHub.")

if __name__ == "__main__":
    main()
