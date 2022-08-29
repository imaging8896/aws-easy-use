import pytest

from hamcrest import assert_that, equal_to, calling, raises

from aws_easy_use import secret_manager


def test_secret_manage_is_resource_valid_arn(secret_manager_secret_string_valid_secret):
    region, name, secret_key, secret_values, reference_key_arn = secret_manager_secret_string_valid_secret
    result = secret_manager.is_resource(reference_key_arn)
    assert_that(result, equal_to(True))


@pytest.mark.parametrize("invalid_resource_arn_format", [
    "",
    "asd",
    "arn:aws:ssm:us-west-2:{account_id}:secret:blabo-dev-aurora-mysql-admin20220819015905167800000001-aaiAzJ:password::",
])
def test_secret_manage_is_resource_invalid_resource_arn(aws_account, invalid_resource_arn_format):
    invalid_resource_arn = invalid_resource_arn_format.format(account_id=aws_account["account_id"])

    result = secret_manager.is_resource(invalid_resource_arn)
    assert_that(result, equal_to(False))


def test_secret_manage_is_reference_key_existed_valid_arn(secret_manager_secret_string_valid_secret):
    region, name, secret_key, secret_values, reference_key_arn = secret_manager_secret_string_valid_secret
    result = secret_manager.is_reference_key_existed(reference_key_arn, region=region)
    assert_that(result, equal_to(True))


def test_secret_manage_is_reference_key_existed_invalid_arn(secret_manager_secret_string_invalid_reference_arn):
    region, reference_key_arn = secret_manager_secret_string_invalid_reference_arn
    assert_that(
        calling(secret_manager.is_reference_key_existed).with_args(reference_key_arn, region=region),
        raises(
            Exception, 
            f"^Invalid 'reference_key_arn' need format\n.+\nGot\n{reference_key_arn}$"
        )
    )


def test_secret_manage_is_reference_key_not_existed_not_existed_arn(secret_manager_secret_string_not_existed_reference_arn):
    region, reference_key_arn = secret_manager_secret_string_not_existed_reference_arn
    result = secret_manager.is_reference_key_existed(reference_key_arn, region=region)
    assert_that(result, equal_to(False))
