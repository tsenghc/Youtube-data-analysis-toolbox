from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import os
import httplib2
import json
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser],description='').parse_args()
except ImportError:
    flags = None

Filepath='./OAuth/'

def get_credentials():
    """
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    #home_dir = os.path.expanduser('~')

    credential_dir = os.path.join(Filepath, '.credentials')

    CLIENT_SECRET_FILE='./OAuth/client_secret.json'

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'drive-python-quickstart.json')

    if not os.path.exists(CLIENT_SECRET_FILE):
        print('**Not find Client_Secret_FIle**')
    else:    
        SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: 
                credentials = tools.run_flow(flow, store)
            print('Storing credentials to ' + credential_path)
        
    return credentials

if __name__ == "__main__":
    get_credentials()