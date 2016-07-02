from __future__ import print_function

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from datetime import datetime

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Dump database to backup on Google Drive'

    def handle(self, *args, **options):
    
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    
        path = "budget/management/commands/"

        SCOPES = 'https://www.googleapis.com/auth/drive.file'
        store = file.Storage(path + 'storage.json')
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(path + 'client_secret.json', SCOPES)
            creds = tools.run(store)

        DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

        metadata = {
            'name': 'budget-data-backup-' + current_datetime +'.json.txt',
            'mimeType': 'text/plain'
        }

        res = DRIVE.files().create(body=metadata, media_body=path + 'budget-data-backup.json.txt').execute()

        if res:
            print('Uploaded "%s" (%s)' % (metadata['name'], res['mimeType']))
