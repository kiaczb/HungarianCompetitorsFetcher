class CompetitorWithRecords:
    def __init__(self, name, wcaid, records = None):
        self.CompetitorName = name
        self.WcaId = wcaid
        self.Records = records if records is not None else {} #dict {category:Record}
    def __str__(self):
        return f"{self.CompetitorName}"