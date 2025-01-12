import datetime
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
import os

# Verzeichnisse und Dateien
output_dir = "./output"
crl_path = os.path.join(output_dir, "intermediateCA.crl")
intermediate_key_path = os.path.join(output_dir, "intermediateCA.key")
intermediate_cert_path = os.path.join(output_dir, "intermediateCA.crt")

# Prüfen, ob Output-Verzeichnis existiert
os.makedirs(output_dir, exist_ok=True)

# Intermediate CA laden
print("Lade Intermediate-CA Schlüssel und Zertifikat...")
with open(intermediate_key_path, "rb") as key_file:
    intermediate_key = serialization.load_pem_private_key(key_file.read(), password=None)
with open(intermediate_cert_path, "rb") as cert_file:
    intermediate_cert = x509.load_pem_x509_certificate(cert_file.read())

# CRL laden oder erstellen
if os.path.exists(crl_path):
    print("CRL existiert bereits. Nichts zu tun.")
else:
    print("Erstelle neue CRL...")
    crl_builder = x509.CertificateRevocationListBuilder()
    crl_builder = crl_builder.issuer_name(intermediate_cert.subject)
    crl_builder = crl_builder.last_update(datetime.datetime.utcnow())
    crl_builder = crl_builder.next_update(datetime.datetime.utcnow() + datetime.timedelta(days=30))

    # CRL signieren
    print("Signiere neue CRL...")
    new_crl = crl_builder.sign(private_key=intermediate_key, algorithm=hashes.SHA256())

    # CRL speichern
    with open(crl_path, "wb") as crl_file:
        crl_file.write(new_crl.public_bytes(serialization.Encoding.PEM))
    print(f"CRL erstellt und gespeichert: {crl_path}")
