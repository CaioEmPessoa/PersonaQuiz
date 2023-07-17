import json
import pylast

# Read the user data json
# In the future prob will change a lot

class UserInfo():

    def get_user_info(self, username):
        try:
            # Pega o usuario na network
            user = self.network.get_user(username)
        except:
            print("Nome não encontrado!")
            pass

        print("Coletando informações...")
        

        artist_list = []
        
        for artist in user.get_top_artists()[:5]:
            artist_list.append(pylast.Artist.get_name(artist.item))



        # Coleta todas informações do usuario kk

        self.info_dict = {
            "nome":username,
            "musicas":user.get_top_tracks()[:5], #listas
            "autores":user.get_top_artists()[:5],
            "albuns":user.get_top_albums()[:5],
            "ultima":user.get_recent_tracks()[:0]
        }


        print(self.info_dict)


        

    def __init__(self):

        # Log into lasfm API
        API_KEY = "be6482f6082f20773c2fb002207e4779" 
        API_SECRET = "c42b24fc49c680db3a8575e46a8463bb"

        username = "CaioEmPessoa"
        password_hash = pylast.md5("Churrasco_02")

        self.network = pylast.LastFMNetwork(
            api_key=API_KEY,
            api_secret=API_SECRET,
            username=username,
            password_hash=password_hash,
        )

user = UserInfo()
user.get_user_info("caioempessoa")