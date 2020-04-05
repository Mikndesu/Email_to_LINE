import requests
import os
import json
from os.path import join, dirname
from dotenv import load_dotenv

class GMail:

    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.client_id = os.environ.get("CLIENT_ID")
        self.client_secret = os.environ.get("CLIENT_SECRET")
        self.access_token = os.environ.get("ACCESS_TOKEN")
        self.refresh_token = os.environ.get("REFRESH_TOKEN")

    def get_email(self):
        messageIds=[]
        mailsDetail = self.checkAccessTokenAvailable()
        for id in mailsDetail["messages"]:
            messageIds.append(id)
        print(messageIds)
        return messageIds

    def checkAccessTokenAvailable(self):
        headers = {
            'Authorization' : 'Bearer ' + self.access_token,
        }
        res = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages/', headers=headers)
        if res.status_code!=200:
            self.generateNewAccessToken()
            header = {
                'Authorization': 'Bearer '+  self.access_token,
            }
            resp = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages/', headers=header)
            return resp.json()
        else:
            return res.json()

    def generateNewAccessToken(self):
        # gen new access_token if previous one is available
        # replace env with it
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        response = requests.post('https://accounts.google.com/o/oauth2/token', data=data).json()
        os.environ["ACCESS_TOKEN"] = response["access_token"]
        self.access_token = response["access_token"]

if __name__ == "__main__":
    g = GMail()
    g.get_email()
