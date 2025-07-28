import json
import requests

def ReadRecords():
       with open('./data/records.json', 'r') as file:
             records = json.load(file)
       return records
localNationalRecords = ReadRecords()

def SaveRecords():
    recordsUrl = "https://www.worldcubeassociation.org/api/v0/records"
    response = requests.get(recordsUrl)
    if response.status_code == 200:
                recordsData = response.json()

    records = {
        "world_records": recordsData["world_records"],
        "european_records": recordsData["continental_records"].get("_Europe", {}),
        "hungarian_records": recordsData["national_records"].get("Hungary", {})
    }
    with open('./data/records.json', 'w') as f:
        json.dump(records, f, indent=4)