from competition import GetCompetitionsWithHungarians
from datetime import datetime, timedelta
from emailSender import WriteEmail
from recordsManager import SaveRecords
import time
start = time.time()

date = datetime.now() - timedelta(weeks=1)
competitionsWithHungarians = GetCompetitionsWithHungarians(date)

end = time.time()
print(f"Runtime: {end - start:.4f} seconds")


WriteEmail(competitionsWithHungarians)
SaveRecords()
#TODO Clean up and layering and DI
#TODO Add comments
#TODO Predict the milestone competition
