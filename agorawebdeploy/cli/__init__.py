# -*- coding: utf-8 -*-
"""
agorawebdeploy -- client to automate deployment of web artifacts to s3 for Agora web apps

Usage: agorawebdeploy [options] <command> [<command_args>...]

Available Commands:
{commands}
"""

import collections
import logging
import os
import sys

import docopt

from .. import config
from .. import logger

SUCCESS = 0
FAILURE = 1

GLOBAL_OPTIONS = """
Global Options:
  These options affect all operations, and are specifiable either before or
  after any command input.

  -p NAME, --profile=NAME
                aws profile to use
  --log=LEVEL   set ecsinfra logging level [default: INFO]
  --log-boto=LEVEL
                set level for boto (AWS API library) [default: ERROR]
"""

CLICommand = collections.namedtuple('CLICommand', ('name', 'function', 'description'))
COMMAND_LIST = []


def _init_logging(level='INFO'):
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime).19s [%(levelname)s] %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level.upper())


def process_global_options(arg_dict):
    """ Take all of the global options and apply them

    Note: This can be run more than once, but the last used value will always win
    """
    config.aws_profile = arg_dict['--profile']
    _init_logging(arg_dict['--log'])
    logging.getLogger('botocore').setLevel(arg_dict['--log-boto'])


def format_and_process_doc(doc, argv, format_kwargs=None, include_globals=False,
                           extended_help=None, strict=False):
    if format_kwargs is None:
        format_kwargs = {}

    if include_globals:
        doc += GLOBAL_OPTIONS
    if extended_help:
        doc += os.linesep.join(('', '*** EXTENDED HELP ***', extended_help))
    doc_formatted = doc.format(**format_kwargs)
    try:
        arg_dict = docopt.docopt(doc_formatted, argv=argv, help=False, options_first=strict)
    except SystemExit:
        print doc_formatted
        raise
    if include_globals:
        process_global_options(arg_dict)
    return doc_formatted, arg_dict


def main(argv=None):
    argv = argv or sys.argv[1:]
    try:
        commands = os.linesep.join(
            ['  {:<14s}{}'.format(c.name, c.description) for c in COMMAND_LIST]
        )
        doc, arg_dict = format_and_process_doc(
            doc=__doc__,
            argv=argv,
            format_kwargs={'commands': commands},
            include_globals=True,
            strict=True
        )
    except SystemExit:
        # allow omission of any commands
        return SUCCESS if not len(argv) else FAILURE

    command_input = arg_dict['<command>']
    command_functions = {c.name: c.function for c in COMMAND_LIST}
    if command_input != 'help' and command_input not in command_functions.keys():
        logger.error('{} is not a valid command'.format(command_input))
        print doc
        return FAILURE

    if command_input == 'help' and not arg_dict['<command_args>']:
        print doc
        return SUCCESS

    help = False
    if command_input == 'help' and arg_dict['<command_args>']:
        command_input = arg_dict['<command_args>'][0]
        help = True

    # tack the global options back onto the end
    global_options = argv[:argv.index(command_input)]
    argv_remainder = argv[argv.index(command_input):]
    return command_functions[command_input](argv_remainder + global_options, help=help)
