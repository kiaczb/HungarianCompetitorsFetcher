import requests
from datetime import datetime, timedelta
from competitors import GetCompetitorsForCompetition
from models.Competition import Competition

def GetCompetitionsWithHungarians(date):
        competitions = GetCompetitionIds(date)
        outputs = [] #Ez lesz majd a végső dolog amibe rakjuk majd a szűrt adatokat
        for comp in competitions:
            competitors = GetCompetitorsForCompetition(comp)
            if competitors:
                output = Competition(comp["name"], comp["country_iso2"], comp["start_date"], comp["end_date"], competitors)
                outputs.append(output)
                    
        if outputs:
            return sorted(outputs, key=lambda oput: oput.To)
        else:
            print("Nincs elérhető verseny.")  # Ha nincs verseny
            return []        

def GetCompetitionIds(date):
        competitionIds = [] #Ez nem Id hanem konkrét versseny objektum(okat tároló lista) vagy dictionary vagy hashmap tudja a tököm hogy hívják ebben a nyelvben
        pageCount = 1
        end = False
        while not end:
            #competitionsUrl = f"https://www.worldcubeassociation.org/api/v0/competitions?sort=start_date&start={date.strftime('%Y-%m-%d')}&end={datetime.now().strftime('%Y-%m-%d')}&page={pageCount}"
            competitionsUrl = f"https://www.worldcubeassociation.org/api/v0/competitions?sort=start_date&start=2025-06-19&end=2025-06-22&page={pageCount}"
            response = requests.get(competitionsUrl)
            if response.status_code != 200:
                print("Error")
                end = True
            competitionData = response.json()
                #Ha túlmegy a pagecount akkor az api egy üres listát ad (ilyet: []) ezért ilyenkor tudjuk hogy végigértünk a versenyeken és leállítjuk
            if not competitionData:
                    end = True
            competitionIds += competitionData
            pageCount += 1
        return competitionIds