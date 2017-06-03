# -*- coding: utf-8 -*-
"""
Invalidate CloudFront distribution cache

Usage: agorawebdeploy invalidate-cache
                   (--s3-bucket=NAME|--distribution-id=ID)
                   (--path=PATH ...)
                   [--no-wait]
                   [options]

Required Arguments:
  These arguments are all required for operation!

  -b NAME, --s3-bucket=NAME
                option 1/2 to specify CloudFront Distribution
                find distribution id using the name of the s3 bucket
                hosting the s3-website
  -i ID, --distribution-id=ID
                option 2/2 to specify CloudFront Distribution
                CloudFront Distribution Id to invalidate caches
  -p PATH, --path=PATH
                path to be invalidated.  This can end with '*' for
                wildcard.  See AWS CloudFront document for more info.
                You can specify this option multiple times.

Wait Argument:
  --no-wait     do not wait for completion of created invalidation.
                Default is to wait for the completion.
"""
import pprint

from .common import format_and_process_doc, SUCCESS, FAILURE, logger
from .. import usecloudfront


def main(argv, help=False):
    try:
        _unused, arg_dict = format_and_process_doc(
            doc=__doc__,
            argv=argv,
            include_globals=True
        )
    except SystemExit:
        return SUCCESS if help else FAILURE

    if not arg_dict['--distribution-id']:
        bucket_name = arg_dict['--s3-bucket']
        logger.info("Finding CloudFront distribution for s3 bucket '{0}'".format(bucket_name))
        distribution_ids = usecloudfront.find_distribution_for_s3_bucket(bucket_name)
        if not distribution_ids:
            logger.error(
                'CloudFront distribution not found for s3 bucket "{0}"'.format(bucket_name)
            )
            return FAILURE
        if len(distribution_ids) > 1:
            logger.warn(
                'Multiple distributions, {0}, found for s3 bucket "{1}"'.format(
                    distribution_ids, bucket_name)
            )
    else:
        distribution_ids = [arg_dict['--distribution-id']]

    invalidations = usecloudfront.invalidate_caches(
        distribution_ids, arg_dict['--path'],
        wait_to_complete=not arg_dict['--no-wait'])
    logger.info(pprint.pformat(invalidations))
