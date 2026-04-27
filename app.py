from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB = "policia.db"

def db():
    return sqlite3.connect(DB)

@app.route("/carteira/<cid>")
def carteira(cid):

    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT id, user_id, patente, ativo, criado_em FROM carteira WHERE id=?", (cid,))
    data = cur.fetchone()

    conn.close()

    if not data:
        return render_template("carteira.html", erro=True)

    # foto simulada (você pode trocar depois por upload real)
    foto_url = f"https://api.dicebear.com/7.x/bottts/png?seed={data[1]}"

    return render_template("carteira.html",
        id=data[0],
        user=data[1],
        patente=data[2],
        ativo=data[3],
        criado=data[4],
        foto=foto_url
    )

if __name__ == "__main__":
    app.run()
