#!/usr/bin/env python3
import os
import time
from datetime import datetime, timedelta
from git import Repo

# Configuration
REPO_PATH = "/workspaces/autopub"  # Chemin vers votre dépôt
LOG_FILE = "maintenance_log.md"    # Fichier de suivi
GIT_USER = "Maintenance Bot"       # Nom pour les commits
GIT_EMAIL = "maintenance@example.com"  # Email pour les commits
WORKING_HOURS = (18, 23)          # Plage horaire (18h-23h)

class MaintenanceManager:
    def __init__(self):
        self.repo = self.setup_repo()
        self.end_date = datetime.now() + timedelta(days=4)  # Jusqu'à vendredi

    def setup_repo(self):
        """Initialise le dépôt Git avec la configuration de base"""
        repo = Repo(REPO_PATH)
        with repo.config_writer() as config:
            config.set_value("user", "name", GIT_USER)
            config.set_value("user", "email", GIT_EMAIL)
        return repo

    def make_commit(self):
        """Effectue un commit valide pour maintenir le streak"""
        try:
            # Crée/modifie le fichier de log
            with open(os.path.join(REPO_PATH, LOG_FILE), "a+") as f:
                f.write(f"- Maintenance check at {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

            # Ajoute les modifications
            self.repo.git.add(LOG_FILE)
            
            if not self.repo.index.diff("HEAD"):
                # Commit vide si aucun changement (mais avec message utile)
                self.repo.git.commit("--allow-empty", 
                                    "-m", f"Daily maintenance {datetime.now().strftime('%d/%m')}")
                print("Commit vide créé pour maintenir le streak")
            else:
                # Commit normal si modifications détectées
                self.repo.index.commit(f"Maintenance update {datetime.now().strftime('%d/%m %H:%M')}")
                print("Commit standard avec modifications")

            self.repo.git.push()
            return True

        except Exception as e:
            print(f"Erreur lors du commit: {str(e)}")
            return False

    def calculate_next_run(self):
        """Calcule le prochain moment d'exécution entre 18h et 23h"""
        now = datetime.now()
        next_run = now.replace(
            hour=WORKING_HOURS[0] + hash(now.date()) % (WORKING_HOURS[1] - WORKING_HOURS[0]),
            minute=0,
            second=0
        )
        
        # Si l'heure est déjà passée aujourd'hui, on planifie pour demain
        if next_run < now:
            next_run += timedelta(days=1)
            
        return next_run

    def run(self):
        """Exécute la boucle principale"""
        print(f"Début de la maintenance automatique jusqu'au {self.end_date.strftime('%A %d %B')}")
        
        while datetime.now() < self.end_date:
            try:
                if self.make_commit():
                    next_run = self.calculate_next_run()
                    wait_seconds = (next_run - datetime.now()).total_seconds()
                    
                    if wait_seconds > 0:
                        print(f"Prochain commit à {next_run.strftime('%H:%M')}")
                        time.sleep(wait_seconds)
                
            except KeyboardInterrupt:
                print("\nArrêt manuel du script")
                break
            except Exception as e:
                print(f"Erreur inattendue: {e}. Nouvelle tentative dans 1h")
                time.sleep(3600)

        print("Maintenance automatique terminée comme prévu")

if __name__ == "__main__":
    manager = MaintenanceManager()
    manager.run()
