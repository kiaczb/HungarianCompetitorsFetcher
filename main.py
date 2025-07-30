from competition import GetCompetitionsWithHungarians
from datetime import datetime, timedelta
from emailSender import WriteEmail
import time
start = time.time()

date = datetime.now() - timedelta(weeks=1)
competitionsWithHungarians = GetCompetitionsWithHungarians(date)

end = time.time()
print(f"Runtime: {end - start:.4f} seconds")

#TODO Figure out why a person object can be null
WriteEmail(competitionsWithHungarians)
# email_sender = CompetitionEmailSender()
# email_sender.send_competition_email(competitionsWithHungarians)

