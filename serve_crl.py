from flask import Flask, send_file, jsonify
import os
from cryptography import x509

app = Flask(__name__)
output_dir = "./output"
crl_file = "intermediateCA.crl"

@app.route('/crl/<filename>')
def serve_crl(filename):
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/pkix-crl')
    return "CRL nicht gefunden", 404

@app.route('/revoked-certificates')
def revoked_certificates():
    crl_path = os.path.join(output_dir, crl_file)
    if os.path.exists(crl_path):
        with open(crl_path, "rb") as crl_file_obj:
            crl = x509.load_pem_x509_crl(crl_file_obj.read())
            revoked = [{
                "serial_number": str(cert.serial_number),
                "revocation_date": cert.revocation_date.isoformat()
            } for cert in crl]
        return jsonify(revoked)
    return jsonify({"error": "CRL nicht verfügbar"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
