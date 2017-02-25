#!/bin/bash

set -o errexit -o nounset

if [ "$TRAVIS_BRANCH" != "master" ]
then
  echo "This commit was made against the $TRAVIS_BRANCH and not the master! No deploy!"
  exit 0
fi

rev=$(git rev-parse --short HEAD)

cd html
# Retrieve blockly 
git clone https://github.com/google/blockly.git

git init
git config user.name "gtribello"
git config user.email "gareth.tribello@gmail.com"

git remote add upstream "https://$GH_TOKEN@github.com/gtribello/mathNET.git"
git fetch upstream
git reset upstream/gh-pages

git add -A .
git commit -m "rebuild pages at ${rev}"
git push -q upstream HEAD:gh-pages
