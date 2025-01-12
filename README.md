# PKI Projekt - Readme


## Voraussetzungen

- **Docker und Docker Compose:** Müssen installiert sein, um die Container zu starten und zu verwalten.
- **Python 3.x:** Muss installiert sein, um die Skripte auszuführen.
- **Python-Abhängigkeiten:** Müssen mit `requirements.txt` installiert werden:
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

## Bereinigung

### Verwendung des Bereinigungsskripts
Um alle Container, Netzwerke und das `output`-Verzeichnis zu entfernen (Arbeitsplatz aufräumen):
```bash
python3 cleanup_docker.py
```
Das Skript entfernt:
- Alle PKI-bezogenen Docker-Container.
- Alle ungenutzten Docker-Ressourcen (Images, Volumes, Netzwerke).
- Den Inhalt des `output`-Verzeichnisses.

---

## Hinweis