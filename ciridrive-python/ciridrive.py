import os.path
import pickle
import time
import json
import pathlib

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

DEFAULT_SETTINGS = {
    "installed": {
        "client_id": "",
        "client_secret": "",
        "project_id": "",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
    }
}

FILE_SETTINGS = "settings_drive.json"
PASS_DRIVE = "pass_drive"


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
    PATH = str(pathlib.Path(__file__).parent.resolve()) + "/pass_drive/"

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(PATH + PASS_DRIVE):
        with open(PATH + PASS_DRIVE, "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_id = input("Digite a cliente_id:")
            client_secret = input("Digite a cliente_secret:")

            if not (os.path.exists(PATH)):
                os.mkdir(PATH)
            if os.path.exists(PATH + FILE_SETTINGS):
                with open(PATH + FILE_SETTINGS, "r") as file:
                    settings = json.load(file)
            else:
                with open(PATH + FILE_SETTINGS, "w") as file:
                    json.dump(DEFAULT_SETTINGS, file)

                with open(PATH + FILE_SETTINGS, "r") as file:
                    settings = json.load(file)

            settings["installed"]["client_id"] = client_id
            settings["installed"]["client_secret"] = client_secret
            settings["installed"]["project_id"] = "Ciridrive-External"

            with open(PATH + FILE_SETTINGS, "w") as file:
                json.dump(settings, file)

            flow = InstalledAppFlow.from_client_secrets_file(
                PATH + FILE_SETTINGS, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(PATH + PASS_DRIVE, "wb") as token:
            pickle.dump(creds, token)

    return creds


if __name__ == "__main__":
    drive_pass()

