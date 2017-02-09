#!/bin/bash

function print_usage {
  echo -e "Usage: build.sh <version>\n"
  exit 1
}

version="$1"
if [ -z "$version" ]; then
  echo -e "Version must be specified!\n"
  print_usage
fi

tarball="accumulo-${version}-bin.tar.gz"
if [ ! -f "SOURCES/$tarball" ]; then
  echo "Tarball does not exist at SOURCES/$tarball"
  exit 1
fi
spec="accumulo-${version}.spec"
if [ ! -f "SPECS/$spec" ]; then
  echo "Spec file does not exist at SPECS/$spec"
  exit 1
fi

hash rpmbuild 2>/dev/null || { echo >&2 "rpmbuild must be installed! aborting."; exit 1; }

mkdir -p tmp/{SOURCES,SPECS,BUILD,RPMS}
cp SOURCES/accumulo-${version}-bin.tar.gz tmp/SOURCES/
cp SOURCES/*.service tmp/SOURCES/
pushd tmp
rpmbuild --define "_topdir `pwd`" -bb "../SPECS/${spec}"
popd
