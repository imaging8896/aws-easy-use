import pytest, mimetypes, allure

from hamcrest import assert_that, equal_to, is_, has_key

from aws_easy_use import s3


@allure.epic("AWS S3")
@allure.feature("Get Object")
@allure.story("Get Object")
@allure.title("Get Object for '{s3_object}'")
@allure.severity("critical")
@allure.testcase("https://www.google.com/", 'Test case link. May be X-Ray')
@allure.issue("https://www.google.com/", 'Issue. May be Jira ticket')
def test_s3_get_object(s3_object):
    bucket, file_s3_path, _ = s3_object

    result_obj = s3.get_object(bucket, file_s3_path)
    assert_that(result_obj, is_(dict))
    assert_that(result_obj, has_key("Body"))
    assert_that(result_obj, has_key("ContentType"))


@allure.epic("AWS S3")
@allure.feature("Get Object")
@allure.story("Read Object Content as Str")
@allure.title("Read Object Content as Str for '{s3_object}'")
def test_s3_read_object_str(s3_object):
    bucket, file_s3_path, expect_file_content = s3_object

    result_str = s3.read_object_string(bucket, file_s3_path)
    assert_that(result_str, equal_to(expect_file_content))


@allure.epic("AWS S3")
@allure.feature("Add Object")
@allure.story("Add file")
@allure.title("Add file '{local_file}' to path '{file_s3_path}' on S3 '{s3_bucket}'")
@pytest.mark.parametrize("file_s3_path", ["asd", "a/b/asd"])
def test_s3_upload_file(s3_bucket, local_file, file_s3_path):
    file_name, file_content = local_file
    bucket = s3_bucket

    s3.upload_file(file_name, bucket, file_s3_path)

    result_obj = s3.get_object(bucket, file_s3_path)

    file_mimetype, _ = mimetypes.guess_type(file_name)
    if file_mimetype:
        assert_that(result_obj["ContentType"], equal_to(file_mimetype))
    else:
        assert_that(result_obj["ContentType"], equal_to("binary/octet-stream"))

    result_str = s3.read_object_string(bucket, file_s3_path)
    assert_that(result_str, equal_to(file_content))


@allure.epic("AWS S3")
@allure.feature("Add Object")
@allure.story("Add directory")
@allure.title("Add directory to path '{dir_s3_path}' on S3 '{s3_bucket}'")
@pytest.mark.parametrize("dir_s3_path", ["asd/", "a/b/asd/"])
def test_s3_add_dir(s3_bucket, dir_s3_path):
    bucket = s3_bucket

    s3.put_dir(bucket, dir_s3_path)

    result_obj = s3.get_object(bucket, dir_s3_path)

    assert_that(result_obj["ContentType"], equal_to("binary/octet-stream"))


@allure.epic("AWS S3")
@allure.feature("Add Object")
@allure.story("Add str file")
@allure.title("Add str '{file_content}' file to path '{file_s3_path}' on S3 '{s3_bucket}'")
@pytest.mark.parametrize("file_s3_path", ["asd", "a/b/asd"])
@pytest.mark.parametrize("file_content", ["",    "asd", "\n".join(["", "a", "", "", "c", ""])])
def test_s3_add_str_file(s3_bucket, file_s3_path, file_content):
    bucket = s3_bucket

    s3.put_string_file(bucket, file_s3_path, file_content)

    result_obj = s3.get_object(bucket, file_s3_path)
    assert_that(result_obj["ContentType"], equal_to("binary/octet-stream"))

    result_str = s3.read_object_string(bucket, file_s3_path)
    assert_that(result_str, equal_to(file_content))
