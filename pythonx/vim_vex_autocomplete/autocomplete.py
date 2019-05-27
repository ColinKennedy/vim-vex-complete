#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module that converts function arguments into an UltiSnips snippet."""

# IMPORT STANDARD LIBRARIES
import re

# IMPORT THIRD-PARTY LIBRARIES
import vim


_FUNCTION_NAME = re.compile('(?P<name>\w+)\((?P<arguments>.+)\)')


def clear(characters):
    """Delete X number of characters, starting from the left of the cursor.

    When a Vim completion result is selected, the cursor is set to
    the right of whatever was completed. This function "deletes" the
    completed result by deleting characters to the left of the cursor
    (which is always whatever was just completed).

    Args:
        characters (int):
            The number of characters that will be deleted. This number
            should match the completed text.

    """
    row, column = vim.current.window.cursor
    row -= 1
    start = column - characters
    vim.current.buffer[row] = vim.current.buffer[row][:start] \
        + vim.current.buffer[row][column:]

    vim.current.window.cursor = (row + 1, start)


def get_argument_tabstops(arguments):
    """str: Convert the given function arguments into an UltiSnips-style snippet."""
    # UltiSnips reservses the "0" tabstop for its own use. User tabstops start at 1
    offset = 1
    return ['${{{tabstop}:{name}}}'.format(tabstop=index + offset, name=name)
            for index, name in enumerate(arguments)]


def get_completion_word(details):
    """Find the completed text from some Vim completion data.

    Args:
        details (dict[str, str]):
            Data that comes from Vim after completion finishes. For more
            information, check out Vim's help documentation. `:help
            v:completed_item`.

    Returns:
        str: The completed function.

    """
    user_made_a_completion_selection = details.get('user_data', '') != ''
    if not user_made_a_completion_selection:
        return ''

    return details['word']


def get_signature_breakdown(signature):
    """tuple[str, list[str]]: Split a caller into its name and arguments."""
    match = _FUNCTION_NAME.match(signature)

    if not match:
        return ('', [])

    arguments = [argument.strip() for argument in match.group('arguments').split(',')]
    return match.group('name'), arguments


def get_snippet(details):
    """Create a snippet for the given Vim completion information.

    Args:
        details (dict[str, str]):
            Data that comes from Vim after completion finishes. For more
            information, check out Vim's help documentation. `:help
            v:completed_item`.

    Returns:
        str: An UltiSnips-style snippet that includes the function and its arguments.

    """
    completion = get_completion_word(details)

    if not completion:
        return ''

    caller, arguments = get_signature_breakdown(completion)

    if not caller or not arguments:
        return ''

    tabstops = get_argument_tabstops(arguments)
    return '{caller}({tabstops})'.format(caller=caller, tabstops=', '.join(tabstops))
