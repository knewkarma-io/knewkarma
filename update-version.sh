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
VERSION_PY="$SCRIPT_DIR/src/knewkarma/meta/version.py"
PYPROJECT_TOML="$SCRIPT_DIR/pyproject.toml"

# Check if files exist
if [ ! -f "$VERSION_PY" ]; then
  echo "Error: $VERSION_PY not found!"
  exit 1
fi

if [ ! -f "$PYPROJECT_TOML" ]; then
  echo "Error: $PYPROJECT_TOML not found!"
  exit 1
fi

# Update version in src/knewkarma/version.py
sed -i.bak "s/major: tuple\[int, str\] = [0-9]\+/major: tuple[int, str] = $MAJOR/" "$VERSION_PY"
sed -i.bak "s/minor: tuple\[int, str\] = [0-9]\+/minor: tuple[int, str] = $MINOR/" "$VERSION_PY"
sed -i.bak "s/patch: tuple\[int, str\] = [0-9]\+/patch: tuple[int, str] = $PATCH/" "$VERSION_PY"
sed -i.bak "s/full: str = \"[0-9]\+\.[0-9]\+\.[0-9]\+\"/full: str = \"$MAJOR.$MINOR.$PATCH\"/" "$VERSION_PY"
sed -i.bak "s/release: str = \"[0-9]\+\.[0-9]\+\"/release: str = \"$MAJOR.$MINOR\"/" "$VERSION_PY"

# Update version in pyproject.toml
sed -i.bak "s/version = \".*\"/version = \"$VERSION\"/" "$PYPROJECT_TOML"

# Clean up backup files created by sed
rm "${VERSION_PY}.bak"
rm "${PYPROJECT_TOML}.bak"

echo "Version updated to $VERSION in $VERSION_PY and $PYPROJECT_TOML"
