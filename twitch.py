from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
import pprint
import os

os.system('clear')

print("""
████████╗██╗    ██╗██╗████████╗ ██████╗██╗  ██╗       ██████╗██╗     ██╗
╚══██╔══╝██║    ██║██║╚══██╔══╝██╔════╝██║  ██║      ██╔════╝██║     ██║
   ██║   ██║ █╗ ██║██║   ██║   ██║     ███████║█████╗██║     ██║     ██║
   ██║   ██║███╗██║██║   ██║   ██║     ██╔══██║╚════╝██║     ██║     ██║
   ██║   ╚███╔███╔╝██║   ██║   ╚██████╗██║  ██║      ╚██████╗███████╗██║
   ╚═╝    ╚══╝╚══╝ ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝       ╚═════╝╚══════╝╚═╝
""")

# create instance of twitch API
twitch = Twitch('xutsqhnjyy8eghpn1hr4ltsepsfwp9', 'd0cumj14p1eg10vt6f2ftzewc0l8k8')
twitch.authenticate_app([])

# get ID of user
user_info = twitch.get_users(logins=['justeuuan'])
user_id = user_info['data'][0]['id']

target_scope = [AuthScope.BITS_READ]
auth = UserAuthenticator(twitch, target_scope, force_verify=False)
# this will open your default browser and prompt you with the twitch verification website
token, refresh_token = auth.authenticate()
# add User authentication
#twitch.set_user_authentication(token, target_scope, refresh_token)

#pprint.pprint(twitch.get_followed_streams())
#pprint.pprint(twitch.get_users_follows(from_id=user_id, first=100))

follows = twitch.get_users_follows(from_id=user_id, first=100)
total = int(follows['total'])

channels = []
for channel in follows['data']:
    channels.append(channel['to_id'])

if total > 100:
    total = total-100
else:
    total = 0

page = follows['pagination']['cursor']
while total != 0:
    if total < 100:
        follows = twitch.get_users_follows(after=page, from_id=user_id, first=total)
        total = 0
    else:
        follows = twitch.get_users_follows(after=page, from_id=user_id, first=100)
        total = total - 100
        page = follows['pagination']['cursor']
    for channel in follows['data']:
        channels.append(channel['to_id'])



#pprint.pprint(follows)

#pprint.pprint(channels)
#pprint.pprint(twitch.get_streams(user_id=channels))
num_channels = len(channels)
streamers = []
games = []
while num_channels != 0:
    if num_channels < 100:
        live_channels = twitch.get_streams(user_id=channels)['data']
        streamers.extend(list(map(lambda x: x['user_name'], live_channels)))
        games.extend(list(map(lambda x: x['game_name'], live_channels)))
        num_channels = 0
    else:
        curr_channels = channels[100:]
        live_channels = twitch.get_streams(user_id=curr_channels)['data']
        streamers.extend(list(map(lambda x: x['user_name'], live_channels)))
        games.extend(list(map(lambda x: x['game_name'], live_channels)))
        channels = channels[:100]
        num_channels = num_channels - 100


for i in range(len(streamers)):
    print(str(i+1)+ ") " + streamers[i] + " is playing " + games[i] + "\n")

choice = input("What stream would you like to watch? (press 'x' for no choice)\n")
if type(choice) != int:
    print("okay cool")
else:
    os.system('./twitch ' + streamers[int(choice)-1])
