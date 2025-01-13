import os
import subprocess

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

def create_fullchain_in_container():
    """Erstellt die Fullchain innerhalb des Docker-Containers."""
    print("Erstelle Fullchain im Container...")
    run_command(
        f"docker exec {CONTAINER_NAME} sh -c 'cat /app/output/client.crt /app/output/intermediateCA.crt > /app/output/client_with_chain.crt'",
        "Fehler beim Erstellen der Fullchain im Container."
    )

def copy_fullchain_to_host():
    """Kopiert die Fullchain aus dem Container auf den Host."""
    print("Kopiere Fullchain vom Container auf den Host...")
    run_command(
        f"docker cp {CONTAINER_NAME}:/app/output/client_with_chain.crt {os.path.join(OUTPUT_DIR, 'client_with_chain.crt')}",
        "Fehler beim Kopieren der Fullchain vom Container."
    )

print("Baue Docker-Image für Client CA...")
run_command(
    f"docker build -t {IMAGE_NAME} -f dockerfiles/Dockerfile-client-ca .",
    "Fehler beim Bauen des Docker-Images für Client CA."
)

print("Starte Container für Client CA...")
run_command(
    f"docker run --name {CONTAINER_NAME} -v {os.path.abspath(OUTPUT_DIR)}:/app/output {IMAGE_NAME}",
    "Fehler beim Starten des Containers für Client CA."
)

create_fullchain_in_container()
copy_fullchain_to_host()

print("Bereinige Container...")
run_command(
    f"docker rm {CONTAINER_NAME}",
    "Fehler beim Entfernen des Containers."
)

print(f"Client-Zertifikate wurden im Ordner '{OUTPUT_DIR}' gespeichert:")
for file in os.listdir(OUTPUT_DIR):
    if "client" in file or "fullchain" in file:
        print(f"- {file}")
