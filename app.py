"""Servidor opcional (PythonAnywhere/local). O jogo roda todo no navegador;
o Flask só entrega os arquivos de web/ e o words.json gerado na hora."""
from pathlib import Path

from flask import Flask, Response, send_from_directory

from banco import banco_json

WEB = Path(__file__).parent / "web"
JSON = banco_json()  # valida o banco ao iniciar

app = Flask(__name__, static_folder=None)


@app.get("/")
def index():
    return send_from_directory(WEB, "index.html")


@app.get("/words.json")
def palavras():
    return Response(JSON, mimetype="application/json")


@app.get("/<path:arquivo>")
def estaticos(arquivo):
    return send_from_directory(WEB, arquivo)


if __name__ == "__main__":
    app.run(debug=True)
