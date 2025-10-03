import subprocess
import tempfile
import shutil
from pathlib import Path
import pytest

SCRIPT = "fix-bib"
TEST_DIR = Path("test")
INPUT_DIR = TEST_DIR / "input"
EXPECTED_DIR = TEST_DIR / "expected"
RESOURCES_DIR = TEST_DIR / "resources-unused"


def run_fix_bib(args, stdin_input=None):
    """Run fix-bib with given arguments."""
    cmd = [SCRIPT] + args
    result = subprocess.run(
        cmd,
        input=stdin_input,
        capture_output=True,
        text=True
    )
    return result


def compare_files(file1, file2):
    """Compare two files and return True if identical."""
    with open(file1) as f1, open(file2) as f2:
        return f1.read() == f2.read()


@pytest.mark.parametrize("test_name,args,stdin_input,tex_file", [
    ("test-noargs-1", [], None, None),
    ("test-noargs-2", [], None, None),
    ("test-noargs-3", [], None, None),
    ("test-sort-1", ["-s"], None, None),
    ("test-sort-2", ["-s"], None, None),
    ("test-sort-3", ["-s"], None, None),
    ("test-todo-1", ["-t"], None, None),
    ("test-names-1", ["-n"], None, None),
    ("test-filter-1", ["-f"], None, None),
    ("test-unused-1", ["-u", "-d", str(RESOURCES_DIR)], None, None),
    ("test-interactive-1", ["-iX"], "10.1234/567890\n", None),
    ("test-keys-1", ["-k"], None, "test-keys-1.tex"),
    ("test-keys-2", ["-k"], None, "test-keys-2.tex"),
    ("test-keys-3", ["-k"], None, "test-keys-3.tex"),
    ("test-keys-4", ["-k"], None, "test-keys-4.tex"),
    ("test-lookup-1", ["-l"], None, None),
    ("test-lookup-2", ["-l"], None, None),
    ("test-replace-1", ["-lr"], None, None),
    ("test-replace-2", ["-lr"], None, None),
    ("test-mark-1", ["-m"], None, None),
])
def test_fix_bib(test_name, args, stdin_input, tex_file):
    """Parameterized test for all fix-bib test cases."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        tmpdir = None

        try:
            # Handle tests that need a temporary directory for .tex files
            if tex_file:
                tmpdir = tempfile.mkdtemp()
                shutil.copy(INPUT_DIR / tex_file, tmpdir)
                args = args + ["-d", tmpdir]

            # Run fix-bib
            run_fix_bib(args + ["-o", tmp.name, str(INPUT_DIR / f"{test_name}.bib")], stdin_input)

            # Compare output .bib file
            assert compare_files(tmp.name, EXPECTED_DIR / f"{test_name}.bib")

            # Compare .tex file if applicable
            if tex_file:
                assert compare_files(Path(tmpdir) / tex_file, EXPECTED_DIR / tex_file)

        finally:
            Path(tmp.name).unlink()
            if tmpdir:
                shutil.rmtree(tmpdir)
