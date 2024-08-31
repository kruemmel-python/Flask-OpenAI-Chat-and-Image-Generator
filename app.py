import logging
from flask import Flask, request, jsonify, render_template, send_file, url_for
from openai import OpenAI
import requests
from io import BytesIO
from PIL import Image
import os

# Setze das Logging für die Ausgabe in eine Datei
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Setzen Sie Ihren OpenAI API-Schlüssel
api_key = "OPENAI_API_KEY"
client = OpenAI(api_key=api_key)

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_code', methods=['POST'])
def generate_code_route():
    prompt = request.form['prompt']
    code = generate_code(prompt)
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
        
        # Zugriff auf das erste Bild in der Antwort
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            logging.debug(f"Bild-URL: {image_url}")
        
            # Herunterladen des Bildes
            image_data = requests.get(image_url).content
            img = Image.open(BytesIO(image_data))
        
            # Speichern des Bildes im gleichen Ordner wie app.py
            file_path = os.path.join(os.getcwd(), "static/generated_image.png")
            img.save(file_path)
        
            logging.debug(f"Bild gespeichert unter: {file_path}")
        
            # Gebe die URL des gespeicherten Bildes zurück
            return jsonify({'image_url': url_for('static', filename='generated_image.png')})
        else:
            logging.error("Kein Bild in der Antwort gefunden.")
            return jsonify({'error': 'Bildgenerierung fehlgeschlagen: Kein Bild gefunden'}), 500
    
    except Exception as e:
        logging.error(f"Fehler bei der Bildgenerierung: {e}")
        return jsonify({'error': f'Bildgenerierung fehlgeschlagen: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True, port=80)
