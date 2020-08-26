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


class ciridrive:
    def __init__(self):
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

        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(PATH + PASS_DRIVE):
            with open(PATH + PASS_DRIVE, "rb") as token:
                self.creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # Receiving client_id and client_secret
                client_id = input("Digite a client_id/Enter the client_id:")
                client_secret = input(
                    "Digite a client_secret//Enter the client_secret:"
                )

                # Checking if folders exist
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

                # Editing the settings for the client values ​​entered by the user
                settings["installed"]["client_id"] = client_id
                settings["installed"]["client_secret"] = client_secret
                settings["installed"]["project_id"] = "Ciridrive-External"

                with open(PATH + FILE_SETTINGS, "w") as file:
                    json.dump(settings, file)

                flow = InstalledAppFlow.from_client_secrets_file(
                    PATH + FILE_SETTINGS, SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(PATH + PASS_DRIVE, "wb") as token:
                pickle.dump(self.creds, token)

    def sheet_to_list(self, SPREADSHEET_ID, TAB_NAME=False, status=False):
        # Verify internet connection
        try:
            service = build("sheets", "v4", credentials=self.creds)
        except:
            print("ERROR: No internet connection")

            return "ERROR"

        # Call the Sheets API
        sheet = service.spreadsheets()

        # Verify variables names
        try:
            # Search the name of all tabs
            if not TAB_NAME:
                list_tab = []
                metadata = sheet.getByDataFilter(spreadsheetId=SPREADSHEET_ID).execute()
                for key_sheet in metadata["sheets"]:
                    list_tab.append(key_sheet["properties"]["title"])
            else:
                list_tab = [TAB_NAME]

            # Download the spreadsheet tabs
            list_values = []
            for tab in list_tab:
                result = (
                    sheet.values()
                    .get(
                        spreadsheetId=SPREADSHEET_ID,
                        range=tab,
                        majorDimension="COLUMNS",
                    )
                    .execute()
                )

                list_values.append(result.get("values", []))

            return list_values
        except:
            print(
                "ERROR: Incorrect Tab_name, Spreadsheet_name or SPREADSHEET_ID. Please check and try again."
            )

            return "ERROR"

    def sheet_to_json(
        self, SPREADSHEET_ID, TAB_NAME=False, status=False, FILE_PATH="sheet_json.json"
    ):
        # Verify internet connection
        try:
            service = build("sheets", "v4", credentials=self.creds)
        except:
            print("ERROR: No internet connection")

            return "ERROR"

        # Call the Sheets API
        sheet = service.spreadsheets()

        # Verify variables names
        try:
            # Search the name of all tabs
            if not TAB_NAME:
                list_tab = []
                metadata = sheet.getByDataFilter(spreadsheetId=SPREADSHEET_ID).execute()
                for key_sheet in metadata["sheets"]:
                    list_tab.append(key_sheet["properties"]["title"])
            else:
                list_tab = [TAB_NAME]

            # Download the spreadsheet tabs
            dict_values = {}
            for tab in list_tab:
                result = (
                    sheet.values()
                    .get(
                        spreadsheetId=SPREADSHEET_ID,
                        range=tab,
                        majorDimension="COLUMNS",
                    )
                    .execute()
                )

                dict_values[tab] = result.get("values", {})

            with open(FILE_PATH, "w") as json_file:
                json.dump(dict_values, json_file)

            return dict_values
        except:
            print(
                "ERROR: Incorrect Tab_name, Spreadsheet_name or SPREADSHEET_ID. Please check and try again."
            )

            return "ERROR"


if __name__ == "__main__":
    values = ciridrive().sheet_to_list(
        "17p_SDlN6eW8jHmrGiHR3mwRzzZgGwGXFXBV7-HMtWBk", "tab"
    )

    print(values)

