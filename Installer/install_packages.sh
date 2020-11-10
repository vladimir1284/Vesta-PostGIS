#!/bin/bash
#
# Install vesta-postgis on Centos5 
# Run as root.
#

if [[ $EUID -ne 0 ]]; then
  echo "You must be a root user" 2>&1
  exit 1
fi

cd inst

sh epd_free-7.3-1-rh5-x86.sh -b -p /opt/epd_free-7.3-1-rh5-x86

echo "Extacting PyGreSQL"
tar -xvzf PyGreSQL.tgz

echo "Installing PyGreSQL"
cd PyGreSQL-4.0
/opt/epd_free-7.3-1-rh5-x86/bin/python setup.py install
cd ..
rm -r PyGreSQL-4.0

echo "Extacting pyproj"
tar -xvzf pyproj-1.9.3.tar.gz

echo "Installing pyproj"
cd pyproj-1.9.3
/opt/epd_free-7.3-1-rh5-x86/bin/python setup.py install
cd ..
rm -r pyproj-1.9.3

