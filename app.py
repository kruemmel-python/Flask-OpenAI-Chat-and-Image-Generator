import logging
from flask import Flask, request, jsonify, render_template, url_for
from openai import OpenAI
import requests
from io import BytesIO
from PIL import Image
import os
import json
from datetime import datetime

# Setze das Logging für die Ausgabe in eine Datei
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Setzen Sie Ihren OpenAI API-Schlüssel
api_key = "OPENAI_API_KEY"
client = OpenAI(api_key=api_key)

app = Flask(__name__)

CHATLOG_FILE = "chatlog.json"

def load_chatlog():
    if os.path.exists(CHATLOG_FILE):
        with open(CHATLOG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_chatlog(chatlog):
    with open(CHATLOG_FILE, "w") as f:
        json.dump(chatlog, f, indent=4)

def generate_code(prompt):
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True,
    )
    code = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            code += chunk.choices[0].delta.content
    return code.strip()

def append_chatlog(prompt, response):
    date = datetime.now().strftime("%Y-%m-%d")
    chatlog = load_chatlog()

    if date not in chatlog:
        chatlog[date] = []

    chatlog[date].append({
        "prompt": prompt,
        "response": response
    })

    save_chatlog(chatlog)

@app.route('/')
def index():
    chatlog = load_chatlog()  # Lädt den Chatlog
    return render_template('index.html', chatlog=chatlog)  # Übergibt den Chatlog an die Vorlage

@app.route('/generate_code', methods=['POST'])
def generate_code_route():
    prompt = request.form['prompt']
    code = generate_code(prompt)
    append_chatlog(prompt, code)
    return jsonify({'code': code})

@app.route('/generate_image', methods=['POST'])
def generate_image():
    prompt = request.form['prompt']

    try:
        logging.debug("Sende Anfrage an OpenAI API...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality="hd",
            n=1,
        )
        logging.debug(f"Antwort von OpenAI erhalten: {response}")
        
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            logging.debug(f"Bild-URL: {image_url}")
        
            image_data = requests.get(image_url).content
            img = Image.open(BytesIO(image_data))
        
            file_path = os.path.join(os.getcwd(), "static/generated_image.png")
            img.save(file_path)
        
            logging.debug(f"Bild gespeichert unter: {file_path}")
        
            append_chatlog(prompt, image_url)
        
            return jsonify({'image_url': url_for('static', filename='generated_image.png')})
        else:
            logging.error("Kein Bild in der Antwort gefunden.")
            return jsonify({'error': 'Bildgenerierung fehlgeschlagen: Kein Bild gefunden'}), 500
    
    except Exception as e:
        logging.error(f"Fehler bei der Bildgenerierung: {e}")
        return jsonify({'error': f'Bildgenerierung fehlgeschlagen: {str(e)}'}), 500

@app.route('/chatlog')
def chatlog():
    chatlog = load_chatlog()
    return render_template('chatlog.html', chatlog=chatlog)

@app.route('/chatlog/<date>/<int:index>')
def view_chat(date, index):
    chatlog = load_chatlog()
    if date in chatlog and 0 <= index < len(chatlog[date]):
        entry = chatlog[date][index]
        return render_template('view_chat.html', prompt=entry['prompt'], response=entry['response'])
    return "Chatverlauf nicht gefunden", 404

if __name__ == "__main__":
    app.run(debug=True, port=80)

