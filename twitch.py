from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
import pprint
import os
import env

class Streamer:
    def __init__(self, name, game, viewers):
        self.name = name
        self.game = game
        self.viewers = viewers

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

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
twitch = Twitch(env.app_id, env.app_secret)
twitch.authenticate_app([])

# get ID of user
user_info = twitch.get_users(logins=[env.user])
user_id = user_info['data'][0]['id']

# target_scope = [AuthScope.BITS_READ]
# auth = UserAuthenticator(twitch, target_scope, force_verify=False)
# this will open your default browser and prompt you with the twitch verification website
# token, refresh_token = auth.authenticate()
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
names = []
games = []
viewers = []
while num_channels != 0:
    if num_channels < 100:
        live_channels = twitch.get_streams(user_id=channels)['data']
        names = list(map(lambda x: x['user_name'], live_channels))
        games = list(map(lambda x: x['game_name'], live_channels))
        viewers = list(map(lambda x: x['viewer_count'], live_channels))
        for i in range(len(names)):
            streamers.append(Streamer(names[i], games[i], viewers[i]))
        num_channels = 0
    else:
        curr_channels = channels[100:]
        live_channels = twitch.get_streams(user_id=curr_channels)['data']
        names = list(map(lambda x: x['user_name'], live_channels))
        games = list(map(lambda x: x['game_name'], live_channels))
        viewers = list(map(lambda x: x['viewer_count'], live_channels))
        for i in range(len(names)):
            streamers.append(Streamer(names[i], games[i], viewers[i]))
        channels = channels[:100]
        num_channels = num_channels - 100

streamers.sort(key=lambda x: x.viewers, reverse=True)
streamer_count = 1

for streamer in streamers:
    name = color.BOLD + streamer.name + color.END
    game = color.BOLD + streamer.game + color.END
    viewers = color.BOLD + str(streamer.viewers) + color.END

    print(str(streamer_count) + ") " + name + " is playing " + game)
    print("\t" + viewers + " viewers\n")
    streamer_count += 1

choice = input("What stream would you like to watch? (press 'x' for no choice)\n")
if choice == 'x':
    os.system('clear')
    print("okay cool")
else:
    os.system('./twitch-helper ' + streamers[int(choice)-1].name + ' &')
    os.system('clear')
    print("Stream is loading, enjoy!")
