#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib2
from bs4 import BeautifulSoup
import bleach
import lha_utils
import MySQLdb


"""
A whole bunch of string identifiers to make life a little easier
"""
# This is the basic address of the location we've saved the IR HTML
# Adding on the page parameter will get us from page to page.
BASE_LIST_URL = 'file:///Users/damian/Documents/Dropbox/Lake-Hill-Analytics/Code/Projects/KEXP/kexp-source-playlists/'
KEY_NAME = 'kexp-source-playlists-2013-02-01-9am.html'
DIR_BASE = '/Users/damian/Documents/Dropbox/Lake-Hill-Analytics/Code/Projects/KEXP/kexp-source-playlists/'

# set the main URL to grab
URL = BASE_LIST_URL + KEY_NAME

# set the bucket name for S3
BUCKET_NAME = 'lha_kexp_playlist_bucket'

# set the directory name
DIR_NAME = DIR_BASE + KEY_NAME

# Name an outfile
OUT = 'kexp-playlist-output.txt'

"""
Done setting up strings
"""

# Connect to a database
db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="hobart93", db="lha_kexp_playlist")
cursor = db.cursor()

# Get the file from S3
lha_utils.get_s3_data(BUCKET_NAME, KEY_NAME, DIR_NAME)

try:
	page = urllib2.urlopen(URL)
	print 'Grabbed: ' + URL

except urllib2.URLError:
	print 'Failed to fetch: ' + URL

try:
	soup = BeautifulSoup(page)
	print 'Made Soup'

except HTMLParser.HTMLParseError:
	print 'Failed to parse: ' + URL

"""
Grab the items we care about
There are 10 categories
"""
# Start with single items
showHost = soup.findAll("div", attrs={'class': 'ShowHost'})
airDate = soup.findAll("div", attrs={'class': 'ShowAirDate'})
showName = soup.findAll("div", attrs={'class': 'ShowName'})

# Strip tags as needed
showHost[0].contents[0] = bleach.clean(showHost[0].contents[0], tags=[], strip=True)
showName[0].contents[1] = bleach.clean(showName[0].contents[1], tags=[], strip=True)

# Now get all the ones that are in the playlist
artistNames = soup.findAll("div", attrs={'class': 'ArtistName'})
releaseNames = soup.findAll("div", attrs={'class': 'ReleaseName'})
trackNames = soup.findAll("div", attrs={'class': 'TrackName'})
airTime = soup.findAll("div", attrs={'class': 'AirDate'})
DJComments = soup.findAll("div", attrs={'class': 'CommentText'})

f = open(OUT, "w")

f.write('Host: ' + showHost[0].contents[0] + '\n')
f.write('Air Date: ' + airDate[0].contents[0] + '\n')
f.write('Show Name: ' + showName[0].contents[1] + '\n\n')

# Check if this host exists in the db already
try:
	cursor.execute("""SELECT name FROM hosts WHERE name = (%s)""", showHost[0].contents[0])
	data = cursor.fetchall()
	rows = cursor.rowcount
	print rows
	if rows > 0:
		# there is only one of this person so we should be safe to go this route.
		print 'Record already exists: ' + str(data[0][0])
	else:
		print 'Creating Data'
		try:
			cursor.execute("""INSERT INTO hosts (name) VALUES (%s)""", showHost[0].contents[0])
			db.commit()
			print 'Successfully added: ' + showHost[0].contents[0]
		except:
			db.rollback()
			print 'Failed to insert data'
except:
	print 'Failed to check properly'

for i in range(len(artistNames)):
	artistNames[i].contents[0] = bleach.clean(artistNames[i].contents[0], tags=[], strip=True)
	airTime[i].contents[0] = bleach.clean(airTime[i].contents[0], tags=[], strip=True)
	DJComments[i].contents[2] = DJComments[i].contents[2].strip('\t\n')

	f.write('Artist: ' + artistNames[i].contents[0] + '\n')
	f.write('Album: ' + releaseNames[i].contents[0] + '\n')
	f.write('Song: ' + trackNames[i].contents[0] + '\n')
	f.write('Air Time: ' + airTime[i].contents[0] + '\n')
	f.write('DJ Comment: ' + DJComments[i].contents[2] + '\n')

f.close()
os.remove(DIR_NAME)
cursor.close()
db.close()
