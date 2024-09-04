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

        self.PERIOD_TRANS = {
            "7day":" sete dias",
            "1month":" um mês",
            "12month":" um ano",
            "overall":"sde o começo"
        }

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
            self.qstn_album, self.qstn_artist, self.qstn_track, self.qstn_recent, 
            self.qstn_f_loved, self.qstn_l_loved, self.qstn_fav_track_fromart
            ]
        
        if self.api.laststats("loved") == []:
            questions_list.remove(self.qstn_f_loved)
            questions_list.remove(self.qstn_l_loved)

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
        period = self.get_period()
        options = self.api.topstats("track", 4, period)

        answer = options[0]

        question = f"Qual a música mais ouvida de {self.USERNAME} no período de{self.PERIOD_TRANS[period]}? "
        return question, options, answer, period
    
    def qstn_f_loved(self):
        options = self.api.laststats("loved", 4)

        answer = options[0]

        question = f"Qual a primeira música amada por {self.USERNAME}?"
        return question, options, answer
    
    def qstn_l_loved(self):
        options = self.api.topstats("loved", 4)

        answer = options[0]

        question = f"Qual a útlima música amada por {self.USERNAME}?"
        return question, options, answer

    def qstn_recent(self):
        options = self.api.topstats("recent", 4)
        
        answer = options[0]

        question = f"Qual a última música (na data de criacao do quiz) ouvida por {self.USERNAME}?"
        return question, options, answer, "null"

    def qstn_artist(self):
        period = self.get_period()
        options = self.api.topstats("artist", 4, period)
        answer = options[0]

        question = f"Qual o artista mais ouvido de {self.USERNAME} no período de{self.PERIOD_TRANS[period]}? "
        return question, options, answer, period
    
    def qstn_album(self):
        period = self.get_period()
        options = self.api.topstats("album", 4, period)
        answer = options[0]

        question = f"Qual o álbum mais ouvido de {self.USERNAME} no período de{self.PERIOD_TRANS[period]}? "
        return question, options, answer, period

    def qstn_fav_track_fromart(self):
        period = self.get_period()
        top_tracks_full = self.api.topstats(type="track", period=period, limit=10, full=True)
        top_tracks = [(track["name"], track["artist"]["name"]) for track in top_tracks_full]
        
        chosen_artist = random.choice(top_tracks)[1]

        options = []

        for track in top_tracks:
            if chosen_artist in track and len(options) == 0:
                answer = track[0]
                options.append(track[0])
            elif chosen_artist in track and len(options) <= 3:
                options.append(track[0])
        
        # if didn't found 4 tracks from artist on top 10 try to find in the top 50
        if len(options) <= 4:
            all_top_tracks_full = self.api.topstats(type="track", period=period, limit=50, full=True)
            for track in all_top_tracks_full:
                if track["artist"]["name"] == chosen_artist and track["name"] not in options:
                    options.append(track["name"])
                if len(options) >= 4:
                    break

        # if still didn't find 4 tracks on top50, grabs random tracks from the artist.
        while len(options) <= 4:
            options.append(random.choice(self.api.topstats(type="track", period=period, artist=chosen_artist)))

        print(options)

        question = f"Qual musica que {self.USERNAME} mais gosta de {chosen_artist}? "
        return question, options, answer, "null"

    def qstn_fav_album_fromart(self):
        # this is just copy-paste from function above, could improove to be just one but I find it well organized like this.
        period = self.get_period()
        top_albuns_full = self.api.topstats(type="album", period=period, limit=10, full=True)
        top_albuns = [(album["name"], album["artist"]["name"]) for album in top_albuns_full]
        
        chosen_artist = random.choice(top_albuns)[1]

        options = []

        for album in top_albuns:
            if chosen_artist in album and len(options) == 0:
                answer = album[0]
                options.append(album[0])
            elif chosen_artist in album and len(options) <= 3:
                options.append(album[0])
        
        # if didn't found 4 albuns from artist on top 10 try to find in the top 50
        if len(options) <= 4:
            all_top_albuns_full = self.api.topstats(type="album", period=period, limit=50, full=True)
            for album in all_top_albuns_full:
                if album["artist"]["name"] == chosen_artist and album["name"] not in options:
                    options.append(album["name"])
                if len(options) >= 4:
                    break

        # if still didn't find 4 albubs on top50, grabs random albuns from the artist.
        while len(options) <= 4:
            options.append(random.choice(self.api.topstats(type="album", period=period, artist=chosen_artist)))

        print(options)

        question = f"Qual album que {self.USERNAME} mais gosta de {chosen_artist}? "

        if self.DEBUG == True:
            print(question, "\n", options)

        return question, options, answer, "null"


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
    info = UserInfo()
    info.get_user_info("caioempessoa", int(1), "overall")
    info.qstn_favfromart()



# TODO: ONLY REQUEST 4 OF THE TRACK (SONG ARTIST ETC)