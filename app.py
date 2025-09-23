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
CONFIG = load_json('config.json', 'd')


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
            marc = None
            req = None
            url = None

            if request.method == 'POST':
                f = request.files['file']
                l = request.form.get('library')
                if f.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
                    barcode = f.filename.split('.')[0].upper()
                    f.save(f"upload/{barcode}.{f.filename.split('.')[-1].lower()}")
                    req, get_iz_mmsid = api_request('get', barcode, 'j', 'items?item_barcode=')
                    data = json.loads(get_iz_mmsid.content.decode(encoding='utf-8'))
                    try:
                        mmsid_iz = data['bib_data']['mms_id']
                        try:
                            req, get_network_id = api_request('get', mmsid_iz, 'j', 'bibs/', CONFIG["api"]["get"])
                            data = json.loads(get_network_id.content.decode(encoding='utf-8'))
                            network_id = data['linked_record_id']['value']
                            url = upload_pdf(f"{barcode}.{f.filename.split('.')[-1].lower()}", l, network_id)
                            msg = f"Upload erfolgreich: Barcode {barcode}, Bibliothek {l}, Netword Id {network_id}"
                            marc = f"$$3 Inhaltsverzeichnis $$q PDF $$u {url}"
                        except:
                            msg = f"abgebrochen: Network Id zu Item {barcode} nicht gefunden ({req})"
                    except:
                        msg = f"abgebrochen: MMS ID zu Item {barcode} nicht gefunden ({req})"
                else:
                    msg = f"ungültiges Dateiformat ({f.filename.split('.')[-1].lower()}), bitte eine pdf-Datei auswählen ({req})"

                return render_template('result.html', title='Inhaltsverzeichnis', marc=marc, message=msg, name=f.filename, url=url)

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