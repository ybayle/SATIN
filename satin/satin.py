#!/usr/bin/python
#
# Author    Yann Bayle
# E-mail    bayle.yann@live.fr
# License   GNU AGPL v3
# Created   23/02/2017
# Updated   11/05/2017
# Version   1.0.0
#

"""
Description of satin.py
======================

API for SATIN database

:Example:

python satin.py

"""

import os
import json
import argparse
import requests
import isrc
import matplotlib.pyplot as plt
from lxml.html import fromstring
from wordcloud import WordCloud

def api_musixmatch(url, params):
    """Description of api_musixmatch
    Gather information about a song
    """
    resp = requests.get(url=url, params=params)
    data = resp.json()
    status_code = data["message"]["header"]["status_code"]
    if status_code == 200:
        return data
    elif status_code == 401:
        print("\tLimit reached")
        input("Press Enter to continue...")
    else:
        print("\tError : " + str(status_code))
        input("Press Enter to continue...")
    return None

def display_lyrics(lyrics_id="15953433", out_file="lyrics.csv"):
    """Description of display_lyrics

    Limitations:
    2000 Api Calls per day
    500 Lyrics display per day
    After you've reached those limit you'll get a 401 Error
    """

    url = "https://api.musixmatch.com/ws/1.1/track.lyrics.get"
    params = dict(
        apikey=os.environ["MUSIXMATCH_API_KEY"],
        track_id=lyrics_id
    )
    data = api_musixmatch(url, params)
    with open(out_file, "w") as filep:
        filep.write(data["message"]["body"]["lyrics"]["lyrics_body"])
    print("Lyrics for " + lyrics_id + " saved in " + out_file)

def api_deezer(isrc_id):
    """Description of api_deezer
    Gather info on a given track on the Deezer API.
    """
    resp = requests.get(url="https://api.deezer.com/2.0/track/isrc:" + isrc_id)
    data = resp.json()
    if "error" in data:
        print("No data available by Deezer API for ISRC " + isrc_id)
        return 0
    else:
        return data

def api_spotify(isrc_id):
    """Description of api_spotify
    Gather info on a given track on the Spotify API.
    """
    url = "https://api.spotify.com/v1/search"
    params = dict(
        q="isrc:" + isrc_id,
        type="track"
    )
    resp = requests.get(url, params)
    data = resp.json()
    if data["tracks"]["total"] == 0:
        print("No data available by Spotify API for ISRC " + isrc_id)
        return 0
    else:
        return data

def api_musicbrainz(isrc_id=None, mbid=None):
    """Description of api_musicbrainz
    Gather info on a given track on the Musicbrainz API.
    """
    if isrc_id is not None:
        url = "https://musicbrainz.org/isrc/" + isrc_id
        resp = requests.get(url)
        tree = fromstring(resp.content)
        if isrc_id in tree.findtext('.//title'):
            print("Musicbrainz has this ISRC here " + url)
        else:
            print("No data available by Musicbrainz API for ISRC " + isrc_id)
    if mbid is not None:
        url = "https://musicbrainz.org/recording/" + mbid
        resp = requests.get(url)
        tree = fromstring(resp.content)
        if "by" in tree.findtext('.//title'):
            print("Musicbrainz has this MBID here " + url)
        else:
            print("No data available by Musicbrainz API for MBID " + mbid)

def track_info(isrc_id="USWB11200587", mbid="e9c5b049-4bcd-4556-a86b-8759d1ac26fb"):
    """Description of track_info
    Look up for info on a given track on multiple API.
    """
    data = api_deezer(isrc_id)
    if data:
        deezer_fn = isrc_id + "_Deezer_info.json"
        with open(deezer_fn, "w") as filep:
            filep.write(json.dumps(data, indent=4))
        print("Deezer info found and written in file " + deezer_fn)
    data = api_spotify(isrc_id)
    if data:
        spotify_fn = isrc_id + "_Spotify_info.json"
        with open(spotify_fn, "w") as filep:
            filep.write(json.dumps(data, indent=4))
        print("Spotify info found and written in file " + spotify_fn)
    api_musicbrainz(isrc_id, mbid)

def genres_word_cloud(infilename="SATIN.csv"):
    """Description of genres_word_cloud
    Display a genre word cloud according to the genres contained in a CSV file.
    """
    genres = ""
    with open(infilename, "r") as filep:
        for line in filep:
            row = line[:-1].split(",")
            genres += row[-1].replace("_", " ")

    wordcloud = WordCloud(background_color="#FFFFFF").generate(genres)

    plt.imshow(wordcloud)
    plt.axis("off")
    # plt.show()
    plt.savefig('genres_word_cloud.png')
    plt.close()
    print("Genres word cloud image saved")

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="SATIN's API")
    PARSER.add_argument(
        "-i",
        "--input_file",
        help="input file containing all ISRCs",
        type=str,
        default="SATIN.csv",
        metavar="input_file")
    PARSER.add_argument(
        "-o",
        "--outfile",
        help="output file containing invalid ISRCs if any found",
        type=str,
        default="ISRC_invalid.txt",
        metavar="outfile")
    PARSER.add_argument(
        "-d",
        "--dir_input",
        help="input dir containing files with name corresponding to an ISRC",
        type=str,
        metavar="dir_input")

    isrc.validate_isrcs(PARSER.parse_args().input_file, \
        PARSER.parse_args().outfile, \
        PARSER.parse_args().dir_input)
    isrc.plot_isrc_year_distribution(PARSER.parse_args().input_file)
    isrc.plot_isrc_country_repartition(PARSER.parse_args().input_file)
    isrc.stat(PARSER.parse_args().input_file)
    display_lyrics()
    track_info()
    genres_word_cloud()
