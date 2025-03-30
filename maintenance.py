#!/usr/bin/env python3
import os
import time
from datetime import datetime, timedelta
from git import Repo

# Configuration spécifique à votre dépôt
REPO_NAME = "david15tonon/autopub"  # Modifié selon votre image
WORK_DIR = "/workspaces/autopub"     # Chemin dans Codespace
COMMIT_FILE = "daily_update.md"      # Fichier à modifier pour les commits

def setup_repo():
    # Initialiser le dépôt
    if not os.path.exists(WORK_DIR):
        repo_url = f"https://github.com/{REPO_NAME}.git"
        repo = Repo.clone_from(repo_url, WORK_DIR)
    else:
        repo = Repo(WORK_DIR)
    
    # Configuration Git minimale
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", "Maintenance Bot")
        git_config.set_value("user", "email", "bot@example.com")
    
    return repo

def make_daily_commit(repo):
    # Créer/modifier le fichier de suivi
    with open(os.path.join(WORK_DIR, COMMIT_FILE), "a+") as f:
        f.write(f"- Maintenance update {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # Commit et push
    repo.git.add(COMMIT_FILE)
    commit_msg = f"Daily maintenance {datetime.now().strftime('%d/%m')}"
    repo.index.commit(commit_msg)
    repo.git.push()
    print(f"Commit effectué: {commit_msg}")

def main():
    repo = setup_repo()
    end_date = datetime.now() + timedelta(days=7)  
    
    try:
        while datetime.now() < end_date:
            make_daily_commit(repo)
            
            # Prochain commit entre 21h et 23h
            next_run = datetime.now().replace(
                hour=21 + hash(datetime.now().date()) % 2,
                minute=0,
                second=0
            ) + timedelta(days=1)
            
            sleep_time = (next_run - datetime.now()).total_seconds()
            print(f"Prochain commit à {next_run}")
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("Arrêt manuel du script")
    finally:
        print("Maintenance automatique terminée")

if __name__ == "__main__":
    main()
