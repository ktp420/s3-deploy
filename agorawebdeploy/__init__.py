# -*- coding: utf-8 -*-
import logging


logger = logging.getLogger('agorawebdeploy')


def _init_logging(level=logging.INFO):
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime).19s [%(levelname)s] %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)



def main():
    # args = docopt.docopt(__doc__)
    # if args['version']:
    #     print('agorawebdeploy ' + _version.__version__)
    #     return 0
    _init_logging()


