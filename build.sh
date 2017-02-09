#!/bin/bash

function print_usage {
  echo -e "Usage: build.sh <tarball>\n"
  exit 1
}

tarball="$1"
if [ -z "$tarball" ]; then
  echo -e "<tarball> must be specified!\n"
  print_usage
fi
if [ ! -f "$tarball" ]; then
  echo "Tarball does not exist at $tarball"
  exit 1
fi

hash rpmbuild 2>/dev/null || { echo >&2 "rpmbuild must be installed! aborting."; exit 1; }

set -e

mkdir -p tmp/{SOURCES,SPECS,BUILD,RPMS}

cp $tarball tmp/SOURCES/
cp services/*.service tmp/SOURCES/
pushd tmp
rpmbuild --define "_topdir `pwd`" -bb "../accumulo.spec"
popd

mv tmp/RPMS/x86_64/accumulo-*.rpm testing/
rm -rf tmp/

echo "RPM was created and moved to testing/ directory"
