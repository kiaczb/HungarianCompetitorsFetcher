import smtplib
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from competitionCount import GetImportantCompetitors
from utils import ConvertResult, ConvertDate
from env import emailFrom, emailTo, emailSubject, emailCode

environment = Environment(loader=FileSystemLoader('templates'))

def WriteEmail(competitionsWithHungarians):
    count_competitors = GetAllImportantCompetitors(competitionsWithHungarians)
    
    html_content = RenderHtmlEmail(competitionsWithHungarians, count_competitors)
    
    SendEmail(html_content)

def RenderHtmlEmail(competitionsWithHungarians, count_competitors):
    template = environment.get_template('emailTemplate.html')
    excludedHungarianCompetitions = []
    for comp in competitionsWithHungarians:
        if not comp.isHungarian:
            excludedHungarianCompetitions.append(comp)
        else:
            for person in comp.CompetitorWithRecords:
                if person.Records:
                    excludedHungarianCompetitions.append(comp)
    return template.render(
        competitions=excludedHungarianCompetitions,
        count_competitors=count_competitors,
        convert_date=ConvertDate,
        convert_result=ConvertResult
    )

def GetAllImportantCompetitors(competitions):
    competitors_by_id = {}

    for comp in competitions:
        for competitor in GetImportantCompetitors(comp.CompetitorWithRecords):
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
