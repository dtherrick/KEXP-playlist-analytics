#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import urllib2
from datetime import date
import calendar
import logging


# This is the basic address of KEXP's playlist. We'll add some logic to call it by year / data / time
# The final URLs will look like: "http://kexp.org/playlist/<yyyy>/<mm>/<dd>/<t><am / pm>"
# Example: "http://kexp.org/playlist/2012/10/05/8am"
BASE_LIST_URL = 'http://kexp.org/playlist/'

# create a subdirectory called 'kexp-source-playlists'
LIST_PAGES_SUBDIR = 'kexp-source-playlists'

d = os.getcwd()

if not os.path.exists(d + '/' + LIST_PAGES_SUBDIR) :
	os.mkdir(d + '/' + LIST_PAGES_SUBDIR)
	print 'Created directory: ' + d + '/' + LIST_PAGES_SUBDIR
	
os.chdir(d + '/' + LIST_PAGES_SUBDIR)

logging.basicConfig(filename = 'aLOG-' + LIST_PAGES_SUBDIR + '.txt', level=logging.INFO, filemode="w", 
	format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info("Started Page Grabs")

try :
	address = BASE_LIST_URL + '2013/1/15/8am'
	page = urllib2.urlopen(address)
	f = open(LIST_PAGES_SUBDIR + '-2013_01_05_8am.html', "w")
	f.write(page.read())
	f.close()
	logging.info(address)

except urllib2.URLError:
	logging.error(address)

logging.info("Done with Grab")