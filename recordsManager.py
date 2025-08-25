import json
import requests
import os
from env import SCRIPT_DIR
records_path = os.path.join(SCRIPT_DIR, 'data', 'records.json')

def ReadRecords():
       with open(records_path, 'r') as file:
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
    with open(records_path, 'w') as f:
        json.dump(records, f, indent=4)