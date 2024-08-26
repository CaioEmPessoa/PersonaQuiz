import json
import random
import string
import os
from decouple import config

from .last_request import LastfmApi

class UserInfo():

    def __init__(self):

        self.API_KEY = config("LASTFM_API_KEY")
        self.DEBUG = config("DEBUG")

        self.user_data_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/user_data"

        if self.DEBUG:
            print("Debugging.")

    def get_period(self):
        period = self.period
        if self.period == "mixed":
            period = random.choice(["7day", "1month", "12month", "overall"])
        return period

    def get_user_info(self, username, ammount, period):

        self.api = LastfmApi(username, self.API_KEY)
        self.USERNAME = username
        self.period = period
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
        
        print("Usuário encontrado com sucesso!")
        
        self.qstn_dict["status"] = "User Found."

        return self.make_qstn(ammount)

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
            question, options, answer, period = questions_list[choosed]()

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
                    "period": period,
                },
            }

            # updates the main dict
            self.qstn_dict.update(question_info)

            # prints and returns the result
            if self.DEBUG:
                print("Questão feita!")
                print(self.period)
                print(json.dumps(self.qstn_dict, indent=4))

        self.save_quiz()
        self.qstn_dict["status"] = "Quiz Criado!"

        return self.qstn_dict

    def qstn_track(self):
        question = f"Qual a música mais ouvida de {self.USERNAME}? "
        period = self.get_period()
        options = self.api.topstats("track", 4, period)

        answer = options[0]

        return question, options, answer, period
    
    def qstn_artist(self):
        question = f"Qual o artista mais ouvido de {self.USERNAME}? "
        period = self.get_period()
        options = self.api.topstats("artist", 4, period)
        answer = options[0]

        return question, options, answer, period
    
    def qstn_album(self):
        question = f"Qual o álbum mais ouvido de {self.USERNAME}? "
        period = self.get_period()
        options = self.api.topstats("album", 4, period)
        answer = options[0]

        return question, options, answer, period

    # TODO: maybe change this function into a separate file to use only them in all quizess
    def save_quiz(self):
        # D:\Área de Trabalho do hd\estudos\.projetos\Lastfm Quiz\user_data
        
        # abc todo + numeros
        options = string.ascii_lowercase + string.digits
        link_id = ''.join(random.choice(options) for i in range(6))
        
        data_list = os.listdir(self.user_data_location)
        
        if link_id in data_list:
            self.save_quiz()
            return
        
        self.qstn_dict["qstn_id"] = link_id
        self.qstn_dict["status"] = "Perguntas Salvas!"
        
        with open(f"{self.user_data_location}/{link_id}.json", "w") as save_file:
            json.dump(self.qstn_dict, save_file, indent=4)

        if self.DEBUG == True:
            print("Perguntas Salvas!")


if __name__ == "__main__":
    info = UserInfo("CaioEmPessoa", 10)



# TODO: ONLY REQUEST 4 OF THE TRACK (SONG ARTIST ETC)