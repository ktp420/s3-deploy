import random
import time

import funcy

from . import logger
from . import useboto


def find_distribution_for_s3_bucket(bucket_name):
    """
    Finds CloudFront distribution for the given s3 bucket_name.
    This assumes that distribution DomainName is s3-website, i.e.
    <bucket_name>.s3-website-us-east-1.amazonaws.com.

    :param bucket_name: s3 bucket name
    :return: list of distribution ids
    """
    client = useboto.get_boto3_client('cloudfront')
    domain_name = '{0}.s3-website-'.format(bucket_name)
    distributions = client.list_distributions()['DistributionList']['Items']
    distribution_ids = [distribution['Id']
                        for distribution in distributions
                        if 'Origins' in distribution and 'Items' in distribution['Origins']
                        for origin in distribution['Origins']['Items']
                        if 'DomainName' in origin and origin['DomainName']
                        and origin['DomainName'].startswith(domain_name)]
    return distribution_ids


def unique_string(prefix='cli'):
    return '%s-%s-%s' % (prefix, int(time.time()), random.randint(1, 1000000))


def invalidate_caches(distribution_ids, paths_list, wait_to_complete=False):
    client = useboto.get_boto3_client('cloudfront')
    if not funcy.is_list(distribution_ids):
        distribution_ids = (distribution_ids,)

    invalidate_requests = {}
    for dist_id in distribution_ids:
        logger.info("Creating cache invalidation for distribution %s", dist_id)
        response = client.create_invalidation(DistributionId=dist_id, InvalidationBatch=dict(
            Paths=dict(Quantity=len(paths_list), Items=paths_list),
            CallerReference=unique_string(dist_id)
        ))
        invalidate_requests[dist_id] = response

    if wait_to_complete:
        waiter = client.get_waiter('invalidation_completed')
        for dist_id, invalidate_response in invalidate_requests.iteritems():
            logger.info("Waiting for cache invalidation to finish for distribution %s", dist_id)
            invalidation_id = invalidate_response['Invalidation']['Id']
            waiter.wait(DistributionId=dist_id,
                        Id=invalidation_id)
            invalidate_requests[dist_id] = client.get_invalidation(
                DistributionId=dist_id,
                Id=invalidation_id
            )

    return invalidate_requests
