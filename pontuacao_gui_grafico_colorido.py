import tkinter as tk
from tkinter import messagebox
import json, os, csv
import matplotlib.pyplot as plt

ARQUIVO = "pontuacoes.json"

def carregar_pontuacoes():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    else:
        return {}

def salvar_pontuacoes():
    with open(ARQUIVO, "w") as f:
        json.dump(pontuacoes, f, indent=4)

pontuacoes = carregar_pontuacoes()

# Funções principais
def adicionar_pontos():
    equipe = entry_equipe.get()
    try:
        pontos = int(entry_pontos.get())
    except ValueError:
        messagebox.showerror("Erro", "Digite um número válido de pontos.")
        return
    if equipe in pontuacoes:
        pontuacoes[equipe] += pontos
        salvar_pontuacoes()
        atualizar_ranking()
    else:
        messagebox.showerror("Erro", "Equipe não encontrada. Cadastre primeiro.")

def cadastrar_equipe():
    equipe = entry_equipe.get()
    if equipe in pontuacoes:
        messagebox.showwarning("Aviso", "Essa equipe já existe!")
    else:
        pontuacoes[equipe] = 0
        salvar_pontuacoes()
        atualizar_ranking()

def remover_equipe():
    equipe = entry_equipe.get()
    if equipe in pontuacoes:
        del pontuacoes[equipe]
        salvar_pontuacoes()
        atualizar_ranking()
    else:
        messagebox.showerror("Erro", "Equipe não encontrada.")

def atualizar_ranking():
    ranking_text.delete("1.0", tk.END)
    ranking = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    for posicao, (equipe, pontos) in enumerate(ranking, start=1):
        ranking_text.insert(tk.END, f"{posicao}. {equipe} - {pontos} pontos\n")

def mostrar_grafico():
    if not pontuacoes:
        messagebox.showwarning("Aviso", "Nenhuma equipe cadastrada ainda.")
        return
    
    equipes = list(pontuacoes.keys())
    pontos = list(pontuacoes.values())
    
    # Paleta de cores (se tiver mais equipes, as cores se repetem)
    cores = ["#ff6347", "#4682b4", "#32cd32", "#ffa500", "#9370db", "#ff69b4", "#00ced1", "#8b4513"]
    cores_usadas = [cores[i % len(cores)] for i in range(len(equipes))]
    
    plt.figure(figsize=(8,5))
    plt.bar(equipes, pontos, color=cores_usadas, edgecolor="black")
    plt.title("Pontuação das Equipes - Acampamento", fontsize=14, fontweight="bold")
    plt.xlabel("Equipes")
    plt.ylabel("Pontos")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

# Interface principal
root = tk.Tk()
root.title("🏕️ Sistema de Pontuação - Acampamento")
root.configure(bg="#f0f8ff")

# Campos de entrada
tk.Label(root, text="Equipe:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
entry_equipe = tk.Entry(root, font=("Arial", 12))
entry_equipe.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Pontos:", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5)
entry_pontos = tk.Entry(root, font=("Arial", 12))
entry_pontos.grid(row=1, column=1, padx=5, pady=5)

# Botões principais
btn_style = {"font":("Arial", 11, "bold"), "bg":"#4682b4", "fg":"white", "width":18}

tk.Button(root, text="Adicionar Pontos", command=adicionar_pontos, **btn_style).grid(row=2, column=0, padx=5, pady=5)
tk.Button(root, text="Cadastrar Equipe", command=cadastrar_equipe, **btn_style).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Remover Equipe", command=remover_equipe, **btn_style).grid(row=3, column=0, padx=5, pady=5)
tk.Button(root, text="Mostrar Gráfico", command=mostrar_grafico, **btn_style).grid(row=3, column=1, padx=5, pady=5)

# Ranking
tk.Label(root, text="Ranking Atual:", font=("Arial", 13, "bold"), bg="#f0f8ff").grid(row=4, column=0, columnspan=2, pady=10)
ranking_text = tk.Text(root, height=10, width=45, font=("Courier New", 11), bg="#fffafa")
ranking_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

atualizar_ranking()
root.mainloop()
