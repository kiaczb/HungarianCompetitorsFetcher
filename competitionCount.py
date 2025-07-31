import json

difference = 3
milestones = [100, 200]
def ReadPeople():
    with open('./data/hungarians.json', 'r', encoding="utf-8") as file:
        return json.load(file)

#TODO: Don't return a competitor twice, but count their competitions according to theri attendance
localPeople = ReadPeople()
def GetImportantCompetitors(persons):
    importantCompetitors = []
    for person in persons:
        if IsImportantCompetitor(person):
            importantCompetitors.append(localPeople[person.WcaId])
    return importantCompetitors

def AddCompetitionToCompetitor(WcaId):
    localPeople[WcaId]["competition_count"] += 1
    with open("./data/hungarians.json", "w", encoding="utf-8") as f:
        json.dump(localPeople, f, indent=2, ensure_ascii=False)

def IsImportantCompetitor(competitor):
    for milestone in milestones:
            if competitor and (milestone-difference < localPeople[competitor.WcaId]["competition_count"] <= milestone):
                return True