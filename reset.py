import requests
url = "https://acampafire.onrender.com/api/reset"
resposta = requests.post(url)
print(resposta.json())