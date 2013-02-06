#! /usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import bleach


# This is the basic address of the location we've saved the IR HTML
# Adding on the page parameter will get us from page to page.
BASE_LIST_URL = 'file:///Users/damian/Documents/Dropbox/Lake-Hill-Analytics/Code/Projects/KEXP/kexp-source-playlists/'

#first do it once
URL = BASE_LIST_URL + 'kexp-source-playlists-2013_01_05_8am.html'

# Name an outfile
OUT = 'kexp-playlist-output.txt'

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
