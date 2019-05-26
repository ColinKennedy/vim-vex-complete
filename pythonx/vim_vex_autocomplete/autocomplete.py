#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import re

# IMPORT THIRD-PARTY LIBRARIES
import vim


_FUNCTION_NAME = re.compile('(?P<name>\w+)\((?P<arguments>.+)\)')


# Reference: https://stackoverflow.com/a/29992065/3626104
def _find_parens(s):
    toret = {}
    pstack = []

    for i, c in enumerate(s):
        if c == '(':
            pstack.append(i)
        elif c == ')':
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            toret[i] = pstack.pop()

    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))

    return toret


def clear_nearest_function():
    row, column = vim.current.window.cursor
    row -= 1

    parentheses = _find_parens(vim.current.buffer[row])
    # If the completion is a function, the cursor position when the
    # function is completed will always be a ). So we can query the
    # matching ( using that column index
    #
    end = column - 1
    start = parentheses[end]

    vim.current.buffer[row] = vim.current.buffer[row][:start] \
        + vim.current.buffer[row][end + 1:]

    vim.current.window.cursor = (row + 1, start - 3)


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

    return [argument.strip() for argument in match.group('arguments').split(',')]


def get_snippet(details):
    completion = get_completion_details(details)

    if not completion:
        return ''

    arguments = get_signature_breakdown(completion)
    tabstops = get_argument_tabstops(arguments)
    return '({tabstops})'.format(tabstops=', '.join(tabstops))
