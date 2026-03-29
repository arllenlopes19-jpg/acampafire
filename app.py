from flask import Flask, render_template, request
import sqlite3, os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "pontuacoes.db")

def inicializar_banco():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS pontuacoes (
            equipe TEXT PRIMARY KEY,
            pontos INTEGER
        )
    """)
    conn.commit()
    conn.close()

def carregar_pontuacoes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT equipe, pontos FROM pontuacoes ORDER BY pontos DESC")
    dados = [{"equipe": row[0], "pontos": row[1]} for row in c.fetchall()]
    conn.close()
    return dados

def atualizar_pontuacao(equipe, pontos):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO pontuacoes (equipe, pontos)
        VALUES (?, ?)
        ON CONFLICT(equipe) DO UPDATE SET pontos=excluded.pontos
    """, (equipe, pontos))
    conn.commit()
    conn.close()

@app.route("/")
def ranking():
    ranking = carregar_pontuacoes()
    medalhas = ["🥇", "🥈", "🥉"]
    return render_template("ranking.html", ranking=ranking, medalhas=medalhas)

@app.route("/api/atualizar", methods=["POST"])
def atualizar_api():
    dados = request.json
    atualizar_pontuacao(dados["equipe"], dados["pontos"])
    return {"status": "ok", "mensagem": f"Equipe {dados['equipe']} atualizada para {dados['pontos']} pontos"}

# rota para inserir dados iniciais
@app.route("/api/reset", methods=["POST"])
def reset():
    atualizar_pontuacao("verde", 80)
    atualizar_pontuacao("vermelho", 50)
    atualizar_pontuacao("rosa", 40)
    atualizar_pontuacao("amarelo", 210)
    return {"status": "ok", "mensagem": "Pontuações iniciais inseridas"}

# garante que o banco exista sempre
inicializar_banco()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
