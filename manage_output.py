import os
import subprocess

OUTPUT_DIR = "./output"
IMAGE_NAME = "client_ca_image"
CONTAINER_NAME = "client_ca_container"

def run_command(command, error_message):
    """Hilfsfunktion zum Ausführen von Shell-Befehlen."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print(error_message)
        exit(1)

def prepare_output_directory():
    """Bereitet das Output-Verzeichnis vor."""
    print("Bereite das Verzeichnis vor...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    run_command(f"chmod 775 {OUTPUT_DIR}", "Fehler beim Setzen der Berechtigungen für das Output-Verzeichnis.")
    run_command(f"chown {os.getuid()}:{os.getgid()} {OUTPUT_DIR}", "Fehler beim Setzen des Besitzers für das Output-Verzeichnis.")

def start_container():
    """Startet den Docker-Container."""
    print("Starte den Docker-Container...")
    run_command(
        f"docker run --name {CONTAINER_NAME} -v {os.path.abspath(OUTPUT_DIR)}:/app/output {IMAGE_NAME}",
        "Fehler beim Starten des Docker-Containers."
    )

def fix_output_permissions():
    """Korrigiert die Berechtigungen nach der Container-Ausführung."""
    print("Korrigiere Berechtigungen für das Output-Verzeichnis...")
    run_command(f"chmod -R 775 {OUTPUT_DIR}", "Fehler beim Setzen der Berechtigungen für das Output-Verzeichnis.")
    run_command(f"chown -R {os.getuid()}:{os.getgid()} {OUTPUT_DIR}", "Fehler beim Setzen des Besitzers für das Output-Verzeichnis.")

def list_output_files():
    """Listet die Dateien im Output-Verzeichnis auf."""
    print("Fertig! Dateien im Output-Verzeichnis:")
    for file in os.listdir(OUTPUT_DIR):
        print(f"- {file}")

# Workflow
if __name__ == "__main__":
    prepare_output_directory()
    start_container()
    fix_output_permissions()
    list_output_files()
