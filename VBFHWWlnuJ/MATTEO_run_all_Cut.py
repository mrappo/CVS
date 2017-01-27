import os,commands
import sys
from optparse import OptionParser
import subprocess

parser = OptionParser()

parser.add_option('-c', '--channel',action="store",type="string",dest="channel",default="em")
parser.add_option('--ntuple', action="store",type="string",dest="ntuple",default="WWTree_22sep_jecV7_lowmass")
parser.add_option('--category', action="store",type="string",dest="category",default="HP")
parser.add_option('--type', action="store",type="string",dest="type",default="")
parser.add_option('--jetalgo', action="store",type="string",dest="jetalgo",default="jet_mass_pr")
parser.add_option('--interpolate', action="store_true",dest="interpolate",default=False)
parser.add_option('--batchMode', action="store_true",dest="batchMode",default=True)
parser.add_option('--vbf', action="store_true",dest="VBF_process",default=True)
parser.add_option('--pseudodata', action="store_true",dest="pseudodata",default=False)
parser.add_option('--lumi', action="store",type="float",dest="lumi",default=2300.0)
parser.add_option('--CrossCuts', action="store_true",dest="CrosCuts",default=True)
#parser.add_option('--SignleCuts', action="store_true",dest="SingleCuts",default=False)
#parser.add_option('--MultipleCuts', action="store_true",dest="MultipleCuts",default=False)
(options, args) = parser.parse_args()

currentDir = os.getcwd();

samples=["BulkGraviton","Higgs"];
lumi_str=str("%.0f"%options.lumi);
########################################################
#### Main Code
########################################################
if __name__ == '__main__':
    
    Ntuple_Dir_mm="output/Ntuple_%s"%(options.ntuple);
    if not os.path.isdir(Ntuple_Dir_mm):
           pd1 = subprocess.Popen(['mkdir',Ntuple_Dir_mm]);
           pd1.wait();


    Lumi_Dir_mm=Ntuple_Dir_mm+"/Lumi_%.0f"%(options.lumi);
    if not os.path.isdir(Lumi_Dir_mm):
           pd2 = subprocess.Popen(['mkdir',Lumi_Dir_mm]);
           pd2.wait();
       


    Cuts_File_Dir_mm="cfg/DataMCComparison_InputCfgFile";
    if not os.path.isdir(Cuts_File_Dir_mm):
           pd3 = subprocess.Popen(['mkdir',Cuts_File_Dir_mm]);
           pd3.wait();
       
  
    
       
    ControlP_Dir_1=Lumi_Dir_mm+"/ControlPlots";
    if not os.path.isdir(ControlP_Dir_1):
           pd4 = subprocess.Popen(['mkdir',ControlP_Dir_1]);
           pd4.wait();  
    
    
    
    ControlP_Dir_2=ControlP_Dir_1+"/%s_Channel"%options.channel;
    if not os.path.isdir(ControlP_Dir_2):
           pd4b = subprocess.Popen(['mkdir',ControlP_Dir_2]);
           pd4b.wait();
    
    
       
    ## DeltaEta Cut
    #DEta_values=[0.0,1.0,1.5,2.0];
    DEta_values=[0.0,1.0,1.5,2.0,2.5,3.0,3.5,4.0];
    #DEta_values=[0.0,1.0];
    
    # Mjj Cut
    DMjj_values=[0.0,100.0,150.0,200.0,250.0,300.0,350.0,400.0];
    #DMjj_values=[0.0,100,200,300];
    
       
    n_eta=0;
    n_mjj=0;
    
    # Count number of DeltaEtajj Cuts
    i=0;
    for i in DEta_values:
        n_eta=n_eta+1;
        print "Deta: %f \t\t n_eta: %.0f"%(i,n_eta)
    
    
    # Count number of Mjj Cuts
    i=0;
    for i in DMjj_values:
        n_mjj=n_mjj+1;
        print "DMjj: %f \t\t n_mjj: %.0f"%(i,n_mjj)
    
    
    n_mjj=int(n_mjj);
    n_eta=int(n_eta);
       
       
       
    # Store all cuts in a Vector: index 0 -> DEltaEta Cut
    #                             index 1 -> Mjj Cut
    if options.CrosCuts:
       print "\nCROSS CUTS\n"
       i=j=0;
       range_value=int((n_mjj*n_eta));
       print range_value
       VBF_cut_values=[0.0 for i in range(range_value)];
       print "\n"
       i=j=0;
       if (n_eta<n_mjj):
          for i in range(n_eta):
              for j in range(n_mjj):
                  i=int(i);
                  j=int(j);
                  tmp=int(i*(n_mjj)+j);
                  #print VBF_cut_values[tmp]
                  #print tmp
                  VBF_cut_values[tmp]=[float("%1.3f"%DEta_values[i]),float("%.1f"%DMjj_values[j])];
                  #print VBF_cut_values[tmp]
          
       elif (n_eta>n_mjj):
          for i in range(n_mjj):
              for j in range(n_eta):
                  i=int(i);
                  j=int(j);
                  tmp=int(i*(n_eta)+j);
                  #print VBF_cut_values[tmp]
                  #print "tmp: %.0f\ti: %.0f\tj: %.0f"%(tmp,i,j) 
                  VBF_cut_values[tmp]=[float("%1.3f"%DEta_values[j]),float("%.1f"%DMjj_values[i])];
                  #print VBF_cut_values[tmp]
       else:
          for i in range(n_mjj):
              for j in range(n_eta):
                  i=int(i);
                  j=int(j);
                  tmp=int(i*(n_mjj)+j);
                  #print VBF_cut_values[tmp]
                  #print "tmp: %.0f\ti: %.0f\tj: %.0f"%(tmp,i,j) 
                  VBF_cut_values[tmp]=[float("%1.3f"%DEta_values[j]),float("%.1f"%DMjj_values[i])];
           
           
           
      
              
    else:
       print "\nSINGLE CUTS\n"
       i=j=0;

       range_value=int(n_mjj+n_eta-1);
       VBF_cut_values=[0.0 for i in range(range_value)];          

       i=j=0;
       for i in range(n_eta):
           VBF_cut_values[i]=[float("%1.3f"%DEta_values[i]),0.0];
          
       for j in range(n_mjj-1):
           VBF_cut_values[n_eta+j]=[0.0,float("%.1f"%DMjj_values[j+1])];
       
       
       

       

    # Check the CutsVector
    i=0;
    print "\n\nVector of Cut Values:\n"
    print "Total CutsNumber: %.0f"%range_value
    print "\n"
    for i in range(range_value):
        i=int(i);
        #print i
        #print VBF_cut_values[i]
        tmp=VBF_cut_values[i];
        DEta_tmp=tmp[0];
        Mjj_tmp=tmp[1];
        DEta_local=float(DEta_tmp);
        Mjj_local=float(Mjj_tmp);
        print " %.0f)  DEta: %1.3f \t\t Mjj: %.1f\n"%((i+1),DEta_local,Mjj_local)
        

    
    i=0;
    for i in range(range_value):
        i=int(i);
        tmp=VBF_cut_values[i];
        DEta_local=float("%1.3f"%tmp[0]);
        Mjj_local=float("%.1f"%tmp[1]);
        
        if (DEta_local==0.0 and Mjj_local==0.0):
           nJetsCut_value=0.0;
        else:
           nJetsCut_value=1.0;
        
        ControlP_Dir_3=ControlP_Dir_2+"/Deta%1.3f_Mjj%.0f_NJ%.0f"%(DEta_local,Mjj_local,nJetsCut_value);
        print ControlP_Dir_3
        if os.path.isdir(ControlP_Dir_3):
           pd5 = subprocess.Popen(['rm','-r',ControlP_Dir_3]);
           pd5.wait();
    
        pd6 = subprocess.Popen(['mkdir',ControlP_Dir_3]);
        pd6.wait(); 
        ## BatchMode
        if (options.batchMode==True):
             
           job_dir=ControlP_Dir_3+"/Job";
           if not os.path.isdir(job_dir):
                  pd7 = subprocess.Popen(['mkdir',job_dir]);
                  pd7.wait();
                  
           log_dir=ControlP_Dir_3+"/Log";
           if not os.path.isdir(log_dir):
                  pd8 = subprocess.Popen(['mkdir',log_dir]);
                  pd8.wait();
           log_file=log_dir+"log_Deta%1.3f_Mjj%.0f_NJ%.0f.log"%(DEta_local,Mjj_local,nJetsCut_value);
            
           fn = job_dir+"/job_%1.3f_%.0f_%s"%(DEta_local,Mjj_local,nJetsCut_value);
           outScript = open(fn+".sh","w");
 
           outScript.write('#!/bin/bash');
           outScript.write("\n"+'cd '+currentDir);
           outScript.write("\n"+'eval `scram runtime -sh`');
           outScript.write("\n"+'export PATH=${PATH}:'+currentDir);
           outScript.write("\n"+'echo ${PATH}');
           outScript.write("\n"+'ls');
           

           
           cmd_tmp = "python run_all_ControlPlots.py --DEtaCut %f --MjjCut %f --nJetsCut %f --dir %s"%(DEta_local,Mjj_local,nJetsCut_value,ControlP_Dir_3);
           cmd=cmd_tmp+" > "+log_file;
           outScript.write("\n"+cmd);
           #outScript.write("\n"+'rm *.out');
           outScript.close();

           os.system("chmod 777 "+currentDir+"/"+fn+".sh");
           os.system("bsub -q cmscaf1nd -cwd "+currentDir+" "+currentDir+"/"+fn+".sh");


        else:
           DEta_local_str=str(DEta_local);
           Mjj_local_str=str(Mjj_local);
           nJetsCut_value_str=str(nJetsCut_value);
              
           pMCP = subprocess.Popen(['python','run_all_ControlPlots.py','--DEtaCut',DEta_local_str,'--MjjCut',Mjj_local_str,'--nJetsCut',nJetsCut_value_str,'--dir',ControlP_Dir_3]);
           pMCP.wait();
