import os,commands
import sys
from optparse import OptionParser
import subprocess

parser = OptionParser()


luminosity=[0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0];

########################################################
#### Main Code
########################################################
if __name__ == '__main__':

    lumi=0.0;
    
    for lumi in luminosity:
                   
        pd1 = subprocess.Popen(['python','MATTEO_run_all_Cut.py','--lumi',str(lumi)]);
        pd1.wait();
    
    
