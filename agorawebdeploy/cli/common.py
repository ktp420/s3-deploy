# -*- coding: utf-8 -*-
import collections
import logging
import os

import boto3
import docopt

from .. import config, logger

handler = logging.StreamHandler()

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


def _init_logging(level='INFO'):
    if level.upper() == 'DEBUG':
        # we should show function-call info to trace execution. aids ramp-up & debugging.
        formatter = logging.Formatter(
            '%(levelname)-5s:%(name)s:%(module)s.%(funcName)s() L%(lineno)d | %(message)s')
    else:
        formatter = logging.Formatter('[%(levelname)-5s] %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level.upper())
    logger.propagate = False


def process_global_options(arg_dict):
    """ Take all of the global options and apply them

    Note: This can be run more than once, but the last used value will always win
    """
    config.aws_profile = arg_dict['--profile']
    _init_logging(arg_dict['--log'])
    boto3.set_stream_logger(name='botocore', level=arg_dict['--log-boto'])


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
