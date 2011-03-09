#!/usr/bin/env python

__all__ = ['load', 'transcoder', 'json', 'yaml', 'plist']

import os

import plistlib
import json as jsonlib

########################################################################

try:
	import yaml as yamllib
except:
	pass

try:
	import bson as bsonlib
except:
	pass

try:
	import msgpack as msgpacklib
except:
	pass

try:
	import bserializer as bserializerlib
except:
	pass


########################################################################

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
	elif name == 'bson':
		return bson
	elif name == 'msgpack':
		return msgpack
	elif name == 'bs':
		return bserializer
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
	elif theExtension == 'bson':
		return bson.load(fp, *args, **kwargs)
	elif theExtension == 'bs':
		return bserializer.load(fp, *args, **kwargs)
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

########################################################################

class bson(object):
	@classmethod
	def load(cls, fp, *args, **kwargs):
		try:
			return bsonlib.load(fp, *args, **kwargs)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def loads(cls, s, *args, **kwargs):
		try:
			return bsonlib.loads(s, *args, **kwargs)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def dump(cls, obj, fp, *args, **kwargs):
		try:
			s = bsonlib.dumps(obj)
			fp.write(s)
		except Exception, e:
			raise TranscoderDumpException(e)

	@classmethod
	def dumps(cls, obj, fp):
		try:
			return bsonlib.dumps(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)

########################################################################

class msgpack(object):
	@classmethod
	def load(cls, fp, *args, **kwargs):
		try:
			return msgpacklib.load(fp, *args, **kwargs)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def loads(cls, s, *args, **kwargs):
		try:
			return msgpacklib.loads(s, *args, **kwargs)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def dump(cls, obj, fp, *args, **kwargs):
		try:
			return msgpacklib.dump(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)

	@classmethod
	def dumps(cls, obj, fp, *args, **kwargs):
		try:
			return msgpacklib.dumps(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)

########################################################################

class bserializer(object):
	@classmethod
	def load(cls, fp, *args, **kwargs):
		try:
			return bserializerlib.load(fp, *args, **kwargs)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def loads(cls, s, *args, **kwargs):
		try:
			return bserializerlib.loads(s, *args, **kwargs)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def dump(cls, obj, fp, *args, **kwargs):
		try:
			return bserializerlib.dump(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)

	@classmethod
	def dumps(cls, obj, fp, *args, **kwargs):
		try:
			return bserializerlib.dumps(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)

########################################################################
