import pytest, os, importlib, sys


@pytest.fixture(scope="session")
def aws_account():
    account_id = "102348888111"

    os.environ["MOTO_ACCOUNT_ID"] = account_id

    # since moto deals with ACCOUNT_ID in a "set-once" manner, we need
    # to reload moto and all of its sub-modules
    importlib.reload(sys.modules['moto'])
    to_reload = [m for m in sys.modules if m.startswith('moto.')]
    for m in to_reload:
        importlib.reload(sys.modules[m])

    return {
        "account_id": account_id,
        "arn":        f"arn:aws:sts::{account_id}:user/moto",
        "user_id":    "AKIAIOSFODNN7EXAMPLE",
    }
