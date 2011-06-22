#!/usr/bin/env python

__all__ = ['load', 'transcoder', 'json', 'yaml', 'plist']

import os

import plistlib
import json as jsonlib
import pickle as picklelib

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

try:
	import bencode as bencodelib
except:
	pass

try:
	import biplist as biplistlib
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
	elif name == 'bencode':
		return bencode
	elif name == 'pickle':
		return bencode
	elif name == 'bplist':
		return biplist
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

class transcoder_object(object):
	@classmethod
	def load(cls, fp, *args, **kwargs):
		return cls.loads(fp.read())

	@classmethod
	def loads(cls, s, *args, **kwargs):
		raise Exception('Unimplemented')

	@classmethod
	def dump(cls, obj, fp, *args, **kwargs):
		return fp.write(cls.dumps(obj))

	@classmethod
	def dumps(cls, obj):
		raise Exception('Unimplemented')

########################################################################

class json(transcoder_object):
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
	def dumps(cls, obj):
		try:
			return jsonlib.dumps(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)

########################################################################

class yaml(transcoder_object):
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

class plist(transcoder_object):
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

class bson(transcoder_object):
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
	def dumps(cls, obj):
		try:
			return bsonlib.dumps(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)

########################################################################

class msgpack(transcoder_object):
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
	def dumps(cls, obj, *args, **kwargs):
		try:
			return msgpacklib.dumps(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)

########################################################################

class bserializer(transcoder_object):
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
	def dumps(cls, obj, *args, **kwargs):
		try:
			return bserializerlib.dumps(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)

########################################################################

class bencode(transcoder_object):
	@classmethod
	def loads(cls, s, *args, **kwargs):
		try:
			return bencodelib.bdecode(s, *args, **kwargs)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def dumps(cls, obj, *args, **kwargs):
		try:
			return bencodelib.bencode(obj)
		except Exception, e:
			raise TranscoderDumpException(e)

########################################################################

class pickle(transcoder_object):
	@classmethod
	def loads(cls, s, *args, **kwargs):
		try:
			return picklelib.loads(s, *args, **kwargs)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def dumps(cls, obj, *args, **kwargs):
		try:
			return picklelib.dumps(obj)
		except Exception, e:
			raise TranscoderDumpException(e)

########################################################################

class biplist(transcoder_object):
	@classmethod
	def load(cls, fp):
		try:
			return biplistlib.readPlist(fp)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def loads(cls, s):
		try:
			return biplistlib.readPlistFromBytes(s)
		except Exception, e:
			raise TranscoderLoadException(e)

	@classmethod
	def dump(cls, obj, fp, indent = False):
		try:
			return biplistlib.writePlist(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)

	@classmethod
	def dumps(cls, obj, fp, indent = False):
		try:
			return biplistlib.writePlistToBytes(obj, fp)
		except Exception, e:
			raise TranscoderDumpException(e)
