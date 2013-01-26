#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import urllib2
from BeautifulSoup import BeautifulSoup
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
	
#artistNames = soup.findAll("div", attrs={'class' : re.compile("Name$")})
artistNames = soup.findAll("div", attrs={'class' : 'ArtistName'})
releaseNames = soup.findAll("div", attrs={'class' : 'ReleaseName'})
trackNames = soup.findAll("div", attrs={'class' : 'TrackName'})

f = open(OUT, "w")

for i in range(len(artistNames)):
	artistNames[i].contents[0] = bleach.clean(artistNames[i].contents[0], tags=[], strip=True)
	f.write(artistNames[i].contents[0] + '\n')
	f.write(releaseNames[i].contents[0] + '\n')
	f.write(trackNames[i].contents[0] + '\n')

f.close()