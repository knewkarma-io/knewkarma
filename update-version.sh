#!/bin/bash

# Check if version argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <version>"
  exit 1
fi

# Extract major, minor, and patch from version argument
VERSION=$1
IFS='.' read -r -a VERSION_PARTS <<< "$VERSION"
MAJOR="${VERSION_PARTS[0]}"
MINOR="${VERSION_PARTS[1]}"
PATCH="${VERSION_PARTS[2]}"

# Get the absolute path of the current directory
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Define absolute file paths
VERSION_PY="$SCRIPT_DIR/knewkarma/version.py"
PYPROJECT_TOML="$SCRIPT_DIR/pyproject.toml"
SNAPCRAFT_YML="$SCRIPT_DIR/snapcraft.yaml"  # Corrected to .yaml

# Print the current directory and the files in it for debugging
echo "Current directory: $SCRIPT_DIR"
echo "Files in the current directory:"
ls -la "$SCRIPT_DIR"

# Check if files exist
if [ ! -f "$VERSION_PY" ]; then
  echo "Error: $VERSION_PY not found!"
  exit 1
fi

if [ ! -f "$PYPROJECT_TOML" ]; then
  echo "Error: $PYPROJECT_TOML not found!"
  exit 1
fi

if [ ! -f "$SNAPCRAFT_YML" ]; then
  echo "Error: $SNAPCRAFT_YML not found!"
  exit 1
fi

# Update version in knewkarma/version.py
sed -i.bak "s/\(major: str = \)\"[^\"]*\"/\1\"$MAJOR\"/" "$VERSION_PY"
sed -i.bak "s/\(minor: str = \)\"[^\"]*\"/\1\"$MINOR\"/" "$VERSION_PY"
sed -i.bak "s/\(patch: str = \)\"[^\"]*\"/\1\"$PATCH\"/" "$VERSION_PY"

# Update version in pyproject.toml
sed -i.bak "s/version = \".*\"/version = \"$VERSION\"/" "$PYPROJECT_TOML"

# Update version in snapcraft.yaml
sed -i.bak "s/version: .*/version: $VERSION/" "$SNAPCRAFT_YML"

# Clean up backup files created by sed
rm "${VERSION_PY}.bak"
rm "${PYPROJECT_TOML}.bak"
rm "${SNAPCRAFT_YML}.bak"

echo "Version updated to $VERSION in $VERSION_PY, $PYPROJECT_TOML, and $SNAPCRAFT_YML"
