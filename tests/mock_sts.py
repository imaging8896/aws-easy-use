import pytest, boto3

from moto import mock_sts


@pytest.fixture(scope="function")
def sts_assumed_role_simple(iam_role_simple):
    with mock_sts():
        region = "ap-northeast-1"
        role_session_name = "sts-mocked-simple-role"

        client = boto3.client("sts")
        assumed_role = client.assume_role(
            RoleArn=iam_role_simple["arn"],
            RoleSessionName=role_session_name,
            ExternalId=iam_role_simple["external_id"]
        )

        boto3.setup_default_session(
            aws_access_key_id     = assumed_role['Credentials']['AccessKeyId'],
            aws_secret_access_key = assumed_role['Credentials']['SecretAccessKey'],
            aws_session_token     = assumed_role['Credentials']['SessionToken'],
            region_name           = region
        )
        yield {
            "role_id": assumed_role["AssumedRoleUser"]["AssumedRoleId"],
            "arn":     assumed_role["AssumedRoleUser"]["Arn"],
            "region":  region, 
            "role_session_name": role_session_name,
        }
        boto3.setup_default_session()
