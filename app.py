from flask import Flask
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "/tmp/policia.db"

# =========================
# CONEXÃO SEGURA
# =========================
def db():
    conn = sqlite3.connect(DB_PATH)
    return conn

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return "🏛️ ATLAS RP ONLINE"

# =========================
# CARTEIRA
# =========================
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
        <head>
            <title>Carteira ATLAS RP</title>
            <style>
                body {{
                    background:#0b0b0b;
                    color:white;
                    font-family:Arial;
                    text-align:center;
                }}
                .card {{
                    margin-top:80px;
                    display:inline-block;
                    padding:20px;
                    background:#1c1c1c;
                    border-radius:12px;
                }}
            </style>
        </head>
        <body>

        <div class="card">
            <h1>🪪 CARTEIRA POLICIAL</h1>
            <p><b>ID:</b> {data[0]}</p>
            <p><b>User:</b> {data[1]}</p>
            <p><b>Patente:</b> {data[2]}</p>
            <p><b>Status:</b> {"🟢 ATIVO" if data[3] else "🔴 INATIVO"}</p>
            <p><b>Data:</b> {data[4]}</p>
        </div>

        </body>
        </html>
        """

    except Exception as e:
        return f"<h1>❌ ERRO INTERNO</h1><p>{e}</p>", 500

# =========================
# RUN (IMPORTANTE NO RENDER)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
