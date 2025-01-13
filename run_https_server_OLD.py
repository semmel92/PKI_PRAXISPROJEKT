import http.server
import ssl

server_address = ('localhost', 4443)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket(
    httpd.socket,
    keyfile='./output/client.key',
    certfile='./output/client.crt',
    ca_certs='./output/intermediateCA.crt',
    server_side=True,
)

print("HTTPS-Server läuft auf https://localhost:4443")
httpd.serve_forever()
