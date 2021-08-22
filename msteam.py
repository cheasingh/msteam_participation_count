import os
from os.path import join, dirname
from dotenv import load_dotenv
from msal import PublicClientApplication
import requests
from pprint import pprint
from collections import Counter

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


app_id = os.environ.get("APP_ID")
tenant_name = os.environ.get("TENANT_NAME")
username = os.environ.get("MS_USER")
password = os.environ.get("MS_PASS")
endpoint = os.environ.get("ENDPOINT")
team_id = os.environ.get("TEAM_ID")
channel_id = os.environ.get("CHANNEL_ID")

app = PublicClientApplication(
    app_id, authority=f"https://login.microsoftonline.com/{tenant_name}")

result = None

# We now check the cache to see
# whether we already have some accounts that the end user already used to sign in before.
accounts = app.get_accounts(username=username)

if accounts:
    # If so, you could then somehow display these accounts and let end user choose
    print("Pick the account you want to use to proceed:")
    for a in accounts:
        print(a["username"])
    # Assuming the end user chose this one
    chosen = accounts[0]
    # Now let's try to find a token in cache for this account
    result = app.acquire_token_silent(["your_scope"], account=chosen)


if not result:
    # So no suitable token exists in cache. Let's get a new one from AAD.
    result = app.acquire_token_by_username_password(
        username, password, scopes=["User.ReadBasic.All", "ChannelMember.Read.All", "ChannelMessage.Read.All"])
if "access_token" in result:
    # print(result["access_token"])  # Yay!
    print('access token received!')
else:
    print(result.get("error"))
    print(result.get("error_description"))
    # You may need this when reporting a bug
    print(result.get("correlation_id"))

channel_message = requests.get(
    f'{endpoint}/{team_id}/channels/{channel_id}/messages',
    headers={'Authorization': 'Bearer ' + result["access_token"]}).json()

valid_chat = []


for i in channel_message['value']:

    if i['from'] != None:
        if i['from']['user'] != None:
            message_id = i['id']
            valid_chat.append(i['from']['user']['displayName'])
            channel_reply = requests.get(
                f'{endpoint}/{team_id}/channels/{channel_id}/messages/{message_id}/replies',
                headers={'Authorization': 'Bearer ' + result["access_token"]}).json()

            if channel_reply['@odata.count'] > 0:
                for value in channel_reply['value']:
                    if value['from'] != None:
                        # print(value['from']['user']['displayName'])
                        if value['from']['user'] != None:
                            valid_chat.append(
                                value['from']['user']['displayName'])

user_score = dict(Counter(valid_chat).items())
