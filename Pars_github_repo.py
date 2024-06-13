import requests
import json

url = "https://api.github.com/users/proks1312"
response = requests.get(url)
j_data = response.json()
with open("1_1_repo.json","w") as f:
    json_repo = json.dump(j_data,f)
print(f"Количество репозиториев: {j_data.get('public_repos')}")
