from __future__ import print_function

from apiclient.discovery import build
import httplib2
import os
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient.http import MediaFileUpload

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Dump database to backup on Google Drive'

    def handle(self, *args, **options):

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/drive-python-quickstart.json
        SCOPES = 'https://www.googleapis.com/auth/drive'
        CLIENT_SECRET_FILE = 'budget/client_secret.json'
        APPLICATION_NAME = 'Home budget backup'

        def get_credentials():
            """Gets valid user credentials from storage.

            If nothing has been stored, or if the stored credentials are invalid,
            the OAuth2 flow is completed to obtain the new credentials.

            Returns:
                Credentials, the obtained credential.
            """
            home_dir = os.path.expanduser('~')
            credential_dir = os.path.join(home_dir, '.credentials')
            if not os.path.exists(credential_dir):
                os.makedirs(credential_dir)
            credential_path = os.path.join(credential_dir,
                                           'home-budget-backup.json')

            store = oauth2client.file.Storage(credential_path)
            credentials = store.get()
            if not credentials or credentials.invalid:
                flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
                flow.user_agent = APPLICATION_NAME
                if flags:
                    credentials = tools.run_flow(flow, store, flags)
                else: # Needed only for compatibility with Python 2.6
                    credentials = tools.run(flow, store)
                print('Storing credentials to ' + credential_path)
            return credentials

        file_to_upload = "budget/backup.json"

        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)

        file_metadata = {
          'name' : 'budget-backup.json',
          'mimeType' : 'application/json'
        }

        media = MediaFileUpload(file_to_upload,
                                mimetype='application/json',
                                resumable=True)

        file = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()

        print('File ID: %s' % file.get('id'))