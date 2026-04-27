from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "SEGREDO_RP_123"

# =========================
# CONEXÃO BANCO
# =========================
def db():
    conn = sqlite3.connect("policia.db")
    conn.row_factory = sqlite3.Row
    return conn

# =========================
# LOGIN SIMPLES POLICIAL
# =========================
POLICIA_LOGIN = {
    "admin": "1234",
    "comandante": "senha123"
}

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        user = request.form["user"]
        senha = request.form["senha"]

        if user in POLICIA_LOGIN and POLICIA_LOGIN[user] == senha:
            session["user"] = user
            return redirect("/painel")

        return "❌ Login inválido"

    return render_template("login.html")

# =========================
# PAINEL ADMIN
# =========================
@app.route("/painel")
def painel():

    if "user" not in session:
        return redirect("/")

    conn = db()
    c = conn.cursor()

    c.execute("SELECT * FROM carteira ORDER BY data DESC")
    carteiras = c.fetchall()

    return render_template("painel.html", user=session["user"], carteiras=carteiras)

# =========================
# BUSCAR CARTEIRA
# =========================
@app.route("/buscar", methods=["GET", "POST"])
def buscar():

    resultado = None

    if request.method == "POST":
        cid = request.form["id"]

        conn = db()
        c = conn.cursor()

        c.execute("SELECT * FROM carteira WHERE id=?", (cid,))
        resultado = c.fetchone()

    return render_template("buscar.html", resultado=resultado)

# =========================
# VER CARTEIRA
# =========================
@app.route("/carteira/<id>")
def carteira(id):

    conn = db()
    c = conn.cursor()

    c.execute("SELECT * FROM carteira WHERE id=?", (id,))
    data = c.fetchone()

    if not data:
        return "Carteira inválida"

    return render_template("carteira.html", data=data)

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)