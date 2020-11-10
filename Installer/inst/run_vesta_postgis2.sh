#!/bin/bash
#
# Run Vesta|Postgis
#

cd $HOME/vesta_postgis
./vesta_postgis $1 -i -p 5908 -d ./products -s $radar rpga1
