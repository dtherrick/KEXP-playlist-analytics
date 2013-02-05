#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import boto


def daterange(start_date, end_date):
	if start_date <= end_date:
		for n in range((end_date - start_date).days + 1):
			yield start_date + datetime.timedelta(n)
	else:
		for n in range((start_date - end_date).days + 1):
			yield start_date + datetime.timedelta(n)


def create_bucket(bucket_name):
	"""
	Create a bucket.  If the bucket already exists and you have
	access to it, no error will be returned by AWS.
	Note that bucket names are global to a S3 region or location
	so you need to choose a unique name.
	"""
	LHA_AWS_ACCESS_KEY = 'AKIAJWV4X2TDHPBE5WIQ'
	LHA_AWS_SECRET_KEY = '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'

	s3 = boto.connect_s3(aws_access_key_id=LHA_AWS_ACCESS_KEY, aws_secret_access_key=LHA_AWS_SECRET_KEY)

	# First let's see if we already have a bucket of this name.
	# The lookup method will return a Bucket object if the
	# bucket exists and we have access to it or None.
	bucket = s3.lookup(bucket_name)
	if bucket:
		print 'Bucket (%s) already exists' % bucket_name
	else:
		# Let's try to create the bucket.  This will fail if
		# the bucket has already been created by someone else.
		try:
			bucket = s3.create_bucket(bucket_name)
		except s3.provider.storage_create_error, e:
			print 'Bucket (%s) is owned by another user' % bucket_name
	return bucket


def store_private_data(bucket_name, key_name, path_to_file):
	"""
	Write the contents of a local file to S3 and also store custom
	metadata with the object.

	bucket_name   The name of the S3 Bucket.
	key_name      The name of the object containing the data in S3.
	path_to_file  Fully qualified path to local file.
	"""

	LHA_AWS_ACCESS_KEY = 'AKIAJWV4X2TDHPBE5WIQ'
	LHA_AWS_SECRET_KEY = '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'
	
	s3 = boto.connect_s3(aws_access_key_id = LHA_AWS_ACCESS_KEY, aws_secret_access_key = LHA_AWS_SECRET_KEY)
	bucket = s3.lookup(bucket_name)

	# Get a new, blank Key object from the bucket.  This Key object only
	# exists locally until we actually store data in it.
	key = bucket.new_key(key_name)

    # Now, overwrite the data with the contents of the file
	key.set_contents_from_filename(path_to_file)

	return key