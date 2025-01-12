from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509 import NameOID
import datetime
from cryptography import x509
import os

# Aktuelles Arbeitsverzeichnis ermitteln
output_dir = os.getcwd()  # Arbeitet innerhalb von /app im Docker-Container

# 1. RSA-Schlüssel generieren
print("Generiere RSA-Schlüssel...")
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
)

# Privaten Schlüssel im PEM-Format speichern
with open(os.path.join(output_dir, "rootCA.key"), "wb") as key_file:
    key_file.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
print(f"Private Key gespeichert: {os.path.join(output_dir, 'rootCA.key')}")

# 2. Root-Zertifikat erstellen
print("Erstelle Root-Zertifikat...")
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "AT"),          # Land (z. B. AT für Österreich)
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Burgenland"),  # Bundesland
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Eisenstadt"),          # Ort
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My CA"),  # Name der Organisation
    x509.NameAttribute(NameOID.COMMON_NAME, "My Root CA"),   # Anzeigename
])

# Zertifikat-Objekt erstellen
root_certificate = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(private_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))  # 10 Jahre gültig
    .add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    )
    .sign(private_key, hashes.SHA256())  # Selbstsigniert
)

# Root-Zertifikat im PEM-Format speichern
with open(os.path.join(output_dir, "rootCA.crt"), "wb") as cert_file:
    cert_file.write(root_certificate.public_bytes(serialization.Encoding.PEM))
print(f"Root-Zertifikat gespeichert: {os.path.join(output_dir, 'rootCA.crt')}")
