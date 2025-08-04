import json

difference = 3
milestones = [40, 100]
def ReadPeople():
    with open('./data/delegates.json', 'r', encoding="utf-8") as file:
        return json.load(file)

#TODO: Add comp_count locally
localDelegates = ReadPeople()
def GetImportantDelegates(persons):
    importantdelegates = []
    for person in persons:
        if IsImportantDelegate(person.WcaId):
            importantdelegates.append(localDelegates[person.WcaId])
    return importantdelegates

def AddCompetitionToDelegate(delegate):
    if not delegate.WcaId:
        return
    if delegate.WcaId not in localDelegates:
        localDelegates[delegate.WcaId] = {
            "wca_id": delegate.WcaId,
            "name": delegate.competitorName,
            "competition_count": 1
        }
    else:
        localDelegates[delegate.WcaId]["competition_count"] += 1

def SaveToDelegatesJson():
    with open("./data/delegates.json", "w", encoding="utf-8") as f:
        json.dump(localDelegates, f, indent=2, ensure_ascii=False)
    

def IsImportantDelegate(wcaId):
    if not wcaId or wcaId not in localDelegates:
        return False
    for milestone in milestones:
            if (milestone-difference <= localDelegates[wcaId]["delegated_competitions_count"] <= milestone):
                return True
def IsDelegate(person):
    return True if person.wcaId in localDelegates else False