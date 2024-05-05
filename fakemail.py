import json
import yaml
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from lxml import html


class TemporaryEmailManager:
    def __init__(self):
        self.db = "DatabaseManager()"

    def create_email(self, expiry_time=None):
        r = requests.get('https://www.fakemail.net/', timeout=5)
        h = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest"
        }
        
        a=r.headers['Set-Cookie'][:-6]
        r = requests.get('https://www.fakemail.net/index/index', headers=h)
        email = json.loads(r.text.encode())['email']
        b=email.split("@")
        a+="TMA="+b[0]+"%40"+b[1]+";"
        self.cookie=a
        print(email)
        return email

    def get_emails(self, email):
        h = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest"
        }
        h['Cookie'] = self.cookie
        r = requests.get('https://www.fakemail.net/index/refresh', headers=h)
        h['Referer'] = 'https://www.fakemail.net/window/id/2'
        r = requests.get('https://www.fakemail.net/email/id/2', headers=h)
        return r.text
    def getnum(self,email):
        emails="There was en error, during loading the email."
        while True:
            print(emails)
            emails = self.get_emails(email)
            if("Ваш код безопасности:" in emails):
                break
            time.sleep(2)  
        tree = html.fromstring(emails)
        email_links = tree.xpath("//p")
        return email_links[-1].text
