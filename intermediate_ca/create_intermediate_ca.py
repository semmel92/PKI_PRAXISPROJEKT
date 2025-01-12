from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509 import NameOID, CertificateBuilder, BasicConstraints
from cryptography import x509
import datetime
import os

output_dir = "./output" 
root_key_path = os.path.join(output_dir, "rootCA.key")
root_cert_path = os.path.join(output_dir, "rootCA.crt")

print("Generiere Intermediate-Schlüssel...")
intermediate_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
)
intermediate_key_path = os.path.join(output_dir, "intermediateCA.key")
with open(intermediate_key_path, "wb") as key_file:
    key_file.write(
        intermediate_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
print(f"Intermediate-Schlüssel gespeichert: {intermediate_key_path}")

print("Erstelle Certificate Signing Request (CSR)...")
subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "AT"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Burgenland"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Eisenstadt"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Intermediate CA"),
    x509.NameAttribute(NameOID.COMMON_NAME, "My Intermediate CA"),
])
csr = x509.CertificateSigningRequestBuilder().subject_name(subject).sign(
    intermediate_key, hashes.SHA256()
)

print("Lade Root-CA Schlüssel und Zertifikat...")
with open(root_key_path, "rb") as key_file:
    root_key = serialization.load_pem_private_key(key_file.read(), password=None)
with open(root_cert_path, "rb") as cert_file:
    root_cert = x509.load_pem_x509_certificate(cert_file.read())

print("Signiere Intermediate-Zertifikat mit Root-CA...")
intermediate_cert = (
    CertificateBuilder()
    .subject_name(csr.subject)
    .issuer_name(root_cert.subject)
    .public_key(csr.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))
    .add_extension(
        BasicConstraints(ca=True, path_length=0),
        critical=True,
    )
    .sign(root_key, hashes.SHA256())
)

intermediate_cert_path = os.path.join(output_dir, "intermediateCA.crt")
with open(intermediate_cert_path, "wb") as cert_file:
    cert_file.write(intermediate_cert.public_bytes(serialization.Encoding.PEM))
print(f"Intermediate-Zertifikat gespeichert: {intermediate_cert_path}")
