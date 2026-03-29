from flask import Flask, render_template, request
import sqlite3, os, requests

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "pontuacoes.db")

# Inicializa o banco local
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

# Carrega pontuações do banco local
def carregar_pontuacoes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT equipe, pontos FROM pontuacoes ORDER BY pontos DESC")
    dados = [{"equipe": row[0], "pontos": row[1]} for row in c.fetchall()]
    conn.close()
    return dados

# Atualiza pontuação local + envia para o site Render
def atualizar_pontuacao(equipe, pontos):
    # Atualiza no banco local
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO pontuacoes (equipe, pontos)
        VALUES (?, ?)
        ON CONFLICT(equipe) DO UPDATE SET pontos=excluded.pontos
    """, (equipe, pontos))
    conn.commit()
    conn.close()

    # Atualiza no site Render
    try:
        url = "https://acampafire.onrender.com/api/atualizar"
        dados = {"equipe": equipe, "pontos": pontos}
        r = requests.post(url, json=dados)
        print("Servidor respondeu:", r.json())
    except Exception as e:
        print("Erro ao atualizar no site:", e)

# Página principal - busca dados da API de ranking
@app.route("/")
def ranking():
    try:
        r = requests.get("https://acampafire.onrender.com/api/ranking")
        ranking = r.json()["ranking"]
    except:
        ranking = carregar_pontuacoes()  # fallback local

    medalhas = ["🥇", "🥈", "🥉"]
    return render_template("ranking.html", ranking=ranking, medalhas=medalhas)

# API para atualizar pontuação
@app.route("/api/atualizar", methods=["POST"])
def atualizar_api():
    dados = request.json
    atualizar_pontuacao(dados["equipe"], dados["pontos"])
    return {"status": "ok", "mensagem": f"Equipe {dados['equipe']} atualizada para {dados['pontos']} pontos"}

# API para resetar pontuações iniciais
@app.route("/api/reset", methods=["POST"])
def reset():
    atualizar_pontuacao("verde", 80)
    atualizar_pontuacao("vermelho", 50)
    atualizar_pontuacao("rosa", 40)
    atualizar_pontuacao("amarelo", 520)
    return {"status": "ok", "mensagem": "Pontuações iniciais inseridas"}

# Nova API para consultar ranking
@app.route("/api/ranking", methods=["GET"])
def api_ranking():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT equipe, pontos FROM pontuacoes ORDER BY pontos DESC")
    dados = [{"equipe": row[0], "pontos": row[1]} for row in c.fetchall()]
    conn.close()
    return {"ranking": dados}

# Garante que o banco exista
inicializar_banco()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))