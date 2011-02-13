#!/usr/bin/env python

__all__ = ['load', 'transcoder', 'json', 'yaml', 'plist']

import plistlib
import json as jsonlib
import yaml as yamllib

import os

class TranscoderLoadException(Exception):
	pass

class TranscoderDumpException(Exception):
	pass

########################################################################

def transcoder(name):
	if name == 'json':
		return json
	elif name == 'yaml':
		return yaml
	elif name == 'plist':
		return plist
	else:
		return None

########################################################################

def load(fp, *args, **kwargs):
	theExtension = os.path.splitext(fp.name)[1][1:]
	if theExtension == 'json':
		return json.load(fp, *args, **kwargs)
	elif theExtension == 'yaml':
		return yaml.load(fp, *args, **kwargs)
	elif theExtension == 'plist':
		return plist.load(fp, *args, **kwargs)
	elif theExtension == 'pyon':
		return pyon.load(fp, *args, **kwargs)
	else:
		raise Exception('No transcoder module for %s' % fp.name)

########################################################################

# def loads(s):
# 	pass

########################################################################

class json(object):
	@classmethod
	def load(cls, fp, *args, **kwargs):
		try:
			return jsonlib.load(fp, *args, **kwargs)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def loads(cls, s, *args, **kwargs):
		try:
			return jsonlib.loads(s, *args, **kwargs)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def dump(cls, obj, fp, *args, **kwargs):
		try:
			return jsonlib.dump(obj, fp, *args, **kwargs)
		except Exception, e:
			raise TranscoderDumpException(e)

	@classmethod
	def dumps(cls, obj, fp):
		try:
			return jsonlib.dumps(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)

########################################################################

class yaml(object):
	@classmethod
	def load(cls, fp, *args, **kwargs):
		try:
			return yamllib.load(fp, *args, **kwargs)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def loads(cls, s, *args, **kwargs):
		try:
			return yamllib.loads(s, *args, **kwargs)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def dump(cls, obj, fp, *args, **kwargs):
		try:
			return yamllib.dump(obj, fp, *args, **kwargs)
		except Exception, e:
			raise TranscoderDumpException(e)

	@classmethod
	def dumps(cls, obj, fp, *args, **kwargs):
		try:
			return yamllib.dumps(obj, fp, *args, **kwargs)
		except Exception, e:
			raise TranscoderDumpException(e)

########################################################################

class plist(object):
	@classmethod
	def load(cls, fp):
		try:
			return plistlib.readPlist(fp)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def loads(cls, s):
		try:
			return plistlib.readPlistFromBytes(s)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def dump(cls, obj, fp, indent = False):
		try:
			return plistlib.writePlist(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)

	@classmethod
	def dumps(cls, obj, fp, indent = False):
		try:
			return plistlib.writePlistToBytes(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)
