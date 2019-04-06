#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import re

# IMPORT THIRD-PARTY LIBRARIES
import vim


_FUNCTION_NAME = re.compile('(?P<name>\w+)\((?P<arguments>.+)\)')


def get_argument_tabstops(arguments):
    # UltiSnips reservses the "0" tabstop for its own use. User tabstops start at 1
    offset = 1
    return ['${{{tabstop}:{name}}}'.format(tabstop=index + offset, name=name)
            for index, name in enumerate(arguments)]


def get_completion_details(details):
    if details.get('user_data', '') == '':
        return ''

    return details['word']


def get_signature_breakdown(signature):
    match = _FUNCTION_NAME.match(signature)

    if not match:
        return ''

    name = match.group('name')
    arguments = [argument.strip() for argument in match.group('arguments').split(',')]

    return (name, arguments)


def get_snippet(details):
    completion = get_completion_details(details)

    if not completion:
        return ''

    function, arguments = get_signature_breakdown(completion)
    tabstops = get_argument_tabstops(arguments)

    return '{function}({tabstops})'.format(function=function, tabstops=', '.join(tabstops))
