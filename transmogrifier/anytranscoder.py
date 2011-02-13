#!/usr/bin/env python

__all__ = ['load', 'transcoder', 'json', 'yaml', 'plist', 'pyon']

import plistlib
import json as json
import yaml

import os

# def dump(obj, fp):
# 	pass

# def dumps(obj):
# 	pass

def transcoder(name):
	if name == 'json':
		return json
	elif name == 'yaml':
		return yaml
	elif name == 'plist':
		return plist
	else:
		return None


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

# def loads(s):
# 	pass

# class json(object):
# 	@classmethod
# 	def load(cls, fp):
# 		return jsonlib.load(fp)
#
# 	@classmethod
# 	def loads(cls, s):
# 		return jsonlib.loads(s)
#
# 	@classmethod
# 	def dump(cls, obj, fp):
# 		return jsonlib.dump(obj, fp)
#
# 	@classmethod
# 	def dumps(cls, obj, fp):
# 		return jsonlib.dumps(obj, fp)


class plist(object):
	@classmethod
	def load(cls, fp):
		return plistlib.readPlist(fp)

	@classmethod
	def loads(cls, s):
		return plistlib.readPlistFromBytes(s)

	@classmethod
	def dump(cls, obj, fp):
		return plistlib.writePlist(obj, fp)

	@classmethod
	def dumps(cls, obj, fp):
		return plistlib.writePlistToBytes(obj, fp)
