import datetime
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
import os

# Verzeichnisse und Dateien
output_dir = "./output"
crl_path = os.path.join(output_dir, "intermediateCA.crl")
intermediate_key_path = os.path.join(output_dir, "intermediateCA.key")
intermediate_cert_path = os.path.join(output_dir, "intermediateCA.crt")

# Verfügbare Zertifikate anzeigen
print("Verfügbare End-Entity-Zertifikate:")
cert_files = [f for f in os.listdir(output_dir) if f.endswith(".crt") and "intermediate" not in f and "root" not in f]

if not cert_files:
    print("Keine End-Entity-Zertifikate gefunden.")
    exit(1)

cert_data = []
for cert_file in cert_files:
    cert_path = os.path.join(output_dir, cert_file)
    with open(cert_path, "rb") as cert_file_obj:
        cert = x509.load_pem_x509_certificate(cert_file_obj.read())
        serial_number = cert.serial_number
        common_name = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        cert_data.append((serial_number, common_name, cert_path))
        print(f"- Seriennummer: {serial_number}, Common Name: {common_name}, Datei: {cert_path}")

# Zertifikat auswählen
try:
    selected_serial = int(input("\nGib die Seriennummer des zu widerrufenden Zertifikats ein: "))
    selected_cert = next((data for data in cert_data if data[0] == selected_serial), None)

    if not selected_cert:
        print("Ungültige Seriennummer eingegeben.")
        exit(1)

    print(f"Zertifikat zum Widerruf ausgewählt: Seriennummer {selected_serial}, Common Name: {selected_cert[1]}")
except ValueError:
    print("Ungültige Eingabe. Bitte eine gültige Seriennummer eingeben.")
    exit(1)

# Intermediate CA laden
print("Lade Intermediate-CA Schlüssel und Zertifikat...")
with open(intermediate_key_path, "rb") as key_file:
    intermediate_key = serialization.load_pem_private_key(key_file.read(), password=None)
with open(intermediate_cert_path, "rb") as cert_file:
    intermediate_cert = x509.load_pem_x509_certificate(cert_file.read())

# CRL laden oder neue erstellen
if os.path.exists(crl_path):
    print("Lade bestehende CRL...")
    with open(crl_path, "rb") as crl_file:
        crl = x509.load_pem_x509_crl(crl_file.read())
    
    # Neuer CRL-Builder mit bestehenden Einträgen
    crl_builder = x509.CertificateRevocationListBuilder()
    crl_builder = crl_builder.issuer_name(crl.issuer)
    crl_builder = crl_builder.last_update(crl.last_update)
    crl_builder = crl_builder.next_update(datetime.datetime.utcnow() + datetime.timedelta(days=30))

    for revoked_cert in crl:
        crl_builder = crl_builder.add_revoked_certificate(revoked_cert)
else:
    print("CRL nicht gefunden. Bitte erstelle eine mit 'create_crl.py'.")
    exit(1)

# Zertifikat widerrufen
print(f"Füge Zertifikat mit Seriennummer {selected_serial} zur CRL hinzu...")
revocation_date = datetime.datetime.utcnow()
revoked_cert = x509.RevokedCertificateBuilder() \
    .serial_number(selected_serial) \
    .revocation_date(revocation_date) \
    .build()
crl_builder = crl_builder.add_revoked_certificate(revoked_cert)

# Aktualisierte CRL signieren
print("Signiere aktualisierte CRL...")
new_crl = crl_builder.sign(private_key=intermediate_key, algorithm=hashes.SHA256())

# CRL speichern
with open(crl_path, "wb") as crl_file:
    crl_file.write(new_crl.public_bytes(serialization.Encoding.PEM))
print(f"CRL aktualisiert und gespeichert: {crl_path}")
