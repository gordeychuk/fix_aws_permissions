from progress.bar import ChargingBar
import boto3

BUCKET_NAME = 'your_bucket_name'
PROFILE = 'stage'  # Select required profile from ~/.aws/credentials


class CustomBar(ChargingBar):
    suffix = '%(percent)d%% [%(index)d / %(max)d] eta: %(remaining_hours)dh'

    @property
    def remaining_hours(self):
        return self.eta // 3600


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

print(f'Total to be processed: {all_obj_len}\n')

with CustomBar('Processing', max=all_obj_len) as bar:
    for idx, obj in enumerate(all_obj, 1):
        acl = obj.Acl()

        _is_acl_read = is_acl_read(acl.grants)

        if not _is_acl_read:
            error_obj.append(obj.key)
            obj = s3.Object(BUCKET_NAME, obj.key)
            obj.Acl().put(ACL='public-read')
        bar.next()

print(f'\n{len(error_obj)} images fixed')
