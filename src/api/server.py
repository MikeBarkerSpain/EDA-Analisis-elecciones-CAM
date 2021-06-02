from flask import Flask, request, render_template
import os, sys
import argparse

dir = os.path.dirname

# se saltan tres veces de directorio para llegar al directorio raíz del proyecto '/Entregable_EDA'
# la primera para eliminar el nombre del archivo 
# las dos siguientes para eliminar los directorios '/utils' y '/src'
src_path = dir(dir(dir(__file__)))

# se incorpora la ruta hasta el directorio raiz al path del archivo
sys.path.append(src_path)

import src.utils.apis_tb as apis

# Mandatory
app = Flask(__name__)  # __name__ --> __main__  

# ---------- Flask functions ----------
@app.route("/pwd", methods=['GET'])
def create_json():
    x = request.args['password']
    if x == "T05290575":
        return apis.flask_return_json()
    else:
        return "No es la contraseña correcta"

# ---------- Other functions ----------

def main(x):
    if x == 8642:
        print("---------STARTING PROCESS---------")
        print(__file__)
        
        # Get the settings fullpath
        # \\ --> WINDOWS
        # / --> UNIX
        # Para ambos: os.sep
        settings_file = os.path.dirname(__file__) + os.sep + "settings.json"
        print(settings_file)
        # Load json from file
        json_readed = apis.read_json(fullpath=settings_file)
        
        # Load variables from jsons
        DEBUG = json_readed["debug"]
        HOST = json_readed["host"]
        PORT_NUM = json_readed["port"]
        # Dos posibilidades:
        # HOST = "0.0.0.0"
        # HOST = "127.0.0.1"  --> localhost
        app.run(debug=DEBUG, host=HOST, port=PORT_NUM)
    else:
        print('The password is wrong')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--x", type=int)
    args = vars(parser.parse_args())
    x = args["x"]
    main(x)