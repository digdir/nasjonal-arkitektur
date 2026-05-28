import os
import subprocess
import sys

def main():
    print("Starter workflow: Bygg og publiser til GitHub\n")
    
    print("Steg 1: Kjører bygg_lokalt.py...")
    # Kjører bygg_lokalt.py
    result = subprocess.run(["python", "bygg_lokalt.py"])
    if result.returncode != 0:
        print("Feil under bygging. Avbryter publisering.")
        sys.exit(1)
        
    print("\nSteg 2: Forbereder Git commit og push...")
    
    # Sjekk om det er endringer
    status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not status_result.stdout.strip():
        print("Ingen endringer å committe. Alt er oppdatert!")
        sys.exit(0)

    # Bruk eventuell commit-melding fra kommandolinjen, ellers en standardmelding
    commit_msg = "Automatisk oppdatering av dokumentasjon"
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    
    print("Legger til endringer i Git (git add .)...")
    subprocess.run(["git", "add", "."])
    
    print(f"Committer endringer med melding: '{commit_msg}'...")
    commit_result = subprocess.run(["git", "commit", "-m", commit_msg])
    if commit_result.returncode != 0:
        print("Feil under commit.")
        sys.exit(1)
        
    print("\nSteg 3: Pusher til GitHub...")
    push_result = subprocess.run(["git", "push"])
    if push_result.returncode != 0:
        print("Feil under push. Sjekk at du har tilgang og at du ikke har konflikter med remote.")
        sys.exit(1)
        
    print("\nSuksess! Prosjektet er bygget og alle endringer er publisert til GitHub.")

if __name__ == "__main__":
    main()
