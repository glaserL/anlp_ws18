#!/bin/bash
# initializing repository by downloading required data from git lfs
set -e

# ensure git lfs is installed
git lfs install

# fetches git lfs information
git lfs fetch

# checks out large files to appropriate locations
git lfs checkout

# move pre-commit hook into local .git folder for activation
cp ./hooks/pre-commit.sample ./.git/hooks/pre-commit
