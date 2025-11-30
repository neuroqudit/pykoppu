#!/bin/bash
set -e

# Install build tools
pip install --upgrade build twine

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build
python -m build

# Check
twine check dist/*

echo "Build successful. To publish, run: twine upload dist/*"
