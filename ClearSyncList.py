"""
Python script to populate a playlist to sync down to a device.
The playlist contains the first episode of each show in the TV section.
Shows specified in ExludeShows are not added to the playlist.
"""
from plexapi.server import PlexServer
#from plexapi.myplex import MyPlexAccount
import ConfigParser

# plex = PlexServer()


baseurl = 'http://192.168.2.50:32400'
token = 'zbv7hDnHEV2aGKRmQsRd'
plex = PlexServer(baseurl, token)
Config = ConfigParser.ConfigParser()
playlistName = ''

Config.read('CreateSyncList.cfg')

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

playlistName = ConfigSectionMap('General')['playlistname']

if playlistName == '':
    print ("No playlist specified. Please add PlaylistName under [General] in CreateSyncList.cfg")
    exit()


Playlist = plex.playlist(playlistName)

# Check for the last show in the playlist and start adding episodes after that.
# We don't want to transcode and sync those again
for episode in Playlist.items():
    showName = episode.grandparentTitle
    if episode.isWatched:
        print '{} S{}E{} - {} - removed from playlist {}'.format(showName,  episode.seasonNumber.zfill(2),
                                                               episode.index.zfill(2), episode.title, playlistName)
        Playlist.removeItem(episode)


