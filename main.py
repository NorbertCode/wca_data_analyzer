import requests


competitions = []
for page in range(1, 18):
    comp_data = requests.get(f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/competitions-page-{page}.json").json()
    comps_names = [comp["id"] for comp in comp_data["items"]]
    competitions.extend(comps_names)
pass
