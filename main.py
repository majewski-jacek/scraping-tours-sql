import requests
import selectorlib
import smtplib, ssl
import os

URL = "https://programmer100.pythonanywhere.com/tours/"
SENDER = "app1generator@gmail.com"
AUTHENTICATION = os.getenv("MAIL_KEY")
RECEIVER = "app1generator@gmail.com"


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(SENDER, AUTHENTICATION)
        server.sendmail(SENDER, RECEIVER, message)



def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


def read():
    with open("data.txt", "r") as file:
        return file.read()

if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    content = read()
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email(message="Hey, new event was found!")