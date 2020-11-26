# fix_aws_permissions

This script is intended to use for fixing incorrect permissions on AWS bucket in Divio-based setup.
See https://github.com/what-digital/divio/issues/39 for details.

How to use:
1. Create aws permissions file on `~/.aws/credentials` like this (it's used by aws cli tool as well):

    ```
    [default]
    aws_access_key_id = {your_key_id_stage}
    aws_secret_access_key = {your_access_key_stage}
    
    [stage]
    aws_access_key_id = {your_key_id_stage}
    aws_secret_access_key = {your_access_key_stage}
    
    [prod]
    aws_access_key_id = {your_key_id_prod}
    aws_secret_access_key = {your_access_key_prod}
    ```

2. Add you bucket name to BUCKET_NAME variable
3. Add the profile name to PROFILE variable
4. Run the script


Tested with python 3.7.3, 3.9.0 and macOS 11.0.1, Debian 4.19
