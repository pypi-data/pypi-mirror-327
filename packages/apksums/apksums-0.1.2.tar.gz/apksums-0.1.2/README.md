# APKSums

APKSums is a Python utility for verifying checksums of installed APK files on Alpine Linux systems. It helps ensure the integrity of installed packages by comparing file checksums against the package database.

## Features

- Verify checksums of installed files against the APK database
- Support for both regular files and symbolic links
- Various output modes (normal, silent, changed-only)
- Configurable root directory for checking alternative installations
- Custom checksums file support

## Installation

```bash
# From source
git clone https://github.com/yourusername/apksums.git
cd apksums
pip install .

# Or directly via pip (if published)
pip install apksums
```

## Usage

Basic usage:
```bash
apksums
```

### Command Line Options

```
-s, --silent       Only report errors
-c, --changed      Report changed file list to stdout (implies -s)
-r, --root DIR     Root directory to check (default /)
-m, --md5sums FILE Read list of checksums from file (default /lib/apk/db/installed)
```

### Examples

Check all files with normal output:
```bash
apksums
```

Only show modified files:
```bash
apksums -c
```

Check files in alternative root:
```bash
apksums -r /mnt/rootfs
```

Use custom checksums file:
```bash
apksums -m /path/to/checksums
```

Silent mode (only show errors):
```bash
apksums -s
```

## Output Format

### Normal Mode
```
OK: /bin/ls (from coreutils)
FAILED: /etc/passwd (from shadow)
  Expected: abc123...
  Got: def456...
MISSING: /etc/config (from base-pkg)
```

### Changed Mode (-c)
```
/etc/passwd
/usr/bin/modified-binary
```

## Exit Codes

- 0: All checks passed
- 1: Some files failed verification or are missing

## Development

### Requirements

- Python 3.6+
- pytest (for running tests)

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```
