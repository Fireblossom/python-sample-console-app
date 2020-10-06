import time
import pickle
import config
from adal import AuthenticationContext
import requests


def device_flow_session(ctx, client_id, renew_session=None, refresh_token=''):
    """Obtain an access token from Azure AD (via device flow) and create
    a Requests session instance ready to make authenticated calls to
    Microsoft Graph.

    client_id = Application ID for registered "Azure AD only" V1-endpoint app

    Returns Requests session object if user signed in successfully. The session
    includes the access token in an Authorization header.

    User identity must be an organizational account (ADAL does not support MSAs).
    """
    if renew_session is None:
        device_code = ctx.acquire_user_code(config.RESOURCE, client_id)

        # display user instructions
        print(device_code['message'])

        token_response = ctx.acquire_token_with_device_code(config.RESOURCE,
                                                            device_code,
                                                            client_id)
    else:
        token_response = ctx.acquire_token_with_refresh_token(refresh_token,
                                                              client_id,
                                                              config.RESOURCE)
    print(token_response['expiresOn'])
    if not token_response.get('accessToken', None):
        return None

    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {token_response["accessToken"]}',
                            'SdkVersion': 'sample-python-adal',
                            'x-client-SKU': 'sample-python-adal'})
    return session, token_response


FILENAME = 'session.pkl'
def save_session(session):
    with open(FILENAME, 'wb') as file:
        pickle.dump(session, file)
    print(time.asctime( time.localtime(time.time()) ), 'session saved.')


if __name__ == '__main__':
    ctx = AuthenticationContext(config.AUTHORITY_URL, api_version=None)
    GRAPH_SESSION = None
    response = {'refreshToken': ''}
    while True:
        GRAPH_SESSION, response = device_flow_session(ctx, config.CLIENT_ID, GRAPH_SESSION, response['refreshToken'])
        save_session(GRAPH_SESSION)
        time.sleep(3000)