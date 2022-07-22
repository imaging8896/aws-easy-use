import pytest, boto3

from moto import mock_iam


trusted_relationship_template = """
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "AWS": "{{ arn }}"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": {{ external_id }}
                }
            }
        }
    ]
}
"""


@pytest.fixture(scope="function")
def iam_role_simple(aws_account):
    with mock_iam():
        external_id = "4be10b85-4b3c-4b59-a71a-d0c1808ad5ac"
        trusted_relationship = trusted_relationship_template.replace("{{ arn }}", aws_account["arn"]).replace("{{ external_id }}", external_id)
        client = boto3.client("iam")
        role_dict = client.create_role(
            Path="/",
            RoleName="MockRoleSimple",
            AssumeRolePolicyDocument=trusted_relationship,
        )["Role"]
        yield {
            "name": role_dict["RoleName"],
            "path": role_dict["Path"],
            "arn": role_dict["Arn"],
            "external_id": external_id,
        }
