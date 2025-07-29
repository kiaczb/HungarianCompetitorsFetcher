import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from env import excludedCompetitorWcaIds
import json

def fetch_persons_page(page):
    url = f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons-page-{page}.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
        return response.json()
    except:
        return []

def getHungarianCompetitors():
    persons = {}
    batch_size = 100
    max_workers = 20
    page = 1
    empty_pages_in_a_row = 0
    max_empty_pages = 5

    while True:
        futures = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(batch_size):
                futures.append(executor.submit(fetch_persons_page, page + i))

            any_nonempty = False

            for future in as_completed(futures):
                personData = future.result()
                if not personData:
                    empty_pages_in_a_row += 1
                    continue
                else:
                    empty_pages_in_a_row = 0
                    any_nonempty = True

                for person in personData["items"]:
                    if person["country"] == "HU" or person["id"] in excludedCompetitorWcaIds:
                        wca_id = person["id"]
                        name = person["name"]
                        competition_count = person["numberOfCompetitions"]
                        persons[wca_id] = {
                            "name": name,
                            "competition_count": competition_count
                        }

        if empty_pages_in_a_row >= max_empty_pages or not any_nonempty:
            print("Abort: Too many empty pages")
            break

        page += batch_size

    return persons


data = getHungarianCompetitors()
with open("./data/hungarians.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)