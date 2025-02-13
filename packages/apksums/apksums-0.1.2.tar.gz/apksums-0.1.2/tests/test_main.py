# test_apksums.py
import os
import pytest
from apksums.main import (
    read_installed_db,
    calculate_sha1,
    verify_checksums
)

# Sample test data
SAMPLE_DB_CONTENT = """
P:package1
V:1.0
F:/usr/bin
R:test1
Z:Q1abcdef1234567890
F:/etc
R:test2
Z:Q1xyz789

P:package2
F:/usr/lib
R:testlib
Z:Q1lib123456789
"""

@pytest.fixture
def temp_db_file(tmp_path):
    """Create a temporary database file with test data."""
    db_file = tmp_path / "installed.db"
    db_file.write_text(SAMPLE_DB_CONTENT)
    return db_file

@pytest.fixture
def temp_test_files(tmp_path):
    """Create temporary test files with known content."""
    root = tmp_path / "root"
    root.mkdir()

    # Create test files
    bin_dir = root / "usr" / "bin"
    bin_dir.mkdir(parents=True)
    test1_file = bin_dir / "test1"
    test1_file.write_text("test content 1")

    etc_dir = root / "etc"
    etc_dir.mkdir()
    test2_file = etc_dir / "test2"
    test2_file.write_text("test content 2")

    # Create a symlink
    lib_dir = root / "usr" / "lib"
    lib_dir.mkdir(parents=True)
    testlib_link = lib_dir / "testlib"
    os.symlink("target", testlib_link)

    return root


def test_read_installed_db(temp_db_file):
    """Test reading and parsing the installed database."""
    checksums = read_installed_db(temp_db_file)

    assert len(checksums) == 3
    assert "/usr/bin/test1" in checksums
    assert checksums["/usr/bin/test1"]["package"] == "package1"
    assert checksums["/usr/bin/test1"]["checksum"] == "abcdef1234567890"

def test_calculate_sha1(temp_test_files):
    """Test SHA1 calculation for files and symlinks."""
    # Test regular file
    file_path = temp_test_files / "usr" / "bin" / "test1"
    sha1 = calculate_sha1(file_path)
    assert sha1 is not None

    # Test symlink
    link_path = temp_test_files / "usr" / "lib" / "testlib"
    sha1 = calculate_sha1(link_path)
    assert sha1 is not None

def test_verify_checksums(temp_db_file, temp_test_files):
    """Test checksum verification."""
    class Args:
        root = str(temp_test_files)
        silent = True
        changed = False

    checksums = read_installed_db(temp_db_file)
    result = verify_checksums(checksums, Args())

    # Since our test files won't match the checksums in the sample database,
    # we expect the verification to fail
    assert result == False

def test_missing_file_handling(temp_db_file, temp_test_files):
    """Test handling of missing files."""
    class Args:
        root = str(temp_test_files)
        silent = True
        changed = False

    # Remove a test file
    os.unlink(temp_test_files / "usr" / "bin" / "test1")

    checksums = read_installed_db(temp_db_file)
    result = verify_checksums(checksums, Args())
    assert result == False
