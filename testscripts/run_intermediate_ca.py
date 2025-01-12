import os
import subprocess

# Variablen
IMAGE_NAME = "intermediate_ca_image"
CONTAINER_NAME = "intermediate_ca_container"
OUTPUT_DIR = "./output"

def run_command(command, error_message):
    """Hilfsfunktion zum Ausführen von Shell-Befehlen."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print(error_message)
        exit(1)

# 1. Docker-Image bauen
print("Baue Docker-Image für Intermediate CA...")
run_command(
    f"docker build -t {IMAGE_NAME} -f Dockerfile-intermediate-ca .",
    "Fehler beim Bauen des Docker-Images für Intermediate CA."
)

# 2. Container starten und Output-Ordner mounten
print("Starte Container für Intermediate CA...")
run_command(
    f"docker run --name {CONTAINER_NAME} -v {os.path.abspath(OUTPUT_DIR)}:/app/output {IMAGE_NAME}",
    "Fehler beim Starten des Containers für Intermediate CA."
)

# 3. Dateien aus dem Container kopieren
print("Kopiere Dateien aus dem Container...")
run_command(
    f"docker cp {CONTAINER_NAME}:/app/output/intermediateCA.key {os.path.join(OUTPUT_DIR, 'intermediateCA.key')}",
    "Fehler beim Kopieren von intermediateCA.key."
)
run_command(
    f"docker cp {CONTAINER_NAME}:/app/output/intermediateCA.crt {os.path.join(OUTPUT_DIR, 'intermediateCA.crt')}",
    "Fehler beim Kopieren von intermediateCA.crt."
)

# 4. Container entfernen
print("Bereinige Container...")
run_command(
    f"docker rm {CONTAINER_NAME}",
    "Fehler beim Entfernen des Containers."
)

# 5. Ergebnisse anzeigen
print(f"\nIntermediate-CA-Dateien wurden im Ordner '{OUTPUT_DIR}' gespeichert:")
for file in os.listdir(OUTPUT_DIR):
    print(f"- {file}")
