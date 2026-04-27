from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

# =========================
# BANCO DE DADOS (SQLite)
# =========================
DB_PATH = "policia.db"

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return """
    <h1>🚔 Sistema Polícia RP ATLAS</h1>
    <p>Status: ONLINE ✅</p>
    <p>API: /api/status</p>
    """


# =========================
# STATUS API (para bot/site)
# =========================
@app.route("/api/status")
def status():
    return jsonify({
        "status": "online",
        "sistema": "Polícia RP ATLAS",
        "versao": "1.0"
    })


# =========================
# CARTEIRA (BASE FUTURA QR)
# =========================
@app.route("/carteira/<user_id>")
def carteira(user_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM carteira_policial WHERE user_id = ?", (user_id,))
    dados = cursor.fetchone()

    if not dados:
        return "<h2>❌ Carteira não encontrada</h2>"

    return f"""
    <h1>🪪 Carteira Policial</h1>
    <p><b>ID:</b> {dados['user_id']}</p>
    <p><b>Patente:</b> {dados['patente']}</p>
    <p><b>Status:</b> {'Ativo' if dados['ativo'] == 1 else 'Inativo'}</p>
    <p><b>Registro:</b> {dados['registro']}</p>
    """


# =========================
# RODAR LOCAL / RENDER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
