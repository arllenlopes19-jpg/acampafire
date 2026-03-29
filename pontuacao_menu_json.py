import json
import os

# Nome do arquivo onde vamos salvar os pontos
ARQUIVO = "pontuacoes.json"

# Carregar pontuações do arquivo (se existir)
def carregar_pontuacoes():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    else:
        # Se não existir, começa com pontuações zeradas
        return {
            "Equipe Azul": 0,
            "Equipe Verde": 0,
            "Equipe Vermelha": 0,
            "Equipe Amarela": 0
        }

# Salvar pontuações no arquivo
def salvar_pontuacoes(pontuacoes):
    with open(ARQUIVO, "w") as f:
        json.dump(pontuacoes, f, indent=4)

# Inicializa pontuações
pontuacoes = carregar_pontuacoes()

def adicionar_pontos():
    equipe = input("Digite o nome da equipe: ")
    pontos = int(input("Digite a quantidade de pontos: "))
    if equipe in pontuacoes:
        pontuacoes[equipe] += pontos
        salvar_pontuacoes(pontuacoes)
        print(f"{pontos} pontos adicionados para {equipe}.")
    else:
        print("Equipe não encontrada.")

def mostrar_ranking():
    ranking = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    print("\nRanking Atual:")
    for posicao, (equipe, pontos) in enumerate(ranking, start=1):
        print(f"{posicao}. {equipe} - {pontos} pontos")

def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Adicionar pontos")
        print("2. Mostrar ranking")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            adicionar_pontos()
        elif opcao == "2":
            mostrar_ranking()
        elif opcao == "3":
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida, tente novamente.")

# Iniciar o programa
menu()
