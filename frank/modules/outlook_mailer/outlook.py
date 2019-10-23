from pyOutlook import OutlookAccount

from urllib.parse import quote, urlencode
from requests_oauthlib import OAuth2Session
from O365 import Account
import base64
import json
import time

# Client ID and secret
client_id = 'e8f4dbda-ae98-4d20-9165-ecd6681c7fa2E'
client_secret = 'C7ZlW@PmXsemCByQhKlwu1eEwFt17:-?'

account = Account(credentials=(client_id, client_secret))
result = account.authenticate(scopes=['basic', 'message_all'])  # request a token for this scopes
print(result)

# credentials = (client_id, client_secret)
# account = Account(credentials)
# m = account.new_message()
# m.to.add('michael.deboeure@gmail.com')
# m.subject = 'Testing!'
# m.body = "George Best quote: I've stopped drinking, but only while I'm asleep."
# m.send()

# # Constant strings for OAuth2 flow
# # The OAuth authority
# authority = 'https://login.microsoftonline.com'

# # The authorize URL that initiates the OAuth2 client credential flow for admin consent
# authorize_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/authorize?{0}')

# # The token issuing endpoint
# token_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/token')

# authorization_base_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
# token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
# scope = ['https://outlook.office.com/calendars.readwrite']
# redirect_uri = 'https://localhost/'     # Should match Site URL

# outlook = OAuth2Session(client_id,scope=scope,redirect_uri=redirect_uri)

# # Redirect  the user owner to the OAuth provider (i.e. Outlook) using an URL with a few key OAuth parameters.
# authorization_url, state = outlook.authorization_url(authorization_base_url)
# print('Please go here and authorize,', authorization_url)

# # Get the authorization verifier code from the callback url
# redirect_response = 'https://localhost/' 

# # Fetch the access token
# token = outlook.fetch_token(token_url,client_secret=client_secret,authorization_response=redirect_response)
# print(token)

# # Fetch a protected resource, i.e. calendar information
# #o = outlook.get('https://outlook.office.com/api/v1.0/me/calendars')
# #print o.content

# # The scopes required by the app
# scopes = [ 'openid',
#            'User.Read',
#            'Mail.Read' ]

# def get_signin_url(redirect_uri):
#     # Build the query parameters for the signin url
#     params = { 'client_id': client_id,
#                 'redirect_uri': redirect_uri,
#                 'response_type': 'code',
#                 'scope': ' '.join(str(i) for i in scopes)
#             }

#     signin_url = authorize_url.format(urlencode(params))

#     return signin_url

# account = OutlookAccount("C7ZlW@PmXsemCByQhKlwu1eEwFt17:-?")
# inbox = account.inbox()
# print(inbox[0].body)
