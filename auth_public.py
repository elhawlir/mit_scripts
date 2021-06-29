import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authorisation(json_file):
    # define the scope
    # access the sheets and drive apis
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/forms']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('google-credentials.json', scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    return client