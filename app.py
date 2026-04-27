from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB = "policia.db"

def db():
    return sqlite3.connect(DB)

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return "🏛️ ATLAS RP - Sistema Governo Online"

# =========================
# VER CARTEIRA
# =========================
@app.route("/carteira/<cid>")
def carteira(cid):

    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM carteira WHERE id=?", (cid,))
    data = cur.fetchone()

    conn.close()

    if not data:
        return render_template("carteira.html", erro=True)

    return render_template("carteira.html",
        id=data[0],
        user=data[1],
        patente=data[2],
        ativo=data[3],
        criado=data[4]
    )

# =========================
# LOGIN POLICIAL (BÁSICO)
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        return redirect("/painel")

    return render_template("login.html")

# =========================
# PAINEL GOVERNO
# =========================
@app.route("/painel")
def painel():
    return render_template("painel.html")

if __name__ == "__main__":
    app.run()
