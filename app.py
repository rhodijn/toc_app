#!/usr/bin/env python3


#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


from flask import Flask, jsonify, render_template, request

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}

class flask_app:
    """
    Eine minimale Flask App, komplett in einer Klasse gekapselt.
    """
    def __init__(self, host: str = '127.0.0.1', port: int = 5000, debug: bool = True):
        # Flask‑Instanz erzeugen
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        # Konfigurationswerte speichern (können später verwendet werden)
        self.host = host
        self.port = port
        self.debug = debug

        # Routen registrieren
        self._register_routes()

    # ------------------------------------------------------------------
    # Routen‑Definitionen
    # ------------------------------------------------------------------
    def _register_routes(self):
        @self.app.route('/')
        def index():
            """Startseite: gibt reinen Text zurück."""
            return 'Hallo aus der klassenbasierten Flask App!'

        @self.app.route('/greet/<name>')
        def greet(name: str):
            """Begrüßt den übergebenen Namen."""
            return f"Hallo, {name}!"

        @self.app.route('/api/add', methods=['POST'])
        def add_numbers():
            """
            Erwartet einen JSON Body wie:
                {'a': 3, 'b': 5}
            Gibt die Summe als JSON zurück
            """
            data = request.get_json(silent=True) or {}
            a = data.get('a', 0)
            b = data.get('b', 0)
            return jsonify({'result': a + b})

        @self.app.route('/api/sub', methods=['POST'])
        def subtract_numbers():
            """
            Erwartet einen JSON Body wie:
                {'a': 3, 'b': 5}
            Gibt die Summe als JSON zurück
            """
            data = request.get_json(silent=True) or {}
            a = data.get('a', 0)
            b = data.get('b', 0)
            return jsonify({'result': a - b})

        @self.app.route('/page')
        def page():
            """
            Rendert ein HTML Template. Der Ordner *templates* muss neben
            dieser Datei liegen und eine Datei *page.html* enthalten.
            """
            return render_template('page.html', title='klassenbasierte Flask Seite')

        @self.app.route('/upload', methods=['GET', 'POST'])
        def upload():
            """
            Rendert ein HTML Formular. Der Ordner *templates* muss neben
            dieser Datei liegen und eine Datei *upload.html* enthalten.
            """
            return render_template('upload.html', title='Bursar Converter')

        @self.app.route('/success', methods=['POST'])
        def success():
            """
            Rendert ein HTML Formular. Der Ordner *templates* muss neben
            dieser Datei liegen und eine Datei *upload.html* enthalten.
            """
            if request.method == 'POST':
                f = request.files['file']
                if f.filename.split('.')[-1] in ALLOWED_EXTENSIONS:
                    f.save(f"uploads/{f.filename}")
                return render_template('success.html', title='Bursar Converter', name=f.filename)

    # ------------------------------------------------------------------
    # Server starten
    # ------------------------------------------------------------------
    def run(self):
        """
        Startet den eingebauten Entwicklungs Server.
        """
        self.app.run(host=self.host, port=self.port, debug=self.debug)


# ----------------------------------------------------------------------
# Wenn das Skript direkt ausgeführt wird, eine Instanz erzeugen und starten
# ----------------------------------------------------------------------
if __name__ == '__main__':
    # Optional: Parameter per Kommandozeile oder Umgebungsvariablen anpassen
    app_instance = flask_app()
    app_instance.run()