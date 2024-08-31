import logging  # Importiert das Logging-Modul, um Ereignisse zu protokollieren
from flask import Flask, request, jsonify, render_template, url_for  # Importiert wichtige Flask-Komponenten für die Webanwendung
from openai import OpenAI  # Importiert die OpenAI-Bibliothek zur Nutzung der OpenAI API
import requests  # Importiert die Requests-Bibliothek, um HTTP-Anfragen zu senden
from io import BytesIO  # Importiert BytesIO für das Arbeiten mit binären Daten im Speicher
from PIL import Image  # Importiert die Pillow-Bibliothek zur Bildverarbeitung
import os  # Importiert das OS-Modul zum Arbeiten mit dem Dateisystem
import json  # Importiert das JSON-Modul zum Arbeiten mit JSON-Daten
from datetime import datetime  # Importiert das datetime-Modul zum Arbeiten mit Datum und Uhrzeit

# Konfiguriert das Logging-Modul, um alle Logmeldungen in eine Datei namens 'app.log' zu schreiben
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Setzt den OpenAI API-Schlüssel für die Authentifizierung
api_key = "OPENAI_API_KEY"
client = OpenAI(api_key=api_key)

# Erstellt eine Flask-Webanwendung
app = Flask(__name__)

# Definiert den Dateinamen für die Speicherung des Chatverlaufs
CHATLOG_FILE = "chatlog.json"

# Lädt den Chatlog aus einer JSON-Datei
def load_chatlog():
    # Überprüft, ob die Datei 'chatlog.json' existiert
    if os.path.exists(CHATLOG_FILE):
        # Öffnet und lädt die JSON-Datei, wenn sie existiert
        with open(CHATLOG_FILE, "r") as f:
            return json.load(f)
    # Gibt einen leeren Chatlog zurück, wenn die Datei nicht existiert
    return {}

# Speichert den Chatlog in einer JSON-Datei
def save_chatlog(chatlog):
    # Öffnet die Datei 'chatlog.json' im Schreibmodus und speichert die Chatdaten
    with open(CHATLOG_FILE, "w") as f:
        json.dump(chatlog, f, indent=4)  # Speichert das JSON mit einer Einrückung von 4 Leerzeichen

# Funktion zur Generierung von Code basierend auf einem Prompt
def generate_code(prompt):
    # Sendet eine Anfrage an die OpenAI API, um Code basierend auf dem Prompt zu generieren
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True,  # Aktiviert das Streaming, um den Code in Teilen zu empfangen
    )
    code = ""  # Initialisiert eine leere Zeichenkette für den generierten Code
    # Iteriert über die empfangenen Teile des Codes
    for chunk in stream:
        # Überprüft, ob der empfangene Teil Inhalt enthält und fügt ihn dem Code hinzu
        if chunk.choices[0].delta.content is not None:
            code += chunk.choices[0].delta.content
    return code.strip()  # Gibt den vollständigen Code zurück, ohne führende oder nachfolgende Leerzeichen

# Fügt einen neuen Eintrag zum Chatlog hinzu
def append_chatlog(prompt, response):
    # Holt das aktuelle Datum im Format 'YYYY-MM-DD'
    date = datetime.now().strftime("%Y-%m-%d")
    # Lädt den bestehenden Chatlog
    chatlog = load_chatlog()

    # Überprüft, ob es für das aktuelle Datum bereits Einträge gibt, ansonsten wird ein neuer Eintrag erstellt
    if date not in chatlog:
        chatlog[date] = []

    # Fügt den neuen Prompt und die zugehörige Antwort zum Chatlog hinzu
    chatlog[date].append({
        "prompt": prompt,
        "response": response
    })

    # Speichert den aktualisierten Chatlog
    save_chatlog(chatlog)

# Route für die Startseite der Webanwendung
@app.route('/')
def index():
    chatlog = load_chatlog()  # Lädt den bestehenden Chatlog
    return render_template('index.html', chatlog=chatlog)  # Übergibt den Chatlog an das HTML-Template

# Route zur Generierung von Code basierend auf einem Prompt
@app.route('/generate_code', methods=['POST'])
def generate_code_route():
    prompt = request.form['prompt']  # Holt den Prompt aus dem übermittelten Formular
    code = generate_code(prompt)  # Generiert den Code basierend auf dem Prompt
    append_chatlog(prompt, code)  # Fügt den Prompt und die Antwort zum Chatlog hinzu
    return jsonify({'code': code})  # Gibt den generierten Code als JSON zurück

# Route zur Generierung von Bildern basierend auf einem Prompt
@app.route('/generate_image', methods=['POST'])
def generate_image():
    prompt = request.form['prompt']  # Holt den Prompt aus dem übermittelten Formular
    
    try:
        logging.debug("Sende Anfrage an OpenAI API...")  # Protokolliert, dass eine Anfrage gesendet wird
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality="hd",
            n=1,
        )
        logging.debug(f"Antwort von OpenAI erhalten: {response}")  # Protokolliert die erhaltene Antwort
        
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url  # Holt die URL des generierten Bildes
            logging.debug(f"Bild-URL: {image_url}")  # Protokolliert die Bild-URL
        
            image_data = requests.get(image_url).content  # Holt die Bilddaten über die URL
            img = Image.open(BytesIO(image_data))  # Öffnet das Bild aus den empfangenen Daten
        
            file_path = os.path.join(os.getcwd(), "static/generated_image.png")  # Setzt den Pfad, unter dem das Bild gespeichert wird
            img.save(file_path)  # Speichert das Bild auf dem Server
        
            logging.debug(f"Bild gespeichert unter: {file_path}")  # Protokolliert, wo das Bild gespeichert wurde
        
            append_chatlog(prompt, image_url)  # Fügt den Prompt und die Bild-URL zum Chatlog hinzu
        
            return jsonify({'image_url': url_for('static', filename='generated_image.png')})  # Gibt die Bild-URL als JSON zurück
        else:
            logging.error("Kein Bild in der Antwort gefunden.")  # Protokolliert, wenn kein Bild gefunden wurde
            return jsonify({'error': 'Bildgenerierung fehlgeschlagen: Kein Bild gefunden'}), 500
    
    except Exception as e:
        logging.error(f"Fehler bei der Bildgenerierung: {e}")  # Protokolliert alle Fehler, die auftreten
        return jsonify({'error': f'Bildgenerierung fehlgeschlagen: {str(e)}'}), 500  # Gibt eine Fehlermeldung als JSON zurück

# Route zum Anzeigen des Chatlogs
@app.route('/chatlog')
def chatlog():
    chatlog = load_chatlog()  # Lädt den bestehenden Chatlog
    return render_template('chatlog.html', chatlog=chatlog)  # Übergibt den Chatlog an das HTML-Template

# Route zum Anzeigen eines spezifischen Chatlog-Eintrags basierend auf Datum und Index
@app.route('/chatlog/<date>/<int:index>')
def view_chat(date, index):
    chatlog = load_chatlog()  # Lädt den bestehenden Chatlog
    # Überprüft, ob der Eintrag für das Datum und den Index existiert
    if date in chatlog and 0 <= index < len(chatlog[date]):
        entry = chatlog[date][index]  # Holt den spezifischen Eintrag
        return render_template('view_chat.html', prompt=entry['prompt'], response=entry['response'])  # Übergibt den Eintrag an das HTML-Template
    return "Chatverlauf nicht gefunden", 404  # Gibt eine Fehlermeldung zurück, wenn der Eintrag nicht existiert

# Startet die Flask-Anwendung, wenn das Skript direkt ausgeführt wird
if __name__ == "__main__":
    app.run(debug=True, port=80)
