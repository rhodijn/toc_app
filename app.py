#!/usr/bin/env python3


#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


from dotenv import dotenv_values
from flask import Flask, render_template, request
from modules.apihandler import *
from modules.uploader import *

ALLOWED_EXTENSIONS = {'pdf'}
SECRETS = dotenv_values('.env')
UPLOAD_FOLDER = 'upload'


class flask_app:
    """
    Eine kleine Flask App, komplett in einer Klasse gekapselt
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
        @self.app.route('/', methods=['GET', 'POST'])
        def upload():
            """
            Rendert ein HTML Formular. Der Ordner *templates* muss neben
            dieser Datei liegen und eine Datei *upload.html* enthalten.
            """
            return render_template('upload.html', title='Inhaltsverzeichnis')

        @self.app.route('/result', methods=['POST'])
        def result():
            """
            Rendert ein HTML Formular. Der Ordner *templates* muss neben
            dieser Datei liegen und eine Datei *result.html* enthalten.
            """
            if request.method == 'POST':
                f = request.files['file']
                if f.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
                    barcode = f.filename.split('.')[0].upper()
                    f.save(f"upload/{f.filename}")
                    msg = f"Die Datei wurde gespeichtert, Barcode: {barcode}"
                else:
                    msg = 'ungültiges Dateiformat, bitte eine pdf-Datei auswählen'

                return render_template('result.html', title='Inhaltsverzeichnis', message=msg, name=f.filename)

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