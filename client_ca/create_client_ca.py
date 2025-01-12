from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509 import NameOID, CertificateBuilder, BasicConstraints
from cryptography import x509
import datetime
import os

output_dir = "./output"
intermediate_key_path = os.path.join(output_dir, "intermediateCA.key")
intermediate_cert_path = os.path.join(output_dir, "intermediateCA.crt")

print("Generiere Client-Schlüssel...")
client_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
)
client_key_path = os.path.join(output_dir, "client.key")
with open(client_key_path, "wb") as key_file:
    key_file.write(
        client_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
print(f"Client-Schlüssel gespeichert: {client_key_path}")

print("Erstelle Certificate Signing Request (CSR)...")
client_subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "AT"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Burgenland"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Eisenstadt"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Client Organization"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])
csr = x509.CertificateSigningRequestBuilder().subject_name(client_subject).sign(
    client_key, hashes.SHA256()
)

print("Lade Intermediate-CA Schlüssel und Zertifikat...")
with open(intermediate_key_path, "rb") as key_file:
    intermediate_key = serialization.load_pem_private_key(key_file.read(), password=None)
with open(intermediate_cert_path, "rb") as cert_file:
    intermediate_cert = x509.load_pem_x509_certificate(cert_file.read())

print("Signiere Client-Zertifikat mit Intermediate-CA...")
client_cert = (
    CertificateBuilder()
    .subject_name(csr.subject)
    .issuer_name(intermediate_cert.subject)
    .public_key(csr.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
    .add_extension(
        BasicConstraints(ca=False, path_length=None),
        critical=True,
    )
    .sign(intermediate_key, hashes.SHA256())
)

client_cert_path = os.path.join(output_dir, "client.crt")
with open(client_cert_path, "wb") as cert_file:
    cert_file.write(client_cert.public_bytes(serialization.Encoding.PEM))
print(f"Client-Zertifikat gespeichert: {client_cert_path}")
