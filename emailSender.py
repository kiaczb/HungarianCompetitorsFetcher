
import smtplib
from email.mime.text import MIMEText
import competitionCount
from utils import ConvertResult, ConvertDate
from env import emailFrom, emailTo, emailSubject, emailCode

def WriteEmail(competitionsWithHungarians):
    message= ""
    competitionCountCompetitiorsMessage = "Upcoming milestones: \n"
    countCompetitors = []
    if competitionsWithHungarians:
        for comp in competitionsWithHungarians:
            message+= (f"{ConvertDate(comp.From, comp.To)}\n{comp.CompetitionName} ({comp.CountryIso}):\n")
            countCompetitors = competitionCount.getImportantCompetitors(comp.CompetitorWithRecords)
            for person in comp.CompetitorWithRecords:
                message+= f"\t- {person.CompetitorName}\n"
                for event, record in person.Records.items():
                    message+= f"\t\tEvent: {event}\n"
                    for item in record:
                        message+= f"\t\tType: {item.Type}\n"
                        message+= f"\t\t   -Result: {ConvertResult(item.Result, event)}\n"
                        message+= f"\t\t   -Record Type: {item.Badge}\n"
                    #message+="------------------------------------------------------\n"
            message+= "----------------------------------------------------------------------------------\n"
    else:
        message = "No competitions"
    for countCompetitor in countCompetitors:
        competitionCountCompetitiorsMessage+= f"{countCompetitor['name']} - {countCompetitor['competition_count']}\n"
    message += competitionCountCompetitiorsMessage
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = f" Bonsz <{emailFrom}>"
    msg['To'] = emailTo
    msg['Subject'] = emailSubject
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:

        server.login(emailFrom, emailCode)
        server.sendmail(emailFrom,emailTo,msg.as_string())
    except:
        print("Email failed to send")
    server.quit()