#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygn
import logging
import MySQLdb


"""
A whole bunch of string identifiers to make life a little easier
"""
# This is the basic address of the location we've saved the IR HTML
# Adding on the page parameter will get us from page to page.
BASE_LIST_URL = 'file:///home/ec2-user/kexp-project/'
DIR_BASE = '/home/ec2-user/kexp-project/'

LHA_AWS_ACCESS_KEY = 'AKIAJWV4X2TDHPBE5WIQ'
LHA_AWS_SECRET_KEY = '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'

# set the bucket name for S3
BUCKET_NAME = 'lha_kexp_playlist_bucket'
"""
Done setting up strings
"""

"""
SET UP LOG
"""
logging.basicConfig(
	filename='aLOG-KEXP_Gracenote.txt',
	level=logging.INFO,
	filemode="w",
	format='%(levelname)s %(asctime)s %(message)s',
	datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info("Started Page Grabs")

"""
LOG SETUP COMPLETE
"""

# Connect to a database
try:
	db = MySQLdb.connect(host="lhakexpmaster.c1kvj0gfryqy.us-east-1.rds.amazonaws.com", port=3306, user="lha_kexp_proof", passwd="Statesman1997", db="lhaKEXPMaster")
	cursor = db.cursor()
	logging.info("Successfully connected to database")
except:
	logging.info("Failed to connect to database")

"""
VARIABLES
"""

clientID = '2408704-C81580978847D7212FF39B94C4F65088'
userID = pygn.register(clientID)

metadata = pygn.searchTrack(clientID, userID, 'Father John Misty', 'Fear Fun', 'Hollywood Forever Cemetary Sings')

print metadata['track_title']

for i in metadata['mood']:
	print metadata['mood'][i]['TEXT']
	
for i in metadata['genre']:
	print metadata['genre'][i]['TEXT']

cursor.close()
db.close()