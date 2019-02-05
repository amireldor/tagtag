import pytest
from taggat.database.inifile import IniFileDatabase
from os.path import join
from collections import Counter  # tag order is not always promised


@pytest.fixture
def db(tmpdir):
    db = IniFileDatabase(join(tmpdir, 'tagtag.db.txt'))
    return db


def test_assigning_tags_to_file(db):
    filename = 'file1.txt'
    tags = ['one', 'two', 'three']
    db.tag(filename, tags)
    assert db.files[filename] == tags


def test_non_existent_file(db):
    with pytest.raises(KeyError):
        db.files['nothing.txt']


def test_reassigning_tags_to_File(db):
    filename = 'file1.txt'
    tags_before = ['one', 'two']
    tags_after = ['three', 'four']

    db.tag(filename, tags_before)
    assert db.files[filename] == tags_before

    db.tag(filename, tags_after)
    assert db.files[filename] == tags_after


def test_merging_tags(db):
    filename = 'file1.txt'
    tags1 = ['one', 'two']
    tags2 = ['three', 'four']

    db.tag(filename, tags1)
    db.merge_tags(filename, tags2)

    assert Counter(db.files[filename]) == Counter(tags1 + tags2)


def test_clear_tags(db):
    filename = 'file1.txt'
    tags = ["it's", "not", "you"]
    expected = ["it's", "you"]
    db.tag(filename, tags)
    db.clear_tags(filename, ["not"])
    assert Counter(db.files[filename]) == Counter(expected)


def test_multiple_files_with_different_tags(db):
    file1 = 'file1.txt'
    file2 = 'document.txt'
    db.tag(file1, ["hi"])
    db.tag(file2, ["hoi", "ho"])
    assert db.files[file1] == ["hi"]
    assert db.files[file2] == ["hoi", "ho"]


def test_saving_and_loading_to_file(db, tmpdir):
    filename = 'file1.txt'
    tags = ['one', 'two', 'three']
    tmp_db_path = join(tmpdir, 'tmp_db.txt')
    db.tag(filename, tags)
    db.write(tmp_db_path)

    other_db = IniFileDatabase(join(tmpdir, tmp_db_path))
    assert other_db.files[filename] == tags
