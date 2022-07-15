import pytest, os


@pytest.fixture(scope='session', params=[
    dict(file_name="empty_file",    file_content=""),
    dict(file_name="one_line_file", file_content="asd"),
    dict(file_name="lines_file",    file_content="\n".join(["asd", "2. ddd", "asd", "", "ddd", "", ""])),
    dict(file_name="a.html",        file_content="asd"),
    dict(file_name="a.js",          file_content="asd"),
    dict(file_name="a.jpg",         file_content="asd"),
    dict(file_name="a.py",          file_content="asd"),
    dict(file_name="a.tar.gz",      file_content="asd"),
    dict(file_name="a.json",        file_content="asd"),
])
def local_file(request):
    file_name, file_content = request.param["file_name"], request.param["file_content"]
    with open(file_name, "w") as fout:
        fout.write(file_content)
    yield file_name, file_content
    os.remove(file_name)
