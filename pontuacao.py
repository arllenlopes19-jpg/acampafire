# Sistema de pontuação para equipes

# Dicionário com equipes e suas pontuações
pontuacoes = {
    "Equipe Azul": 0,
    "Equipe Verde": 0,
    "Equipe Vermelha": 0,
    "Equipe Amarela": 0
}

def adicionar_pontos(equipe, pontos):
    if equipe in pontuacoes:
        pontuacoes[equipe] += pontos
        print(f"{pontos} pontos adicionados para {equipe}.")
    else:
        print("Equipe não encontrada.")

def mostrar_ranking():
    ranking = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    print("\nRanking Atual:")
    for posicao, (equipe, pontos) in enumerate(ranking, start=1):
        print(f"{posicao}. {equipe} - {pontos} pontos")

# Exemplo de uso
adicionar_pontos("Equipe Azul", 10)
adicionar_pontos("Equipe Verde", 15)
adicionar_pontos("Equipe Vermelha", 5)

mostrar_ranking()
