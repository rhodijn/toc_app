#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


from flask import Flask, render_template, request
from modules.api_handler import *
from modules.uploader import *

ALLOWED_EXTENSIONS = {'pdf'}
SECRETS = dotenv_values('.env')
CONFIG = load_json('config.json', 'd')


class toc_app:
    """
    Eine Flask App, komplett in einer Klasse gekapselt
    """
    def __init__(self, host: str = '127.0.0.1', port: int = 5000, debug: bool = True):
        # Flask‑Instanz erzeugen
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = CONFIG['path']['u']

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
            dieser Datei liegen und die Datei *upload.html* enthalten.
            """
            return render_template('upload.html')

        @self.app.route('/result', methods=['POST'])
        def result():
            """
            Rendert ein HTML Formular. Der Ordner *templates* muss neben
            dieser Datei liegen und die Datei *result.html* enthalten.
            """
            marc = ''
            network_id = None
            req = None
            url = None
            val = ''

            if request.method == 'POST':
                f = request.files['file']
                l = request.form.get('library')
                if f.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
                    barcode = f.filename.split('.')[0].split('_')[0].upper()
                    f.save(f"{CONFIG['path']['u']}/{barcode}.{f.filename.split('.')[-1].lower()}")
                    try:
                        req, get_iz_mmsid = api_request(SECRETS['API_URL'], SECRETS['API_KEY'], 'get', barcode, 'json', 'items?item_barcode=')
                        data = json.loads(get_iz_mmsid.content.decode(encoding='utf-8'))
                        mmsid_iz = data['bib_data']['mms_id']
                    except:
                        msg = f"MMS ID zu Item {barcode} nicht gefunden"
                        val = 'nicht '
                    else:
                        try:
                            req, get_network_id = api_request(SECRETS['API_URL'], SECRETS['API_KEY'], 'get', mmsid_iz, 'json', 'bibs/', CONFIG["api"]["get"])
                            data = json.loads(get_network_id.content.decode(encoding='utf-8'))
                            network_id = data['linked_record_id']['value']
                        except:
                            msg = f"Network Id zu Datensatz {mmsid_iz} nicht gefunden"
                            val = 'nicht '
                        else:
                            try:
                                url = upload_pdf(f"{barcode}.{f.filename.split('.')[-1].lower()}", l, network_id)
                                msg = f"Bibliothek: {CONFIG['library'][l].rstrip('/').capitalize()}"
                            except:
                                msg = f"Upload von {barcode}.{f.filename.split('.')[-1].lower()} fehlgeschlagen"
                                val = 'nicht '
                            else:
                                if url:
                                    marc = f"$$3 Inhaltsverzeichnis $$q PDF $$u {url}"
                                else:
                                    msg = f"Datei {network_id}.pdf bereits online"
                                    val = 'nicht '
                else:
                    msg = f"ungültiges Dateiformat ({f.filename.split('.')[-1].lower()}), bitte eine pdf-Datei auswählen"
                return render_template('result.html', id=network_id, marc=marc, message=msg, name=f.filename, url=url, val=val)

    # ------------------------------------------------------------------
    # Server starten
    # ------------------------------------------------------------------
    def run(self):
        """
        Startet den eingebauten Entwicklungs-Server
        """
        self.app.run(host=self.host, port=self.port, debug=self.debug)


# ----------------------------------------------------------------------
# wenn das Skript direkt ausgeführt wird, Instanz erzeugen und starten
# ----------------------------------------------------------------------
if __name__ == '__main__':
    # Optional: Parameter per Kommandozeile oder Umgebungsvariable anpassen
    app_instance = toc_app()
    app_instance.run()