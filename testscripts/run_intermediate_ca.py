import os
import subprocess

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

print("Baue Docker-Image für Intermediate CA...")
run_command(
    f"docker build -t {IMAGE_NAME} -f dockerfiles/Dockerfile-intermediate-ca .",
    "Fehler beim Bauen des Docker-Images für Intermediate CA."
)

print("Starte Container für Intermediate CA...")
run_command(
    f"docker run --name {CONTAINER_NAME} -v {os.path.abspath(OUTPUT_DIR)}:/app/output {IMAGE_NAME}",
    "Fehler beim Starten des Containers für Intermediate CA."
)

print("Kopiere Dateien aus dem Container...")
run_command(
    f"docker cp {CONTAINER_NAME}:/app/output/intermediateCA.key {os.path.join(OUTPUT_DIR, 'intermediateCA.key')}",
    "Fehler beim Kopieren von intermediateCA.key."
)
run_command(
    f"docker cp {CONTAINER_NAME}:/app/output/intermediateCA.crt {os.path.join(OUTPUT_DIR, 'intermediateCA.crt')}",
    "Fehler beim Kopieren von intermediateCA.crt."
)

print("Bereinige Container...")
run_command(
    f"docker rm {CONTAINER_NAME}",
    "Fehler beim Entfernen des Containers."
)

print(f"\nIntermediate-CA-Dateien wurden im Ordner '{OUTPUT_DIR}' gespeichert:")
for file in os.listdir(OUTPUT_DIR):
    print(f"- {file}")
