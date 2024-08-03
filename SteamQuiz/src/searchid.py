from steam_web_api import Steam
from decouple import config

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

user = steam.users.get_user_details("caioempessoa")

print(user)