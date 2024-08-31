# Flask OpenAI Chat and Image Generator

Dieses Projekt implementiert eine Flask-Webanwendung, die die OpenAI API nutzt, um basierend auf Benutzereingaben Code und Bilder zu generieren. Die Anwendung bietet eine einfache Benutzeroberfläche, um mit diesen Funktionen zu interagieren.

## Inhaltsverzeichnis

- [Flask OpenAI Code and Image Generator](#flask-openai-code-and-image-generator)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [Über das Projekt](#über-das-projekt)
  - [Voraussetzungen](#voraussetzungen)
  - [Installation](#installation)
  - [Umgebungsvariablen](#umgebungsvariablen)
  - [Verwendung](#verwendung)
  - [Projektstruktur](#projektstruktur)
  - [Endpunkte](#endpunkte)
    - [GET /](#get-)
    - [POST /generate_code](#post-generate_code)
    - [POST /generate_image](#post-generate_image)
  - [Logging](#logging)
  - [Fehlerbehandlung](#fehlerbehandlung)
  - [Lizenz](#lizenz)

## Über das Projekt

Diese Flask-Anwendung ermöglicht es, Antworten basierend auf einem gegebenen Prompt zu generieren und Bilder mithilfe von OpenAIs Bildgenerierungs-API zu erstellen. Die resultierenden Bilder werden auf dem Server gespeichert und dem Benutzer zum Download zur Verfügung gestellt.

## Voraussetzungen

- Python 3.x
- Flask
- OpenAI Python Client
- PIL (Pillow)
- Requests

## Installation

1. Klone das Repository:
    ```bash
    git clone https://github.com/kruemmel-python/Flask-OpenAI-Chat-and-Image-Generator.git
    cd Repo-Name
    ```

2. Erstelle und aktiviere eine virtuelle Umgebung:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Für Windows: venv\Scripts\activate
    ```

3. Installiere die Abhängigkeiten:
    ```bash
    pip install -r requirements.txt
    ```

4. Stelle sicher, dass der OpenAI API-Schlüssel in der Umgebungsvariablen `OPENAI_API_KEY` gesetzt ist oder im Code direkt definiert wird.

## Umgebungsvariablen

Um die Anwendung lokal auszuführen, setze die folgende Umgebungsvariable:

- `OPENAI_API_KEY`: Dein OpenAI API-Schlüssel.

## Verwendung

Starte den Flask-Server lokal:

```bash
python app.py
```

Navigiere dann zu `http://localhost:80` in deinem Webbrowser.

## Projektstruktur

```plaintext
/
├── app.py                # Hauptdatei mit der Flask-Anwendung
├── templates/
│   └── index.html        # HTML-Template für die Hauptseite
├── static/
│   └── generated_image.png  # Hier wird das generierte Bild gespeichert
├── app.log               # Log-Datei für die Anwendung
├── requirements.txt      # Liste der Python-Abhängigkeiten
└── README.md             # Diese README-Datei
```

## Endpunkte

### GET /

Rendert die Startseite mit einem Formular, um Prompts für die Code- und Bildgenerierung einzugeben.

### POST /generate_code

Erwartet ein Formularfeld `prompt` und gibt ein JSON-Objekt mit dem generierten Code zurück.

- **Request**: `POST`
- **Parameter**: `prompt` (Text)
- **Response**: `{ "code": "..." }`

### POST /generate_image

Erwartet ein Formularfeld `prompt` und gibt ein JSON-Objekt mit der URL des generierten Bildes zurück.

- **Request**: `POST`
- **Parameter**: `prompt` (Text)
- **Response**: `{ "image_url": "/static/generated_image.png" }`

## Logging

Die Anwendung verwendet eine `app.log` Datei, um verschiedene Aktionen und Fehler zu protokollieren. Hier sind einige der protokollierten Ereignisse:

- **DEBUG: Sende Anfrage an OpenAI API...**: Wird protokolliert, wenn eine Anfrage zur Bildgenerierung an die OpenAI API gesendet wird.
- **DEBUG: Antwort von OpenAI erhalten: {response}**: Loggt die empfangene Antwort von der OpenAI API.
- **DEBUG: Bild-URL: {image_url}**: Protokolliert die URL des vom OpenAI API generierten Bildes.
- **DEBUG: Bild gespeichert unter: {file_path}**: Protokolliert den Speicherort des generierten Bildes auf dem Server.
- **ERROR: Kein Bild in der Antwort gefunden.**: Wird protokolliert, wenn kein Bild in der Antwort von OpenAI enthalten ist.
- **ERROR: Fehler bei der Bildgenerierung: {e}**: Loggt Fehler, die während der Bildgenerierung auftreten.

## Fehlerbehandlung

Die Anwendung protokolliert Fehler und gibt eine entsprechende JSON-Antwort mit einem 500-Statuscode zurück, wenn bei der Bildgenerierung ein Fehler auftritt.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der `LICENSE` Datei.
```

### `requirements.txt` Beispiel

Hier ist ein Beispiel für die `requirements.txt`, die alle notwendigen Python-Bibliotheken enthält:

```plaintext
Flask==2.3.2
openai==0.27.0
Pillow==9.4.0
requests==2.28.1
```

Diese Datei stellt sicher, dass alle im Code verwendeten Bibliotheken installiert werden, wenn der Befehl `pip install -r requirements.txt` ausgeführt wird.


