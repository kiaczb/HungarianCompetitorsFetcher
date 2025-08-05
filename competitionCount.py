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
        if IsImportantCompetitor(person.WcaId):
            importantCompetitors.append(localPeople[person.WcaId])
    return importantCompetitors

def AddCompetitionToCompetitor(competitor):
    if not competitor.WcaId:
        return
    if competitor.WcaId not in localPeople:
        localPeople[competitor.WcaId] = {
            "wca_id": competitor.WcaId,
            "name": competitor.CompetitorName,
            "competition_count": 1
        }
    else:
        localPeople[competitor.WcaId]["competition_count"] += 1

def SaveToHungariansJson():
    with open("./data/hungarians.json", "w", encoding="utf-8") as f:
        json.dump(localPeople, f, indent=2, ensure_ascii=False)
    

def IsImportantCompetitor(wcaId):
    if not wcaId or wcaId not in localPeople:
        return False
    for milestone in milestones:
            if (milestone-difference <= localPeople[wcaId]["competition_count"] <= milestone):
                return True
