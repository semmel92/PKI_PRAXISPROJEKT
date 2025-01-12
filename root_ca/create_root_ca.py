from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509 import NameOID
import datetime
from cryptography import x509
import os

output_dir = os.getcwd()

print("Generiere RSA-Schlüssel...")
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
)

with open(os.path.join(output_dir, "rootCA.key"), "wb") as key_file:
    key_file.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
print(f"Private Key gespeichert: {os.path.join(output_dir, 'rootCA.key')}")

print("Erstelle Root-Zertifikat...")
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "AT"),      
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Burgenland"), 
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Eisenstadt"),   
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My CA"), 
    x509.NameAttribute(NameOID.COMMON_NAME, "My Root CA"), 
])

root_certificate = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(private_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))
    .add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    )
    .sign(private_key, hashes.SHA256())
)

with open(os.path.join(output_dir, "rootCA.crt"), "wb") as cert_file:
    cert_file.write(root_certificate.public_bytes(serialization.Encoding.PEM))
print(f"Root-Zertifikat gespeichert: {os.path.join(output_dir, 'rootCA.crt')}")
