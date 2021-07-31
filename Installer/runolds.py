#!/usr/bin/python
import subprocess
prods = subprocess.getoutput('ls products').split('\n')

for prod in prods:
    radarID = prod.split('_')[3]
    subprocess.getoutput('./Vesta-PostGIS.py -s=%s -f=products/%s' % (radarID, prod))
    print ('done: %s' % prod)
