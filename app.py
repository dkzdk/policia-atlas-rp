from flask import Flask
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "policia.db"

# =========================
# AUTO SETUP BANCO
# =========================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS carteira (
        id TEXT PRIMARY KEY,
        user_id INTEGER,
        patente TEXT,
        ativo INTEGER,
        criado_em TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS set_pedido (
        id TEXT PRIMARY KEY,
        user_id INTEGER,
        nome_cidade TEXT,
        status TEXT,
        recrutor_id INTEGER,
        criado_em TEXT
    )
    """)

    conn.commit()
    conn.close()

# roda automaticamente ao iniciar
init_db()

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return "🏛️ ATLAS RP - Sistema Online"

# =========================
# CARTEIRA PÚBLICA
# =========================
@app.route("/carteira/<cid>")
def carteira(cid):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM carteira WHERE id=?", (cid,))
    data = cur.fetchone()

    conn.close()

    if not data:
        return "<h1>❌ Carteira não encontrada</h1>", 404

    return f"""
    <h1>🪪 CARTEIRA POLICIAL</h1>
    <p>ID: {data[0]}</p>
    <p>Patente: {data[2]}</p>
    <p>Status: {"ATIVO" if data[3] else "INATIVO"}</p>
    """

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
