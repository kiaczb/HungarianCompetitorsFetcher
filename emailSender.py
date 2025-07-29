import smtplib
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from competitionCount import getImportantCompetitors
from utils import ConvertResult, ConvertDate
from env import emailFrom, emailTo, emailSubject, emailCode

env = Environment(loader=FileSystemLoader('templates'))

def WriteEmail(competitionsWithHungarians):
    count_competitors = get_all_important_competitors(competitionsWithHungarians)
    
    html_content = render_html_email(competitionsWithHungarians, count_competitors)
    
    send_email(html_content)

def render_html_email(competitions, count_competitors):
    template = env.get_template('emailTemplate.html')
    return template.render(
        competitions=competitions,
        count_competitors=count_competitors,
        convert_date=ConvertDate,
        convert_result=ConvertResult
    )

def get_all_important_competitors(competitions):
    count_competitors = []
    if competitions:
        for comp in competitions:
            count_competitors.extend(getImportantCompetitors(comp.CompetitorWithRecords))
    return count_competitors

def send_email(html_body):
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
