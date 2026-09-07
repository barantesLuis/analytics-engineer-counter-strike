import requests
import json
from pathlib import Path
from datetime import date


BASE_URL = "https://api.csapi.de"

ENDPOINTS = {
    "rankings": "/rankings/",
    "teams": "/teams/",
    "players_stats": "/players/stats",
    "matches": "/matches/",
}


today = date.today().isoformat()

base_path = Path("../02-data/bronze")


for name, endpoint in ENDPOINTS.items():
    print(f"Buscando {name}...")

    response = requests.get(BASE_URL + endpoint)

    response.raise_for_status()

    data = response.json()

    output_path = base_path / name
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / f"{today}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"Salvo em: {file_path}")
