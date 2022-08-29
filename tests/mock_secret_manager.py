import pytest, boto3

from moto import mock_secretsmanager


@pytest.fixture(scope="function", params=[
    ("ap-northeast-1", "dev-aurora-mysql-admin", "password", {
        "password": "a",
        "dddd": "cccc",
    }),
    ("us-west-2",      "prod-aurora-mysql-admin", "host", {
        "host": "dddd",
        "yyyy": "zzzz",
    }),
])
def secret_manager_secret_string_valid_secret(request, aws_account):
    with mock_secretsmanager():
        region, name, secret_key, secret_values = request.param

        client = boto3.client("secretsmanager", region_name=region)
        response = client.create_secret(
            Name=name,
            SecretString=str(secret_values)
        )
        yield region, name, secret_key, secret_values, f"{response['ARN']}:{secret_key}::"


@pytest.fixture(scope="function", params=[
    ("us-west-2", ""),
    ("us-west-2", "asd"),
    ("us-west-2", "arn:aws:ssm:us-west-2:{account_id}:secret:prod-aurora-mysql-admin:password::"),
    ("us-west-2", "arn:aws:secretsmanager:us-west-2:{account_id}:secret:prod-aurora-mysql-admin"),
    ("us-west-2", "arn:aws:secretsmanager:us-west-2:{account_id}:secret:prod-aurora-mysql-admin:host"),
    ("us-west-2", "arn:aws:secretsmanager:us-west-2:{account_id}:secret:prod-aurora-mysql-admin:host:"),
    ("us-west-2", "arn:aws:secretsmanager:us-west-2:{account_id}:secrets:prod-aurora-mysql-admin:host::"),
])
def secret_manager_secret_string_invalid_reference_arn(request, aws_account):
    with mock_secretsmanager():
        region, invalid_reference_arn_format = request.param
        invalid_reference_arn = invalid_reference_arn_format.format(account_id=aws_account["account_id"])

        client = boto3.client("secretsmanager", region_name="us-west-2")
        response = client.create_secret(
            Name="prod-aurora-mysql-admin",
            SecretString='{"host": "dddd", "yyyy": "zzzz"}'
        )
        yield region, invalid_reference_arn


@pytest.fixture(scope="function", params=[
    # ("us-west-2", "arn:aws:secretsmanager:us-west-2:{account_id}:secret:prod-aurora-mysql-admin:a::"),
    ("us-west-2", "arn:aws:secretsmanager:us-west-2:{account_id}:secret:prod-aurora-mysql-admina:host::"),
    ("us-west-2", "arn:aws:secretsmanager:ap-northeast-1:{account_id}:secret:prod-aurora-mysql-admin:host::"),
    ("ap-northeast-1", "arn:aws:secretsmanager:ap-northeast-1:{account_id}:secret:prod-aurora-mysql-admin:host::"),
    ("ap-northeast-1", "arn:aws:secretsmanager:us-west-2:{account_id}:secret:prod-aurora-mysql-admin:host::"),
])
def secret_manager_secret_string_not_existed_reference_arn(request, aws_account):
    with mock_secretsmanager():
        region, invalid_reference_arn_format = request.param
        invalid_reference_arn = invalid_reference_arn_format.format(account_id=aws_account["account_id"])

        client = boto3.client("secretsmanager", region_name="us-west-2")
        response = client.create_secret(
            Name="prod-aurora-mysql-admin",
            SecretString='{"host": "dddd", "yyyy": "zzzz"}'
        )
        yield region, invalid_reference_arn
