import requests
from datetime import datetime
from competitors import GetCompetitionsParallel

def GetCompetitionsWithHungarians(date):
    competitions = GetCompetitionIds(date)
    #outputs = []
    competition_results = GetCompetitionsParallel(competitions)

    if competition_results:
        return sorted(competition_results, key=lambda oput: oput.From)
    else:
        print("Nincs elérhető verseny.")
        return []       

def GetCompetitionIds(date):
        competitionIds = [] #This is not an id it's a competition object list or dict or hashmap or whateve.
        pageCount = 1
        end = False
        while not end:
            competitionsUrl = f"https://www.worldcubeassociation.org/api/v0/competitions?sort=start_date&start={date.strftime('%Y-%m-%d')}&end={datetime.now().strftime('%Y-%m-%d')}&page={pageCount}"
            #competitionsUrl = f"https://www.worldcubeassociation.org/api/v0/competitions?sort=start_date&start=2025-07-01&end=2025-07-27&page={pageCount}"
            response = requests.get(competitionsUrl)
            if response.status_code != 200:
                print("Error")
                end = True
            competitionData = response.json()
                #If tha pagecount is bigger than the actual competition list (in the API) the API returns an empty list (like this []). When this happens we know that we went through all of the competitions.
            if not competitionData:
                    end = True
            competitionIds += competitionData
            pageCount += 1
        return competitionIds

