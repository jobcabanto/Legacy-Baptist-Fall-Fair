from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path

class Token:
    
    def __init__(self):
      self.scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
      self.creds = None

    def access_api(self):
        if os.path.exists("token.json"):
          self.creds = Credentials.from_authorized_user_file("token.json", self.scopes)
  # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
          if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
          else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.scopes)
            self.creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
          with open("token.json", "w") as token:
            token.write(self.creds.to_json())

        try:
          return [True, build("sheets", "v4", credentials=self.creds)]
        except HttpError as err:
          print(err)
