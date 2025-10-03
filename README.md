# fix-bib

A tool to clean up and manage BibTeX files according to Flix contributor conventions.

## Installation

### Using pipx

```bash
pipx install git+https://github.com/mlutze/fix-bib.git
```

Or install from a local clone:

```bash
pipx install .
```

## Options

```
usage: fix-bib [-h] [-d DIR] [-f] [-i] [-k] [-l] [-m] [-n] [-o OUTPUT] [-r]
               [-s] [-t] [-u]
               bib_file

positional arguments:
  bib_file              Path to the BibTeX file to process

options:
  -h, --help            Show this help message and exit
  -d DIR, --dir DIR     Specify a directory for .tex files (default: current directory)
  -f, --filter          Filter down to required fields only
  -i, --interactive     Run in interactive mode for manual corrections
  -k, --keys            Modify entry keys based on author/year convention
  -l, --lookup          Look up citations via CrossRef to complete metadata
  -m, --mark            Mark transformed entries with a comment
  -n, --names           Format author names consistently
  -o OUTPUT, --output OUTPUT
                        Specify an output file (default: in-place)
  -r, --replace         Replace existing fields with CrossRef fields (use with -l)
  -s, --sort            Sort entries by citation key
  -t, --todo            Mark required fields with TODO comments
  -u, --unused          Remove unused entries (requires .tex files in -d)
```
