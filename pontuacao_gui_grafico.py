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
        messagebox.showinfo("Sucesso", f"{pontos} pontos adicionados para {equipe}.")
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
        messagebox.showinfo("Sucesso", f"Equipe {equipe} cadastrada com sucesso!")

def remover_equipe():
    equipe = entry_equipe.get()
    if equipe in pontuacoes:
        del pontuacoes[equipe]
        salvar_pontuacoes()
        atualizar_ranking()
        messagebox.showinfo("Sucesso", f"Equipe {equipe} removida com sucesso!")
    else:
        messagebox.showerror("Erro", "Equipe não encontrada.")

def atualizar_ranking():
    ranking_text.delete("1.0", tk.END)
    ranking = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    for posicao, (equipe, pontos) in enumerate(ranking, start=1):
        ranking_text.insert(tk.END, f"{posicao}. {equipe} - {pontos} pontos\n")

def exportar_txt():
    ranking = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    with open("ranking_final.txt", "w") as f:
        f.write("Ranking Final do Acampamento\n\n")
        for posicao, (equipe, pontos) in enumerate(ranking, start=1):
            f.write(f"{posicao}. {equipe} - {pontos} pontos\n")
    messagebox.showinfo("Exportação", "Ranking exportado para ranking_final.txt")

def exportar_csv():
    ranking = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    with open("ranking_final.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Posição", "Equipe", "Pontos"])
        for posicao, (equipe, pontos) in enumerate(ranking, start=1):
            writer.writerow([posicao, equipe, pontos])
    messagebox.showinfo("Exportação", "Ranking exportado para ranking_final.csv")

def mostrar_grafico():
    if not pontuacoes:
        messagebox.showwarning("Aviso", "Nenhuma equipe cadastrada ainda.")
        return
    equipes = list(pontuacoes.keys())
    pontos = list(pontuacoes.values())
    
    plt.figure(figsize=(8,5))
    plt.bar(equipes, pontos, color="skyblue", edgecolor="black")
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

# Título
titulo = tk.Label(root, text="Controle de Pontuação", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#2f4f4f")
titulo.grid(row=0, column=0, columnspan=2, pady=10)

# Campos de entrada
tk.Label(root, text="Equipe:", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_equipe = tk.Entry(root, font=("Arial", 12))
entry_equipe.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Pontos:", font=("Arial", 12), bg="#f0f8ff").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_pontos = tk.Entry(root, font=("Arial", 12))
entry_pontos.grid(row=2, column=1, padx=5, pady=5)

# Botões principais
btn_style = {"font":("Arial", 11, "bold"), "bg":"#4682b4", "fg":"white", "width":18, "height":1}

tk.Button(root, text="Adicionar Pontos", command=adicionar_pontos, **btn_style).grid(row=3, column=0, padx=5, pady=5)
tk.Button(root, text="Cadastrar Equipe", command=cadastrar_equipe, **btn_style).grid(row=3, column=1, padx=5, pady=5)
tk.Button(root, text="Remover Equipe", command=remover_equipe, **btn_style).grid(row=4, column=0, padx=5, pady=5)
tk.Button(root, text="Exportar Ranking TXT", command=exportar_txt, **btn_style).grid(row=4, column=1, padx=5, pady=5)
tk.Button(root, text="Exportar Ranking CSV", command=exportar_csv, **btn_style).grid(row=5, column=0, padx=5, pady=5)
tk.Button(root, text="Mostrar Gráfico", command=mostrar_grafico, **btn_style).grid(row=5, column=1, padx=5, pady=5)

# Ranking
tk.Label(root, text="Ranking Atual:", font=("Arial", 13, "bold"), bg="#f0f8ff").grid(row=6, column=0, columnspan=2, pady=10)
ranking_text = tk.Text(root, height=10, width=45, font=("Courier New", 11), bg="#fffafa")
ranking_text.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

atualizar_ranking()

root.mainloop()
