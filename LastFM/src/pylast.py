import requests

class LastfmApi():
    def __init__(self, name):
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
            }
        }

        self.NAME = name

    def request(self, type, 
                limit, period):

        type = self.TYPE_DICT[type]

        params={"method": f"user.{type["method"]}",
                "format":"json",
                "user":self.NAME,
                "limit":limit,
                "period":period,
                "api_key":"9f3fa3157847ef46f91210ac5da2116d"}


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


api = LastfmApi("caioempessoa")
api.topstats("track", 5, "7day")