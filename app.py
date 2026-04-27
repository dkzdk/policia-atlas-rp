from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "ATLAS_SECRET"

DATABASE_URL = os.environ.get("DATABASE_URL")

# =========================
# CONEXÃO POSTGRES
# =========================
def db():
    return psycopg2.connect(DATABASE_URL)

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return "🏛️ ATLAS RP - Governo Online"

# =========================
# CARTEIRA PÚBLICA
# =========================
@app.route("/carteira/<cid>")
def carteira(cid):

    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM carteira WHERE id=%s", (cid,))
    data = cur.fetchone()

    conn.close()

    if not data:
        return render_template("carteira.html", erro=True)

    return render_template("carteira.html", data=data)

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        session["user"] = request.form["user"]
        return redirect("/painel")

    return render_template("login.html")

# =========================
# PAINEL POLICIAL
# =========================
@app.route("/painel")
def painel():

    if "user" not in session:
        return redirect("/login")

    return render_template("painel.html")

# =========================
# ADMIN GOVERNO
# =========================
@app.route("/admin")
def admin():

    return render_template("admin.html")

if __name__ == "__main__":
    app.run()
