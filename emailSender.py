import smtplib
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from competitionCount import GetImportantCompetitors
from delegatesCount import GetImportantDelegates
from utils import ConvertResult, ConvertDate
from env import emailFrom, emailTo, emailSubject, emailCode

environment = Environment(loader=FileSystemLoader('templates'))

def WriteEmail(competitionsWithHungarians):
    count_competitors = GetAllImportantCompetitors(competitionsWithHungarians, GetImportantCompetitors)
    count_delegates = GetAllImportantCompetitors(competitionsWithHungarians, GetImportantDelegates)
    
    html_content = RenderHtmlEmail(competitionsWithHungarians, count_competitors, count_delegates)
    
    SendEmail(html_content)

def RenderHtmlEmail(competitionsWithHungarians, count_competitors, count_delegates):
    template = environment.get_template('competitions.html')
    excludedHungarianCompetitions = []
    for comp in competitionsWithHungarians:
        if not comp.isHungarian:
            excludedHungarianCompetitions.append(comp)
        else:
            recorders = []
            for person in comp.CompetitorWithRecords:
                if person.Records:
                    recorders.append(person)
            comp.CompetitorWithRecords = recorders
            if recorders:
                excludedHungarianCompetitions.append(comp)

    print(count_delegates, " Filip")
    print(count_competitors, " Filip")
    return template.render(
        competitions=excludedHungarianCompetitions,
        count_competitors=count_competitors,
        delegate_milestones=count_delegates,
        convert_date=ConvertDate,
        convert_result=ConvertResult
    )

def GetAllImportantCompetitors(competitions, func): #Gets the important competitors OR delegates based on the func function
    competitors_by_id = {}

    for comp in competitions:
        for competitor in func(comp.CompetitorWithRecords):
            print(competitor)
            competitors_by_id[competitor["wca_id"]] = competitor  # felülírja, ha már volt ilyen

    return list(competitors_by_id.values())
def SendEmail(html_body):
    msg = MIMEText(html_body, 'html', 'utf-8')
    msg['From'] = f"Bonsz <{emailFrom}>"
    msg['To'] = emailTo
    msg['Subject'] = emailSubject

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(emailFrom, emailCode)
        server.sendmail(emailFrom, emailTo, msg.as_string())
    except Exception as e:
        print(f"Email failed to send: {str(e)}")
    finally:
        server.quit()
