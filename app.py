from flask import Flask
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "policia.db"

# =========================
# CONEXÃO SEGURA
# =========================
def conectar():
    conn = sqlite3.connect(DB_PATH)
    return conn

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return "🚔 ATLAS RP - Sistema Online Funcionando"

# =========================
# CARTEIRA (VERIFICAÇÃO PÚBLICA)
# =========================
@app.route("/carteira/<cid>")
def carteira(cid):

    try:
        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, user_id, patente, ativo, criado_em
            FROM carteira
            WHERE id=?
        """, (cid,))

        data = cur.fetchone()
        conn.close()

        # ❌ não achou
        if not data:
            return """
            <h1 style='color:red;text-align:center'>❌ CARTEIRA NÃO ENCONTRADA</h1>
            <p style='text-align:center'>ID inválido ou removido</p>
            """, 404

        # 🔥 carteira válida
        return f"""
        <html>
        <head>
            <title>ATLAS RP - Carteira</title>
        </head>

        <body style="background:#0f0f0f;color:white;font-family:Arial;text-align:center;padding-top:50px;">

            <div style="background:#1c1c1c;padding:20px;border-radius:10px;display:inline-block;">

                <h1>🪪 CARTEIRA POLICIAL</h1>

                <hr>

                <p><b>ID:</b> {data[0]}</p>
                <p><b>USER ID:</b> {data[1]}</p>
                <p><b>PATENTE:</b> {data[2]}</p>

                <p>
                    <b>STATUS:</b> 
                    {"🟢 ATIVO" if data[3] else "🔴 INATIVO"}
                </p>

                <p><b>CRIADO EM:</b> {data[4]}</p>

                <br>
                <small>ATLAS RP - Sistema Oficial de Verificação</small>

            </div>

        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <h1>❌ ERRO NO SERVIDOR</h1>
        <p>{str(e)}</p>
        """, 500


# =========================
# RUN LOCAL (Render ignora isso)
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
