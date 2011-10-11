#!/bin/sh

make html
cd ../../docs-openportfolio
git clean -dxf
cp -r ../openportfolio/sphinx/_build/html/* .
touch .nojekyll
git add .nojekyll
git add *
git commit -m "Updated docs"
git push origin gh-pages
