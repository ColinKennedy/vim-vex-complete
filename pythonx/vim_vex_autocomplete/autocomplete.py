#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import re

# IMPORT THIRD-PARTY LIBRARIES
import vim


_FUNCTION_NAME = re.compile('(?P<name>\w+)\((?P<arguments>.+)\)')


def clear(characters):
    row, column = vim.current.window.cursor
    row -= 1
    start = column - characters
    vim.current.buffer[row] = vim.current.buffer[row][:start] \
        + vim.current.buffer[row][column:]

    vim.current.window.cursor = (row + 1, start)


def get_argument_tabstops(arguments):
    # UltiSnips reservses the "0" tabstop for its own use. User tabstops start at 1
    offset = 1
    return ['${{{tabstop}:{name}}}'.format(tabstop=index + offset, name=name)
            for index, name in enumerate(arguments)]


def get_completion_details(details):
    user_made_a_completion_selection = details.get('user_data', '') != ''
    if not user_made_a_completion_selection:
        return ''

    return details['word']


def get_signature_breakdown(signature):
    match = _FUNCTION_NAME.match(signature)

    if not match:
        return ''

    arguments = [argument.strip() for argument in match.group('arguments').split(',')]
    return match.group('name'), arguments


def get_snippet(details):
    completion = get_completion_details(details)

    if not completion:
        return ''

    caller, arguments = get_signature_breakdown(completion)
    tabstops = get_argument_tabstops(arguments)
    return '{caller}({tabstops})'.format(caller=caller, tabstops=', '.join(tabstops))
