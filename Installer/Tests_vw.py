'''
Created on 16/04/2013

@author: vladimir
'''
import commands

level_IIIs = commands.getoutput('ls ../products/V*').split('\n')
for filename in level_IIIs:
    cmd_str = 'python Vesta-PostGIS.py --log=error -s=CCSB -f=../products/'+filename
    print commands.getoutput(cmd_str)