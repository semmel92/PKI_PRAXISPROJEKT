# PKI Projekt - Readme

## Voraussetzungen

- **Docker und Docker Compose:** Müssen installiert sein, um die Container zu starten und zu verwalten.
- **Python 3.x:** Muss installiert sein, um die Skripte auszuführen.
- **Python-Abhängigkeiten:** Müssen mit requirements.txt installiert werden:
  ```bash
  pip install -r requirements.txt
  ```

---

## Schritte zur Ausführung des Projekts

### 1. Docker-Container starten
```bash
docker-compose -f docker-compose.yml up --build
```
Das erstellt die Container für Root CA, Intermediate CA und Client CA.

---

### 2. Erstellung der Certificate Revocation List (CRL)
Nach dem Start der Container:
```bash
python3 create_crl.py
```

---

### 3. Zertifikat widerrufen
Falls ein Zertifikat widerrufen werden soll:
```bash
python3 revoke_crl.py
```
Das Skript zeigt die verfügbaren Zertifikate an und fordert auf, die Seriennummer des zu widerrufenden Zertifikats einzugeben.

---

### 4. Ausführung des Flask-Servers
```bash
python serve_crl.py
```
Der Webserver startet und ist unter `http://localhost:8080` erreichbar.

#### Zugriff auf die Funktionen
- **CRL abrufen:**
  Besuche die URL `http://localhost:8080/crl/intermediateCA.crl` in einem Browser oder lade die Datei mit curl:
  ```bash
  curl http://localhost:8080/crl/intermediateCA.crl -o intermediateCA.crl
  ```
- **Liste der widerrufenen Zertifikate anzeigen:**
  Besuche die URL `http://localhost:8080/revoked-certificates` oder nutze curl:
  ```bash
  curl http://localhost:8080/revoked-certificates
  ```
---

### Optional für Präsentation
### 5. Präsi Server starten
```bash
python3 run_https_server.py
```
## Reminder: Prozess erklären - was passiert wann
- Öffne `https://localhost:4443` im Browser.
- Curlen:
  ```bash
  curl -v --cacert ./output/intermediateCA.crt https://localhost:4443
  ```

#### Widerruf demonstrieren
1. Widerrufemit `revoke_crl.py`.
3. Teste erneut mit curl:
   ```bash
   curl -v --cacert ./output/intermediateCA.crt --crlfile ./output/intermediateCA.crl https://localhost:4443
   ```

---

## Bereinigung

### Verwendung des Bereinigungsskripts
Um alle Container, Netzwerke und das output-Verzeichnis zu entfernen (Arbeitsplatz aufräumen):
```bash
python3 cleanup_docker.py
```
Das Skript entfernt:
- Alle PKI-bezogenen Docker-Container.
- Alle ungenutzten Docker-Ressourcen (Images, Volumes, Netzwerke).
- Den Inhalt des output-Verzeichnisses.
