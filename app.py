from flask import Flask, render_template
import json, os

app = Flask(__name__)

# Caminho correto para o arquivo dentro da pasta dist
ARQUIVO = os.path.join("dist", "pontuacoes.json")

def carregar_pontuacoes():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # cria o arquivo vazio se não existir
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}

@app.route("/")
def ranking():
    pontuacoes = carregar_pontuacoes()
    # transforma o dicionário em lista de tuplas e ordena
    ranking = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    medalhas = ["🥇", "🥈", "🥉"]
    return render_template("ranking.html", ranking=ranking, medalhas=medalhas)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
