#!/usr/bin/python
#
# Author    Yann Bayle
# E-mail    bayle.yann@live.fr
# License   MIT
# Created   23/02/2017
# Updated   23/02/2017
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

    satin_file = PARSER.parse_args().input_file
    isrc.validate_isrcs(satin_file, \
        PARSER.parse_args().outfile, \
        PARSER.parse_args().dir_input)
    isrc.plot_isrc_year_distribution(satin_file)
    isrc.plot_isrc_country_repartition(satin_file)
    isrc.stat(satin_file)
