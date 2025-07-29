from models.Record import Record
from models.CompetitorWithRecords import CompetitorWithRecords
from env import excludedCompetitorWcaIds, badges
from recordsManager import localNationalRecords
import requests
from concurrent.futures import ThreadPoolExecutor
import flatdict

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

def process_person(person, events, isHungarianCompetition=False):
    if person["countryIso2"] != "HU" and person["wcaId"] not in excludedCompetitorWcaIds:
        return None  # Skip non-Hungarian and non-exceptional competitors.

    if not person.get("registration"):
        return None

    registered_event_ids = set(person["registration"]["eventIds"])
    competitor = None

    def is_person_result(result):
        return result.get("personId") == person["registrantId"]

    for event in events:
        if event["id"] not in registered_event_ids:
            continue

        isAdvanced = True

        # Flatten all rounds and results into a single list of (round, result) pairs
        round_result_pairs = [
            (_round, result)
            for _round in event.get("rounds", [])
            for result in _round.get("results", [])
            if is_person_result(result)
        ]

        for _round, result in round_result_pairs:
            if not isAdvanced:
                break

            if competitor is None:
                competitor = CompetitorWithRecords(person["name"], person["wcaId"])

            update_records("average", result["average"], competitor, event["id"], localNationalRecords, badges)
            update_records("single", result["best"], competitor, event["id"], localNationalRecords, badges)

            adv = _round.get("advancementCondition")
            if adv and result.get("ranking"):
                if adv["type"] == "ranking":
                    isAdvanced = result["ranking"] <= adv["level"]
                elif adv["type"] == "percent":
                    threshold = round(len(_round["results"]) * (adv["level"] / 100))
                    isAdvanced = result["ranking"] <= threshold

    if competitor and isHungarianCompetition and not competitor.Records:
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