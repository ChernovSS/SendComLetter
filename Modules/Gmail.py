import base64
import os
import pickle
from email.mime.text import MIMEText
from pathlib import Path

import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery


class Gmail:
    def __init__(self):
        pass

    def retry_credential_request(self, force=False):
        """ Deletes token.pickle file and re-runs the original request function """
        print("⚠ Insufficient permission, probably due to changing scopes.")
        i = input("Type [D] to delete token and retry: ") if force == False else 'd'
        if i.lower() == "d":
            os.remove("token.pickle")
            print("Deleted token.pickle")
            self()

    def get_google_api_credentials(self, scopes):
        """ Returns credentials for given Google API scope(s) """
        credentials = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if Path('token.pickle').is_file():
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(google.auth.transport.requests.Request())
            else:
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../token.pickle', 'wb') as token:
                pickle.dump(credentials, token)
        return credentials

    def send_gmail(self, to, subject, message_text):
        """Send a simple email using Gmail API"""
        scopes = ['https://www.googleapis.com/auth/gmail.compose']
        gmail_api = googleapiclient.discovery.build('gmail', 'v1', credentials=self.get_google_api_credentials(scopes))
        message = MIMEText(message_text)
        message['to'] = to
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        try:
            request = gmail_api.users().messages().send(userId='me', body={'raw': raw}).execute()
            print(request)
        except googleapiclient.errors.HttpError as E:
            print(E)
            return
        return request
