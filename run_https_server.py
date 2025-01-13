import http.server
import ssl

server_address = ('localhost', 4443)

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

context.load_cert_chain(
    certfile='./output/client.crt',
    keyfile='./output/client.key' 
)

context.load_verify_locations(cafile='./output/intermediateCA.crt')

context.verify_mode = ssl.CERT_REQUIRED

context.load_verify_locations(cafile="./output/intermediateCA.crl")

httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("HTTPS-Server läuft mit CRL-Überprüfung auf https://localhost:4443")
httpd.serve_forever()
