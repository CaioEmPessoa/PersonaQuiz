import requests
from decouple import config
from functools import lru_cache

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
                "method":"getTopAlbums",
                "name":"topalbums",
                "single":"album"
            },
            "recent":{
                "method":"getrecenttracks",
                "name":"recenttracks",
                "single":"track"
            },
            "loved":{
                "method":"getLovedTracks",
                "name":"lovedtracks",
                "single":"track"
            }
        }

        self.NAME = name

        self.API_KEY = key

        self.DEBUG = config("DEBUG")

    def request(self, type, page=1,
                limit=10, period="7day"):

        type = self.TYPE_DICT[type]

        params={"method": f"user.{type["method"]}",
                "format":"json",
                "user":self.NAME,
                "limit":limit,
                "period":period,
                "page": page,
                "api_key":self.API_KEY}


        return requests.get("https://ws.audioscrobbler.com/2.0/", params=params)

    @lru_cache
    def topstats(self, type, limit=10, period="overall", full=False):
        
        if self.DEBUG:
            print("looking for top", type)

        name = self.TYPE_DICT[type]["name"]
        single = self.TYPE_DICT[type]["single"]

        r = self.request(type=type, limit=limit, period=period)

        if r.json()[name]["@attr"]["total"] == "0":
            return []

        stat_list = r.json()[name][single]


        stat_list_org = [stat["name"] for stat in stat_list]

        if full == False:
            return stat_list_org
        else:
            return stat_list

    @lru_cache
    def laststats(self, type, limit=10, page=1, period="overall"):
        if self.DEBUG:
            print("looking for last", type)

        name = self.TYPE_DICT[type]["name"]
        single = self.TYPE_DICT[type]["single"]

        first_r = self.request(type=type, limit=limit, page=page, period=period)

        if first_r.json()[name]["@attr"]["total"] == "0":
            return []

        page = first_r.json()[name]["@attr"]["totalPages"] # go to last page
        last_limit = first_r.json()[name]["@attr"]["perPage"] # get the limit of the page to get the last item in it

        last_r = self.request(type=type, limit=last_limit, page=page, period=period)

        stat_list = last_r.json()[name][single]

        stat_list_org = [stat["name"] for stat in stat_list]
        stat_list_org[limit:] # cuts the list to the limit requested

        return stat_list_org

    def artiststats(self, name):
        # TODO: request and retrieve data from specific artist, like top tracks/albuns etc...
        pass
    
    def test_user(self):
        r = self.request("track").json()

        if "error" in r:
            raise Exception("USER NOT FOUND!!")


if __name__ == "__main__":
    from decouple import config

    API_KEY = config("LASTFM_API_KEY")
    api = LastfmApi("caioempessoa", API_KEY)

    re = api.laststats("recent", limit=10)
    print(re)