import httplib2
import os
import csv
import os.path
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

# Google Sheet API dependencies
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

APPLICATION_NAME = 'sgb-cloud-teste'
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'


class NaturalLanguageProcessor:
    def most_common_words(self,
                          corpus,
                          add_stop_words=[""],
                          bloco='' ,
                          palestrante='',
                          arquivo='Most_Common_Words.csv',
                          save_csv=False):

        """
            Função que recebe um texto, recebe identificadores (bloco, palestrante...) e
            exporta um csv com contagem das palavras para o bloco/palestrante.

            Parâmetros:

                str     corpus:         Texto a ter as palavras contadas
                list    add_stop_words: (opcional) Lista dedicada a palavras que a biblioteca nltk não remove sozinha.
                str     bloco:           (opcional) bloco do festival
                str     palestrante:    (opcional) Palestrante
                bool    save_csv:       (opcional)
                str     arquivo:        (padrão: 'Most_Common_Words.csv') Nome do Arquivo a ser lido/salvo.

        """

        tokens = [w for w in word_tokenize(corpus.lower()) if w.isalpha()]

        stopWords_nltk = set(stopwords.words('portuguese'))

        chumbadas = set(["apenas","outro","pode","trás","lado","frente"])

        stopWords = stopWords_nltk.union(set(add_stop_words)).union(chumbadas)

        no_stops = [w for w in tokens if w not in stopWords and len(w) > 2]

        if save_csv:
            if not os.path.isfile(arquivo):
                with open(arquivo, 'w') as csvfile:
                    Writer = csv.writer(csvfile)
                    Writer.writerow(['palavra','bloco','palestrante'])
            for word in no_stops:
                with open(arquivo,'a') as csvfile:
                    Writer = csv.writer(csvfile)
                    Writer.writerow([word,bloco,palestrante])

        rows = [[w,bloco,palestrante] for w in no_stops]
        return rows


    def generate_and_upload_words(self, text, speaker, block):
        rows = self.most_common_words(text, speaker, block)

        update_spreadsheet(rows,
                           headers = [['palavra', 'palestrante', 'block']],
                           spreadsheetId='12nX-xkjk5YiZvNhf0SXHDusefO942CRpxlgkDJeD5qg',
                           sheet='common_words')

        print('##################################################')
        print('Google Spreadsheet updated! URL: {}'.format(link))


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
