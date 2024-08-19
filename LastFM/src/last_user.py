import json
import random

from decouple import config

class UserInfo():

    def get_user_info(self, username):

        self.qstn_dict = {
            "status":"undefined",
            "qstn_count": 0,
            "qstn_id": "undefined",
        }

        print("Coletando informações de " + username + "...")
        user = self.network.get_user(username)
        
        try:
            print("procurando usuario..")
            user.get_top_tracks()
        except:
            print("Usuário não encontrado!")
            self.qstn_dict["status"] = "Usuário não encontrado ou sem nenhuma música reproduzida!"
            return
        
        print("Usuário encontrado com sucesso! Buscando informações ...")

        tracks_list = []
        artist_list = []
        albuns_list = []
        recent_tracks = []

        for track in user.get_top_tracks()[:8]:
            tracks_list.append("pylast.Track.get_name(track.item)")

        for artist in user.get_top_artists()[:8]:
            artist_list.append("pylast.Artist.get_name(artist.item)")

        for album in user.get_top_albums()[:8]:
            albuns_list.append("pylast.Album.get_name(album.item)")


        self.info_dict = {
            "nome":username,
            "tracks":tracks_list, #listas
            "artists":artist_list,
            "albuns":albuns_list,
            "ultima":recent_tracks
        }

        # Just to print out the data in a better way
        data = json.dumps(self.info_dict, indent=4)

        print("Informações coletadas!")

        print(data)

    def qstn_track(self):
        question = f"Qual a música mais ouvida de {self.info_dict['name']}? "
        options = self.info_dict["tracks"][4]
        answer = options[0]
        options = random.shuffle(self.info_dict["tracks"][4])

        return question, options, answer
    
    def qstn_track(self):
        question = f"Qual o artista mais ouvido de {self.info_dict['name']}? "
        options = self.info_dict["artists"][4]
        answer = options[0]
        options = random.shuffle(self.info_dict["artists"][4])

        return question, options, answer
    
    def qstn_track(self):
        question = f"Qual o álbum mais ouvido de {self.info_dict['name']}? "
        options = self.info_dict["albuns"][4]
        answer = options[0]
        options = random.shuffle(self.info_dict["albuns"][4])

        return question, options, answer

    def __init__(self, username):

        # Log into lasfm API
        API_KEY = config("LASTFM_API_KEY")
        API_SECRET = config("LAST_FM_API_SECRET") 

        self.get_user_info(username)

UserInfo("CaioEmPessoa")