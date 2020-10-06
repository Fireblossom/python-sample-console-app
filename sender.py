import time
import os
import requests
import pickle
from helpers import api_endpoint, sharing_link, upload_file
import pprint
import config


def get_FileModifyTime(filePath):
    t = os.path.getmtime(filePath)
    return time.time() - t 


def upload_and_share(session, filename):
    #print(f'Upload to OneDrive ------->',
    #      f'https://graph.microsoft.com/beta/me/drive/root/children/{profile_pic}/content')
    upload_response = upload_file(session, filename=filename)
    print(28*' ' + f'<Response [{upload_response.status_code}]>')
    if not upload_response.ok:
        #pprint.pprint(upload_response.json()) # show error message
        requests.get(config.SERVER_JIANG+'?text=upload出问题啦~?desp='+str(upload_response.json()))
        return

    #print('Create sharing link ------>',
    #      'https://graph.microsoft.com/beta/me/drive/items/{id}/createLink')
    response, link_url = sharing_link(session, item_id=upload_response.json()['id'])
    print(28*' ' + f'<Response [{response.status_code}]>',
          f'bytes returned: {len(response.text)}')
    if not response.ok:
        #pprint.pprint(response.json()) # show error message
        requests.get(config.SERVER_JIANG+'?text=share出问题啦~?desp='+str(response.json()))
        return

    return link_url


FILENAME = 'session.pkl'
TEAMS = "76320c2f-0059-4763-b5ec-a85a3ce68928"
CHANNEL = "19:7fc0eb9a9227433bbed0eaa5b79e5575@thread.tacv2"


def sender_service(filename):
    if get_FileModifyTime(FILENAME) >= 3600:
        requests.get(config.SERVER_JIANG+'?text=刷新tokens出问题啦~?desp='+str(r.json()))
        return
    with open(FILENAME, 'rb') as file:
        GRAPH_SESSION = pickle.load(file)

    link_url = upload_and_share(GRAPH_SESSION, filename)
    
    messages = GRAPH_SESSION.get('https://graph.microsoft.com/beta/teams/'+TEAMS+'/channels/'+CHANNEL+'/messages')
    if messages.status_code != 200:
        requests.get(config.SERVER_JIANG+'?text=读messages出问题啦~?desp='+str(messages.json()))
        return
    else:
        message_id = messages.json()['value'][0]['id']
    
    body = {"body":{"contentType":"html","content":filename + '  ' + link_url}}
    r = GRAPH_SESSION.post('https://graph.microsoft.com/beta/teams/'+TEAMS+'/channels/'+CHANNEL+'/messages/'+message_id+'/replies', data=body)
    if r.status_code >= 300:
        requests.get(config.SERVER_JIANG+'?text=发reply出问题啦~?desp='+str(r.json()))
        return
