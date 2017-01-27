import os,commands
import sys
from optparse import OptionParser
import subprocess





import glob
import math
import array
import ROOT
import ntpath




from array import array
from datetime import datetime



###########################################################################################
######## PARSER OPTIONS
###########################################################################################

parser = OptionParser()

parser.add_option('--channel', action="store", type="string", dest="channel", default="em")
parser.add_option('--ntuple', action="store", type="string", dest="ntuple", default="WWTree_22sep_jecV7_lowmass")
parser.add_option('--lumi', action="store", type="float", dest="lumi", default="2300")
parser.add_option('--scalewNLO', action="store", type="float", dest="scalewNLO", default="1.21")
parser.add_option('--nodata', action='store_true', dest='nodata', default=False)
parser.add_option('--inverse', action='store_true', dest='inverse', default=False)
parser.add_option('--sampleUsed', action="store", type="string", dest="sampleUsed", default="1")
#parser.add_option('--scaleTTB', action='store_true', dest='scaleTTB', default=False)
(options, args) = parser.parse_args()
currentDir = os.getcwd();








###########################################################################################
######## GLOBAL VARIABLE DEFINITION
###########################################################################################

channel=options.channel;
ntuple=options.ntuple;
lumi=options.lumi;
scalewNLO=options.scalewNLO;
sampleUsed=options.sampleUsed;








###########################################################################################
######## SAMPLE DEFINITION
###########################################################################################      
BulkGraviton_xsec=[0.177400,0.0331548,0.008993];
VBF_BulkGraviton_xsec=[0.01089,0.00217,0.000655];
Higgs_xsec=[0.33639,0.06765];
VBF_Higgs_xsec=[0.03354,0.02375];

xsec_BulkGraviton=[0.177400,0.0331548,0.008993];
xsec_VBF_BulkGraviton=[0.01089,0.00217,0.000655];
xsec_Higgs=[0.33639,0.06765];
xsec_VBF_Higgs=[0.03354,0.02375];
		    
NumEntriesBefore_BulkGraviton=[49600,50000,50000];
NumEntriesBefore_VBF_BulkGraviton=[50000,50000,50000];
NumEntriesBefore_Higgs=[399600,400000];
NumEntriesBefore_VBF_Higgs=[398400,400000];
		    
ScaleFactor_BulkGraviton=[900,2000,6000];
#ScaleFactor_BulkGraviton=[900,2000,6000];
ScaleFactor_Higgs=[25,120]

used=options.sampleUsed;
i=0;
used_sample=[0 for i in range(len(used))];

i=0;
for i in range(len(used)):
    used_sample[i]=int(used[i]);

sampleValue_tmp =[["BulkGraviton","BG_600",600,xsec_BulkGraviton[0],NumEntriesBefore_BulkGraviton[0],ScaleFactor_BulkGraviton[0]],
                  ["BulkGraviton","BG_800",800,xsec_BulkGraviton[1],NumEntriesBefore_BulkGraviton[1],ScaleFactor_BulkGraviton[1]],
                  ["BulkGraviton","BG_1000",1000,xsec_BulkGraviton[2],NumEntriesBefore_BulkGraviton[2],ScaleFactor_BulkGraviton[2]],
                  ["Higgs","H_650",650,xsec_Higgs[0],NumEntriesBefore_Higgs[0],ScaleFactor_Higgs[0]],
                  ["Higgs","H_1000",1000,xsec_Higgs[1],NumEntriesBefore_Higgs[1],ScaleFactor_Higgs[1]]];
              
              
sampleValue_VBF_tmp =[["BulkGraviton","VBF_BG_600",600,xsec_VBF_BulkGraviton[0],NumEntriesBefore_VBF_BulkGraviton[0],ScaleFactor_BulkGraviton[0]],
                      ["BulkGraviton","VBF_BG_800",800,xsec_VBF_BulkGraviton[1],NumEntriesBefore_VBF_BulkGraviton[1],ScaleFactor_BulkGraviton[1]],
                      ["BulkGraviton","VBF_BG_1000",1000,xsec_VBF_BulkGraviton[2],NumEntriesBefore_VBF_BulkGraviton[2],ScaleFactor_BulkGraviton[2]],
                      ["Higgs","VBF_H_650",650,xsec_VBF_Higgs[0],NumEntriesBefore_VBF_Higgs[0],ScaleFactor_Higgs[0]],
                      ["Higgs","VBF_H_1000",1000,xsec_VBF_Higgs[1],NumEntriesBefore_VBF_Higgs[1],ScaleFactor_Higgs[1]]];
                  
                  
                  
                  
                  
i=j=0;
for i in used_sample:
    j=j+1;

Total_Number_Sample_Used=j;
i=0;
sampleValue = [0 for i in range(Total_Number_Sample_Used)];

i=0;
sampleValue_VBF = [0 for i in range(Total_Number_Sample_Used)]
i=0;

for i in range(Total_Number_Sample_Used):  
    sampleValue[i]=sampleValue_tmp[used_sample[i]];
    sampleValue_VBF[i]=sampleValue_VBF_tmp[used_sample[i]];
    

total_sample_value=[sampleValue,sampleValue_VBF];






###########################################################################################
######## FUNCTION DEFINITION
###########################################################################################


def print_lined_string_File(in_string_vector,out_file):
    
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
    
    print final_line
    print line_empty









def print_boxed_string_File(in_string_vector,out_file):
    
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
    
    print line_ext
    print "\n\n"








def GetDataFromFile(filename):
    
    f = open(filename,'r');
    lines=f.readlines();
    
    return lines;









###########################################################################################
######## MAIN FUNCTION 
###########################################################################################

if __name__ == '__main__':

    
    ##########################################
    ###### DYRECTORY AND FILE CREATION
    ##########################################
    
    Ntuple_Dir_mm="output/Ntuple_%s"%(ntuple);
    if not os.path.isdir(Ntuple_Dir_mm):
           pd1 = subprocess.Popen(['mkdir',Ntuple_Dir_mm]);
           pd1.wait();


    Lumi_Dir_mm=Ntuple_Dir_mm+"/Lumi_%.0f"%(lumi);
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
    
    
    ControlP_Dir_2=ControlP_Dir_1+"/%s_Channel"%channel;
    if not os.path.isdir(ControlP_Dir_2):
           pd5 = subprocess.Popen(['mkdir',ControlP_Dir_2]);
           pd5.wait(); 
    
    # Make TTBar Directory
    ControlP_Dir_T12=ControlP_Dir_2+"/TTBarCR_12";
    if not os.path.isdir(ControlP_Dir_T12):
           pd6 = subprocess.Popen(['mkdir',ControlP_Dir_T12]);
           pd6.wait();
           
    ControlP_Dir_T21=ControlP_Dir_2+"/TTBarCR_21";
    if not os.path.isdir(ControlP_Dir_T21):
           pd7 = subprocess.Popen(['mkdir',ControlP_Dir_T21]);
           pd7.wait();
           
           
    ControlP_Dir_TSF=ControlP_Dir_2+"/TTBarCR_SF";
    if not os.path.isdir(ControlP_Dir_TSF):
           pd8 = subprocess.Popen(['mkdir',ControlP_Dir_TSF]);
           pd8.wait();
           
    ControlP_Dir_TTB=ControlP_Dir_2+"/TTBarCR";
    if not os.path.isdir(ControlP_Dir_TTB):
           pd9 = subprocess.Popen(['mkdir',ControlP_Dir_TTB]);
           pd9.wait();
    
    # W+Jets SideBand Directory       
    ControlP_Dir_WJ=ControlP_Dir_2+"/WJetsSB";
    if not os.path.isdir(ControlP_Dir_WJ):
           pd10 = subprocess.Popen(['mkdir',ControlP_Dir_WJ]);
           pd10.wait();
           
    # SignalRegion Directory       
    ControlP_Dir_SR=ControlP_Dir_2+"/SignalRegion";
    if not os.path.isdir(ControlP_Dir_SR):
           pd11 = subprocess.Popen(['mkdir',ControlP_Dir_SR]);
           pd11.wait();
           
    
    
    
    
    
    


    
    
    #########################################################
    ######### MAKE OUTPUT FILE
    #########################################################    
    summaryF = ControlP_Dir_2+"/Summary_ControlPlots_%s_Channel.txt"%channel;
    Output_Summary_File=open(summaryF,'w+');
    Output_Summary_File.write("\n\nSUMMARY CONTROL PLOTS %s Channel\n\n"%channel);
    
    tmp_string=["INPUT PARAMETER FOR CONTROL PLOTS MAKING",
                " ",
                "Ntuple: %s"%ntuple,
                " ",
                "Luminosity: %.0f"%lumi,
                " ",
                "Channel: %s"%channel,
                " ",
                "ScaleWNLO: %f"%scalewNLO,
                " ",
                "Sample: %s"%sampleValue[0][0],
                " ",
                "Mass: %.0f"%sampleValue[0][2]]
    
    print_boxed_string_File(tmp_string,Output_Summary_File);
    Output_Summary_File.close();
    
    
    
    
    
    
    
    #########################################################
    ######### MAKE EFFICIENCY TTBAR FILE
    #########################################################
    '''    
    E12 = subprocess.Popen(['python','MATTEO_TTB_epsilon.py','--sampleUsed',sampleUsed,'--channel',channel,'--ntuple',ntuple,'--sumFile',summaryF,'--dir',ControlP_Dir_2]); 
    E12.wait();

    E21 = subprocess.Popen(['python','MATTEO_TTB_epsilon.py','--inverse','--sampleUsed',sampleUsed,'--channel',channel,'--ntuple',ntuple,'--sumFile',summaryF,'--dir',ControlP_Dir_2]);
    E21.wait();
    '''
    # Save in the Output_Efficiency_File_mm -> /TTBarCR_12/ScaleW1.21ScaleT1.0/Efficiency.txt
    # 0 SAMPLE
    # 1 MASS
    # 2 N_A_MC
    # 3 N_B_MC
    # 4 N_A_DATA
    # 5 N_B_DATA
    # 6 EPSILON_MC
    # 7 SIGMA_EPSILON_MC
    # 8 EPSILON_DATA
    # 9 SIGMA_EPSILON_DATA
    # 10 K-FACTOR
    # 11 SIGMA_K_FACTOR
    # 12 SF TTBAR
    # 13 SIGMA_SF_TTBAR
 
    TTBEfficiency12FileName=ControlP_Dir_T12+"/Efficiency.txt";
    TTB_Efficiency12_DataFileVector=GetDataFromFile(TTBEfficiency12FileName);

    TTBEfficiency21FileName=ControlP_Dir_T21+"/Efficiency.txt";
    TTB_Efficiency21_DataFileVector=GetDataFromFile(TTBEfficiency21FileName);
    
    b12_epsilon_data=float(TTB_Efficiency12_DataFileVector[8]);
    b12_epsilon_mc=float(TTB_Efficiency12_DataFileVector[6]);
    Sigma_b12_epsilon_data=float(TTB_Efficiency12_DataFileVector[9]);
    Sigma_b12_epsilon_mc=float(TTB_Efficiency12_DataFileVector[7]);    
    
    b21_epsilon_data=float(TTB_Efficiency21_DataFileVector[8]);
    b21_epsilon_mc=float(TTB_Efficiency21_DataFileVector[6]);
    Sigma_b21_epsilon_data=float(TTB_Efficiency21_DataFileVector[9]);
    Sigma_b21_epsilon_mc=float(TTB_Efficiency21_DataFileVector[7]);
    
    
    #########################################################
    ######### GET THE CORRECT TTBAR SCALE FACTOR
    #########################################################

    SFTTB = subprocess.Popen(['python','MATTEO_TTB_SF.py','--sampleUsed',sampleUsed,'--channel',channel,'--ntuple',ntuple,'--sumFile',summaryF,'--dir',ControlP_Dir_2]);
    SFTTB.wait();

    # Save in the Output_ScaleFactorTrue_File_mm -> /TTBarCR/ScaleFactorTrue.txt
    # 0 SAMPLE
    # 1 MASS
    # 2 N_mc
    # 3 N_data
    # 4 True TTBar ScaleFactor
    # 5 Sigma True TTBar ScaleFactor

    TTBScaleFactorFileName=ControlP_Dir_TTB+"/ScaleFactorTrue.txt";
    
    TTB_TrueSF_DataFileVector=GetDataFromFile(TTBScaleFactorFileName);
    
    TTB_True_ScaleFactor=float(TTB_TrueSF_DataFileVector[4]);
    Sigma_TTB_True_ScaleFactor=float(TTB_TrueSF_DataFileVector[5]);
    
    
    
    
    
    #########################################################
    ######### GET THE WJets SCALE FACTOR
    #########################################################
    InputWJetsFileName=ControlP_Dir_WJ+"/WJ_input.txt";
    InputWJetsFile=open(InputWJetsFileName,'w+');
    #InputWJetsFile.write("%f\n"%);
    InputWJetsFile.write("%f\n"%b12_epsilon_data);
    InputWJetsFile.write("%f\n"%b21_epsilon_data);
    InputWJetsFile.write("%f\n"%b12_epsilon_mc);
    InputWJetsFile.write("%f\n"%b21_epsilon_mc);
    
    InputWJetsFile.write("%f\n"%Sigma_b12_epsilon_data);
    InputWJetsFile.write("%f\n"%Sigma_b21_epsilon_data);
    InputWJetsFile.write("%f\n"%Sigma_b12_epsilon_mc);
    InputWJetsFile.write("%f\n"%Sigma_b21_epsilon_mc);    
    
    InputWJetsFile.write("%f\n"%TTB_True_ScaleFactor);
    InputWJetsFile.write("%f\n"%Sigma_TTB_True_ScaleFactor);
    
    InputWJetsFile.close();
    
    SFWJ = subprocess.Popen(['python','MATTEO_WJets_SF.py','--sampleUsed',sampleUsed,'--channel',channel,'--ntuple',ntuple,'--sumFile',summaryF,'--dir',ControlP_Dir_2,'--inData',InputWJetsFileName]);
    SFWJ.wait();


    # Save the output in -> /WJetsSB/WJets_SideBand_output.txt
    # 0 SAMPLE
    # 1 MASS
    # 2 N_mc
    # 3 N_data
    # 4 WJets ScaleFactor
    # 5 Sigma WJets ScaleFactor
    
    WJScaleFactorFileName=ControlP_Dir_WJ+"/WJets_SideBand_output.txt";
    
    WJ_SF_DataFileVector=GetDataFromFile(WJScaleFactorFileName);
    
    WJ_ScaleFactor=float(WJ_SF_DataFileVector[4]);
    Sigma_WJ_ScaleFactor=float(WJ_SF_DataFileVector[5]);
    
    #########################################################
    ######### MAKE CONTROL PLOTS
    #########################################################
    
    InputControlPlotsFileName=ControlP_Dir_SR+"/SR_input.txt";
    InputControlPlotsFile=open(InputControlPlotsFileName,'w');
    
    InputControlPlotsFile.write("%f\n"%b12_epsilon_data);
    InputControlPlotsFile.write("%f\n"%b21_epsilon_data);
    InputControlPlotsFile.write("%f\n"%b12_epsilon_mc);
    InputControlPlotsFile.write("%f\n"%b21_epsilon_mc);
    
    InputControlPlotsFile.write("%f\n"%Sigma_b12_epsilon_data);
    InputControlPlotsFile.write("%f\n"%Sigma_b21_epsilon_data);
    InputControlPlotsFile.write("%f\n"%Sigma_b12_epsilon_mc);
    InputControlPlotsFile.write("%f\n"%Sigma_b21_epsilon_mc);    
    
    InputControlPlotsFile.write("%f\n"%TTB_True_ScaleFactor);
    InputControlPlotsFile.write("%f\n"%Sigma_TTB_True_ScaleFactor);
       
    InputControlPlotsFile.write("\n%f"%WJ_ScaleFactor);
    InputControlPlotsFile.write("\n%f"%Sigma_WJ_ScaleFactor);
    
    InputControlPlotsFile.close();
    
    SRCP = subprocess.Popen(['python','MATTEO_SignalRegion_CP.py','--sampleUsed',sampleUsed,'--channel',channel,'--ntuple',ntuple,'--sumFile',summaryF,'--dir',ControlP_Dir_2,'--inData',InputControlPlotsFileName]);
    SRCP.wait();

