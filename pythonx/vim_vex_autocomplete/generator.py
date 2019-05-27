#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module that is designed to create the ctags file for this plugin.

You can run this module at any time to generate new VEX function completions.

Requires:
    >>> pip install BeautifulSoup4

Example:
    python generator.py

"""

# IMPORT STANDARD LIBRARIES
import argparse
import logging
import urllib2
import sys
import os

# IMPORT THIRD-PARTY LIBRARIES
import bs4


_ROOT_URL = 'http://www.sidefx.com/docs/houdini/vex/functions'

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
_CTAGS_FOLDER = os.path.dirname(os.path.dirname(_CURRENT_DIR))
OUTPUT_FILE = os.path.join(_CTAGS_FOLDER, 'ctags', 'vex-tags')

LOGGER = logging.getLogger(__name__)
_HANDLER = logging.StreamHandler(sys.stdout)
_HANDLER.setLevel(logging.DEBUG)
_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_HANDLER.setFormatter(_FORMATTER)
LOGGER.addHandler(_HANDLER)


def _get_page(url):
    """`bs4.BeautifulSoup` or NoneType: Create a parse-able object for the given URL."""
    try:
        page = urllib2.urlopen(url)
    except Exception:
        LOGGER.exception('Could not load url "%s".', url)
        return None
    return bs4.BeautifulSoup(page, 'html.parser')


def iter_all_function_pages():
    """`bs4.BeautifulSoup`: Find every function page of Houdini VEX documentation."""
    page = urllib2.urlopen(_ROOT_URL)
    soup = bs4.BeautifulSoup(page, 'html.parser')

    for function in soup.find_all('li', {'class': 'subtopics_item'}):
        link = function.find('a', href=True)
        url = _ROOT_URL + '/' + link['href']

        function_page = _get_page(url)
        if function_page:
            yield function_page


def iter_all_page_signatures(page):
    """str: Find every signature of every page of Houdini VEX documentation."""
    def _extract_class(signature, class_name):
        unwanted = signature.find('span', {'class': class_name})
        if not unwanted:
            return
        unwanted.extract()

    for signature in page.find_all('code', {'class': 'vexsignature'}):
        # Remove the return type and other things that we don't care about
        _extract_class(signature, 'vexargtype')
        _extract_class(signature, 'vexpattern')
        _extract_class(signature, 'vexrtype')
        _extract_class(signature, 'vextype')

        try:
            yield signature.get_text().encode('utf-8').strip()
        except Exception:
            pass


def write_signatures():
    """Parse Houdini's VEX command documentation and save all found functions."""
    signatures = []
    for page in iter_all_function_pages():
        for signature in iter_all_page_signatures(page):
            signatures.append('{signature}\t/\tlanguage:vex'.format(signature=signature))
            LOGGER.debug('Found signature "%s".', signature)

    LOGGER.info('Finished getting signatures')

    with open(OUTPUT_FILE, 'w') as handler:
        handler.write('\n'.join(sorted(signatures)))


def main():
    """Run this module and save all found VEX functions."""
    parser = argparse.ArgumentParser(
        description='Run this file to regenerate Houdini VEX function ctags',
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        help='If enabled, log messages will be printed. Repeat for more detailed messages.',
    )

    arguments = parser.parse_args()

    verbosity = arguments.verbose
    if verbosity == 1:
        verbosity = logging.INFO
    elif verbosity > 1:
        verbosity = logging.DEBUG
    else:
        verbosity = logging.CRITICAL + 1

    LOGGER.setLevel(verbosity)
    LOGGER.info('Starting to get signatures.')

    write_signatures()

    LOGGER.info('Signatures found.')


if __name__ == '__main__':
    main()
