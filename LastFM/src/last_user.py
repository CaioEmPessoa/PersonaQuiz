import json
import pylast

# Read the user data json
# In the future prob will change a lot

class UserInfo():

    def get_user_info(self, username, user):

        print("Coletando informações de " + username + "...")
        

        tracks_list = []
        artist_list = []
        albuns_list = []
        recent_tracks = []

        for track in user.get_top_tracks()[:5]:
            tracks_list.append(pylast.Track.get_name(track.item))

        for artist in user.get_top_artists()[:5]:
            artist_list.append(pylast.Artist.get_name(artist.item))

        for album in user.get_top_albums()[:5]:
            albuns_list.append(pylast.Album.get_name(album.item))

#       Maybe do a last played track later.
#        for track in user.get_recent_tracks()[:5]:
#            recent_tracks.append(pylast.PlayedTrack.get_name(track.item))
#

        # Coleta todas informações do usuario kk

        self.info_dict = {
            "nome":username,
            "tracks":tracks_list, #listas
            "artists":artist_list,
            "albuns":albuns_list,
            "ultima":recent_tracks
        }

        # Just to print out the data in a better way
        data = json.dumps(self.info_dict, indent=4)

        print("Informações coletadas!")


    def __init__(self):

        # Log into lasfm API
        API_KEY = "be6482f6082f20773c2fb002207e4779" 
        API_SECRET = "c42b24fc49c680db3a8575e46a8463bb"

        username = "CaioEmPessoa"
        password_hash = pylast.md5("Churrasco_02")

        self.network = pylast.LastFMNetwork(
            api_key=API_KEY,
            api_secret=API_SECRET,
            username=username,
            password_hash=password_hash,
        )
