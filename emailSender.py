import smtplib
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from competitionCount import GetImportantCompetitors
from utils import ConvertResult, ConvertDate
from env import emailFrom, emailTo, emailSubject, emailCode

env = Environment(loader=FileSystemLoader('templates'))

def WriteEmail(competitionsWithHungarians):
    count_competitors = GetAllImportantCompetitors(competitionsWithHungarians)
    
    html_content = RenderHtmlEmail(competitionsWithHungarians, count_competitors)
    
    SendEmail(html_content)

def RenderHtmlEmail(competitions, count_competitors):
    template = env.get_template('emailTemplate.html')
    return template.render(
        competitions=competitions,
        count_competitors=count_competitors,
        convert_date=ConvertDate,
        convert_result=ConvertResult
    )

def GetAllImportantCompetitors(competitions):
    count_competitors = []
    if competitions:
        for comp in competitions:
            importantCompetitorsByCompetition = GetImportantCompetitors(comp.CompetitorWithRecords)
            if importantCompetitorsByCompetition not in count_competitors:
                count_competitors.extend(importantCompetitorsByCompetition)
    return count_competitors

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
