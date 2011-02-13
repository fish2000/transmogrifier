
from setuptools import setup, find_packages

# http://docs.python.org/distutils/setupscript.html#additional-meta-data

setup(
	name = 'transmogrifier',
	version = '0.1.0dev',

	install_requires = ['argparse >= 1.1', 'yaml >= 3.0.9'],
	packages = find_packages(exclude = [ 'ez_setup', 'Test Data' ]),
	include_package_data = True,
	scripts = ['scripts/transmogrifier'],
	zip_safe = False,
	author = 'Jonathan Wight',
	author_email = 'jwight@mac.com',
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		],
	description = 'Python command line tool to convert data between different formats',
	license = 'BSD License',
	long_description = file('README.markdown').read(),
	url = 'http://github.com/schwa/transmogrifier',
	)

