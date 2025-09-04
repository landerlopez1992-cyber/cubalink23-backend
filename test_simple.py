import os, requests
os.environ["DUFFEL_API_KEY"] = "duffel_live_Rj6u0G0cT2hUeIw53ou2HRTNNf0tXl6oP-pVzcGvI7e"
headers = {"Accept": "application/json", "Authorization": "Bearer " + os.environ["DUFFEL_API_KEY"], "Duffel-Version": "v2"}
url = "https://api.duffel.com/air/airports?search=MIA&limit=20"
response = requests.get(url, headers=headers)
print("Status:", response.status_code)
if response.status_code == 200: print("✅ API funciona"); data = response.json(); print("Aeropuertos:", len(data.get("data", [])))
