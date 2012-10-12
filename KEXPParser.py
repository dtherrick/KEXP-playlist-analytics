#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import urllib2
import HTMLParser
from BeautifulSoup import BeautifulSoup


# This is the basic address of the location we've saved the IR HTML 
# Adding on the page parameter will get us from page to page.
BASE_LIST_URL = 'file:///Users/damian/Documents/Lake%20Hill%20Analytics/Code/Python/ir500-list-pages/'

# the individual file names
LIST_PAGES_SUBDIR = 'ir500-list-pages-'

# We found this by looking at the pages
# last page is 5, so need to get up to 6 for the range() function to work
LAST_PAGE_NUMBER = 6

#first do it once
i = 1
URL = BASE_LIST_URL + LIST_PAGES_SUBDIR + str(i) + '.html'

try:
	page = urllib2.urlopen(URL)
except urllib2.URLError:
	print 'Failed to fetch: ' + URL
	
try:
	soup = BeautifulSoup(page)
except HTMLParser.HTMLParseError:
	print 'Failed to parse: ' + URL
	
anchorTags = soup.findAll('a')
paraTags = soup.findAll('p')
	
for a in anchorTags:
	if a.has_key('name') :
		print a['name']
		
for p in paraTags:
	if p.has_key('class') :
		if p['class'] == 'rank' :
			print p.contents[0]
		if p['class'] == 'company_name' :
			print p.contents[0].next
		if p['class'] == 'company_category' :
			print p.contents[0]