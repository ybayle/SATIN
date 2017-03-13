#!/usr/bin/python
#
# Author    Yann Bayle
# E-mail    bayle.yann@live.fr
# License   MIT
# Created   23/02/2017
# Updated   27/02/2017
# Version   1.0.0
#

"""
Description of satin.py
======================

API for SATIN database

:Example:

python satin.py

"""

import re
import os
import sys
import csv
import argparse
from datetime import date
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import isrc
import requests
import pprint
from lxml.html import fromstring
import string
import json
from wordcloud import WordCloud

def compare_results(groundtruths_file, dir_pred):
    """Description of compare_results

    groundtruths_file: path to file containing the ground truths and identifiers
    dir_pred: directory containing one prediction file per algorithm
    """
    utils.print_success("Comparing results")
    predictions_files = os.listdir(dir_pred)
    gts = read_item_tag(groundtruths_file)
    for pred_file in predictions_files:
        algo_name = pred_file.split("/")[-1][:-4]
        utils.print_info(algo_name)
        test_groundtruths = []
        predictions = []
        with open(dir_pred + pred_file, "r") as filep:
            for line in filep:
                row = line[:-1].split(",")
                isrc = row[0]
                if isrc in gts:
                    test_groundtruths.append(gts[isrc]) 
                    predictions.append(float(row[1]))
        
        print("Accuracy : " + str(accuracy_score(test_groundtruths, predictions)))
        print("F-score  : " + str(f1_score(test_groundtruths, predictions, average="weighted")))
        print("Precision: " + str(precision_score(test_groundtruths, predictions, average=None)))
        print("Recall   : " + str(recall_score(test_groundtruths, predictions, average=None)))
        print("F-score " + str(f1_score(test_groundtruths, predictions, average=None)))

def api_musixmatch(url, params):
    resp = requests.get(url=url, params=params)
    data = resp.json()
    statusCode = data["message"]["header"]["status_code"]
    if statusCode == 200 :
        return data
    elif statusCode == 401 :
        print("\tLimit reached")
        input("Press Enter to continue...")
    else :
        print("\tError : " + str(statusCode))
        input("Press Enter to continue...")
    return null

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
    print("Lyrics saved in " + out_file)

def api_deezer(isrc):
    resp = requests.get(url="https://api.deezer.com/2.0/track/isrc:" + isrc)
    data = resp.json()
    if "error" in data:
        print("No data available by Deezer API for ISRC " + isrc)
        return 0
    else:
        return data

def api_spotify(isrc):
    url = "https://api.spotify.com/v1/search"
    params = dict(
        q="isrc:" + isrc,
        type="track"
    )
    resp = requests.get(url, params)
    data = resp.json()
    if data["tracks"]["total"] == 0:
        print("No data available by Spotify API for ISRC " + isrc)
        return 0
    else:
        return data

import re

def api_musicbrainz(isrc=None, mbid=None):
    if isrc is not None:
        url = "https://musicbrainz.org/isrc/" + isrc
        resp = requests.get(url)
        tree = fromstring(resp.content)
        if isrc in tree.findtext('.//title'):
            print("Musicbrainz has this ISRC here " + url)
        else:
            print("No data available by Musicbrainz API for ISRC " + isrc)
    if mbid is not None:
        url = "https://musicbrainz.org/recording/" + mbid
        resp = requests.get(url)
        tree = fromstring(resp.content)
        if "by" in tree.findtext('.//title'):
            print("Musicbrainz has this MBID here " + url)
        else:
            print("No data available by Musicbrainz API for MBID " + mbid)

def track_info(isrc="USWB11200587", mbid="e9c5b049-4bcd-4556-a86b-8759d1ac26fb"):
    data = api_deezer(isrc)
    if data:
        deezer_fn = isrc + "_Deezer_info.json"
        with open(deezer_fn, "w") as filep:
            filep.write(json.dumps(data, indent=4))
        print("Deezer info found and written in file " + deezer_fn)
    data = api_spotify(isrc)
    if data:
        spotify_fn = isrc + "_Spotify_info.json"
        with open(spotify_fn, "w") as filep:
            filep.write(json.dumps(data, indent=4))
        print("Spotify info found and written in file " + spotify_fn)
    api_musicbrainz(isrc, mbid)

def genres_word_cloud(infilename="SATIN.csv"):
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

    # satin_file = PARSER.parse_args().input_file
    # isrc.validate_isrcs(satin_file, \
    #     PARSER.parse_args().outfile, \
    #     PARSER.parse_args().dir_input)
    # isrc.plot_isrc_year_distribution(satin_file)
    # isrc.plot_isrc_country_repartition(satin_file)
    # isrc.stat(satin_file)
    # display_lyrics()
    # track_info(isrc="USWB11200587", mbid="e9c5b049-4bcd-4556-a86b-8759d1ac26fb")
    genres_word_cloud()
