import logging
import pprint

import boto3
from botocore.config import Config

from . import config

logger = logging.getLogger('agorawebdeploy')


class UnexpectedAPIResponseException(Exception):
    """An exception to throw when the API gives a status code other than 200"""
    pass


def get_boto3_client(aws_service, region=None):
    if config.aws_profile:
        session = boto3.Session(profile_name=config.aws_profile, region_name=region)
    else:
        session = boto3.Session(region_name=region)
    if aws_service == 's3':
        return session.client(aws_service, config=Config(signature_version='s3v4'))
    return session.client(aws_service)


def _200_or_die(response):
    """ If we didn't get a 200 back on a call, raise an exception

    .. doctests ::

        >>> response = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        >>> _200_or_die(response)
        >>> response['ResponseMetadata']['HTTPStatusCode'] = 404
        >>> _200_or_die(response)  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        UnexpectedAPIResponseException: status code was 404 not 200
    """
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code != 200:
        logger.fatal(response['ResponseMetadata'])
        logger.debug(pprint.pformat(response))
        raise UnexpectedAPIResponseException(
            "status code was {} not 200".format(status_code)
        )


def s3_bucket_exists(bucket_name):
    s3 = get_boto3_client('s3')
    if bucket_name in [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]:
        return True
    return False
