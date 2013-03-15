#! /usr/bin/python
# -*- coding: utf-8 -*-

#import os
#import urllib2
#import datetime
#import calendar
#import logging
#import lha_utils
import pygn


"""
VARIABLES
"""

clientID = '2408704-C81580978847D7212FF39B94C4F65088'
userID = pygn.register(clientID)

metadata = pygn.searchTrack(clientID, userID, 'Father John Misty', 'Fear Fun', 'Hollywood Forever Cemetary Sings')

for i in metadata['genre']:
	print metadata['genre'][i]['TEXT']
