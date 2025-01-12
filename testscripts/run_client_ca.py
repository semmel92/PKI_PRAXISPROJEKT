import os
import subprocess

# Variablen
IMAGE_NAME = "client_ca_image"
CONTAINER_NAME = "client_ca_container"
OUTPUT_DIR = "./output"

def run_command(command, error_message):
    """Hilfsfunktion zum Ausführen von Shell-Befehlen."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print(error_message)
        exit(1)

# 1. Docker-Image bauen
print("Baue Docker-Image für Client CA...")
run_command(
    f"docker build -t {IMAGE_NAME} -f Dockerfile-client-ca .",
    "Fehler beim Bauen des Docker-Images für Client CA."
)

# 2. Container starten
print("Starte Container für Client CA...")
run_command(
    f"docker run --name {CONTAINER_NAME} -v {os.path.abspath(OUTPUT_DIR)}:/app/output {IMAGE_NAME}",
    "Fehler beim Starten des Containers für Client CA."
)

# 3. Container bereinigen
print("Bereinige Container...")
run_command(
    f"docker rm {CONTAINER_NAME}",
    "Fehler beim Entfernen des Containers."
)

# 4. Ergebnisse anzeigen
print(f"Client-Zertifikate wurden im Ordner '{OUTPUT_DIR}' gespeichert:")
for file in os.listdir(OUTPUT_DIR):
    if "client" in file:
        print(f"- {file}")
