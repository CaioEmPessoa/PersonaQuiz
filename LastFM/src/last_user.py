import json
import random

from decouple import config

from last_request import LastfmApi

class UserInfo():

    def __init__(self, username):

        # Log into lasfm API
        API_KEY = config("LASTFM_API_KEY")
        self.DEBUG = config("DEBUG")

        self.USERNAME = username

        self.api = LastfmApi(username, API_KEY)

        
        self.get_user_info()

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

        if self.DEBUG:
            print(data)

        self.qstn_dict["status"] = "Got Info."

    def make_qstn(self, ammount):

        # Lista de todas funções que fazem as perguntas
        questions_list = [
            self.qstn_album, self.qstn_artist, self.qstn_track
            ]
        
        if ammount > len(questions_list):
            ammount = len(questions_list)

        # A list with the itens on the list
        can_choose = list(range(len(questions_list)))

        for question in range(ammount):
            # chooses a random value in can_choose to use it as a index for the questions_list
            choosed = random.choice(can_choose)

            # remove the already choosed item of the list
            can_choose.remove(choosed)

            # Opens the function and gets the returned values
            question, options, answer = questions_list[choosed]()

            # Shuffles the options of the quiz
            random.shuffle(options)

            # add a number to the questions made
            self.qstn_dict["qstn_count"] += 1

            # make a dict about the question being made
            question_info = {
                "Question " + str(self.qstn_dict["qstn_count"]): {
                    "question": question,
                    "options": options,
                    "answer": answer,
                },
            }

            # updates the main dict
            self.qstn_dict.update(question_info)

            # prints and returns the result
            if self.DEBUG:
                print("Questão feita!")
                print(json.dumps(self.qstn_dict, indent=4))

        # self.save_quiz()
        self.qstn_dict["status"] = "Quiz Criado!"
        return self.qstn_dict

    def qstn_track(self):
        question = f"Qual a música mais ouvida de {self.info_dict['name']}? "
        options = self.info_dict["tracks"]
        answer = options[0]

        return question, options, answer
    
    def qstn_artist(self):
        question = f"Qual o artista mais ouvido de {self.info_dict['name']}? "
        options = self.info_dict["artists"]
        answer = options[0]

        return question, options, answer
    
    def qstn_album(self):
        question = f"Qual o álbum mais ouvido de {self.info_dict['name']}? "
        options = self.info_dict["albuns"]
        answer = options[0]

        return question, options, answer




info = UserInfo("CaioEmPessoa")

info.make_qstn(10)
