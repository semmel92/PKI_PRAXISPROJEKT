import os
import subprocess

output_dir = "./output"
webserver_cert = os.path.join(output_dir, "client.crt")
webserver_key = os.path.join(output_dir, "client.key")
p12_file = os.path.join(output_dir, "client.p12")

if not os.path.exists(webserver_cert) or not os.path.exists(webserver_key):
    print("Fehler: Zertifikat oder Schlüssel für PKCS#12-Datei nicht gefunden.")
    exit(1)

def create_p12():
    try:
        subprocess.run(
            [
                "openssl", "pkcs12", "-export",
                "-in", webserver_cert,
                "-inkey", webserver_key,
                "-out", p12_file,
                "-name", "Client Certificate",
                "-password", "pass:1234" 
            ],
            check=True
        )
        print(f"✅ PKCS#12-Datei erstellt: {p12_file}")
        print(f"   Passwort: 1234")
    except subprocess.CalledProcessError:
        print("❌ Fehler beim Erstellen der PKCS#12-Datei.")
        exit(1)

create_p12()
