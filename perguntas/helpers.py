import json

# Read the user data json
# In the future prob will change a lot

class UserInfo():
    def __init__(self):
        super().__init__()

    def read_json(self):
        with open("userinfo.json", "r") as read_file:
            self.data = json.load(read_file)

            self.info_dict = {
                "nome":self.data["name"],
                "musicas":self.data["Musicas"], #lista
                "autores":self.data["Autores"]
            }




UserInfo.read_json(UserInfo)