import pytest, boto3

from moto import mock_s3


@pytest.fixture(scope='function')
def s3_bucket():
    with mock_s3():
        bucket = "mybucket"
        client = boto3.resource('s3')
        client.create_bucket(Bucket=bucket)
        yield bucket


@pytest.fixture(scope='function', params=[
    "root_file.txt",
    "a/b/c/path_file",
])
def s3_object(request, s3_bucket, local_file):
    file_name, file_content = local_file
    bucket = s3_bucket
    file_s3_path = request.param

    client = boto3.resource('s3')
    client.meta.client.upload_file(file_name, bucket, file_s3_path)

    yield bucket, file_s3_path, file_content