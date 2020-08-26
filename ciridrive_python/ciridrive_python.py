import os.path
import pickle
import time
import json
import pathlib

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import io  # Added
from googleapiclient.http import MediaIoBaseDownload
from apiclient import http

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
DICT_MIME_TYPE = {
    "google-apps": {
        "application/vnd.google-apps.document": "docx",
        "application/vnd.google-apps.spreadsheet": "xlsx",
        "application/vnd.google-apps.presentation": "pptx",
    },
    "general": {
        "application/pdf": "pdf",
        "text/plain": "txt",
        "application/vnd.ms-excel": "xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        "text/xml": "xml",
        "application/vnd.oasis.opendocument.spreadsheet": "ods",
        "application/x-httpd-php": "php",
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        "image/bmp": "bmp",
        "application/msword": "doc",
        "text/js": "js",
        "application/x-shockwave-flash": "swf",
        "audio/mpeg": "mp3",
        "application/zip": "zip",
        "application/rar": "rar",
        "application/tar": "tar",
        "application/arj": "arj",
        "application/cab": "cab",
        "text/html": "html",
        "text/html": "htm",
        "application/octet-stream": "default",
    },
}


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
            "https://www.googleapis.com/auth/drive.appdata",
            "https://www.googleapis.com/auth/drive.apps.readonly",
            "https://www.googleapis.com/auth/drive.photos.readonly",
        ]

        # Path to credential
        self.path_script = str(pathlib.Path(__file__).parent.resolve())
        PATH = self.path_script + "/pass_drive/"

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

    def sheet_to_list(self, spreadsheet_id, tab_name=False, status=False):
        # Verify internet connection
        try:
            service = build("sheets", "v4", credentials=self.creds)
        except:
            print("ERROR: No internet connection")

            return False

        # Call the Sheets API
        sheet = service.spreadsheets()

        # Verify variables names
        try:
            # Search the name of all tabs
            if not tab_name:
                list_tab = []
                metadata = sheet.getByDataFilter(spreadsheetId=spreadsheet_id).execute()
                for key_sheet in metadata["sheets"]:
                    list_tab.append(key_sheet["properties"]["title"])
            else:
                list_tab = [tab_name]

            # Download the spreadsheet tabs
            list_values = []
            for tab in list_tab:
                result = (
                    sheet.values()
                    .get(
                        spreadsheetId=spreadsheet_id,
                        range=tab,
                        majorDimension="COLUMNS",
                    )
                    .execute()
                )

                list_values.append(result.get("values", []))

            return list_values
        except:
            print(
                "ERROR: Incorrect Tab_name, Spreadsheet_name or spreadsheet_id. Please check and try again."
            )

            return False

    def sheet_to_json(
        self, spreadsheet_id, tab_name=False, status=False, file_path="sheet_json.json"
    ):
        # Verify internet connection
        try:
            service = build("sheets", "v4", credentials=self.creds)
        except:
            print("ERROR: No internet connection")

            return False

        # Call the Sheets API
        sheet = service.spreadsheets()

        # Verify variables names
        try:
            # Search the name of all tabs
            if not tab_name:
                list_tab = []
                metadata = sheet.getByDataFilter(spreadsheetId=spreadsheet_id).execute()
                for key_sheet in metadata["sheets"]:
                    list_tab.append(key_sheet["properties"]["title"])
            else:
                list_tab = [tab_name]

            # Download the spreadsheet tabs
            dict_values = {}
            for tab in list_tab:
                result = (
                    sheet.values()
                    .get(
                        spreadsheetId=spreadsheet_id,
                        range=tab,
                        majorDimension="COLUMNS",
                    )
                    .execute()
                )

                dict_values[tab] = result.get("values", {})

            with open(file_path, "w") as json_file:
                json.dump(dict_values, json_file)

            return dict_values
        except:
            print(
                "ERROR: Incorrect Tab_name, Spreadsheet_name or spreadsheet_id. Please check and try again."
            )

            return False

    def create_folder(self, name_folder=False, id_folder_main=False):
        """
            Goal:
                Create folder on the drive
            Args:
                name_folder: Folder name(Required).
                id_folder_main: If the folder is created inside a shared drive.
                credentials: Password to access the drive, If not, this function will create
            Returns:
                Normal return: created folder id.
                False: If an error has occurred.
        """

        # Checks whether the arguments were passed correctly
        if False in [name_folder]:
            print("up_Drive: Argument is missing, please check and try again.\n")
            print(
                """Args:
            name_folder: Folder name(Required).
            id_folder_main: If the folder is created inside another.
            credentials: Password to access the drive, If not, this function will create\n"""
            )
            return False

        # Logging into the drive and receiving credentials
        try:
            service = build("drive", "v3", credentials=self.creds)
        except:
            print("ERROR: No internet connection")

            return False

        # Configures the file name and folder on the drive
        file_metadata = {
            "name": name_folder,
            "mimeType": "application/vnd.google-apps.folder",
        }

        # if the folder is created inside another
        if id_folder_main:
            file_metadata["parents"] = [str(id_folder_main)]

        drive_folder = (
            service.files()
            .create(body=file_metadata, fields="id", supportsAllDrives=True)
            .execute()
        )

        return drive_folder.get("id")

    def drive_upload(self, path_file, id_folder=False, name_file_inDrive=False):
        """
            Goal:
                Access the drive and upload the file
            Args:
                path_file: Path of the file to be uploaded(Required).
                id_folder: Folder id on the drive(Required).
                name_file_inDrive: If you leave a different name for the file on the drive.
                credentials: Password to access the drive, If not, this function will create
            Returns:
                "sucess": The upload was successful.
                False: If an error has occurred.
        """

        # Logging into the drive and receiving credentials
        try:
            service = build("drive", "v3", credentials=self.creds)
        except:
            print("ERROR: No internet connection")

            return False

        # Checking if the file to be sent exists
        if os.path.exists(path_file):
            # Configures the file name and folder on the drive
            name_file = (
                name_file_inDrive if name_file_inDrive else path_file.split("/")[-1]
            )

            id_file = service.files().generateIds(count=1, space="drive").execute()
            file_metadata = {"name": str(name_file), "id": id_file["ids"][0]}

            if id_folder:
                file_metadata["parents"] = [str(id_folder)]

            # Configure the file
            media = MediaFileUpload(path_file, resumable=True)

            # Responsible for uploading
            request = service.files().create(
                body=file_metadata, media_body=media, supportsAllDrives=True
            )
        else:
            print("UpDrive: File not found\n")

            return False

        # Shows the upload progress on the terminal
        response, progresso_ant = None, 0
        start = time.time()
        print(f"\n--- Uploading the file : {name_file} ---\n")
        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    progresso = status.progress() * 100
                    speed_upload = time.time() - start
                    start = time.time()
                    taxa = (
                        (progresso - progresso_ant if progresso_ant else progresso)
                    ) / speed_upload

                    print(f"Uploaded: {int(progresso)}%.", end=" | ")
                    print(f"Time remaining: {round((100-progresso)/taxa,2)}s.")
                    progresso_ant = progresso
            except:
                print("No internet connection\n")

                return False
        print(f"--> Upload Complete! : {name_file} <--\n")

        return id_file

    def drive_download(self, file_id, save_path=False, status=True):
        # Authenticates to the drive
        try:
            service = build("drive", "v3", credentials=self.creds)
        except:
            print("ERROR: No internet connection")

            return False

        # Creates the folder where the downloaded file will be saved
        default_path_download = self.path_script + "/download"
        if not (os.path.exists(default_path_download)) and not (save_path):
            os.mkdir(default_path_download)
        elif save_path:
            default_path_download = save_path

        # Receives file metadata
        metadata_arq = service.files().get(fileId=file_id).execute()
        name_file = metadata_arq["name"]

        # Sets the file type
        if metadata_arq["mimeType"] in DICT_MIME_TYPE["google-apps"]:
            type_file = DICT_MIME_TYPE["google-apps"][metadata_arq["mimeType"]]
            request = service.files().export_media(
                fileId=file_id, mimeType="application/pdf"
            )
            file_save = io.FileIO(
                f"{default_path_download}/{name_file}.{type_file}", mode="wb"
            )
        elif metadata_arq["mimeType"] in DICT_MIME_TYPE["general"]:
            request = service.files().get_media(fileId=file_id)
            file_save = io.FileIO(f"{default_path_download}/{name_file}", mode="wb")
        else:
            print("The file type cannot be downloaded")

            return False

        downloader = MediaIoBaseDownload(file_save, request)

        # Download the file, and print the remaining time on the screen
        done, progresso_ant = False, 0
        start = time.time()
        if status:
            print(f"\n--- Downloading the file : {name_file} ---\n")
        while done is False:
            try:
                status_download, done = downloader.next_chunk()
                if status_download and status:
                    progresso = status_download.progress() * 100
                    speed_upload = time.time() - start
                    start = time.time()
                    taxa = (
                        (progresso - progresso_ant if progresso_ant else progresso)
                    ) / speed_upload

                    print(f"Downloading: {int(progresso)}%.", end=" | ")
                    print(f"Time remaining: {round((100-progresso)/taxa,2)}s.")
                    progresso_ant = progresso
            except:
                print("No internet connection\n")

                return False
        if status:
            print(f"--> Downloading Complete! : {name_file} <--\n")

        return True

    def copy_file(self, file_id, new_name=False):
        try:
            service = build("drive", "v3", credentials=self.creds)
        except:
            print("ERROR: No internet connection")

            return False

        file_metadata = {"description": "This file is a copy"}
        if new_name:
            file_metadata["name"] = str(new_name)

        config_copy_file = (
            service.files()
            .copy(fileId=file_id, body=file_metadata, supportsAllDrives=True)
            .execute()
        )

        return config_copy_file["id"]

    def move_file(self, file_id, folder_id):
        try:
            service = build("drive", "v3", credentials=self.creds)
        except:
            print("ERROR: No internet connection")

            return False

        # Retrieve the existing parents to remove
        file = service.files().get(fileId=file_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents"))

        # Move the file to the new folder
        file = (
            service.files()
            .update(
                fileId=file_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields="id, parents",
                supportsAllDrives=True,
            )
            .execute()
        )

    def search_files(self):
        # AINDA NÃO TERMINEI
        try:
            service = build("drive", "v3", credentials=self.creds)
        except:
            print("ERROR: No internet connection")

            return False

        page_token = None
        while True:
            response = (
                service.files()
                .list(
                    q="mimeType = 'application/vnd.google-apps.folder'",
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )
            for file in response.get("files", []):
                # Process change
                print("Found file: %s (%s)" % (file.get("name"), file.get("id")))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break


if __name__ == "__main__":
    values = ciridrive().sheet_to_list(
        "17p_SDlN6eW8jHmrGiHR3mwRzzZgGwGXFXBV7-HMtWBk", "tab"
    )

    print(values)

