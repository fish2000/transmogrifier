#!/usr/bin/env python

import StringIO as io
#import io
import struct
import types
import math

########################################################################

SIZE_8 = 0
SIZE_16 = 1
SIZE_32 = 2
SIZE_64 = 3

TYPE_UNSIGNED = 0 << 2
TYPE_SIGNED = 1 << 2

# string, sequence, dictionary, integer, float, special | date, object, key, data

TYPE_DATA =					1 << 4
TYPE_DATA_8  =				TYPE_DATA | SIZE_8
TYPE_DATA_16 =				TYPE_DATA | SIZE_16
TYPE_DATA_32 =				TYPE_DATA | SIZE_32

TYPE_STRING =				2 << 4
TYPE_STRING_8  =			TYPE_STRING | SIZE_8
TYPE_STRING_16 =			TYPE_STRING | SIZE_16
TYPE_STRING_32 =			TYPE_STRING | SIZE_32

TYPE_SEQUENCE =				3 << 4
TYPE_SEQUENCE_8 =			TYPE_SEQUENCE | SIZE_8
TYPE_SEQUENCE_16 =			TYPE_SEQUENCE | SIZE_16
TYPE_SEQUENCE_32 =			TYPE_SEQUENCE | SIZE_32

TYPE_DICTIONARY =			4 << 4
TYPE_DICTIONARY_8 =			TYPE_DICTIONARY | SIZE_8
TYPE_DICTIONARY_16 =		TYPE_DICTIONARY | SIZE_16
TYPE_DICTIONARY_32 =		TYPE_DICTIONARY | SIZE_32

TYPE_INTEGER =				5 << 4
TYPE_INTEGER_8 =			TYPE_INTEGER | TYPE_SIGNED | SIZE_8
TYPE_INTEGER_16 =			TYPE_INTEGER | TYPE_SIGNED | SIZE_16
TYPE_INTEGER_32 =			TYPE_INTEGER | TYPE_SIGNED | SIZE_32

TYPE_FLOAT =				6 << 4
TYPE_FLOAT_32 =				TYPE_FLOAT | SIZE_32
TYPE_FLOAT_64 =				TYPE_FLOAT | SIZE_64

TYPE_SPECIAL =				7 << 4
TYPE_SPECIAL_NULL = 		TYPE_SPECIAL | 0 << 2
TYPE_SPECIAL_BOOL = 		TYPE_SPECIAL | 1 << 2
TYPE_SPECIAL_BOOL_FALSE =	TYPE_SPECIAL_BOOL | 0
TYPE_SPECIAL_BOOL_TRUE =	TYPE_SPECIAL_BOOL | 1

########################################################################

class Serializer(object):
	def serialize(self, s, o):
		return self.serialize_object(s, o)

	def serialize_object(self, s, o):
		if type(o) == bytes:
			return self.serialize_data(s, o)
		elif type(o) in types.StringTypes:
			return self.serialize_string(s, o)
		elif type(o) in [types.ListType, types.TupleType]:
			return self.serialize_sequence(s, o)
		elif type(o) in [types.DictType]:
			return self.serialize_dictionary(s, o)
		elif type(o) is types.IntType:
			return self.serialize_integer(s, o)
		elif type(o) is types.FloatType:
			return self.serialize_float(s, o)
		elif type(o) is types.BooleanType:
			return self.serialize_bool(s, o)
		else:
			raise Exception('Unsupported type: %s' % (type(o)))

	def serialize_data(self, s, o):
		l = len(o)
		if l <= 0xFF:
			format = '!BB%ds' % l
			d = struct.pack(format, TYPE_DATA_8, l, o)
		elif l <= 0xFFFF:
			format = '!BH%ds' % l
			d = struct.pack(format, TYPE_DATA_16, l, o)
		else:
			format = '!BL%ds' % l
			d = struct.pack(format, TYPE_DATA_32, l, o)
		s.write(d)
		return len(d)

	def serialize_string(self, s, o):
		o = o.encode('utf-8')
		l = len(o)
		if l <= 0xFF:
			format = '!BB%ds' % l
			d = struct.pack(format, TYPE_STRING_8, l, o)
		elif l <= 0xFFFF:
			format = '!BH%ds' % l
			d = struct.pack(format, TYPE_STRING_16, l, o)
		else:
			format = '!BL%ds' % l
			d = struct.pack(format, TYPE_STRING_32, l, o)
		s.write(d)
		return len(d)

	def serialize_sequence(self, s, o):
		l = len(o)
		if l <= 0xFF:
			format = '!BB'
			d = struct.pack(format, TYPE_SEQUENCE_8, l)
		elif l <= 0xFFFF:
			format = '!BH'
			d = struct.pack(format, TYPE_SEQUENCE_16, l)
		else:
			format = '!BL'
			d = struct.pack(format, TYPE_SEQUENCE_32, l)
		s.write(d)
		count = len(d)
		for i in o:
			count += self.serialize_object(s, i)
		return count

	def serialize_dictionary(self, s, o):
		l = len(o)
		if l <= 0xFF:
			format = '!BB'
			d = struct.pack(format, TYPE_DICTIONARY_8, l)
		elif l <= 0xFFFF:
			format = '!BH'
			d = struct.pack(format, TYPE_DICTIONARY_16, l)
		else:
			format = '!BL'
			d = struct.pack(format, TYPE_DICTIONARY_32, l)
		s.write(d)
		count = len(d)
		# TODO sort by key
		for k,v in o.items():
			count += self.serialize_object(s, k)
			count += self.serialize_object(s, v)
		return count

	def serialize_integer(self, s, o):
		if o >= -128 and o <= 127:
			format = '!BB'
			d = struct.pack(format, TYPE_INTEGER_8, o)
		elif o >= -32768 and o <= 32767:
			format = '!BH'
			d = struct.pack(format, TYPE_INTEGER_16, o)
		else:
			format = '!BL'
			d = struct.pack(format, TYPE_INTEGER_32, 0)
		s.write(d)
		return len(d)

	def serialize_float(self, s, o):
		format = '!Bf'
		d = struct.pack(format, TYPE_FLOAT_32, o)
		s.write(d)
		return len(d)

	def serialize_bool(self, s, o):
		format = '!B'
		d = struct.pack(format, TYPE_SPECIAL_BOOL_TRUE if o else TYPE_SPECIAL_BOOL_FALSE)
		s.write(d)
		return len(d)

	def serialize_none(self, s, o):
		format = '!B'
		d = struct.pack(format, TYPE_SPECIAL_NULL)
		s.write(d)
		return len(d)

########################################################################

class Deserializer(object):
	def deserialize(self, s):
		b, = struct.unpack('!B', s.read(1))
		s.seek(-1, 1)

		t = b & 0b11110000
		if t == TYPE_DATA:
			return self.deserialize_data(s)
		elif t == TYPE_STRING:
			return self.deserialize_string(s)
		elif t == TYPE_INTEGER:
			return self.deserialize_integer(s)
		elif t == TYPE_FLOAT:
			return self.deserialize_float(s)
		elif t == TYPE_SEQUENCE:
			return self.deserialize_sequence(s)
		elif t == TYPE_DICTIONARY:
			return self.deserialize_dictionary(s)
		elif t == TYPE_SPECIAL:
			return self.deserialize_special(s)
		else:
			raise Exception('TODO')

	def deserialize_data(self, s):
# 		'''
# 		>>> s = io.StringIO()
# 		>>> Serializer().serialize(s, bytes('Hello world'))
# 		13
# 		>>> s.seek(0)
# 		>>> s = Deserializer().deserialize(s)
# 		>>> type(s)
# 		<type 'bytes'>
# 		>>> s
# 		'Hello world'
# 		'''
		b, = struct.unpack('!B', s.read(1))
		size = b & 0b00000011
		format, size = [('!B',1), ('!H',2), ('!I',4), ('Q',8)][size]
		count, = struct.unpack(format, s.read(size))
		theData = bytes(s.read(count))
		return theData


	def deserialize_string(self, s):
		'''
		>>> s = io.StringIO()
		>>> Serializer().serialize(s, 'Hello world')
		13
		>>> s.seek(0)
		>>> s = Deserializer().deserialize(s)
		>>> type(s)
		<type 'str'>
		>>> s
		'Hello world'
		'''
		b, = struct.unpack('!B', s.read(1))
		size = b & 0b00000011
		format, size = [('!B',1), ('!H',2), ('!I',4), ('Q',8)][size]
		count, = struct.unpack(format, s.read(size))
		theString = s.read(count)
		return theString

	def deserialize_integer(self, s):
		'''
		>>> s = io.StringIO()
		>>> Serializer().serialize(s, 42)
		2
		>>> s.seek(0)
		>>> print Deserializer().deserialize(s)
		42
		'''
		b, = struct.unpack('!B', s.read(1))
		size = b & 0b00000011
		format, size = [('!B',1), ('!H',2), ('!I',4), ('!Q',8)][size]
		theInteger, = struct.unpack(format, s.read(size))
		return theInteger

	def deserialize_float(self, s):
		'''
		>>> s = io.StringIO()
		>>> Serializer().serialize(s, 3.14)
		5
		>>> s.seek(0)
		>>> v = Deserializer().deserialize(s)
		>>> v
		3.1400001049041748
		'''
		b, = struct.unpack('!B', s.read(1))
		size = b & 0b00000011
		format, size = [None, None, ('!f',4), ('!d',8)][size]
		theValue, = struct.unpack(format, s.read(size))
		return theValue

	def deserialize_sequence(self, s):
		'''
		>>> s = io.StringIO()
		>>> Serializer().serialize(s, [])
		2
		>>> s.seek(0)
		>>> print Deserializer().deserialize(s)
		[]
		'''
		b, = struct.unpack('!B', s.read(1))
		size = b & 0b00000011
		format, size = [('!B',1), ('!H',2), ('!I',4), ('Q',8)][size]
		count, = struct.unpack(format, s.read(size))
		theList = []
		for n in xrange(0, count):
			theList.append(self.deserialize(s))
		return theList

	def deserialize_dictionary(self, s):
		'''
		>>> s = io.StringIO()
		>>> Serializer().serialize(s, {'key':'value'})
		14
		>>> s.seek(0)
		>>> print Deserializer().deserialize(s)
		{'key': 'value'}
		'''
		b, = struct.unpack('!B', s.read(1))
		size = b & 0b00000011
		format, size = [('!B',1), ('!H',2), ('!I',4), ('Q',8)][size]
		count, = struct.unpack(format, s.read(size))
		theValue = dict()
		for n in xrange(0, count):
			k = self.deserialize(s)
			v = self.deserialize(s)
			theValue[k] = v
		return theValue

	def deserialize_special(self, s):
		'''
		>>> s = io.StringIO()
		>>> Serializer().serialize(s, True)
		1
		>>> s.seek(0)
		>>> print Deserializer().deserialize(s)
		True
		'''
		b, = struct.unpack('!B', s.read(1))
		if b == TYPE_SPECIAL_NULL:
			return None
		elif b == TYPE_SPECIAL_BOOL_FALSE:
			return False
		elif b == TYPE_SPECIAL_BOOL_TRUE:
			return True
		else:
			raise Exception('TODO')

########################################################################

def dump(o, s):
	c = Serializer().serialize(s, o)
	return c


if __name__ == '__main__':
 	o = {'key':'value'}
 	s = io.StringIO()
 	c = Serializer().serialize(s, o)
 	print(c)
 	d = s.getvalue()
 	print(d)
 	print(len(d))

 	o = Deserializer().deserialize(io.StringIO(d))
 	print(o)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
