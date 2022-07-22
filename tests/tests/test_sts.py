from moto import mock_sts
from hamcrest import assert_that, is_, has_entries, ends_with

from aws_easy_use import sts


def test_sts_get_caller_identity(aws_account):
    with mock_sts():
        result = sts.get_caller_identity()
        assert_that(result, is_(dict))
        assert_that(result, has_entries(UserId=aws_account["user_id"], Account=aws_account["account_id"], Arn=aws_account["arn"]))


def test_sts_get_caller_identity_when_assuming_role(aws_account, sts_assumed_role_simple):
    result = sts.get_caller_identity()
    assert_that(result, is_(dict))
    assert_that(result, 
        has_entries(
            UserId=sts_assumed_role_simple["role_id"], 
            Account=aws_account["account_id"], 
            Arn=sts_assumed_role_simple["arn"]
        )
    )


def test_sts_assume_role(aws_account, iam_role_simple):
    role_session_name = "sts-assume-role-1"
    region =            "ap-northeast-1"


    @sts.assume_role(
        assume_role_arn=iam_role_simple["arn"], 
        assume_role_session_name=role_session_name,
        assume_role_region=region,
        external_id="4be10b85-4b3c-4b59-a71a-d0c1808ad5ac"
    )
    def _test_func():
        result = sts.get_caller_identity()
        assert_that(result, is_(dict))
        assert_that(result, 
            has_entries(
                UserId=ends_with(f":{role_session_name}"), 
                Account=aws_account["account_id"], 
                Arn=f"arn:aws:sts::{aws_account['account_id']}:assumed-role{iam_role_simple['path']}{iam_role_simple['name']}/{role_session_name}"
            )
        )


    with mock_sts():
        _test_func()

        result = sts.get_caller_identity()
        assert_that(result, is_(dict))
        assert_that(result, has_entries(UserId=aws_account["user_id"], Account=aws_account["account_id"], Arn=aws_account["arn"]))
