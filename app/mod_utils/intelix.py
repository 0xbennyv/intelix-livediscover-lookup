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
    j = r.json()
    response = {}
    # File reponses
    if validators.sha256(ioc) or validators.md5(ioc):
        if 'reputationScore' in j:
            response['reputationScore'] = j['reputationScore']
            if j['reputationScore'] <= 19:
                response['fileReputation'] = 'Malware'
            elif j['reputationScore'] <= 29:
                response['fileReputation'] = 'PUA (potentially unwanted application)'
            elif j['reputationScore'] <= 69:
                response['fileReputation'] = 'Unknown/suspicious'
            elif j['reputationScore'] <= 100:
                response['fileReputation'] = 'Known good'
        if 'detectionName' in j:
            response['detectionName'] = j['detectionName']

    # IP reponses
    if validators.ipv4(ioc):
        if 'category' in j:
            response['category'] = j['category']
        else:
            response['category'] = 'Unknown IP Address'

        if 'ttl' in j:
            response['ttl'] = j['ttl']

    # Generic consistent repsponses
    if 'correlationId' in j:
        response['correlationId'] = j['correlationId']
    if 'requestId' in j:
        response['requestId'] = j['requestId']

    # Generic Error Handling based on reponses 
    # https://api.labs.sophos.com/doc/lookup/ips.html
    # https://api.labs.sophos.com/doc/lookup/files.html
    if 'error' in j:
        response['error'] = j['error']
    if 'message' in j:
        response['message'] = j['message']
    # Return a dict, flask will return this as JSON to the browser
    return response
    
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