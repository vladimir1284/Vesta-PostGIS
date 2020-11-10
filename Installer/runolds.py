#!/usr/bin/python
import commands
prods = commands.getoutput('ls products').split('\n')

for prod in prods:
    radarID = prod.split('_')[3]
    commands.getoutput('./Vesta-PostGIS.py -s=%s -f=products/%s' % (radarID, prod))
    print 'done: %s' % prod
