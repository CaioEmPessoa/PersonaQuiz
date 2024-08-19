import json
import random

from decouple import config

from last_request import LastfmApi

class UserInfo():

    def __init__(self, username):

        # Log into lasfm API
        API_KEY = config("LASTFM_API_KEY")

        self.USERNAME = username

        self.api = LastfmApi(username, API_KEY)

    def get_user_info(self):

        self.qstn_dict = {
            "status":"undefined",
            "qstn_count": 0,
            "qstn_id": "undefined",
        }
        
        try:
            print("procurando usuario..")
            self.api.test_user()
        except:
            print("Usuário não encontrado!")
            self.qstn_dict["status"] = "Usuário não encontrado ou sem nenhuma música reproduzida!"
            return
        
        print("Usuário encontrado com sucesso! Buscando informações ...")

        tracks_list = self.api.topstats("track", 5)
        artist_list = self.api.topstats("artist", 5)
        albuns_list = self.api.topstats("album", 5)
        recent_tracks = self.api.topstats("recent", 5)

        self.info_dict = {
            "name":self.USERNAME,
            "tracks":tracks_list, #listas
            "artists":artist_list,
            "albuns":albuns_list,
            "recent":recent_tracks
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



UserInfo("CaioEmPessoa").get_user_info()