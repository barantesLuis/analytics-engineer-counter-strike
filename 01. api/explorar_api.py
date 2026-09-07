import requests

BASE_URL = "https://api.csapi.de"

endpoints = [
    "/rankings/",
    "/teams/",
    "/players/stats",
    "/matches/",
]

for endpoint in endpoints:
    response = requests.get(BASE_URL + endpoint)

    print("=" * 50)
    print(f"ENDPOINT: {endpoint}")
    print(f"STATUS: {response.status_code}")

    data = response.json()

    print(f"TIPO: {type(data)}")

    if isinstance(data, list):
        print(f"QUANTIDADE: {len(data)}")

        if data:
            print("PRIMEIRO REGISTRO:")
            print(data[0])

    elif isinstance(data, dict):
        print("CHAVES:")
        print(data.keys())

    print()
