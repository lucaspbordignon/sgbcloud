 #!/usr/bin/env python3 

from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from glob import glob

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

 # Available at:
 # https://console.developers.google.com/apis/credentials?project=gestaodeleadsteste&hl=pt-br
APPLICATION_NAME = 'sgb-cloud-teste' 
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets' 

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
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
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

def update_spreadsheet( rows, headers,
                        spreadsheetId, sheet ):
    """
    Function for appending a new row in a Google Spreadsheet.

    list of lists   rows 
    list of lists   headers
    str             spreadsheetId
    list of lists   headers (Ex. [["Header 1", "Header 2","Header 3"]])
    str             sheet (Ex. "Sheet1")
    
    """

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets',
                              'v4',
                              http=http,
                              discoveryServiceUrl=discoveryUrl)
    
    global link 

    link = 'https://docs.google.com/spreadsheets/d/'+ spreadsheetId +'/edit#gid=0'

    rangeName = sheet + '!A1:C'

    result = service.spreadsheets().values().get(
                                    spreadsheetId=spreadsheetId,
                                    range=rangeName).execute()
    current_values = result.get('values', [])

    last_row = len(current_values)

    if last_row == 0:
        body = { 'values': headers }

        rangeName = sheet + '!A1:C1'

        result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId, range=rangeName,
        valueInputOption='USER_ENTERED', body=body).execute()

        last_row=1

    rangeName = sheet + '!A' + str(last_row+1) + ':C'

    body = { 'values': rows }
    
    result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheetId, range=rangeName,
            valueInputOption='USER_ENTERED', body=body).execute()
