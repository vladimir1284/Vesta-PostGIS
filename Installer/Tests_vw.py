'''
Created on 16/04/2013

@author: vladimir
'''
import subprocess

level_IIIs = subprocess.getoutput('ls ../products/V*').split('\n')
for filename in level_IIIs:
    cmd_str = 'python Vesta-PostGIS.py --log=error -s=CCSB -f=../products/'+filename
    print subprocess.getoutput(cmd_str)