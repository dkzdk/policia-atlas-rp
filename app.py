from flask import Flask
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "/tmp/policia.db"

def db():
    conn = sqlite3.connect(DB_PATH)
    return conn

# 🔥 CRIA TABELA AUTOMATICAMENTE
def init_db():
    conn = db()
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

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "🏛 ATLAS RP ONLINE"

@app.route("/carteira/<cid>")
def carteira(cid):

    try:
        conn = db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM carteira WHERE id=?", (cid,))
        data = cur.fetchone()

        conn.close()

        if not data:
            return "<h1>❌ Carteira não encontrada</h1>", 404

        return f"""
        <html>
        <body style="background:#111;color:white;text-align:center;font-family:Arial;">
            <h1>🪪 CARTEIRA ATLAS RP</h1>
            <p><b>ID:</b> {data[0]}</p>
            <p><b>User:</b> {data[1]}</p>
            <p><b>Patente:</b> {data[2]}</p>
            <p><b>Status:</b> {"🟢 ATIVO" if data[3] else "🔴 INATIVO"}</p>
            <p><b>Data:</b> {data[4]}</p>
        </body>
        </html>
        """

    except Exception as e:
        return f"<h1>❌ ERRO INTERNO</h1><p>{e}</p>", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
