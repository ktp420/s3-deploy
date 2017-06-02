# -*- coding: utf-8 -*-
"""
Invalidate CloudFront distribution cache

Usage: agorawebdeploy invalidate-cache
                   (--s3-bucket=NAME|--distribution-id=ID)
                   (--path=PATH ...)
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
"""
