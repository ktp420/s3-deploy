# -*- coding: utf-8 -*-
"""
agorawebdeploy -- client to automate deployment of web artifacts to s3 for Agora web apps

Usage: agorawebdeploy [options] <command> [<command_args>...]

Available Commands:
{commands}
"""

import os
import sys

from . import cache
from . import common

logger = common.logger

COMMAND_LIST = (
    common.CLICommand('invalidate-cache', cache.main, 'invalidate CloudFront distribution cache'),
    common.CLICommand('help', None, 'print help information'),
)


def main(argv=None):
    argv = argv or sys.argv[1:]
    try:
        commands = os.linesep.join(
            ['  {:<17s}{}'.format(c.name, c.description) for c in COMMAND_LIST]
        )
        doc, arg_dict = common.format_and_process_doc(
            doc=__doc__,
            argv=argv,
            format_kwargs={'commands': commands},
            include_globals=True,
            strict=True
        )
    except SystemExit:
        # allow omission of any commands
        return common.SUCCESS if not len(argv) else common.FAILURE

    command_input = arg_dict['<command>']
    command_functions = {c.name: c.function for c in COMMAND_LIST}
    if command_input != 'help' and command_input not in command_functions.keys():
        logger.error('{} is not a valid command'.format(command_input))
        print doc
        return common.FAILURE

    if command_input == 'help' and not arg_dict['<command_args>']:
        print doc
        return common.SUCCESS

    help = False
    if command_input == 'help' and arg_dict['<command_args>']:
        command_input = arg_dict['<command_args>'][0]
        help = True

    # tack the global options back onto the end
    global_options = argv[:argv.index(command_input)]
    argv_remainder = argv[argv.index(command_input):]
    return command_functions[command_input](argv_remainder + global_options, help=help)
