#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import urllib2
from datetime import date, datetime
import calendar


# This is the basic address of KEXP's playlist. We'll add some logic to call it by year / data / time
# The final URLs will look like: "http://kexp.org/playlist/<yyyy>/<mm>/<dd>/<t><am / pm>"
# Example: "http://kexp.org/playlist/2012/10/05/8am"
BASE_LIST_URL = 'http://kexp.org/playlist/'

# create a subdirectory called 'ir500-list-pages'
LIST_PAGES_SUBDIR = 'kexp-source-playlists'

YEARS = (2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012)

d = os.getcwd()

if not os.path.exists(d + '/' + LIST_PAGES_SUBDIR) :
	os.mkdir(d + '/' + LIST_PAGES_SUBDIR)
	print 'Created directory: ' + d + '/' + LIST_PAGES_SUBDIR
	
os.chdir(d + '/' + LIST_PAGES_SUBDIR)

log = open('aLOG-' + LIST_PAGES_SUBDIR + '.txt', "w")

#for y in YEARS :
#	for m in range(12) :
#		for d in range(31) :
#			for t in range(6, 11) :
				# check if current date is within range (part of the month)
#				if (d + 1) <= calendar.monthrange(y, m + 1)[1] : 
					# check for day of week - only want a weekday
#					dayOfWeek = date.weekday(date(y, m + 1, d + 1))
#					if dayOfWeek <= 4 :
						# make sure we're looking at today and earlier
#						if date(y, m + 1, d + 1) <= date.today() :
#							try :
#								address = BASE_LIST_URL + str(y) + '/' + str(m + 1) + '/' + str(d + 1) + '/' + str(t) + 'am'
#								page = urllib2.urlopen(address)
#								f = open(LIST_PAGES_SUBDIR + '-' + str(date(y, m + 1, d + 1) + '.html', "w")
#								f.write(page.read())
#								f.close()
#								time.sleep(4)
#								print 'Successfully grabbed: ' + address
#								log.write(datetime.datetime.now() + ': Successfully grabbed: ' + address + '\n')

#							except urllib2.URLError:
#								print 'Failed to fetch: ' + address
#								log.write(datetime.datetime.now() + ': Failed to fetch: ' + address + '\n')

try :
	address = BASE_LIST_URL + '2012/10/9/8am'
	page = urllib2.urlopen(address)
	f = open(LIST_PAGES_SUBDIR + '-2012-10-9-8am.html' , "w")
	f.write(page.read())
	f.close()
	time.sleep(4)
	print 'Successfully grabbed: ' + address
	log.write('Successfully grabbed: ' + address + '\n')

except urllib2.URLError:
	print 'Failed to fetch: ' + address
	log.write('Failed to fetch: ' + address + '\n')

log.close()