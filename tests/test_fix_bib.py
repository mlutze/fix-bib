import subprocess
import tempfile
import shutil
import sys
from pathlib import Path
import pytest

TEST_DIR = Path(__file__).parent / "data"
INPUT_DIR = TEST_DIR / "input"
EXPECTED_DIR = TEST_DIR / "expected"
RESOURCES_DIR = TEST_DIR / "resources-unused"


def run_fix_bib(args, stdin_input=None):
    """Run fix-bib with given arguments."""
    # Use python -m fix_bib to work in CI environments
    cmd = [sys.executable, "-m", "fix_bib"] + args
    result = subprocess.run(
        cmd,
        input=stdin_input,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"\n=== Command failed with return code {result.returncode} ===")
        print(f"Command: {' '.join(cmd)}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
    return result


def compare_files(file1, file2):
    """Compare two files and return True if identical."""
    with open(file1, encoding='utf-8') as f1, open(file2, encoding='utf-8') as f2:
        content1 = f1.read()
        content2 = f2.read()
        if content1 != content2:
            print(f"\n=== Expected ({file2}) ===")
            print(content2[:500])
            print(f"\n=== Actual ({file1}) ===")
            print(content1[:500])
        return content1 == content2


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
    # Create temp file, close it, and let Python auto-delete on context exit
    with tempfile.NamedTemporaryFile(mode='w', delete=True, suffix='.bib') as tmp:
        tmp_name = tmp.name
        # Close the file so fix-bib can open it (required on Windows)
        tmp.close()

        tmpdir = None
        try:
            # Handle tests that need a temporary directory for .tex files
            if tex_file:
                tmpdir = tempfile.mkdtemp()
                shutil.copy(INPUT_DIR / tex_file, tmpdir)
                args = args + ["-d", tmpdir]

            # Run fix-bib
            run_fix_bib(args + ["-o", tmp_name, str(INPUT_DIR / f"{test_name}.bib")], stdin_input)

            # Compare output .bib file
            assert compare_files(tmp_name, EXPECTED_DIR / f"{test_name}.bib")

            # Compare .tex file if applicable
            if tex_file:
                assert compare_files(Path(tmpdir) / tex_file, EXPECTED_DIR / tex_file)

        finally:
            if tmpdir:
                shutil.rmtree(tmpdir)
