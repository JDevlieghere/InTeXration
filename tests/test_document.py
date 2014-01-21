import os
import shutil
import pytest
from intexration.document import Document


def move_to_temp(tmpdir, file):
    source = os.path.join(os.path.dirname(__file__), 'files', file)
    dest = os.path.join(tmpdir.strpath, file)
    shutil.copyfile(source, dest)
    return dest


class TestDocument:

    def test_constructor1(self):
        with pytest.raises(RuntimeWarning):
            Document("test", "")

    def test_constructor2(self, tmpdir):
        move_to_temp(tmpdir, 'test.log')
        Document("test", tmpdir.strpath)
        assert True

    def test_read_lines(self, tmpdir):
        move_to_temp(tmpdir, 'test.log')
        document = Document("test", tmpdir.strpath)
        assert len(document._lines)

    def test_read_errors(self, tmpdir):
        move_to_temp(tmpdir, 'test.log')
        document = Document("test", tmpdir.strpath)
        assert len(document.get_errors()) == 1

    def test_read_warnings(self, tmpdir):
        move_to_temp(tmpdir, 'test.log')
        document = Document("test", tmpdir.strpath)
        assert len(document.get_warnings()) == 5

