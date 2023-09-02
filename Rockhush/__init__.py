from Rockhush.core.bot import RockhushBot
from Rockhush.core.dir import dirr
from Rockhush.core.git import git
from Rockhush.core.userbot import Userbot
from Rockhush.misc import dbb, heroku, sudo

from .logging import LOGGER


dirr()

git()

dbb()

heroku()

sudo()

# Clients
app = RockhushBot()
userbot = Userbot()


from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
