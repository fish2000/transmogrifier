#!/usr/bin/env python

import commands
import datetime
import glob
import logging
import optparse
import os
import pkg_resources
import plistlib
import pprint
import re
import subprocess
import sys
import tempfile
import argparse
import json
import yaml

import types
import Foundation
import anytranscoder

logging.basicConfig(level = logging.DEBUG, format = '%(message)s', stream = sys.stderr)
logger = logging.getLogger()

class InputException(Exception):
	pass

def cleanup(s):
	lines = s.splitlines()
	lines = [line.rstrip() for line in lines]
	lines = [line.expandtabs() for line in lines]
	s = '\n'.join(lines) + '\n'
	return s

def parse_args(args):
	def store_open_file(option, opt_str, value, parser, *args, **kwargs):
		if value == '-':
			theFile = option.default
		else:
			theFile = file(value, kwargs['mode'])
		setattr(parser.values, option.dest, theFile)

	####################################################################

	argparser = argparse.ArgumentParser()
	argparser.add_argument('-i', '--input', action='store', dest='input', type=argparse.FileType(), default = None, metavar='INPUT',
		help='The input file (type is inferred by file extension).')
	argparser.add_argument('--input-type', action='store', dest='input_type', type=str, metavar='INPUT_TYPE',
		help='The input file type (overides file extension if any).')
	argparser.add_argument('-o', '--output', action='store', dest='output', type=argparse.FileType('w'), default = None, metavar='OUTPUT',
		help='Output directory for generated files.')
	argparser.add_argument('--output-type', action='store', dest='output_type', type=str, metavar='INPUT_TYPE',
		help='The output file type (overides file extension if any).')

	argparser.add_argument('-v', '--verbose', action='store_const', dest='loglevel', const=logging.INFO, default=logging.WARNING,
		help='set the log level to INFO')
	argparser.add_argument('--loglevel', action='store', dest='loglevel', type=int,
		help='set the log level, 0 = no log, 10+ = level of logging')
	argparser.add_argument('--logfile', dest='logstream', type = argparse.FileType('w'), default = sys.stderr, action="store", metavar='LOG_FILE',
		help='File to log messages to. If - or not provided then stdout is used.')

	argparser.add_argument('args', nargs='*')

	theOptions = argparser.parse_args(args = args[1:])

	if not theOptions.input and theOptions.args:
		theOptions.input = file(theOptions.args.pop(0))

	if not theOptions.output and theOptions.args:
		theOptions.output = file(theOptions.args.pop(0), 'w')

	if not theOptions.input:
		theOptions.input = sys.stdin
#
	if not theOptions.output:
		theOptions.output = sys.stdout

	if not theOptions.input_type:
		theOptions.input_type = os.path.splitext(theOptions.input.name)[1][1:]

	if not theOptions.output_type:
		theOptions.output_type = os.path.splitext(theOptions.output.name)[1][1:]

	print theOptions

	return theOptions

def main(args):
	theOptions = parse_args(args)

	for theHandler in logger.handlers:
		logger.removeHandler(theHandler)

#	logger.setLevel(theOptions.loglevel)
	logger.setLevel(logging.DEBUG)

	theHandler = logging.StreamHandler(theOptions.logstream)
	logger.addHandler(theHandler)

	####################################################################

#	logger.debug(theOptions)

	try:
		transmogrifier(theOptions)
	except Exception, e:
		raise
# 		logger.error('Error: %s' % e.args)
#
# 		argparser.print_help();
#
# 		sys.exit(1)

	####################################################################

def purify(o):
	if type(o) is types.UnicodeType:
		try:
			o = o.encode("utf-8")
		except:
			pass
	elif type(o) is types.DictType:
		o = dict([(purify(k), purify(v)) for k, v in o.items()])
	elif type(o) is types.ListType:
		o = [purify(v) for v in o]
	elif hasattr(o, 'items'):
		o = dict([(purify(k), purify(v)) for k, v in o.items()])
	return o

	####################################################################


def transmogrifier(options):
	theDecoder = anytranscoder.transcoder(options.input_type)
	o = theDecoder.load(options.input)
	o = purify(o)


	theEncoder = anytranscoder.transcoder(options.output_type)
	theEncoder.dump(o, options.output)
#
# 	theOutputExtension = os.path.splitext(options.output)[1][1:]
# 	if theOutputExtension == 'plist':
# 		plistlib.writePlist(o, options.output)
# 	elif theOutputExtension == 'json':
# 		json.dump(o, file(options.output, 'w'))
# 	elif theOutputExtension == 'yaml':
# #		yaml.dump(o, file(options.output, 'w'), canonical=True)
# #		yaml.dump(o, file(options.output, 'w'), default_flow_style=True, default_style='"')
# 		yaml.dump(o, file(options.output, 'w'), allow_unicode = True)


if __name__ == '__main__':
	os.chdir(os.path.expanduser('/Users/schwa/Desktop/transmogrifier/Test Data'))
 	main('transmogrifier -i Test.json -o Test.pyon'.split(' '))
# 	main('transmogrifier'.split(' '))
# 	main('transmogrifier -i Test.plist --output-type json'.split(' '))
#  	main('transmogrifier Test.yaml Test.json'.split(' '))
#  	main('transmogrifier --input-type=json Test.json Test.yaml'.split(' '))
#  	main('transmogrifier --input-type=yaml Test.json Test.yaml'.split(' '))
# 	main('transmogrifier Test.json Test.yaml'.split(' '))
