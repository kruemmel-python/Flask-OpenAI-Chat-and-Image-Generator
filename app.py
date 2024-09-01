from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from openai import OpenAI
import os
import json
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import requests
from io import BytesIO
from PIL import Image
import logging

# Initialisiere die App und Konfiguration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Initialisiere SQLAlchemy und Flask-Login
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Benutzermodell
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    chatlog = db.Column(db.Text, default='{}')

# Lade den Benutzer anhand der User-ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Setze das Logging für die Ausgabe in eine Datei
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Lade die .env-Datei und den API-Schlüssel manuell
load_dotenv(find_dotenv())

# Manuelles Einlesen des API-Schlüssels
api_key = None
with open(".env", "r") as f:
    for line in f:
        if line.startswith("OPENAI_API_KEY"):
            key_value = line.strip().split('=', 1)
            if len(key_value) == 2:
                api_key = key_value[1].strip('"')
                os.environ[key_value[0]] = api_key

if not api_key:
    raise ValueError("API-Schlüssel konnte nicht aus der .env-Datei geladen werden.")

print(f"Länge des API-Schlüssels: {len(api_key)}")
print(f"API-Schlüssel: {api_key}")

client = OpenAI(api_key=api_key)

# Definition der generate_code Funktion
def generate_code(prompt):
    """
    Generiert Code basierend auf einem Prompt mithilfe der OpenAI-API.

    Args:
        prompt (str): Der Prompt zur Codegenerierung.

    Returns:
        str: Der generierte Code.
    """
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index'))
        except:
            return 'Benutzername existiert bereits. Bitte wähle einen anderen.'
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Suche den Benutzer in der Datenbank
        user = User.query.filter_by(username=username).first()

        # Überprüfe das Passwort und melde den Benutzer an, wenn alles korrekt ist
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Anmeldung fehlgeschlagen. Überprüfe deinen Benutzernamen und dein Passwort.')

    return render_template('login.html')                                                                                                                                                                            

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Anpassungen für benutzerspezifische Chatlogs
def load_chatlog():
    if current_user.is_authenticated:
        return json.loads(current_user.chatlog)
    return {}

def save_chatlog(chatlog):
    if current_user.is_authenticated:
        current_user.chatlog = json.dumps(chatlog)
        db.session.commit()

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
@login_required
def index():
    chatlog = load_chatlog()
    return render_template('index.html', chatlog=chatlog)

@app.route('/generate_code', methods=['POST'])
@login_required
def generate_code_route():
    prompt = request.form.get('prompt')  # Verwende 'get', um Fehler zu vermeiden, wenn der prompt fehlt
    if not prompt:
        return jsonify({'error': 'Kein Prompt erhalten'}), 400
    
    try:
        code = generate_code(prompt)
        append_chatlog(prompt, code)
        return jsonify({'code': code})
    except Exception as e:
        logging.error(f"Fehler bei der Codegenerierung: {e}")
        return jsonify({'error': f'Codegenerierung fehlgeschlagen: {str(e)}'}), 500

@app.route('/generate_image', methods=['POST'])
@login_required
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

            # Erzeuge den Dateinamen mit Zeitstempel
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"generated_image_{timestamp}.png"
            file_path = os.path.join(os.getcwd(), "static", file_name)
            img.save(file_path)

            logging.debug(f"Bild gespeichert unter: {file_path}")

            append_chatlog(prompt, image_url)

            # Gebe den Dateinamen in der JSON-Antwort zurück
            return jsonify({'image_url': url_for('static', filename=file_name)})
        else:
            logging.error("Kein Bild in der Antwort gefunden.")
            return jsonify({'error': 'Bildgenerierung fehlgeschlagen: Kein Bild gefunden'}), 500

    except Exception as e:
        logging.error(f"Fehler bei der Bildgenerierung: {e}")
        return jsonify({'error': f'Bildgenerierung fehlgeschlagen: {str(e)}'}), 500

@app.route('/chatlog')
@login_required
def chatlog():
    chatlog = load_chatlog()
    return render_template('chatlog.html', chatlog=chatlog)

@app.route('/chatlog/<date>/<int:index>')
@login_required
def view_chat(date, index):
    chatlog = load_chatlog()
    if date in chatlog and 0 <= index < len(chatlog[date]):
        entry = chatlog[date][index]
        return render_template('view_chat.html', prompt=entry['prompt'], response=entry['response'])
    return "Chatverlauf nicht gefunden", 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Erstellt die SQLite-Datenbank und die Tabellen, falls nicht vorhanden
    app.run(debug=True, host='0.0.0.0', port=80)
