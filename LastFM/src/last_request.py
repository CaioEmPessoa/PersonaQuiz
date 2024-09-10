import requests
from decouple import config
from functools import lru_cache

class LastfmApi():
    def __init__(self, name, key):
        super().__init__()

        self.TYPE_DICT = {
            "track":{
                "method":"getTopTracks",
                "name":"toptracks",
                "single":"track"
            },
            "artist":{
                "method":"getTopArtists",
                "name":"topartists",
                "single":"artist"
            },
            "album":{
                "method":"getTopAlbums",
                "name":"topalbums",
                "single":"album"
            },
            "recent":{
                "method":"getRecentTracks",
                "name":"recenttracks",
                "single":"track"
            },
            "loved":{
                "method":"getLovedTracks",
                "name":"lovedtracks",
                "single":"track"
            },
            "info": {
                "method":"getinfo",
                "name":"user"
            }
        }

        self.NAME = name

        self.API_KEY = key

        self.DEBUG = config("DEBUG")

    def request(self, type, artist=False, page=1, limit=10, period="overall"):

        type = self.TYPE_DICT[type]

        params={"format":"json",
                "limit":limit,
                "period":period,
                "page": page,
                "api_key":self.API_KEY}

        if artist != False:
            params["artist"] = artist
            params["method"] = f"artist.{type["method"]}"
        else:
            params["user"] = self.NAME
            params["method"] = f"user.{type["method"]}"

        if self.DEBUG:
            print("request params:", params)
        return requests.get("https://ws.audioscrobbler.com/2.0/", params=params)

    @lru_cache
    def topstats(self, type, limit=10, artist=False, period="overall", full=False):
        
        if self.DEBUG:
            print("request: top", type)

        name = self.TYPE_DICT[type]["name"]
        single = self.TYPE_DICT[type]["single"]

        r = self.request(type=type, limit=limit, period=period, artist=artist).json()

        if r[name]["@attr"]["total"] == "0":
            return []

        stat_list = r[name][single]

        stat_list_org = [stat["name"] for stat in stat_list]

        if full == False:
            return stat_list_org
        else:
            return {"stat":stat_list, "ammount":r[name]["@attr"]["total"]}

    @lru_cache
    def laststats(self, type, limit=10, page=1, period="overall", artist=False):
        if self.DEBUG:
            print("request: last", type)

        name = self.TYPE_DICT[type]["name"]
        single = self.TYPE_DICT[type]["single"]

        first_r = self.request(type=type, limit=limit, page=page, period=period, artist=artist)

        if first_r.json()[name]["@attr"]["total"] == "0":
            return []

        page = first_r.json()[name]["@attr"]["totalPages"] # go to last page
        last_limit = first_r.json()[name]["@attr"]["perPage"] # get the limit of the page to get the last item in it

        last_r = self.request(type=type, limit=last_limit, page=page, period=period, artist=artist)

        stat_list = last_r.json()[name][single]

        stat_list_org = [stat["name"] for stat in stat_list]
        stat_list_org[limit:] # cuts the list to the limit requested

        stat_list_org.reverse()

        return stat_list_org
    
    def test_user(self):
        r = self.request("info").json()

        if "error" in r:
            raise Exception("USER NOT FOUND!!")
        
        return r


if __name__ == "__main__":
    from decouple import config

    API_KEY = config("LASTFM_API_KEY")
    api = LastfmApi("joansus", API_KEY)

    re = api.test_user()
    print(re)