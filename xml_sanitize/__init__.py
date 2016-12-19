import argparse
import codecs
import glob
import sys
import re

import pkg_resources

import itertools

_illegal_unichrs = [(0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F),
                    (0x7F, 0x84), (0x86, 0x9F),
                    (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF)]
if sys.maxunicode >= 0x10000:  # not narrow build
    _illegal_unichrs.extend([(0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF),
                             (0x3FFFE, 0x3FFFF), (0x4FFFE, 0x4FFFF),
                             (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF),
                             (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF),
                             (0x9FFFE, 0x9FFFF), (0xAFFFE, 0xAFFFF),
                             (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF),
                             (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF),
                             (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF)])

_illegal_ranges = ["%s-%s" % (unichr(low), unichr(high))
                   for (low, high) in _illegal_unichrs]
_illegal_xml_chars_RE = re.compile(u'[%s]' % u''.join(_illegal_ranges))


def main():
    p = argparse.ArgumentParser(version=pkg_resources.require('xml_sanitize')[0].version)
    p.add_argument('input_files', metavar='INPUT', type=str, nargs='+',
                   help='File to process. Glob expression may be used to select more files.')
    p.add_argument('-e', '--encoding', default='utf-8')
    args = p.parse_args()
    if args.encoding != 'utf-8':
        sys.exit('Encodings other than UTF-8 are not supported yet')

    input_files = list(itertools.chain.from_iterable([glob.glob(f) for f in args.input_files]))
    for input_file_name in input_files:
        print "Processing:", input_file_name
        with codecs.open(input_file_name, 'r', args.encoding) as input_f:
            txt = input_f.read()
        sanitized = re.sub(_illegal_xml_chars_RE, '#invalid_xml_char', txt)
        with codecs.open(input_file_name, 'w', args.encoding) as output_f:
            output_f.write(sanitized)


if __name__ == '__main__':
    main()
