import json
output = []
difference = 5
milestones = [100, 200]
def readPersons():
    with open('./data/hungarians.json', 'r', encoding="utf-8") as file:
        return json.load(file)

checkedCompetitors = []
localPersons = readPersons()
def getImportantCompetitors(persons):
    checkedCompetitors.append(persons)
    for person in persons:
        # if person in checkedCompetitors:
        #     continue
        # Sajnos nem lehet egyszer nézni csak egy versenyzőt
        print(person)
        for milestone in milestones:
            if milestone-difference < localPersons[person.WcaId]["competition_count"] <= milestone:
                output.append(localPersons[person.WcaId])
        addCompetitionToCompetitor(person.WcaId)
    return output

def addCompetitionToCompetitor(WcaId):
    localPersons[WcaId]["competition_count"] += 1
    with open("./data/hungarians.json", "w", encoding="utf-8") as f:
        json.dump(localPersons, f, indent=2, ensure_ascii=False)