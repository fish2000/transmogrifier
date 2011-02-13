# transmogrifier

## Author

Jonathan Wight <[jwight@mac.com][]\>

## Description

Python command line tool to convert data between different formats

Currently works with JSON, [yaml][] and (XML based) plists

## Install

From source:

	$ python setup.py install

Or if you wish to help develop transmogrifier

	$ python setup.py develop

With [pip][]:

    $ pip install transmogrifier

## Usage

    usage: transmogrifier [-h] [-i INPUT] [--input-type INPUT_TYPE] [-o OUTPUT]
                          [--output-type INPUT_TYPE] [--pretty] [-v]
                          [--loglevel LOGLEVEL] [--logfile LOG_FILE]
                          [args [args ...]]

    positional arguments:
      args

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            The input file (type is inferred by file extension).
      --input-type INPUT_TYPE
                            The input file type (overides file extension if any).
      -o OUTPUT, --output OUTPUT
                            Output directory for generated files.
      --output-type INPUT_TYPE
                            The output file type (overides file extension if any).
      --pretty              Prettify the output (where possible).
      -v, --verbose         set the log level to INFO
      --loglevel LOGLEVEL   set the log level, 0 = no log, 10+ = level of logging
      --logfile LOG_FILE    File to log messages to. If - or not provided then
                            stdout is used.

## Examples

Read Test.json, prettify it and print it to standard output

	$ transmogrifier —pretty -i Test.json

Read Test.plist and save it as Test.json

	$ transmogrifier -i Test.plist —output-type json

Read file Test.txt as JSON and save it as yaml file Test.yaml

	t$ ransmogrifier —input-type=json Test.txt Test.yaml

## Known Issues

* Doesn’t work with multiple YAML documents in one file. YAML parsing
* seems too accepting. Check that what you’re converting makes sense.

  [jwight@mac.com]: mailto:jwight@mac.com
  [yaml]: http://pyyaml.org/wiki/PyYAMLDocumentation
  [pip]: http://pypi.python.org/pypi/pip
