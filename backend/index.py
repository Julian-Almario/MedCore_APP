from flask import Flask, jsonify, send_from_directory, abort
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) 

# Carpeta donde están los .md
MDS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "guias"))

@app.route("/pearls", methods=["GET"])
def listar_pearls():
    archivos = [f for f in os.listdir(MDS_DIR) if f.lower().endswith(".md")]
    return jsonify({"pearls": archivos})

@app.route("/pearls/<nombre_md>", methods=["GET"])
def obtener_pearl(nombre_md):
    if not os.path.isfile(os.path.join(MDS_DIR, nombre_md)):
        abort(404)
    return send_from_directory(MDS_DIR, nombre_md, mimetype="text/markdown")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)