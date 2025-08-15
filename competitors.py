from CompetitionModels.Record import Record
from CompetitionModels.CompetitorWithRecords import CompetitorWithRecords
from env import excludedCompetitorWcaIds, badges
from recordsManager import localNationalRecords
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from CompetitionModels.Competition import Competition
from competitionCount import AddCompetitionToCompetitor, SaveToHungariansJson
from delegatesCount import IsDelegate, AddCompetitionToDelegate, SaveToDelegatesJson
import time
def UpdateRecords(record_type, value, competitor, event_id, localNationalRecords, badges):
    #Updates the competitor's recoords and handles national records.
    if value > 0:
        for index, nationalRecord in enumerate(localNationalRecords.values()):
            if competitor.WcaId in excludedCompetitorWcaIds and index == 2: #If the person is not representing Hungary but a member of the Hungarian community
                continue
            if value <= nationalRecord[event_id][record_type]:
                nationalRecord[event_id][record_type] = value
                if event_id in competitor.Records:
                    competitor.Records[event_id].append(Record(record_type, value, badges[index]))
                else:
                    competitor.Records[event_id] = [Record(record_type, value, badges[index])]
                break

def ProcessPerson(person, events):
    if person["countryIso2"] != "HU" and person["wcaId"] not in excludedCompetitorWcaIds:
        return None  # Skip non-Hungarian and non-exceptional competitors.

    if not person.get("registration"):
        return None

    registered_event_ids = set(person["registration"]["eventIds"])
    competitor = CompetitorWithRecords(person["name"], person["wcaId"])

    def IsPersonResult(result):
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
            if IsPersonResult(result)
        ]

        for _round, result in round_result_pairs:
            if not isAdvanced:
                break

            UpdateRecords("average", result["average"], competitor, event["id"], localNationalRecords, badges)
            UpdateRecords("single", result["best"], competitor, event["id"], localNationalRecords, badges)

            adv = _round.get("advancementCondition")
            if adv and result.get("ranking"):
                if adv["type"] == "ranking":
                    isAdvanced = result["ranking"] <= adv["level"]
                elif adv["type"] == "percent":
                    threshold = round(len(_round["results"]) * (adv["level"] / 100))
                    isAdvanced = result["ranking"] <= threshold

    AddCompetitionToCompetitor(competitor)

    if IsDelegate(competitor):
        AddCompetitionToDelegate(competitor)
    
    return competitor

def IsHungarianCompetition(comp):
     return True if comp["country_iso2"] == "HU" else False

def GetCompetitorsForCompetition(comp):
    url = f"https://www.worldcubeassociation.org/api/v0/competitions/{comp['id']}/wcif/public"
    for attempt in range(5):
        response = requests.get(url)
        if response.status_code == 200:
            break
        #When we get a 429 error (too muck requests) we wait
        elif response.status_code == 429:
            wait = 2 ** attempt  # 1s, 2s, 4s, 8s, …
            time.sleep(wait)
            continue
        else:
            print(f"HTTP {response.status_code} for {comp['id']}")
            return []
    else:
        print(f"Too many retries for {comp['id']}")
        return []

    # We can make sure that here the response.status_code == 200
    competitionWCIF = response.json()
    persons = competitionWCIF["persons"]
    events = competitionWCIF["events"]
    competitors = []


    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda p: ProcessPerson(p, events), persons))

    SaveToHungariansJson()
    SaveToDelegatesJson()
    # We add only the not None competitors.
    competitors = [c for c in results if c]

    return competitors

def GetCompetitionsParallel(competitions):
    results = []

    def process(comp):
        competitors = GetCompetitorsForCompetition(comp)
        if competitors:
            return Competition(comp["name"], comp["country_iso2"], comp["start_date"], comp["end_date"], IsHungarianCompetition(comp), competitors)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process, comp) for comp in competitions]
        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    results.append(result)  # (comp, competitors)
            except Exception as e:
                print(f"Hiba a verseny feldolgozásakor: {e}")

    return results