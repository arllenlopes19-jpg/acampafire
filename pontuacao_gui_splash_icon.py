import tkinter as tk
from tkinter import PhotoImage
import time, threading
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

# --- Funções principais (mesmas do programa anterior) ---
def adicionar_pontos():
    equipe = entry_equipe.get()
    try:
        pontos = int(entry_pontos.get())
    except ValueError:
        return
    if equipe in pontuacoes:
        pontuacoes[equipe] += pontos
        salvar_pontuacoes()
        atualizar_ranking()

def cadastrar_equipe():
    equipe = entry_equipe.get()
    if equipe not in pontuacoes:
        pontuacoes[equipe] = 0
        salvar_pontuacoes()
        atualizar_ranking()

def remover_equipe():
    equipe = entry_equipe.get()
    if equipe in pontuacoes:
        del pontuacoes[equipe]
        salvar_pontuacoes()
        atualizar_ranking()

def atualizar_ranking():
    ranking_text.delete("1.0", tk.END)
    ranking = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    for posicao, (equipe, pontos) in enumerate(ranking, start=1):
        ranking_text.insert(tk.END, f"{posicao}. {equipe} - {pontos} pontos\n")

def mostrar_grafico():
    if not pontuacoes: return
    equipes = list(pontuacoes.keys())
    pontos = list(pontuacoes.values())
    plt.figure(figsize=(8,5))
    plt.bar(equipes, pontos, color="orange", edgecolor="black")
    plt.title("Pontuação das Equipes - Acampamento", fontsize=14, fontweight="bold")
    plt.xlabel("Equipes")
    plt.ylabel("Pontos")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

# --- Splash Screen ---
def splash_screen():
    splash = tk.Tk()
    splash.title("Bem-vindo ao Acampamento")
    splash.geometry("320x240")
    splash.configure(bg="#fff8dc")

    # Carregar ícone da fogueira
    try:
        icon_img = PhotoImage(file="fogueira.ico")
        tk.Label(splash, image=icon_img, bg="#fff8dc").pack(pady=10)
        splash.iconphoto(False, icon_img)  # também define como ícone da janela
    except:
        tk.Label(splash, text="🔥", font=("Arial", 30), bg="#fff8dc").pack(pady=10)

    tk.Label(splash, text="🏕️ Acampamento 2026", font=("Arial", 14, "bold"), bg="#fff8dc").pack(pady=10)
    tk.Label(splash, text="Carregando sistema de pontuação...", font=("Arial", 10), bg="#fff8dc").pack(pady=10)

    # Fecha o splash depois de 3 segundos
    def fechar():
        time.sleep(3)
        splash.destroy()
        iniciar_programa()

    threading.Thread(target=fechar).start()
    splash.mainloop()

# --- Programa principal ---
def iniciar_programa():
    global entry_equipe, entry_pontos, ranking_text
    root = tk.Tk()
    root.title("🏕️ Sistema de Pontuação - Acampamento")
    root.configure(bg="#f0f8ff")

    tk.Label(root, text="Equipe:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
    entry_equipe = tk.Entry(root, font=("Arial", 12))
    entry_equipe.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Pontos:", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5)
    entry_pontos = tk.Entry(root, font=("Arial", 12))
    entry_pontos.grid(row=1, column=1, padx=5, pady=5)

    btn_style = {"font":("Arial", 11, "bold"), "bg":"#4682b4", "fg":"white", "width":18}

    tk.Button(root, text="Adicionar Pontos", command=adicionar_pontos, **btn_style).grid(row=2, column=0, padx=5, pady=5)
    tk.Button(root, text="Cadastrar Equipe", command=cadastrar_equipe, **btn_style).grid(row=2, column=1, padx=5, pady=5)
    tk.Button(root, text="Remover Equipe", command=remover_equipe, **btn_style).grid(row=3, column=0, padx=5, pady=5)
    tk.Button(root, text="Mostrar Gráfico", command=mostrar_grafico, **btn_style).grid(row=3, column=1, padx=5, pady=5)

    tk.Label(root, text="Ranking Atual:", font=("Arial", 13, "bold"), bg="#f0f8ff").grid(row=4, column=0, columnspan=2, pady=10)
    ranking_text = tk.Text(root, height=10, width=45, font=("Courier New", 11), bg="#fffafa")
    ranking_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    atualizar_ranking()
    root.mainloop()

# Inicia pelo splash
splash_screen()
