import os
import shutil
import subprocess

def run_command(command, success_message, error_message):
    """Hilfsfunktion zum Ausführen von Shell-Befehlen."""
    try:
        subprocess.run(command, check=True, shell=True)
        print(success_message)
    except subprocess.CalledProcessError:
        print(error_message)

print("Überprüfe und entferne den Container 'root_ca_container'...")
run_command(
    "docker stop root_ca_container",
    "Container 'root_ca_container' wurde gestoppt.",
    "Container 'root_ca_container' läuft nicht oder konnte nicht gestoppt werden."
)
run_command(
    "docker rm root_ca_container",
    "Container 'root_ca_container' wurde entfernt.",
    "Container 'root_ca_container' existiert nicht oder konnte nicht entfernt werden."
)

print("Überprüfe und entferne den Container 'intermediate_ca_container'...")
run_command(
    "docker stop intermediate_ca_container",
    "Container 'intermediate_ca_container' wurde gestoppt.",
    "Container 'intermediate_ca_container' läuft nicht oder konnte nicht gestoppt werden."
)
run_command(
    "docker rm intermediate_ca_container",
    "Container 'intermediate_ca_container' wurde entfernt.",
    "Container 'intermediate_ca_container' existiert nicht oder konnte nicht entfernt werden."
)

print("Überprüfe und entferne den Container 'client_ca_container'...")
run_command(
    "docker stop client_ca_container",
    "Container 'client_ca_container' wurde gestoppt.",
    "Container 'client_ca_container' läuft nicht oder konnte nicht gestoppt werden."
)
run_command(
    "docker rm client_ca_container",
    "Container 'client_ca_container' wurde entfernt.",
    "Container 'client_ca_container' existiert nicht oder konnte nicht entfernt werden."
)

print("Überprüfe und entferne den Container 'webserver'...")
run_command(
    "docker stop webserver",
    "Container 'webserver' wurde gestoppt.",
    "Container 'webserver' läuft nicht oder konnte nicht gestoppt werden."
)
run_command(
    "docker rm webserver",
    "Container 'webserver' wurde entfernt.",
    "Container 'webserver' existiert nicht oder konnte nicht entfernt werden."
)

print("Stoppe und entferne alle Container aus 'docker-compose.yml'...")
run_command(
    "docker-compose -f docker-compose.yml down",
    "Alle PKI-Komponenten wurden gestoppt und entfernt.",
    "Fehler beim Stoppen und Entfernen der PKI-Komponenten."
)

print("Stoppe und entferne alle Container aus 'docker-compose-web.yml'...")
run_command(
    "docker-compose -f docker-compose-web.yml down",
    "Webserver und Client wurden gestoppt und entfernt.",
    "Fehler beim Stoppen und Entfernen des Webservers und Clients."
)

print("Bereinige ungenutzte Docker-Ressourcen...")
run_command(
    "docker image prune -f",
    "Ungenutzte Docker-Images wurden entfernt.",
    "Fehler beim Entfernen ungenutzter Docker-Images."
)
run_command(
    "docker volume prune -f",
    "Ungenutzte Docker-Volumes wurden entfernt.",
    "Fehler beim Entfernen ungenutzter Docker-Volumes."
)
run_command(
    "docker network prune -f",
    "Ungenutzte Docker-Netzwerke wurden entfernt.",
    "Fehler beim Entfernen ungenutzter Docker-Netzwerke."
)

output_dir = "./output"
if os.path.exists(output_dir):
    print("Bereinige Output-Verzeichnis...")
    shutil.rmtree(output_dir)
os.makedirs(output_dir, exist_ok=True)
print("Output-Verzeichnis wurde bereinigt.")

print("\nDocker-Bereinigung abgeschlossen!")
