#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib2
import datetime
import calendar
import logging
import lha_utils

#------------ DEFINE VARIABLES ------------------

# This is the basic address of KEXP's playlist.
# We'll add some logic to call it by year / data / time
# The final URLs will look like:
# "http://kexp.org/playlist/<yyyy>/<mm>/<dd>/<t><am / pm>"
# Example: "http://kexp.org/playlist/2012/10/05/8am"
BASE_LIST_URL = 'http://kexp.org/playlist/'

# create a subdirectory called 'kexp-source-playlists'
LIST_PAGES_SUBDIR = 'kexp-source-playlists'

# set the bucket name for S3
BUCKET_NAME = 'lha_kexp_playlist_bucket'

timerange = ["6am", "7am", "8am", "9am"]

#----------- END VARIABLE DEFINITIONS -----------

#----------- DO THE WORK ------------------------

"""
Start with the local directory structure
"""
d = os.getcwd()

if not os.path.exists(d + '/' + LIST_PAGES_SUBDIR):
	os.mkdir(d + '/' + LIST_PAGES_SUBDIR)
	print 'Created directory: ' + d + '/' + LIST_PAGES_SUBDIR

os.chdir(d + '/' + LIST_PAGES_SUBDIR)

# reset d variable to the new directory
d = os.getcwd()

"""
Confirm that S3 Bucket is set up
"""
kexp_bucket = lha_utils.create_bucket(BUCKET_NAME)

logging.basicConfig(
	filename='aLOG-' + LIST_PAGES_SUBDIR + '.txt',
	level=logging.INFO,
	filemode="w",
	format='%(levelname)s %(asctime)s %(message)s',
	datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info("Started Page Grabs")

start = datetime.date(year=2013, month=1, day=1)
end = datetime.date(year=2013, month=1, day=1)
#end = datetime.date.today()

for date in lha_utils.daterange(start, end):
	if (date.day) <= calendar.monthrange(date.year, date.month)[1]:
		if date.weekday() <= 4:
			for t in timerange:
				try:
					address = BASE_LIST_URL + str(date.year) + '/' + str(date.month) + '/' + str(date.day) + '/' + t
					fname = LIST_PAGES_SUBDIR + '-' + str(date) + '-' + t + '.html'
					pathname = d + '/' + fname
					page = urllib2.urlopen(address)
#					f = open(fname, "w")
#					f.write(page.read())
#					f.close()
#					lha_utils.store_private_data(BUCKET_NAME, fname, pathname)
#					time.sleep(4)
					logging.info(address + ": OK")

				except urllib2.URLError:
					logging.error(address)

logging.info("Done with Grab")
