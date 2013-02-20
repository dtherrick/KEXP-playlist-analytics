#! /usr/bin/python
# -*- coding: utf-8 -*-


import os
import boto
from boto.s3.key import Key

LIST_PAGES_SUBDIR = 'kexp-source-playlists'

# Name an outfile
OUT = 'kexp-bucket-dump.txt'

LHA_AWS_ACCESS_KEY = 'AKIAJWV4X2TDHPBE5WIQ'
LHA_AWS_SECRET_KEY = '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'

bucket_name = 'lha_kexp_playlist_bucket'

"""
Start with the local directory structure
"""
d = os.getcwd()

if not os.path.exists(d + '/' + LIST_PAGES_SUBDIR):
	os.mkdir(d + '/' + LIST_PAGES_SUBDIR)
	print 'Created directory: ' + d + '/' + LIST_PAGES_SUBDIR

os.chdir(d + '/' + LIST_PAGES_SUBDIR)

# connect to the bucket
conn = boto.connect_s3(LHA_AWS_ACCESS_KEY, LHA_AWS_SECRET_KEY)

bucket = conn.get_bucket(bucket_name)
# go through the list of files

k = Key(bucket)

k.key = 'kexp-source-playlists-2013-02-01-9am.html'

k.get_contents_to_filename(OUT)
