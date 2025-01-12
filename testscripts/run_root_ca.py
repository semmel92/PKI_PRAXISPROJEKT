import os
import subprocess

# Variablen
IMAGE_NAME = "root_ca_image"
CONTAINER_NAME = "root_ca_container"
OUTPUT_DIR = "./output"

def run_command(command, error_message):
    """Hilfsfunktion zum Ausführen von Shell-Befehlen."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print(error_message)
        exit(1)

# 1. Docker-Image bauen
print("Baue Docker-Image für Root CA...")
run_command(
    f"docker build -t {IMAGE_NAME} -f Dockerfile-root-ca .",
    "Fehler beim Bauen des Docker-Images für Root CA."
)

# 2. Container starten
print("Starte Container für Root CA...")    
run_command(
    f"docker run --name {CONTAINER_NAME} {IMAGE_NAME}",
    "Fehler beim Starten des Containers für Root CA."
)

# 3. Output-Verzeichnis erstellen
print("Bereite Output-Verzeichnis vor...")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 4. Dateien aus dem Container kopieren
print("Kopiere Dateien aus dem Container...")
run_command(
    f"docker cp {CONTAINER_NAME}:/app/rootCA.key {os.path.join(OUTPUT_DIR, 'rootCA.key')}",
    "Fehler beim Kopieren von rootCA.key."
)
run_command(
    f"docker cp {CONTAINER_NAME}:/app/rootCA.crt {os.path.join(OUTPUT_DIR, 'rootCA.crt')}",
    "Fehler beim Kopieren von rootCA.crt."
)

# 5. Container entfernen
print("Bereinige Container...")
run_command(
    f"docker rm {CONTAINER_NAME}",
    "Fehler beim Entfernen des Containers."
)

# 6. Ergebnisse anzeigen
print(f"Root-CA-Dateien wurden im Ordner '{OUTPUT_DIR}' gespeichert:")
for file in os.listdir(OUTPUT_DIR):
    print(f"- {file}")
