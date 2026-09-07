import requests

team_name = "furia"

response = requests.get(f"https://api.csapi.de/teams/?name={team_name}")

print(response.status_code)

data = response.json()

print(data)

if data:
    print(data[0]["name"])
else:
    print("Team not found.")
data[0]["name"]

print(bool([]))
print(bool(["FURIA"]))

if response.status_code == 200:
    data = response.json()
else:
    print("Error:", response.status_code)
response.raise_for_status()


def get_team(team_name):
    response = requests.get(f"https://api.csapi.de/teams/?name={team_name}")
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["name"]
        else:
            return "Team not found."
    else:
        return f"Error: {response.status_code}"


get_team("furia")
