import validators
import requests
import base64
from app import app

def intelixlookup(ioc):
    #Get a token
    token = get_token()
    # use Validators to redirect the IOC to the correct Intelix endpoint
    if validators.ipv4(ioc):
        u = f"https://de.api.labs.sophos.com/lookup/ips/v1/{ioc}"
    elif validators.md5(ioc):
        u = f"https://de.api.labs.sophos.com/lookup/urls/v1/{ioc}"
    elif validators.sha256(ioc):
        u = f"https://de.api.labs.sophos.com/lookup/files/v1/{ioc}"
    h = {"Authorization": f"{token}"}
    r = requests.get(u, headers=h)
    # Return the Intelix JSON
    return r.json()
    
def get_token():
    # This is lazy, the token should be stored for quicker request times. 
    creds = f"{app.config['INTELIX_CLIENT_ID']}:{app.config['INTELIX_CLIENT_SECRET']}"
    t = base64.b64encode(creds.encode("UTF-8")).decode("ascii")
    d = {'grant_type': 'client_credentials'}
    h = {'Authorization': f"Basic {t}",
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    r = requests.post('https://api.labs.sophos.com/oauth2/token', headers=h, data=d)
    r = r.json()
    return r['access_token']