from competition import GetCompetitionsWithHungarians
from datetime import datetime, timedelta
from emailSender import WriteEmail

date = datetime.now() - timedelta(weeks=1)
competitionsWithHungarians = GetCompetitionsWithHungarians(date)

WriteEmail(competitionsWithHungarians)