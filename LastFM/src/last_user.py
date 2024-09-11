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
            "7day":"nos últimos sete dias",
            "1month":"no último mês",
            "12month":"no último ano",
            "overall":"no total"
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

        # list of questions already made with x artist
        # so they are 'reusable' with diff artists
        self.chosen_favs = {}

        return self.make_qstn(ammount)

    def make_qstn(self, ammount):
        # Lista de todas funções que fazem as perguntas
        questions_list = [
            self.qstn_album, self.qstn_artist, self.qstn_track, self.qstn_recent, 
            self.qstn_scrobble_ammount, self.qstn_track_ammount, self.qstn_artist_ammount, self.qstn_album_ammount,
            self.qstn_f_loved, self.qstn_l_loved, 
            self.qstn_fav_track_from, self.qstn_fav_track_from, self.qstn_fav_track_from,
            self.qstn_fav_album_from, self.qstn_fav_album_from, self.qstn_fav_album_from
            ]
        
        # TODO: smth like this
        # if self.period == "mixed":
        #     repeatable = [
        #         self.qstn_album, self.qstn_artist, self.qstn_track
        #     ]
        
        if self.api.laststats("loved") == []:
            questions_list.remove(self.qstn_f_loved)
            questions_list.remove(self.qstn_l_loved)

        if ammount > len(questions_list):
            ammount = len(questions_list)

        # A list with the itens on the list
        can_choose = list(range(len(questions_list)))

        while ammount >= 1:
            # chooses a random value in can_choose to use it as a index for the questions_list
            choosed = random.choice(can_choose)

            if self.DEBUG:
                print("attempting:", questions_list[choosed].__name__)
            # remove the already choosed item of the list
            can_choose.remove(choosed)

            # Opens the function and gets the returned values
            # TODO: make a dict of only one var and stop the need to return 'null' period for all other functions
            question, options, answer, period = questions_list[choosed]()

            if question == "":
                continue

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
            
            ammount-=1

        self.save_quiz()
        self.qstn_dict["status"] = "Quiz Criado!"

        return self.qstn_dict

    def qstn_track(self):
        period = self.get_period()
        options = self.api.topstats(type="track", limit=4, period=period)

        answer = options[0]

        question = f"Qual a música mais ouvida de {self.USERNAME} {self.PERIOD_TRANS[period]}? "

        return question, options, answer, period
    
    def qstn_artist(self):
        period = self.get_period()
        options = self.api.topstats(type="artist", limit=4, period=period)
        answer = options[0]

        question = f"Qual o artista mais ouvido de {self.USERNAME} {self.PERIOD_TRANS[period]}? "

        return question, options, answer, period
    
    def qstn_album(self):
        period = self.get_period()
        options = self.api.topstats(type="album", limit=4, period=period)
        answer = options[0]

        question = f"Qual o álbum mais ouvido de {self.USERNAME} {self.PERIOD_TRANS[period]}? "

        if period == "overall":
            question = f"Qual o álbum mais ouvido de {self.USERNAME} no total? "
        return question, options, answer, period
    
    def round_tree(self, numb:int):
        s_len = 10**(len(str(numb))-3) # numb lenght, how decimals will be saved from int
        numb = round(numb/s_len)*s_len
        return numb

    def stat_ammount(self, stat, question):
        s_ammount = int(self.api.test_user()["user"][stat])
        print(s_ammount)
        s_ammount = self.round_tree(s_ammount)
        
        s_range = list(range(round(s_ammount/1.5), round(s_ammount*1.5))) # range of questions
        
        options = [s_ammount]

        for i in range(3):
            rand_opt = random.choice(s_range)
            rand_opt = self.round_tree(rand_opt)

            if rand_opt == s_ammount:
                rand_opt = 20 # funny
                
            options.append(rand_opt)

        answer = options[0]

        return question, options, answer, "null"

    def qstn_scrobble_ammount(self):
        question = f"Quantos scrobbles {self.USERNAME} possui? (arredondado)"
        return self.stat_ammount("playcount", question)

    def qstn_track_ammount(self):
        question = f"Quantas músicas {self.USERNAME} já ouviu? (arredondado)"
        return self.stat_ammount("track_count", question)

    def qstn_artist_ammount(self):
        question = f"Quantos artistas {self.USERNAME} já ouviu? (arredondado)"
        return self.stat_ammount("artist_count", question)

    def qstn_album_ammount(self):
        question = f"Quantos albúns {self.USERNAME} já ouviu? (arredondado)"
        return self.stat_ammount("album_count", question)

    def qstn_f_loved(self):
                                            # idk why but it just bugs when asking for limit of 4 on this function 
        options = self.api.laststats(type="loved", limit=5)[:4]

        answer = options[0]

        question = f"Qual a primeira música amada por {self.USERNAME}?"
        return question, options, answer, "null"
    
    def qstn_l_loved(self):
        options = self.api.topstats(type="loved", limit=4)

        answer = options[0]

        question = f"Qual a útlima música amada por {self.USERNAME}?"
        return question, options, answer, "null"

    def qstn_recent(self):
        options = self.api.topstats(type="recent", limit=4)
        
        answer = options[0]

        question = f"Qual a última música (na data de criacao do quiz) ouvida por {self.USERNAME}?"
        return question, options, answer, "null"

    def fav_stat_fromart(self, fav_type, question):
        period = self.get_period()

        ## GETTING THE ARTIST NAMES
        # IF NOT CREATED, CREATES A DICT WITH ALL TOP ARTISTS FROM GOTTEN PERIOD
        if self.chosen_favs == {} or period not in self.chosen_favs or fav_type not in self.chosen_favs[period]:
            top_tracks_full = self.api.topstats(type=fav_type, period=period, limit=10, full=True)["stat"]
            top_tracks = [(track["name"], track["artist"]["name"]) for track in top_tracks_full]
            artist_list = list(set([track[1] for track in top_tracks]))
            
            self.chosen_favs[period] = {"artists" : artist_list, fav_type:top_tracks}
        
        # IF CREATED GETS ITS INFO
        else:
            top_tracks = self.chosen_favs[period][fav_type]
            artist_list = self.chosen_favs[period]["artists"]
        
        if self.chosen_favs[period]["artists"] != []:
            chosen_artist = random.choice(artist_list)
            self.chosen_favs[period]["artists"].remove(chosen_artist)
        else:
            return "" "" "" ""    

        ## GETS ARTIST FAVE TRACKS
        options = []
        for track in top_tracks:
            if chosen_artist in track and len(options) == 0:
                answer = track[0]
                options.append(track[0])
            elif chosen_artist in track and len(options) <= 3:
                options.append(track[0])
        
        # if didn't found 4 tracks from artist on top 10 try to find in the top 50
        if len(options) <= 4:
            all_top_tracks_full = self.api.topstats(type="track", period=period, limit=50, full=True)["stat"]
            for track in all_top_tracks_full:
                if track["artist"]["name"] == chosen_artist and track["name"] not in options:
                    options.append(track["name"])
                if len(options) >= 4:
                    break

        # if still didn't find 4 tracks on top50, grabs random tracks from the artist.
        while len(options) <= 4:
            options.append(random.choice(self.api.topstats(type="track", period=period, artist=chosen_artist)))
        self.chosen_favs[period][fav_type].append(chosen_artist)
        question += chosen_artist + " " + self.PERIOD_TRANS[period] + "?"
        return question, options, answer, "null"

    def qstn_fav_track_from(self):
        question = f"Qual musica que {self.USERNAME} mais ouviu de "
        return self.fav_stat_fromart("track", question)


    def qstn_fav_album_from(self):
        question = f"Qual album que {self.USERNAME} mais ouviu de "
        return self.fav_stat_fromart("album", question)


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
    info.get_user_info("caioempessoa", int(0), "overall")

    output = []

    for i in range(5):
        output.append(info.qstn_fav_track_from())
        output.append(info.qstn_fav_album_from())

    print("\n\n\n\n#####OUTPUT######\n")
    for i in output:
        print(i)



# TODO: ONLY REQUEST 4 OF THE TRACK (SONG ARTIST ETC)