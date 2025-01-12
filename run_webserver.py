import os
import subprocess

# Verzeichnisse und Dateien
output_dir = "./output"
webserver_cert = os.path.join(output_dir, "client.crt")
webserver_key = os.path.join(output_dir, "client.key")
crl_file = os.path.join(output_dir, "intermediateCA.crl")
nginx_conf = "./nginx.conf"

# Docker-Container-Name
webserver_container = "webserver"

# Sicherstellen, dass alle benötigten Dateien existieren
required_files = [webserver_cert, webserver_key, crl_file, nginx_conf]
missing_files = [file for file in required_files if not os.path.exists(file)]

if missing_files:
    print(f"Fehler: Die folgenden Dateien fehlen:\n" + "\n".join(missing_files))
    exit(1)

# Funktion: Webserver starten
def start_webserver():
    try:
        subprocess.run(
            [
                "docker", "run", "--name", webserver_container, "-d", "-p", "443:443",
                "-v", os.path.abspath(webserver_cert) + ":/etc/nginx/certs/client.crt",
                "-v", os.path.abspath(webserver_key) + ":/etc/nginx/certs/client.key",
                "-v", os.path.abspath(crl_file) + ":/etc/nginx/certs/intermediateCA.crl",
                "-v", os.path.abspath(nginx_conf) + ":/etc/nginx/nginx.conf",
                "nginx:latest"
            ],
            check=True
        )
        print("✅ Webserver wurde erfolgreich gestartet.")
        print("\n🔗 Aufruf des Servers:")
        print("   Öffne deinen Browser: https://localhost")
    except subprocess.CalledProcessError:
        print("❌ Fehler beim Starten des Webservers.")
        exit(1)

# Funktion: Vorherige Instanz entfernen
def clean_webserver():
    subprocess.run(["docker", "stop", webserver_container], stderr=subprocess.DEVNULL)
    subprocess.run(["docker", "rm", webserver_container], stderr=subprocess.DEVNULL)

# Webserver stoppen, falls er läuft, und neu starten
clean_webserver()
start_webserver()
