from models.Record import Record
from models.CompetitorWithRecords import CompetitorWithRecords
from env import excludedCompetitorWcaIds, badges
from recordsManager import localNationalRecords
import requests
from concurrent.futures import ThreadPoolExecutor

def update_records(record_type, value, competitor, event_id, localNationalRecords, badges):
    #Frissíti a versenyző rekordjait és kezeli a nemzeti és speciális rekordokat.
    if value > 0:
        for index, nationalRecord in enumerate(localNationalRecords.values()):
            if competitor.WcaId in excludedCompetitorWcaIds and index == 2:
                continue
            if value <= nationalRecord[event_id][record_type]:
                nationalRecord[event_id][record_type] = value
                if event_id in competitor.Records:
                    competitor.Records[event_id].append(Record(record_type, value, badges[index]))
                else:
                    competitor.Records[event_id] = [Record(record_type, value, badges[index])]
                break

def process_person(person, events, isHungarianCompetition = False):

    if person["countryIso2"] != "HU" and person["wcaId"] not in excludedCompetitorWcaIds:
        return None  # Ha nem magyar vagy  Alexey, nem dolgozzuk fel.

    competitor = None

    # Most minden eseményhez egy dict-et tárolunk, ahol külön kulcsokban van az "average" és a "single"
    
    #TODO Remove the nested for loops using flatdict or recursion
    for event in events:
        if person["registration"] and event["id"] not in person["registration"]["eventIds"]:
            continue  # Ha nem regisztrált az adott eventre, kihagyjuk.
        isAdvanced = True
        for _round in event["rounds"]:
            if not isAdvanced:
                break
            for result in _round["results"]:
                if result["personId"] != person["registrantId"]:
                    continue

                if competitor is None:
                    competitor = CompetitorWithRecords(person["name"], person["wcaId"])

                #best = personal_bests.get(event["id"], {})
                # Átlag rekord ellenőrzés
                update_records("average", result["average"], competitor, event["id"], localNationalRecords, badges)

                    # Single rekord ellenőrzés
                update_records("single", result["best"],  competitor, event["id"], localNationalRecords, badges)
                # Ha nem jut tovább, állítsuk akkor isAdvanced = False
                if _round["advancementCondition"]:
                    adv = _round["advancementCondition"]
                    if result["ranking"]:
                        if (adv["type"] == "ranking" and result["ranking"] > adv["level"]) or \
                        (adv["type"] == "percent" and result["ranking"] > len(_round["results"]) * (round(adv["level"] / 100))):
                            isAdvanced = False
    if competitor and isHungarianCompetition and competitor.Records == {}: #Ha létezik a versenyző de magyar verseny volt és nem rakott rekordot
        return None
    return competitor


def GetCompetitorsForCompetition(comp):
    """Lekéri a versenyzőket és párhuzamosan feldolgozza őket."""
    competitorsUrl = f"https://www.worldcubeassociation.org/api/v0/competitions/{comp['id']}/wcif/public"
    #competitorsUrl = f"https://www.worldcubeassociation.org/api/v0/competitions/BudapestSummer2024/wcif/public"
    response = requests.get(competitorsUrl)
    if response.status_code != 200:
        return [], comp
    competitionWCIF = response.json()
    persons = competitionWCIF["persons"]
    events = competitionWCIF["events"]
    competitors = []

    isHungarianCompetition = True if comp["country_iso2"] == "HU" else False

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda p: process_person(p, events,isHungarianCompetition), persons))

    # Csak a nem None versenyzőket adjuk hozzá
    competitors = [c for c in results if c]

    return competitors