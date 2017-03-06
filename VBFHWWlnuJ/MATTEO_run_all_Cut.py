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
parser.add_option('--batchMode', action="store_true",dest="batchMode",default=False)
parser.add_option('--vbf', action="store_true",dest="VBF_process",default=True)
parser.add_option('--pseudodata', action="store_true",dest="pseudodata",default=False)
parser.add_option('--lumi', action="store",type="float",dest="lumi",default=2300.0)
parser.add_option('--CrossCuts', action="store_true",dest="CrosCuts",default=True)
parser.add_option('--NoOutFile', action="store_true",dest="NoOutFile",default=True)

(options, args) = parser.parse_args()

currentDir = os.getcwd();


########################################################
#### Global Variable Definition
########################################################
samples=["BulkGraviton","Higgs"];
lumi_str=str("%.0f"%options.lumi);
## DeltaEta Cut
#DEta_values=[0.0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0,2.25,2.5,2.75,3.0];
#DEta_values=[0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0];
DEta_values=[0.0];
   
# Mjj Cut
#DMjj_values=[0.0,25.0,50.0,75.0,100.0,125.0,150.0,175.0,200.0,225.0,250.0,275.0,300.0,325.0];
#DMjj_values=[0.0,20.0,40.0,60.0,80.0,100.0,120.0,140.0,160.0,180.0,200.0,220.0,240.0,260.0,280.0,300.0,320.0,340.0];
DMjj_values=[500.0,520.0,540.0,560.0,580.0,600.0];









########################################################
#### Function Definiton
########################################################


def print_lined_string_File(in_string_vector,out_fileName):
    
    offset=3;

    s_number=0;
    for t in in_string_vector:
        s_number=s_number+1;
    
    lenght=0;
    for i in in_string_vector:
        tmp_lenght=len(i);
        if tmp_lenght>lenght:
           lenght=tmp_lenght;
    total_lenght=int(lenght*1.40)
    if total_lenght > 140:
       total_lenght=140;


        
    line_empty="\n";
    line_zero=""
    for k in range(offset):
        line_zero=line_zero+" ";
    
    out_file=open(out_fileName,'a');
    out_file.write("\n"+line_empty);
    out_file.write("\n"+line_empty);
    print line_empty
    print line_empty
    z=0;
    for i in in_string_vector:
        if z:
          
           print_string=line_zero+i;
           out_file.write("\n"+print_string);
           print print_string
        else:
           tmp_len=len(i);
           pos=int((total_lenght-tmp_len)/2);
           tmp_final_space="";
           for k in range(pos):
               tmp_final_space=tmp_final_space+"-";
           
           if not i==" ":
               print_string=tmp_final_space+" "+i+" "+tmp_final_space;
           else:
               print_string=tmp_final_space+"---"+tmp_final_space;
           out_file.write("\n"+line_empty);
           out_file.write("\n"+line_empty);
           out_file.write("\n"+print_string);
           out_file.write("\n"+line_empty);
           
           print line_empty
           print line_empty
           print print_string
           print line_empty
           
           z=1;
    
        
    out_file.write("\n"+line_empty);
    print line_empty
    
    final_line="";
    for k in range(total_lenght+1):
        final_line=final_line+"-";
    
    out_file.write("\n"+final_line);
    out_file.write("\n"+line_empty);
    out_file.close();
    print final_line
    print line_empty









def print_boxed_string_File(in_string_vector,out_file_name):
    
    offset_1=3;
    offset_2=4;
    s_number=0;
    t=0;
    for t in in_string_vector:
        s_number=s_number+1;
    
    lenght=0;
    i=0;
    for i in in_string_vector:
        tmp_lenght=len(i);
        if tmp_lenght>lenght:
           lenght=tmp_lenght;
    total_lenght=int(lenght*1.30)
    if total_lenght > 140:
       total_lenght=140;
    line_ext="";
    line_in="";
    zero_space="";
    i=0;
    for i in range(offset_1):
        line_ext=line_ext+" ";
        line_in=line_in+" ";
    i=0;
    for i in range(offset_2):
        zero_space=zero_space+" ";
    line_ext=line_ext+" ";
    
    i=0;
    for i in range(total_lenght):
        line_ext=line_ext+"-";
        
    line_empty=line_in+"|";
    for i in range(total_lenght):
        line_empty=line_empty+" ";
    line_empty=line_empty+"|";
    
    out_file=open(out_file_name,'a');
    out_file.write("\n");
    out_file.write("\n");
    out_file.write("\n");
    out_file.write("\n"+line_ext);
    out_file.write("\n"+line_empty);
    
    print "\n\n"
    print line_ext
    print line_empty
    
    z=0;
    for i in in_string_vector:
        if z:
           tmp_len=len(i);
           tmp_final_space=""
           for k in range(total_lenght-offset_2-tmp_len):
               tmp_final_space=tmp_final_space+" ";
           print_string=line_in+"|"+zero_space+i+tmp_final_space+"|"
           out_file.write("\n"+print_string);
           print print_string
         
        else:
           tmp_len=len(i);
           tmp_final_space=""
           add=int((total_lenght-tmp_len)/2)
           for k in range(add):
               tmp_final_space=tmp_final_space+" ";
           add_line="";
           if (2*add+tmp_len)<total_lenght:
              add_line=" ";
         
           print_string=line_in+"|"+tmp_final_space+i+tmp_final_space+add_line+"|"
           #out_file.write("\n"+line_empty
           out_file.write("\n"+print_string);
           out_file.write("\n"+line_empty);
           
           print print_string
           print line_empty
           
           z=1;
    
    if (s_number-1): 
       out_file.write("\n"+line_empty);
       print line_empty
    out_file.write("\n"+line_ext);
    out_file.write("\n");
    out_file.write("\n");
    out_file.close();
    print line_ext
    print "\n\n"











########################################################
#### Main Code
########################################################
if __name__ == '__main__':
    
    run2_dir="output/run2";
    if not os.path.isdir(run2_dir):
           pd0 = subprocess.Popen(['mkdir',run2_dir]);
           pd0.wait();
    
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
    
    outputFileName=ControlP_Dir_2+"/ControlPlotsExecuted.txt";
    outputFile=open(outputFileName,'w');
    outputFile.write("\nStore what's done in ControlPlots Making\n\n");
    outputFile.close();
       
    
    
       
    
    
    
    # Count number of DeltaEtajj Cuts
    n_eta=0;
    i=0;
    for i in DEta_values:
        n_eta=n_eta+1;
        print "Deta: %f \t\t n_eta: %.0f"%(i,n_eta)
    n_eta=int(n_eta);
    
    
    
    
    # Count number of Mjj Cuts
    n_mjj=0;
    i=0;
    for i in DMjj_values:
        n_mjj=n_mjj+1;
        print "DMjj: %f \t\t n_mjj: %.0f"%(i,n_mjj)
        
    n_mjj=int(n_mjj);
    
       
       
       
    # Store all cuts in a Vector: index 0 -> DEltaEta Cut
    #                             index 1 -> Mjj Cut
    if options.CrosCuts:
       #print "\nCROSS CUTS\n"
       i=j=0;
       range_value=int((n_mjj*n_eta));
       #print range_value
       VBF_cut_values=[0.0 for i in range(range_value)];
       #print "\n"
       tmp_string=["CROSS CUTS",
                   " ",
                   "N DEta Cuts: %.0f"%(n_eta),
                   " ",
                   "N Mjj Cuts: %.0f"%(n_mjj),
                   " ",
                   "Total Cuts Number: %.0f"%(range_value)];
       print_boxed_string_File(tmp_string,outputFileName);
       
       i=j=0;
       for i in range(n_mjj):
           for j in range(n_eta):
               i=int(i);
               j=int(j);
               tmp=int(i*(n_eta)+j);
               VBF_cut_values[tmp]=[float("%1.3f"%DEta_values[j]),float("%.1f"%DMjj_values[i])];
           
      
      
              
    else:
       range_value=int(n_mjj+n_eta-1);
       tmp_string=["SINGLE CUTS",
                   " ",
                   "N DEta Cuts: %.0f"%(n_eta),
                   " ",
                   "N Mjj Cuts: %.0f"%(n_mjj),
                   " ",
                   "Total Cuts Number: %.0f"%(range_value)];
                   
       print_boxed_string_File(tmp_string,outputFileName);
       
       i=j=0;
       
       VBF_cut_values=[0.0 for i in range(range_value)];          

       i=j=0;
       for i in range(n_eta):
           VBF_cut_values[i]=[float("%1.3f"%DEta_values[i]),0.0];
          
       for j in range(n_mjj-1):
           VBF_cut_values[n_eta+j]=[0.0,float("%.1f"%DMjj_values[j+1])];
       
       
       

       

    # Check the CutsVector
    
    i=0;
    
    tmp_vector=[0.0 for i in range(range_value+4)];
    i=0;
    for i in range(range_value):
        i=int(i);
        tmp=VBF_cut_values[i];
        DEta_tmp=tmp[0];
        Mjj_tmp=tmp[1];
        DEta_local=float(DEta_tmp);
        Mjj_local=float(Mjj_tmp);
        tmp_string=" %.0f)     DEta: %1.3f    Mjj: %.1f\n"%((i+1),DEta_local,Mjj_local);
        tmp_vector[i+4]=tmp_string;

    tmp_vector[0]="Cuts Values Vector";
    tmp_vector[2]=" ";
    tmp_vector[1]="Total CutsNumber: %.0f"%range_value;
    tmp_vector[3]=" ";
    
                    
    
    print_lined_string_File(tmp_vector,outputFileName);   
    
       
    CuTfileName=ControlP_Dir_2+"/CutValues.txt";
    CuTfile=open(CuTfileName,'w+');
    
    i=0;
    for i in range(range_value):
        
        # Get the value of Deta and Mjj 
        i=int(i);
        tmp=VBF_cut_values[i];
        DEta_local=float("%1.3f"%tmp[0]);
        Mjj_local=float("%.1f"%tmp[1]);
        
        if (DEta_local==0.0 and Mjj_local==0.0):
           nJetsCut_value=0.0;
        else:
           nJetsCut_value=1.0;
        
        # Erase Directory if any and  then make it
        ControlP_Dir_3=ControlP_Dir_2+"/Deta%1.3f_Mjj%.0f_NJ%.0f"%(DEta_local,Mjj_local,nJetsCut_value);
        CuTfile.write("%f %f %f\n"%(DEta_local,Mjj_local,nJetsCut_value));
        print ControlP_Dir_3
     
        if os.path.isdir(ControlP_Dir_3):
           pd5 = subprocess.Popen(['rm','-r',ControlP_Dir_3]);
           pd5.wait();
    
        pd6 = subprocess.Popen(['mkdir',ControlP_Dir_3]);
        pd6.wait(); 
        
        # Make ControlPlots
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
           

           
           cmd_tmp = "python MATTEO_run_OneCut_ControlPlots.py --DEtaCut %f --MjjCut %f --nJetsCut %f --dir %s --sampleUsed 1 --channel %s"%(DEta_local,Mjj_local,nJetsCut_value,ControlP_Dir_3,options.channel);
           cmd=cmd_tmp+" > "+log_file;
           outScript.write("\n"+cmd);
           #outScript.write("\n"+'rm *.out');
           outScript.close();
           
           
           tmp_run_command=currentDir+"/"+fn+".sh";
           pBM1 = subprocess.Popen(['chmod','777',tmp_run_command]);
           pBM1.wait();
           
           pBM2 = subprocess.Popen(['bsub','-q','1nh','-cwd',currentDir,tmp_run_command]);
           pBM2.wait();
           
           #os.system("chmod 777 "+currentDir+"/"+fn+".sh");
           #os.system("bsub -q cmscaf1nd -cwd "+currentDir+" "+currentDir+"/"+fn+".sh");



        else:
           DEta_local_str=str(DEta_local);
           Mjj_local_str=str(Mjj_local);
           nJetsCut_value_str=str(nJetsCut_value);
              
           pMCP = subprocess.Popen(['python','MATTEO_run_OneCut_ControlPlots.py','--DEtaCut',DEta_local_str,'--MjjCut',Mjj_local_str,'--nJetsCut',nJetsCut_value_str,'--dir',ControlP_Dir_3,'--sampleUsed','1','--channel',options.channel]);
           pMCP.wait();

           
    CuTfile.close();
    

