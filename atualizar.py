import requests

url = "https://acampafire.onrender.com/api/atualizar"
dados = {"equipe": "verde", "pontos": 150}

resposta = requests.post(url, json=dados)
print(resposta.json())