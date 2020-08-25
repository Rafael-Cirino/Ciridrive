import os.path
import pickle
import time
import json

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def drive_pass():
    """
        Goal:
            Responsible for "logging" into the drive.
        Returns:
            Returns the credential to service log into the drive.
    """
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = [
        "https://www.googleapis.com/auth/drive.metadata.readonly",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
    ]

    # Path to credential
    PATH = os.getcwd() + "/"

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(PATH + "pass_drive"):
        with open(PATH + "pass_drive", "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_id = input("Digite a cliente_id:")
            client_secret = input("Digite a cliente_secret:")

            settings = {}
            with open(PATH + "settings.json", "r") as file:
                settings = json.load(file)

            settings["installed"]["client_id"] = client_id
            settings["installed"]["client_secret"] = client_secret
            settings["installed"]["project_id"] = "Ciridrive-External"

            with open(PATH + "settings.json", "w") as file:
                json.dump(settings, file)

            flow = InstalledAppFlow.from_client_secrets_file(
                PATH + "settings.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(PATH + "pass_drive", "wb") as token:
            pickle.dump(creds, token)

    return creds


if __name__ == "__main__":
    drive_pass()

