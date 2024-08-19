import requests

class LastfmApi():
    def __init__(self, name, key):
        super().__init__()

        self.TYPE_DICT = {
            "track":{
                "method":"gettoptracks",
                "name":"toptracks",
                "single":"track"
            },
            "artist":{
                "method":"gettopartists",
                "name":"topartists",
                "single":"artist"
            },
            "album":{
                "method":"gettopalbuns",
                "name":"topalbuns",
                "single":"album"
            },
            "recent":{
                "method":"getrecenttracks",
                "name":"recenttracks",
                "single":"track"
            }
        }

        self.NAME = name

        self.API_KEY = key

    def request(self, type, 
                limit=10, period="7day"):

        type = self.TYPE_DICT[type]

        params={"method": f"user.{type["method"]}",
                "format":"json",
                "user":self.NAME,
                "limit":limit,
                "period":period,
                "api_key":self.API_KEY}


        return requests.get("https://ws.audioscrobbler.com/2.0/", params=params)

    def topstats(self, type, limit=10, period="overall"):

        type = self.TYPE_DICT[type]
        name = type["name"]
        single = type["single"]

        r = self.request(single, limit, period)

        stat_list = r.json()[name][single]

        for stat in stat_list:
            print(stat["name"])
            # print(stat["image"][1]["#text"])
    
    def test_user(self):
        r = self.request("track").json()

        if "error" in r:
            raise Exception("USER NOT FOUND!!")


