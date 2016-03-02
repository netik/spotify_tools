#!/usr/bin/python
# Adds tracks to a playlist

import csv
import os
import pprint
import spotipy
import spotipy.util as util
import sys

def search(search_str): 
  # get a track id
  sp = spotipy.Spotify()
  results = sp.search(search_str)

  if len(results['tracks']['items']) > 0:
    return results['tracks']['items'][0]['id']
  else:
    return None

#  pprint.pprint(result)
if len(sys.argv) > 1:
    username = sys.argv[1]
    csvfilename = sys.argv[2]
    playlist_id = None

    try: 
      playlist_id = sys.argv[3]
    except IndexError:
      pass

else:
    print("Usage: %s username csvfilename" % (sys.argv[0],))
    print("       or, %s username csvfilename playlistID" % (sys.argv[0],))
    sys.exit()

# get auth if we need it, this is jank.
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False

    # create or update a playlist...
    if playlist_id == None:
      playlists = sp.user_playlist_create(username, os.path.basename(csvfilename))
      pprint.pprint(playlists)
      playlist_id = playlists['id']

    # for line in file
    with open(csvfilename, 'r') as csvfile:
      csvreader = csv.DictReader(csvfile)

      for row in csvreader:
        searchterm = row['artist'] + " - " + row['title']
        print "search: %s" % searchterm

        # search
        res_id = search(searchterm);
        
        if res_id: 
          # add 
          results = sp.user_playlist_add_tracks(username, playlist_id, [res_id])
          print(results)
        else:
          print "Couldn't find it!"

else:
    print("Can't get token for", username)

