# Flask OpenAI Chat and Image Generator

![image](https://github.com/user-attachments/assets/42cf9ab4-bd61-48a9-86c8-0b562b443421)

Dieses Projekt implementiert eine Flask-Webanwendung, die die OpenAI API nutzt, um basierend auf Benutzereingaben Code und Bilder zu generieren. Die Anwendung bietet eine einfache Benutzeroberfläche, um mit diesen Funktionen zu interagieren und speichert zudem den gesamten Chatverlauf.

## Inhaltsverzeichnis

- [Flask OpenAI Chat and Image Generator](#flask-openai-chat-and-image-generator)
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
    - [GET /chatlog](#get-chatlog)
    - [GET /chatlog/<date>/<int:index>](#get-chatlogdateindex)
    - [POST /register](#post-register)
    - [POST /login](#post-login)
    - [GET /logout](#get-logout)
  - [Logging](#logging)
  - [Fehlerbehandlung](#fehlerbehandlung)
  - [Lizenz](#lizenz)

## Über das Projekt

Diese Flask-Anwendung ermöglicht es, Antworten basierend auf einem gegebenen Prompt zu generieren und Bilder mithilfe von OpenAIs Bildgenerierungs-API zu erstellen. Die resultierenden Bilder werden auf dem Server gespeichert und dem Benutzer zum Download zur Verfügung gestellt. Zusätzlich wird der gesamte Chatverlauf automatisch gespeichert und kann über die Benutzeroberfläche abgerufen werden.

Neu hinzugefügt wurden Benutzerregistrierung, -anmeldung und -abmeldung. Jeder Benutzer hat seinen eigenen Chatverlauf, der nur für diesen Benutzer sichtbar ist.

## Voraussetzungen

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Login
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
├── models.py             # Definition der Datenbankmodelle
├── templates/
│   ├── index.html        # HTML-Template für die Hauptseite
│   ├── login.html        # HTML-Template für die Anmeldung
│   ├── register.html     # HTML-Template für die Registrierung
│   ├── chatlog.html      # HTML-Template für die Anzeige des Chatverlaufs
│   └── view_chat.html    # HTML-Template für die detaillierte Ansicht eines Chat-Eintrags
├── static/
│   ├── generated_image_*.png  # Hier werden die generierten Bilder mit Zeitstempel gespeichert
│   └── styles/
│       ├── styles.css    # CSS-Datei für die Gestaltung
│       └── scripts.js    # JavaScript-Datei für zusätzliche Funktionen
├── instance/
│   └── users.db          # SQLite-Datenbank für Benutzerdaten
├── app.log               # Log-Datei für die Anwendung
├── requirements.txt      # Liste der Python-Abhängigkeiten
└── README.md             # Diese README-Datei
```

## Endpunkte

### GET /

Rendert die Startseite mit einem Formular, um Prompts für die Code- und Bildgenerierung einzugeben. Der Chatverlauf wird auf der rechten Seite angezeigt.

### POST /generate_code

Erwartet ein Formularfeld `prompt` und gibt ein JSON-Objekt mit dem generierten Code zurück. Der Prompt und die Antwort werden im Chatlog des angemeldeten Benutzers gespeichert.

- **Request**: `POST`
- **Parameter**: `prompt` (Text)
- **Response**: `{ "code": "..." }`

### POST /generate_image

Erwartet ein Formularfeld `prompt` und gibt ein JSON-Objekt mit der URL des generierten Bildes zurück. Der Prompt und die Bild-URL werden im Chatlog des angemeldeten Benutzers gespeichert.

- **Request**: `POST`
- **Parameter**: `prompt` (Text)
- **Response**: `{ "image_url": "/static/generated_image_TIMESTAMP.png" }`

### GET /chatlog

Zeigt eine Liste der gespeicherten Chatlogs des aktuellen Benutzers an, gruppiert nach Datum. Jeder Chatlog-Eintrag kann angeklickt werden, um eine detaillierte Ansicht des Prompts und der zugehörigen Antwort zu öffnen.

- **Request**: `GET`
- **Response**: Eine HTML-Seite mit einer Liste der Chatlog-Einträge.

### GET /chatlog/<date>/<int:index>

Zeigt die detaillierte Ansicht eines spezifischen Chatlog-Eintrags an, basierend auf Datum und Index.

- **Request**: `GET`
- **Parameter**:
  - `date`: Das Datum des Chatlog-Eintrags (z.B. `2024-08-31`)
  - `index`: Der Index des spezifischen Eintrags für dieses Datum
- **Response**: Eine HTML-Seite mit dem spezifischen Prompt und der zugehörigen Antwort.

### POST /register

Ermöglicht die Registrierung eines neuen Benutzers. Erforderlich sind `username` und `password`.

- **Request**: `POST`
- **Parameter**:
  - `username`: Der gewünschte Benutzername (muss eindeutig sein)
  - `password`: Das Passwort
- **Response**: Bei Erfolg wird der Benutzer angemeldet und zur Startseite weitergeleitet.

### POST /login

Ermöglicht es einem registrierten Benutzer, sich anzumelden. Erforderlich sind `username` und `password`.

- **Request**: `POST`
- **Parameter**:
  - `username`: Der Benutzername
  - `password`: Das Passwort
- **Response**: Bei Erfolg wird der Benutzer zur Startseite weitergeleitet.

### GET /logout

Meldet den aktuellen Benutzer ab und leitet zur Anmeldeseite weiter.

- **Request**: `GET`
- **Response**: Der Benutzer wird abgemeldet und zur Anmeldeseite (`/login`) weitergeleitet.

## Logging

Die Anwendung verwendet eine `app.log` Datei, um verschiedene Aktionen und Fehler zu protokollieren. Hier sind einige der protokollierten Ereignisse:

- **DEBUG: Sende Anfrage an OpenAI API...**: Wird protokolliert, wenn eine Anfrage zur Bildgenerierung an die OpenAI API gesendet wird.
- **DEBUG: Antwort von OpenAI erhalten: {response}**: Loggt die empfangene Antwort von der OpenAI API.
- **DEBUG: Bild-URL: {image_url}**: Protokolliert die URL des vom OpenAI API generierten Bildes.
- **DEBUG: Bild gespeichert unter: {file_path}**: Protokolliert den Speicherort des generierten Bildes auf dem Server.
- **ERROR: Kein Bild in der Antwort gefunden.**: Wird protokolliert, wenn kein Bild in der Antwort von OpenAI enthalten ist.
- **ERROR: Fehler bei der Bildgenerierung: {e}**: Loggt Fehler, die während der Bildgenerierung auftreten.
- **ERROR: Fehler bei der Codegenerierung: {e}**: Loggt Fehler, die während der Codegenerierung auftreten.

## Fehlerbehandlung

Die Anwendung protokolliert Fehler und gibt eine entsprechende JSON-Antwort mit einem 500-Statuscode zurück, wenn bei der Code- oder Bildgenerierung ein Fehler auftritt.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der `LICENSE` Datei.

