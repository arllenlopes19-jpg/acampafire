import requests

# Sistema de pontuação para equipes com menu interativo
pontuacoes = {
    "Equipe Azul": 0,
    "Equipe Verde": 0,
    "Equipe Vermelha": 0,
    "Equipe Amarela": 0
}

# Função para enviar pontos ao servidor Render
def enviar_pontos(equipe, pontos):
    url = "https://acampafire.onrender.com/api/atualizar"
    dados = {"equipe": equipe, "pontos": pontos}
    try:
        resposta = requests.post(url, json=dados)
        print("Servidor respondeu:", resposta.json())
    except Exception as e:
        print("Erro ao enviar pontos:", e)

def adicionar_pontos():
    equipe = input("Digite o nome da equipe: ")
    pontos = int(input("Digite a quantidade de pontos: "))
    if equipe in pontuacoes:
        pontuacoes[equipe] += pontos
        print(f"{pontos} pontos adicionados para {equipe}.")
        # envia para o servidor Render
        enviar_pontos(equipe, pontuacoes[equipe])
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