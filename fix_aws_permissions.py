"""
This script is intended to use for fixing incorrect permissions on AWS bucket in Divio-based setup.

How to use:
1. Create aws permissions file on ~/.aws/credentials like this (it's used by aws cli tool as well):

[default]
aws_access_key_id = {your_key_id_stage}
aws_secret_access_key = {your_access_key_stage}

[stage]
aws_access_key_id = {your_key_id_stage}
aws_secret_access_key = {your_access_key_stage}

[prod]
aws_access_key_id = {your_key_id_prod}
aws_secret_access_key = {your_access_key_prod}

2. Add you bucket name to BUCKET_NAME variable
3. Add the profile name to PROFILE variable
4. Run the script


Tested with python 3.9.0 on macOS 11.0.1
"""

from pprint import pprint

import boto3

BUCKET_NAME = 'your_bucket_name'
PROFILE = 'stage'  # Select required profile from ~/.aws/credentials


def is_acl_read(grants):
    all_users = 'http://acs.amazonaws.com/groups/global/AllUsers'

    for grant in grants:
        if grant['Permission'] == 'READ':
            if grant['Grantee']['URI'] == all_users:
                return True
    return False


session = boto3.Session(profile_name=PROFILE)
stage_s3_client = session.client('s3')
s3 = session.resource('s3')


bucket = s3.Bucket(BUCKET_NAME)

all_obj = list(bucket.objects.all())

all_obj_len = len(all_obj)
error_obj = []
for idx, obj in enumerate(all_obj, 1):
    print(f'{idx} / {all_obj_len}')
    acl = obj.Acl()

    _is_acl_read = is_acl_read(acl.grants)

    if not _is_acl_read:
        error_obj.append(obj.key)
        obj = s3.Object(BUCKET_NAME, obj.key)
        pprint(obj.Acl().put(ACL='public-read'))
        print(f'Fixed image: {obj.key}')

pprint(error_obj)
print(len(error_obj))
