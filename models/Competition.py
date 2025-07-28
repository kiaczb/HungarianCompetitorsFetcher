from datetime import datetime
class Competition:
    def __init__(self, name, iso, From, to, competitorWResults):
        self.CompetitionName = name
        self.CountryIso = iso
        self.From = self._ensure_datetime(From)
        self.To = self._ensure_datetime(to)
        self.CompetitorWithRecords = competitorWResults
        
    def AddPerson(self, competitorWithRecord):
        self.CompetitorWithRecords.append(competitorWithRecord)
    
    def _ensure_datetime(self, value):
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, "%Y-%m-%d")