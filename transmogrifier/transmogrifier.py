#!/usr/bin/env python

import glob
import logging
import os
import sys
import types

# argparse was added in Python 3.2 - for earlier Pythons just install it manually (easy_install argparse)
import argparse

import anytranscoder

logging.basicConfig(level = logging.DEBUG, format = '%(message)s', stream = sys.stderr)
logger = logging.getLogger()

########################################################################

class InputException(Exception):
	pass

def cleanup(s):
	lines = s.splitlines()
	lines = [line.rstrip() for line in lines]
	lines = [line.expandtabs() for line in lines]
	s = '\n'.join(lines) + '\n'
	return s

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

########################################################################

class Transmogrifier(object):

	def __init__(self):
		self._argparser = None

	@property
	def argparser(self):
		if not self._argparser:
			argparser = argparse.ArgumentParser()
			argparser.add_argument('-i', '--input', action='store', dest='input', type=argparse.FileType(), default = None, metavar='INPUT',
				help='The input file (type is inferred by file extension).')
			argparser.add_argument('--input-type', action='store', dest='input_type', type=str, metavar='INPUT_TYPE',
				help='The input file type (overides file extension if any).')
			argparser.add_argument('-o', '--output', action='store', dest='output', type=argparse.FileType('w'), default = None, metavar='OUTPUT',
				help='Output directory for generated files.')
			argparser.add_argument('--output-type', action='store', dest='output_type', type=str, metavar='INPUT_TYPE',
				help='The output file type (overides file extension if any).')
			argparser.add_argument('--pretty', action='store_const', const=True, default=False, metavar='PRETTY',
				help='Prettify the output (where possible).')

			argparser.add_argument('-v', '--verbose', action='store_const', dest='loglevel', const=logging.INFO, default=logging.WARNING,
				help='set the log level to INFO')
			argparser.add_argument('--loglevel', action='store', dest='loglevel', type=int,
				help='set the log level, 0 = no log, 10+ = level of logging')
			argparser.add_argument('--logfile', dest='logstream', type = argparse.FileType('w'), default = sys.stderr, action="store", metavar='LOG_FILE',
				help='File to log messages to. If - or not provided then stdout is used.')

			argparser.add_argument('args', nargs='*')
			self._argparser = argparser
		return self._argparser

	def parse(self, args):

		theOptions = self.argparser.parse_args(args = args)

		if theOptions.args == list('transmogrifier'):
			theOptions.args = []

		if not theOptions.input and theOptions.args:
			theFile = theOptions.args.pop(0)
			if not os.path.exists(theFile):
				raise InputException('No file at path')
			theOptions.input = file(theFile)

		if not theOptions.output and theOptions.args:
			theFile = theOptions.args.pop(0)
			theOptions.output = file(theFile, 'w')

		if not theOptions.input:
			theOptions.input = sys.stdin
	#
		if not theOptions.output:
			theOptions.output = sys.stdout

		if not theOptions.input_type:
			theOptions.input_type = os.path.splitext(theOptions.input.name)[1][1:]

		if not theOptions.output_type:
			theOptions.output_type = os.path.splitext(theOptions.output.name)[1][1:]

		self.options = theOptions

	def main(self, args):
		self.parse(args)

		for theHandler in logger.handlers:
			logger.removeHandler(theHandler)

	#	logger.setLevel(self.options.loglevel)
		logger.setLevel(logging.DEBUG)

		theHandler = logging.StreamHandler(self.options.logstream)
		logger.addHandler(theHandler)

		####################################################################

		try:
			if not self.options.input_type or not self.options.input:
				raise InputException('No input')

			theDecoder = anytranscoder.transcoder(self.options.input_type)
			o = theDecoder.load(self.options.input)
			o = purify(o)

			theEncoder = anytranscoder.transcoder(self.options.output_type)

			theEncoder.dump(o, self.options.output, indent = self.options.pretty)


		except InputException, e:
			logger.error('Input Exception')
			self.argparser.print_help();
			sys.exit(1)
		except Exception, e:
			logger.debug('Options: %s' % self.options)
			raise

		####################################################################

def main(args):
	t = Transmogrifier()
	t.main(args)

if __name__ == '__main__':
	os.chdir(os.path.expanduser('~/Desktop/transmogrifier/Test Data'))
# 	main('transmogrifier')
 	main('transmogrifier --pretty -i Test.json -o Test2.yaml'.split(' '))
# 	main('transmogrifier'.split(' '))
# 	main('transmogrifier -i Test.plist --output-type json'.split(' '))
#  	main('transmogrifier Test.yaml Test.json'.split(' '))
#  	main('transmogrifier --input-type=json Test.json Test.yaml'.split(' '))
#  	main('transmogrifier --input-type=yaml Test.json Test.yaml'.split(' '))
# 	main('transmogrifier Test.json Test.yaml'.split(' '))
