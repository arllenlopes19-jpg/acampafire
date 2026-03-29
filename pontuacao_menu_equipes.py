import json
import os

ARQUIVO = "pontuacoes.json"

def carregar_pontuacoes():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    else:
        return {}

def salvar_pontuacoes(pontuacoes):
    with open(ARQUIVO, "w") as f:
        json.dump(pontuacoes, f, indent=4)

pontuacoes = carregar_pontuacoes()

def adicionar_pontos():
    equipe = input("Digite o nome da equipe: ")
    pontos = int(input("Digite a quantidade de pontos: "))
    if equipe in pontuacoes:
        pontuacoes[equipe] += pontos
        salvar_pontuacoes(pontuacoes)
        print(f"{pontos} pontos adicionados para {equipe}.")
    else:
        print("Equipe não encontrada. Cadastre a equipe primeiro!")

def mostrar_ranking():
    if not pontuacoes:
        print("\nNenhuma equipe cadastrada ainda.")
        return
    ranking = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    print("\nRanking Atual:")
    for posicao, (equipe, pontos) in enumerate(ranking, start=1):
        print(f"{posicao}. {equipe} - {pontos} pontos")

def cadastrar_equipe():
    equipe = input("Digite o nome da nova equipe: ")
    if equipe in pontuacoes:
        print("Essa equipe já existe!")
    else:
        pontuacoes[equipe] = 0
        salvar_pontuacoes(pontuacoes)
        print(f"Equipe {equipe} cadastrada com sucesso!")

def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Adicionar pontos")
        print("2. Mostrar ranking")
        print("3. Cadastrar nova equipe")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            adicionar_pontos()
        elif opcao == "2":
            mostrar_ranking()
        elif opcao == "3":
            cadastrar_equipe()
        elif opcao == "4":
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida, tente novamente.")

menu()
