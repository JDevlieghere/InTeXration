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
        move_to_temp(tmpdir, 'test_document.log')
        Document("test_document", tmpdir.strpath)
        assert True

    def test_read_lines(self, tmpdir):
        move_to_temp(tmpdir, 'test_document.log')
        document = Document("test_document", tmpdir.strpath)
        assert len(document._lines)

    def test_read_errors(self, tmpdir):
        move_to_temp(tmpdir, 'test_document.log')
        document = Document("test_document", tmpdir.strpath)
        assert len(document.get_errors()) == 1

    def test_read_warnings(self, tmpdir):
        move_to_temp(tmpdir, 'test_document.log')
        document = Document("test_document", tmpdir.strpath)
        assert len(document.get_warnings()) == 5

    def test_paths(self, tmpdir):
        move_to_temp(tmpdir, 'test_document.log')
        document = Document("test_document", tmpdir.strpath)
        pdf_path = os.path.join(tmpdir.strpath, 'test_document.pdf')
        log_path = os.path.join(tmpdir.strpath, 'test_document.log')
        assert document.pdf_path() == pdf_path
        assert document.log_path() == log_path

