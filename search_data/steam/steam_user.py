from steam import Steam
from decouple import config
import json
import random
import string
import os
from flask import Flask, jsonify

# STARTS FLASK APP
app = Flask(__name__)

class SteamMaker():

    def __init__(self):
        super().__init__()
        # GET STEAM API KEY FROM .ENV
        KEY = config("STEAM_API_KEY")
        self.steam = Steam(KEY)
        self.user_data_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\..\\..\\user_data"
        

    def user_data(self, username, ammount):

        # Pesquisando por ID
        print("pesquisando por id...")
        self.user = self.steam.users.search_user(username)
        # Caso não tenha encontrado
        if self.user == "No match":
            print("nome de usuário '" + username + "' não válido! Tentando busca por id...")
            
            # Tenta pegar os detalhes do usuário pelo ID
            try:
                self.user = self.steam.users.get_user_details(username)
                print(self.user["player"]["personaname"] + " encontrado!")
            
            except:
                print("Id também não válido! saindo do programa...")
                self.qstn_dict["status"] = "O link provido não é de nenhum usuário."
                return self.qstn_dict
            
        if self.user["player"]["communityvisibilitystate"] != 3:
            print("Perfil de usuário é privado!")

            self.qstn_dict["status"] = "Perfil de usuário é privado!"
            return self.qstn_dict


        # Pegar Dados User ---------------------------<
        self.id = self.user["player"]["steamid"]
        self.user = self.steam.users.get_user_details(self.id)
        self.games = self.steam.users.get_owned_games(self.id)["games"]
        self.ammount = ammount
        self.qstn_dict = {
            "status":"undefined",
            "qstn_count": 0,
            "qstn_id": "undefined",
        }
        # >--------------------------------------- END
        return self.make_qstn()

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

        print("Perguntas Salvas!")

    def make_qstn(self):

        # Lista de todas funções que fazem as perguntas
        questions_list = [self.by_recent]
        for question in range(self.ammount):
            question, options, answer = random.choice(questions_list)()
            print(question, options, answer)


            # Create a question list with the itens of the topic and shufles it
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
            print("Questão feita!")
            print(json.dumps(self.qstn_dict, indent=4))

        self.save_quiz()
        self.qstn_dict["status"] = "Quiz Criado!"
        return self.qstn_dict


    def by_hours(self):
        question = f"Qual o jogo mais jogado de {self.user['player']['personaname']}?"
        print("pergunta: " + question)
        sort_by_hours = []


        # get the list sorted by most played games
        for game in self.games:
            sort_by_hours.append([game["playtime_forever"], game["name"]])

        sort_by_hours.sort(reverse=True)
        sort_by_hours = sort_by_hours[:4]

        games_name = []
        for game_name in sort_by_hours:
            games_name.append(game_name[1])

        # the first item of the list is the right
        return question, games_name, sort_by_hours[0][1]

    def by_recent(self):
        question = f"Qual foi o último jogo jogado por {self.user['player']['personaname']}?"
        print("pergunta: " + question)

        self.recent_games = self.steam.users.get_user_recently_played_games(self.id)

        for s in self.recent_games["games"]:
            print(s["last_playtime"])

        sort_by_last = []

        for game in self.games:
            print(self.recent_games[str(game["appid"])])
            sort_by_last.append(self.recent_games[game["appid"]]["last_playtime"], game["name"])



        # get the list sorted by most played games
        for game in self.games:
            sort_by_last.append([game["rtime_last_played"], game["name"]])

        sort_by_last.sort(reverse=True)
        sort_by_last = sort_by_last[:4]

        games_name = []
        for game_name in sort_by_last:
            games_name.append(game_name[1])

        # the first item of the list is the right
        return question, games_name, sort_by_last[0][1]
    
        # the correct answer is the smallest number on "rtime_last_played", under the "games" list

    def by_money(self):
        question = f"Qual o jogo mais caro da biblioteca de {self.user['player']['personaname']}?"
        print("pergunta: " + question)

        # creating lists
        sort_by_money = []
        id_list = []

        # get a list of all games id's
        for game in self.games:
            id_list.append(str(game["appid"]))

        # make a request abt all the prices of the games
        games_price_dict = json.loads(self.steam.apps.get_app_details(",".join(id_list), "price_overview"))

        # for each game
        for game in self.games:
            
            # It tryies to found the initial price of the game, in case it has somed discount
            try:
                game_price = games_price_dict[str(game["appid"])]["data"]["price_overview"]["initial_formatted"]
                
                # If the game isn't in promotion, it gets only the final price of it
                if game_price == 0 or game_price == "":
                    game_price = games_price_dict[str(game["appid"])]["data"]["price_overview"]["final_formatted"]
                    
            except:
                # If the game isn't on the dict, it is "free"
                game_price = "R$ 0"

            if game_price == "Free":
                game_price = "R$ 0"

            # The game price comes like "R$ xx,xx" so I had to convert to "xx.xx"
            sort_by_money.append([float(game_price[3:].replace(",", ".")), game["name"]])

        sort_by_money.sort(reverse=True)
        sort_by_money = sort_by_money[:4]
        print(sort_by_money)

        games_name = []
        for game_name in sort_by_money:
            games_name.append(game_name[1])

        return question, games_name, sort_by_money[0][1]

    def by_achievements(self): # not working
        question = f"Qual o jogo com mais conquistas de {self.user['player']['personaname']}?"
        print("pergunta: " + question)

        sort_by_achievements = []
        game_achievements = self.steam.apps.get_user_achievements(self.id, 4000)

        print(game_achievements)
    
        '''   
            for game in self.games:
                print(game["name"])
                game_achievements = self.steam.apps.get_user_achievements(self.id, game["appid"])
                total_achievements = sum(1 for achievement in game_achievements['playerstats']['achievements'] if achievement['achieved'] == 1)

                sort_by_achievements.append([total_achievements, game["name"]])

            sort_by_achievements.sort(reverse=True)
            sort_by_achievements = sort_by_achievements[:5]

            print(sort_by_achievements)
        '''

    def level(self): # steam level
        print("ta bom")


@app.route("/steam_app/test")
def server_test():
    return ("sucesso!")

@app.route("/steam_app/create/<username>/<ammount>")
def start(username, ammount):
    data = jsonify(Start.user_data(username, int(ammount)))
    return data

@app.route("/steam_app/open_created/<user_id>")
def open_created(user_id):
    try:
        with open(f"{Start.user_data_location}/{user_id}.json", "r") as load_file:
            data = json.load(load_file)
            data["status"] = "Quiz Carregado!"
            return jsonify(data)
    except:
        return(jsonify({"status":"Esse quiz não existe! Verifique seu código."}))


@app.after_request
def header_apply(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] ="True"
    return response

if __name__ == "__main__":
    Start = SteamMaker()
    app.add_url_rule
    app.run(debug=True)

