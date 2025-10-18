from flask import Flask, jsonify, send_from_directory, abort
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) 

# Carpeta donde están los .md
MDS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "guias"))
IMAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "imagenes"))

@app.route("/pearls", methods=["GET"])
def listar_pearls():
    archivos = [f for f in os.listdir(MDS_DIR) if f.lower().endswith(".md")]
    return jsonify({"pearls": archivos})

@app.route("/pearls/<nombre_md>", methods=["GET"])
def obtener_pearl(nombre_md):
    if not os.path.isfile(os.path.join(MDS_DIR, nombre_md)):
        abort(404)
    return send_from_directory(MDS_DIR, nombre_md, mimetype="text/markdown")

# NUEVAS RUTAS PARA IMÁGENES
@app.route("/imagenes", methods=["GET"])
def listar_images():
    if not os.path.isdir(IMAGES_DIR):
        return jsonify({"imagenes": []})
    archivos = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg"))]
    return jsonify({"imagenes": archivos})

@app.route("/imagenes/<nombre_img>", methods=["GET"])
def obtener_image(nombre_img):
    if not os.path.isfile(os.path.join(IMAGES_DIR, nombre_img)):
        abort(404)
    return send_from_directory(IMAGES_DIR, nombre_img)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)