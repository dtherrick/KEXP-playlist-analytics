#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib2
from bs4 import BeautifulSoup
import bleach
import logging
import MySQLdb
import boto


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
os.chdir(DIR_BASE)

logging.basicConfig(
	filename='aLOG-KEXP_Parser.txt',
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
	db = MySQLdb.connect(host="lhakexpmain.c1kvj0gfryqy.us-east-1.rds.amazonaws.com", port=3306, user="lha_kexp_proof", passwd="Statesman1997", db="lhaKEXPMain")
	cursor = db.cursor()
	logging.info("Successfully connected to database")
except:
	logging.info("Failed to connect to database")

# Get the file from S3

s3 = boto.connect_s3(aws_access_key_id=LHA_AWS_ACCESS_KEY, aws_secret_access_key=LHA_AWS_SECRET_KEY)
bucket = s3.get_bucket(BUCKET_NAME)

bucket_list = bucket.list()
for l in bucket_list:
	nameFlag = False
	hostFlag = False
	airFlag = False

	key_string = str(l.key)

	# set the URL name for BeautifulSoup
	URL = BASE_LIST_URL + key_string

	# set the directory name for local file
	DIR_NAME = DIR_BASE + key_string

	try:
		l.get_contents_to_filename(DIR_NAME)
		logging.info("Successfully grabbed file: " + key_string)
	except:
		logging.info("Failed to grab: " + key_string)

	try:
		page = urllib2.urlopen(URL)
		logging.info("Grabbed: " + URL)

	except urllib2.URLError:
		logging.info("Failed to fetch: " + URL)

	try:
		soup = BeautifulSoup(page)
		logging.info("Made Soup")

	except:
		logging.info("Failed to parse: " + URL)

	"""
	Grab the items we care about
	There are 10 categories
	"""
	# Start with single items
	showHost = soup.findAll("div", attrs={'class': 'ShowHost'})
	airDate = soup.findAll("div", attrs={'class': 'ShowAirDate'})
	showName = soup.findAll("div", attrs={'class': 'ShowName'})

	try:
		if not showHost[0].contents:
			showHost[0].contents.insert(0, "No Host Provided")
		hostFlag = True
	except:
		hostFlag = False
		host = "No Host Provided"

	try:
		if not showName[0].contents:
			showName[0].contents.insert(0, "No Show Name Provided")
			showName[0].contents.insert(1, "No Show Name Provided")
		nameFlag = True
	except:
		nameFlag = False
		name = "No Show Name Provided"

	try:
		if not airDate[0].contents:
			airDate[0].contents[0] = "No Show Date Provided"
		airFlag = True
	except:
		airFlag = False
		air = "No Show Date Provided"

	# Strip tags as needed
	if hostFlag:
		showHost[0].contents[0] = bleach.clean(showHost[0].contents[0], tags=[], strip=True)

	if nameFlag:
		showName[0].contents[1] = bleach.clean(showName[0].contents[1], tags=[], strip=True)

	if airFlag:
		strippedDate = airDate[0].contents[0].split(' - ')[0]
	else:
		strippedDate = air

	# Now get all the ones that are in the playlist
	artistNames = soup.findAll("div", attrs={'class': 'ArtistName'})
	releaseNames = soup.findAll("div", attrs={'class': 'ReleaseName'})
	trackNames = soup.findAll("div", attrs={'class': 'TrackName'})
	airTime = soup.findAll("div", attrs={'class': 'AirDate'})
	DJComments = soup.findAll("div", attrs={'class': 'CommentText'})

	"""
	PARSING FINISHED, NOW WRITE TO MYSQL
	"""

	"""
	HOSTS
	"""
	try:
		if hostFlag:
			cursor.execute("""SELECT name FROM hosts WHERE name = (%s)""", showHost[0].contents[0])
		else:
			cursor.execute("""SELECT name FROM hosts WHERE name = (%s)""", host)

		data = cursor.fetchall()
		rows = cursor.rowcount
		if rows > 0:
			# there is only one of this person so we should be safe to go this route.
			logging.info("Record already exists: " + str(data[0][0]))
		else:
			logging.info("Creating Data")
			try:
				if hostFlag:
					cursor.execute("""INSERT INTO hosts (name) VALUES (%s)""", showHost[0].contents[0])
					db.commit()
					logging.info("Successfully added: " + showHost[0].contents[0])
				else:
					cursor.execute("""INSERT INTO hosts (name) VALUE (%s)""", host)
					db.commit()
					logging.info("Successfully added: " + host)
			except:
				db.rollback()
				logging.info("Failed to insert data: Hosts")
	except:
		logging.info("Data Check failed (Hosts)")

	"""
	END HOSTS
	"""

	"""
	SHOW NAME
	"""
	try:
		if nameFlag:
			cursor.execute("""SELECT name FROM shows WHERE name = (%s)""", showName[0].contents[1])
		else:
			cursor.execute("""SELECT name FROM shows WHERE name = (%s)""", name)

		data = cursor.fetchall()
		rows = cursor.rowcount
		if rows > 0:
			# there is only one of this person so we should be safe to go this route.
			logging.info("Record already exists: " + str(data[0][0]))
		else:
			logging.info("Creating Data")
			try:
				if nameFlag:
					cursor.execute("""INSERT INTO shows (name) VALUES (%s)""", showName[0].contents[1])
					db.commit()
					logging.info("Successfully added: " + showName[0].contents[1])
				else:
					cursor.execute("""INSERT INTO shows (name) VALUES (%s)""", name)
					db.commit()
					logging.info("Successfully added: " + name)

			except:
				db.rollback()
				logging.info("Failed to insert data: Show Name")
	except:
		logging.info("Data Check failed (Show Name)")

	"""
	END SHOW NAME
	"""

	for i in range(len(artistNames)):
		artistNames[i].contents[0] = bleach.clean(artistNames[i].contents[0], tags=[], strip=True)
		airTime[i].contents[0] = bleach.clean(airTime[i].contents[0], tags=[], strip=True)
#		DJComments[i].contents[2] = DJComments[i].contents[2].strip('\t\n')

		# Make sure we actually have data to populate.
		# If it doesn't exist then pop in a N/A or something similar

		if not artistNames[i].contents:
			artistNames[i].contents.insert(0, "No Artist")

		if not releaseNames[i].contents:
			releaseNames[i].contents.insert(0, "No Album")

		if not trackNames[i].contents:
			trackNames[i].contents.insert(0, "No Track")

		if not airTime[i].contents:
			airTime[i].contents.insert(0, "No AirTime")

#		if (len(DJComments[i].contents[2]) == 0):
#			DJComments[i].contents[2] = "No DJ Comment"

		"""
		ARTIST
		"""
		try:
			cursor.execute("""SELECT name FROM artist WHERE name = (%s)""", artistNames[i].contents[0])
			data = cursor.fetchall()
			rows = cursor.rowcount
			if rows > 0:
				# there is only one of this person so we should be safe to go this route.
				logging.info("Record already exists: " + str(data[0][0]))
			else:
				logging.info("Creating Data")
				try:
					cursor.execute("""INSERT INTO artist (name) VALUES (%s)""", artistNames[i].contents[0])
					db.commit()
					logging.info("Successfully added: " + artistNames[i].contents[0])
				except:
					db.rollback()
					logging.info("Failed to insert data: Artist Name")
		except:
			logging.info("Data Check failed (artist name)")

		"""
		END ARTISTS
		"""

		"""
		ALBUM
		"""
		try:
			cursor.execute("""SELECT name FROM albums WHERE name = (%s)""", releaseNames[i].contents[0])
			data = cursor.fetchall()
			rows = cursor.rowcount
			if rows > 0:
				# there is only one of this person so we should be safe to go this route.
				logging.info("Record already exists: " + str(data[0][0]))
			else:
				logging.info("Creating Data")
				try:
					cursor.execute("""INSERT INTO albums (name) VALUES (%s)""", releaseNames[i].contents[0])
					db.commit()
					logging.info("Successfully added: " + releaseNames[i].contents[0])
				except:
					db.rollback()
					logging.info("Failed to insert data: Album")
		except:
			logging.info("Data Check failed (album name)")

		"""
		END ALBUM
		"""

		"""
		SONG
		"""
		try:
			cursor.execute("""SELECT title FROM songs WHERE title = (%s)""", trackNames[i].contents[0])
			data = cursor.fetchall()
			rows = cursor.rowcount
			if rows > 0:
				# there is only one of this person so we should be safe to go this route.
				logging.info("Record already exists: " + str(data[0][0]))
			else:
				logging.info("Creating Data")
				try:
					cursor.execute("""SELECT id FROM artist WHERE name = (%s)""", artistNames[i].contents[0])
					data = cursor.fetchall()
					id_artist = data[0][0]

					cursor.execute("""SELECT id FROM albums WHERE name = (%s)""", releaseNames[i].contents[0])
					data = cursor.fetchall()
					id_album = data[0][0]

					cursor.execute("""INSERT INTO songs (title, artistID, albumID) VALUES (%s, %s, %s)""",
						(trackNames[i].contents[0], id_artist, id_album))
					db.commit()
					logging.info("Successfully added: " + trackNames[i].contents[0])
				except:
					db.rollback()
					logging.info("Failed to insert data (Song)")
		except:
			logging.info("Data Check failed (song name)")

		"""
		END SONG
		"""

		"""
		PLAYLIST
		"""
		try:
			logging.info("Starting playlist Insert: " + trackNames[i].contents[0])
			cursor.execute("""SELECT id FROM songs WHERE title = (%s)""", trackNames[i].contents[0])
			data = cursor.fetchall()
			id_song = data[0][0]

			cursor.execute("""SELECT id FROM artist WHERE name = (%s)""", artistNames[i].contents[0])
			data = cursor.fetchall()
			id_artist = data[0][0]

			cursor.execute("""SELECT id FROM albums WHERE name = (%s)""", releaseNames[i].contents[0])
			data = cursor.fetchall()
			id_album = data[0][0]

			cursor.execute("""SELECT id FROM shows WHERE name = (%s)""", showName[0].contents[1])
			data = cursor.fetchall()
			id_show = data[0][0]

			cursor.execute("""SELECT id FROM hosts WHERE name = (%s)""", showHost[0].contents[0])
			data = cursor.fetchall()
			id_host = data[0][0]

			cursor.execute("""INSERT INTO playlist (songID, artistID, albumID, hostID, showID, date, time)
				VALUES (%s, %s, %s, %s, %s, %s, %s)""",
				(id_song, id_artist, id_album, id_host, id_show, strippedDate, airTime[i].contents[0]))
			db.commit()
			logging.info("Successfully added (playlist): " + trackNames[i].contents[0])
		except:
			db.rollback()
			logging.info("Failed to insert data (playlist)")

		"""
		END PLAYLIST
		"""

	os.remove(DIR_NAME)
cursor.close()
db.close()
