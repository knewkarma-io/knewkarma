#!/bin/bash

# Function to check if the version argument is provided
check_version_argument() {
  if [ -z "$1" ]; then
    echo "Usage: $0 <version>"
    exit 1
  fi
}

# Function to extract version parts (major, minor, patch)
extract_version_parts() {
  VERSION=$1
  IFS='.' read -r -a VERSION_PARTS <<< "$VERSION"
  MAJOR="${VERSION_PARTS[0]}"
  MINOR="${VERSION_PARTS[1]}"
  PATCH="${VERSION_PARTS[2]}"
}

# Function to get the absolute path of the current directory
get_script_dir() {
  SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
}

# Function to define absolute file paths
define_file_paths() {
  VERSION_PY="$SCRIPT_DIR/src/knewkarma/meta/version.py"
  PYPROJECT_TOML="$SCRIPT_DIR/pyproject.toml"
}

# Function to check if files exist
check_files_exist() {
  if [ ! -f "$VERSION_PY" ]; then
    echo "Error: $VERSION_PY not found!"
    exit 1
  fi

  if [ ! -f "$PYPROJECT_TOML" ]; then
    echo "Error: $PYPROJECT_TOML not found!"
    exit 1
  fi
}

# Function to update version in version.py
update_version_py() {
  sed -i.bak "s/major: tuple\[int, str\] = [0-9]\+/major: tuple[int, str] = $MAJOR/" "$VERSION_PY"
  sed -i.bak "s/minor: tuple\[int, str\] = [0-9]\+/minor: tuple[int, str] = $MINOR/" "$VERSION_PY"
  sed -i.bak "s/patch: tuple\[int, str\] = [0-9]\+/patch: tuple[int, str] = $PATCH/" "$VERSION_PY"
  sed -i.bak "s/full: str = \"[0-9]\+\.[0-9]\+\.[0-9]\+\"/full: str = \"$MAJOR.$MINOR.$PATCH\"/" "$VERSION_PY"
  sed -i.bak "s/release: str = \"[0-9]\+\.[0-9]\+\"/release: str = \"$MAJOR.$MINOR\"/" "$VERSION_PY"
}

# Function to update version in pyproject.toml
update_pyproject_toml() {
  sed -i.bak "s/version = \".*\"/version = \"$VERSION\"/" "$PYPROJECT_TOML"
}

# Function to clean up backup files created by sed
cleanup_backup_files() {
  rm "${VERSION_PY}.bak"
  rm "${PYPROJECT_TOML}.bak"
}

# Main function
main() {
  check_version_argument "$1"
  extract_version_parts "$1"
  get_script_dir
  define_file_paths
  check_files_exist
  update_version_py
  update_pyproject_toml
  cleanup_backup_files
  echo "Version updated to $VERSION in $VERSION_PY and $PYPROJECT_TOML"
}

# Call the main function with the version argument
main "$1"
