import os,commands
import sys
from optparse import OptionParser
import subprocess
from MATTEO_Functions import run_log,make_latex_table,print_boxed_string_File,print_lined_string_File,SumSquareRelErrors,replace_latex,latex_graph_include,GetDataFromFile






import glob
import math
import array
import ROOT
import ntpath




from array import array
from datetime import datetime

from ROOT import gROOT, TPaveLabel, gStyle, gSystem, TGaxis, TStyle, TLatex, TString, TF1,TFile,TLine, TLegend, TH1D,TH2D,THStack,TChain, TCanvas, TMatrixDSym, TMath, TText, TPad, RooFit, RooArgSet, RooArgList, RooArgSet, RooAbsData, RooAbsPdf, RooAddPdf, RooWorkspace, RooExtendPdf,RooCBShape, RooLandau, RooFFTConvPdf, RooGaussian, RooBifurGauss, RooArgusBG,RooDataSet, RooExponential,RooBreitWigner, RooVoigtian, RooNovosibirsk, RooRealVar,RooFormulaVar, RooDataHist, RooHist,RooCategory, RooChebychev, RooSimultaneous, RooGenericPdf,RooConstVar, RooKeysPdf, RooHistPdf, RooEffProd, RooProdPdf, TIter, kTRUE, kFALSE, kGray, kRed, kDashed, kGreen,kAzure, kOrange, kBlack,kBlue,kYellow,kCyan, kMagenta, kWhite




parser = OptionParser()

parser.add_option('--channel', action="store", type="string", dest="channel", default="em")
parser.add_option('--inData', action="store", type="string", dest="inData", default="WJ_input.txt")
parser.add_option('--ntuple', action="store", type="string", dest="ntuple", default="WWTree_22sep_jecV7_lowmass")
parser.add_option('--lumi', action="store", type="float", dest="lumi", default="2300")
parser.add_option('--scalew', action="store", type="float", dest="scalew", default="1.21")
parser.add_option('--nodata', action='store_true', dest='nodata', default=False)
parser.add_option('--sampleUsed', action="store", type="string", dest="sampleUsed", default="1")
parser.add_option('--sumFile', action="store", type="string", dest="sumFile", default="output.txt")
parser.add_option('--DEtaCut', action="store", type="string", dest="DEtaCut", default="0.0")
parser.add_option('--MjjCut', action="store", type="string", dest="MjjCut", default="0.0")
parser.add_option('--nJetsCut', action="store", type="string", dest="nJetsCut", default="0.0")
parser.add_option('--dir', action="store", type="string", dest="dir", default="")

(options, args) = parser.parse_args()
currentDir = os.getcwd();

###########################################################################################
######## GLOBAL VARIABLE DEFINITION
###########################################################################################

DEtaCut_value=options.DEtaCut;
MjjCut_value=options.MjjCut;
nJetsCut_value=options.nJetsCut;


Events_type_global=["Wjets_Pythia_Events_g",      # 0
                    "Wjets_Herwig_Events_g",      # 1
                    "TTbar_Powegh_Events_g",      # 2
                    "TTbar_MC_Events_g",          # 3
                    "VV_QCD_Events_g",            # 4
                    "WW_EWK_Events_g",            # 5
                    "STop_Events_g",              # 6
                    "All_bkg_Pythia_g",           # 7
                    "All_bkg_Herwig_g",           # 8
                    "Signal_gg_g",                # 9
                    "Signal_VBF_g"];              # 10

number_Events_type=11;



## Incertezze
N_simulatedMC_WJets_global=10152718+5221599+1745914+4041997+1574633+255637+253036; 
                           
N_simulatedMC_TTBar_global=19757190;

N_simulatedMC_VV_global=1951600+14346866+18790122;
                                               
N_simulatedMC_STop_global=613384+1680200+3299800+995600+988500;






## Sample Detinition       
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

lumi=options.lumi;
lumi_str=str("%.0f"%lumi);
Channel_global=options.channel;





####################
## CUTS STRING
####################


#sideBand 40<Mj<65, 135<Mj<150



### Luca CutString=
#cuts_itemize=["1==1 && njets>2 && abs(vbf_maxpt_j1_pt-vbf_maxpt_j2_pt)>0.0001"];
### pag 134 tesi dottorato Luca

###### Cut String for B-TAGGING nella regione di segnale VBF
###per eliminare eventi con jet b-taggati
#nBTagJet_medium==0 && vbf_maxpt_j1_bDiscriminatorCSV<0.89 && vbf_maxpt_j2_bDiscriminatorCSV<0.89

###regione arricchita ttbar
#nBTagJet_medium >0 || vbf_maxpt_j1_bDiscriminatorCSV>0.89 || vbf_maxpt_j2_bDiscriminatorCSV>0.89






### ELECTRON TYPE
'''
Cuts For Significance Optimization:

     ## NO CUTS
        "1==1",    							
     
     
     
     ## BASIC SELECTIONS CUTS
     
          # ANGULAR CUTS to ensure BackToBack Topology
              "deltaR_lak8jet>(TMath::Pi()/2.0)",
              "TMath::Abs(deltaphi_METak8jet)>2.0",		
              "TMath::Abs(deltaphi_Vak8jet)>2.0",    
              
          # BOSON SELECTIONS
              "v_pt>200",								# Pt of Vector Boson (leptonic)
              "ungroomed_jet_pt>200", 					# Boson Selections
                        
          # LEPTON SELECTION
              ELECTRON: "l_pt>45",								# Lepton Pt selection
              MUON: "l_pt>40",
          
          # MET SELECTION 
              ELECTRON: "pfMET>80",								# Particle Flow MET
              MUON: "pfMET>40",
     




     ## BTAGGING CONDITIONS
          
          # NO B-TAGGING
              "nBTagJet_medium==0 && vbf_maxpt_j1_bDiscriminatorCSV<0.89 && vbf_maxpt_j2_bDiscriminatorCSV<0.89"

          # B-TAGGING -> TTBar ControlRegion
              "nBTagJet_medium >0 || vbf_maxpt_j1_bDiscriminatorCSV>0.89 || vbf_maxpt_j2_bDiscriminatorCSV>0.89"




     # W-TAGGER -> N-Subjettines
        "jet_tau2tau1 < 0.6",
     
     
     ## VBF SELECTIONS
          "njets>1",								# VBF Topology: we request at least two jets
          "abs(vbf_maxpt_j1_pt-vbf_maxpt_j2_pt)>0.0001"		# In order to regularize the first bin
              #
     
     
     
     
     ## Mj SELECTIONS
          
          # SIGNAL REGION
              "(jet_mass_pr > 65 && jet_mass_pr < 105 )",
                   
          # SideBand
              "((jet_mass_pr > 40 && jet_mass_pr < 65 )  || ( jet_mass_pr > 135 && jet_mass_pr < 150))",
     
     
	
     
     


'''

####################################
#### CUTS DEFINITION
####################################

if (float(DEtaCut_value) and float(MjjCut_value)):
   
   
   ### EM SAMPLE and e-only sample
   if (options.channel=="el" or options.channel=="em"):
   
      frameSubTitle_AD_string="\hspace{6pt} SignalRegion";
      cuts_itemize=["1==1",
                    "deltaR_lak8jet>(TMath::Pi()/2.0)",
                    "TMath::Abs(deltaphi_METak8jet)>2.0",
                    "TMath::Abs(deltaphi_Vak8jet)>2.0",
                    "v_pt>200",
                    "ungroomed_jet_pt>200",
                    "l_pt>45",
                    "pfMET>80",
                    "jet_tau2tau1 < 0.6",
                    "(jet_mass_pr > 65 && jet_mass_pr < 105 )",
                    "nBTagJet_medium==0 && vbf_maxpt_j1_bDiscriminatorCSV<0.89 && vbf_maxpt_j2_bDiscriminatorCSV<0.89 ",
                    "njets > %s"%(nJetsCut_value),
                    "abs(vbf_maxpt_j1_eta-vbf_maxpt_j2_eta) > %s"%(DEtaCut_value),
                    "vbf_maxpt_jj_m > %s"%(MjjCut_value)];
    
   else:
      
      ### MU SAMPLE
      frameSubTitle_AD_string="\hspace{6pt} SignalRegion";
      cuts_itemize=["1==1",
                    "deltaR_lak8jet>(TMath::Pi()/2.0)",
                    "TMath::Abs(deltaphi_METak8jet)>2.0",
                    "TMath::Abs(deltaphi_Vak8jet)>2.0",
                    "v_pt>200",
                    "ungroomed_jet_pt>200",
                    "l_pt>40",
                    "pfMET>40",
                    "jet_tau2tau1 < 0.6",
                    "(jet_mass_pr > 65 && jet_mass_pr < 105 )",
                    "nBTagJet_medium==0 && vbf_maxpt_j1_bDiscriminatorCSV<0.89 && vbf_maxpt_j2_bDiscriminatorCSV<0.89 ",
                    "njets > %s"%(nJetsCut_value),
                    "abs(vbf_maxpt_j1_eta-vbf_maxpt_j2_eta) > %s"%(DEtaCut_value),
                    "vbf_maxpt_jj_m > %s"%(MjjCut_value)];
    









else:
   if (options.channel=="el" or options.channel=="em"):
      
      
      ### EM SAMPLE and e-only sample
      frameSubTitle_AD_string="\hspace{6pt} SignalRegion";
      cuts_itemize=["1==1",
                    "deltaR_lak8jet>(TMath::Pi()/2.0)",
                    "TMath::Abs(deltaphi_METak8jet)>2.0",
                    "TMath::Abs(deltaphi_Vak8jet)>2.0",
                    "mass_lvj_type2>600 && mass_lvj_type2<2000",
                    "v_pt>200",
                    "ungroomed_jet_pt>200",
                    "l_pt>45",
                    "pfMET>80",
                    "jet_tau2tau1 < 0.6",
                    "(jet_mass_pr > 65 && jet_mass_pr < 105 )",
                    "nBTagJet_medium==0 && vbf_maxpt_j1_bDiscriminatorCSV<0.89 && vbf_maxpt_j2_bDiscriminatorCSV<0.89 ",
                    "abs(vbf_maxpt_j1_eta-vbf_maxpt_j2_eta) > 0.001"];
#"njets > %s"%(nJetsCut_value),
#"abs(vbf_maxpt_j1_eta-vbf_maxpt_j2_eta) > %s"%(DEtaCut_value),
#"vbf_maxpt_jj_m > %s"%(MjjCut_value),
    


   else:
      
      ### MU SAMPLE
      frameSubTitle_AD_string="\hspace{6pt} SignalRegion";
      cuts_itemize=["1==1",
                    "deltaR_lak8jet>(TMath::Pi()/2.0)",
                    "TMath::Abs(deltaphi_METak8jet)>2.0",
                    "TMath::Abs(deltaphi_Vak8jet)>2.0",
                    "v_pt>200",
                    "ungroomed_jet_pt>200",
                    "l_pt>40",
                    "pfMET>40",
                    "jet_tau2tau1 < 0.6",
                    "(jet_mass_pr > 65 && jet_mass_pr < 105 )",
                    "nBTagJet_medium==0 && vbf_maxpt_j1_bDiscriminatorCSV<0.89 && vbf_maxpt_j2_bDiscriminatorCSV<0.89 ",
                    "abs(vbf_maxpt_j1_eta-vbf_maxpt_j2_eta) > 0.001"];

#"njets > %s"%(nJetsCut_value),
#"abs(vbf_maxpt_j1_eta-vbf_maxpt_j2_eta) > %s"%(DEtaCut_value),
#                  "vbf_maxpt_jj_m > %s"%(MjjCut_value),
    






###########################################################################################
######## FUNCTION DEFINITION
###########################################################################################





    
###########################################################################################
######## MAIN FUNCTION 
###########################################################################################



if __name__ == '__main__':

    Lumi_mm=options.lumi;
    Lumi_mm_str=str("%.0f"%Lumi_mm);
    Lumi_mm_str_all=str("%f"%Lumi_mm);
    
    print "\n\n\nWelcome! \nControl Plots Maker!\n"
    print "\nNtuple:\t%s\n"%options.ntuple
    print "Luminosity:\t%f"%Lumi_mm
    
   

    
    #########################################################
    ######### MAKING DIRECTORY
    #########################################################

    Cuts_File_Dir_mm="cfg/DataMCComparison_InputCfgFile";
    if not os.path.isdir(Cuts_File_Dir_mm):
           pd3 = subprocess.Popen(['mkdir',Cuts_File_Dir_mm]);
           pd3.wait();
       

    Control_Plots_Dir_mm=options.dir;
    

    
    
    #########################################################
    ######### GET INPUT VALUE FROM FILE
    ######################################################### 
    
    InFile=options.inData;
    InputValueVector=GetDataFromFile(InFile);
    
    epsilon_12_data=float(InputValueVector[0]);#0.180540;
    epsilon_21_data=float(InputValueVector[1]);#0.235448;
    epsilon_12_MC=float(InputValueVector[2]);#0.216463;
    epsilon_21_MC=float(InputValueVector[3]);#0.305039;

    Sigma_epsilon_12_data=float(InputValueVector[4]);#0.019437;
    Sigma_epsilon_21_data=float(InputValueVector[5]);#0.025842;
    Sigma_epsilon_12_MC=float(InputValueVector[6]);#0.021647;
    Sigma_epsilon_21_MC=float(InputValueVector[7]);#0.030504;

    Beta_ScaleFactor_TTBar=float(InputValueVector[8]);#0.886664;
    Sigma_Beta_ScaleFactor=float(InputValueVector[9]);#0.200185;
    
    Scale_W_from_Control_Plots=float(InputValueVector[10]);#0.814414;
    Sigma_Scale_W_from_Control_Plots=float(InputValueVector[11]);

    Scale_W_Factor_global=options.scalew*Scale_W_from_Control_Plots;
    
    Scale_W_Factor_global_str=str(Scale_W_Factor_global);
    
    B_Tagging_Correction_Factor=(1-epsilon_12_data)*(1-epsilon_21_data)/((1-epsilon_12_MC)*(1-epsilon_21_MC));

    Scale_T_Factor_global=Beta_ScaleFactor_TTBar*B_Tagging_Correction_Factor;
    
    
    #Scale_W_Factor_global  
    #Scale_W_Factor_global_str
    #B_Tagging_Correction_Factor=(1-epsilon_12_data)*(1-epsilon_21_data)/((1-epsilon_12_MC)*(1-epsilon_21_MC));
    #Scale_T_Factor_global
    
    

    
    #########################################################
    ######### MAKE OUTPUT FILE
    #########################################################    
    summaryF_mm = Control_Plots_Dir_mm+"/Summary_ControlPlots.txt";
    Output_Summary_File_mm=open(summaryF_mm,'w+');
    Output_Summary_File_mm.write("\n\nFinal CONTROL PLOTS\n\n");
    Output_Summary_File_mm.close();
    
    latex_file = Control_Plots_Dir_mm+"/SignalRegion_ControlPlots.tex";
    Output_Beamer_Latex_File_mm=open(latex_file,'w+');


    ################################################
    #### TTBar Scale Factor
    #################################################
    tmp_scale_T_factor_string=["TTBar ScaleFactor UTILIZED",
                               " ",
                               "SF TTBar: %f"%Beta_ScaleFactor_TTBar,
                               " ",
                               "B-Tag CorrectionFactor: %f"%B_Tagging_Correction_Factor,
                               " ",
                               "Total TTBar SF: %f"%Scale_T_Factor_global];
    
    print_boxed_string_File(tmp_scale_T_factor_string,summaryF_mm);


    

    
    #########################################################
    ######### MAKE CONFIGURATION FILE
    ######################################################### 
    
    # Make Cuts File
    counter=0;
    for line in cuts_itemize:
        counter=counter+1;
    

    Cuts_Total_Number_mm=counter;  
    
    cut_string1="";
    cut_string2="";
    conjunction=" && ";
    
    i=j=0;
    Cuts_filename_table=[[0 for j in range(Cuts_Total_Number_mm)]for i in range(2)]; 
    
    i=j=0;
    cuts_table_main=[[0 for j in range(Cuts_Total_Number_mm)]for i in range(2)];
    cut_counter=0;
    for cut_counter in range(Cuts_Total_Number_mm):
        
        
        ### Make the cutFiles
        ###### index 1: consecutive cuts
        ###### index 2: single cut   
        
        
           
           
        if cut_counter==0:
           cut_string1=cuts_itemize[cut_counter];
           cut_string2=cuts_itemize[cut_counter];
    
        else:
           cut_string1=cut_string1+conjunction+cuts_itemize[cut_counter];
           cut_string2=cuts_itemize[cut_counter];

        
        
        Plus_Cut_Counter=cut_counter+1;
        
        cuts_table_main[0][cut_counter]=cut_string1;
        cuts_table_main[1][cut_counter]=cut_string2;
        
        cuts_file1=Cuts_File_Dir_mm+"/MATTEO_SR_cuts_file1_%s_%s_%s_%s_%s.txt"%(options.channel,str(Plus_Cut_Counter),DEtaCut_value,MjjCut_value,nJetsCut_value);
        output_cuts_file1=open(cuts_file1,'w+');
        output_cuts_file1.write(cut_string1);
        output_cuts_file1.close();

        cuts_file2=Cuts_File_Dir_mm+"/MATTEO_SR_cuts_file2_%s_%s_%s_%s_%s.txt"%(options.channel,str(Plus_Cut_Counter),DEtaCut_value,MjjCut_value,nJetsCut_value);
        output_cuts_file2=open(cuts_file2,'w+');
        output_cuts_file2.write(cut_string2);
        output_cuts_file2.close();
        
        
        
        #def print_lined_string_File(in_string_vector,out_file):
        
        resume_making_cuts_file=["Making CutsFile",
                                 "Total number of cuts:\t%.0f"%(Cuts_Total_Number_mm),
                                 "Current cut:\t%.0f"%(Plus_Cut_Counter),
                                 " ",
                                 "Cut file 1:\t%s"%(cuts_file1),
                                 "Cut String 1:\t%s"%(cut_string1),
                                 " ",
                                 "Cut file 2:\t%s"%(cuts_file2),
                                 "Cut String 2:\t%s"%(cut_string2)];
        #print_lined_string(resume_making_cuts_file)
        print_lined_string_File(resume_making_cuts_file,summaryF_mm)

        Cuts_filename_table[0][cut_counter]=cuts_file1;
        Cuts_filename_table[1][cut_counter]=cuts_file2;
    
    
    
    # Make VariableList
    FileName_VariableList_mm="cfg/DataMCComparison_InputCfgFile/MATTEO_VariableList_SR_%s_%s_%s_%s.txt"%(options.channel,DEtaCut_value,MjjCut_value,nJetsCut_value);
    Output_VariableList_mm=open(FileName_VariableList_mm,'w+');
    Output_VariableList_mm.write("############################################################################\n");
    Output_VariableList_mm.write("##  Variable						Nbin		Min		Max			Label\n");
    Output_VariableList_mm.write("############################################################################\n");
    Output_VariableList_mm.write("# nPV								25			0		50			nPV\n");
    Output_VariableList_mm.write("# l_pt							25			0		500			pT_{l}_(GeV)\n");
    Output_VariableList_mm.write("# l_eta							25			-2.5	2.5			#eta_{l}\n");
    Output_VariableList_mm.write("# l_eta							20			-2.5	2.5			#eta_{l}\n");
    Output_VariableList_mm.write("# l_phi							30			-3.14	3.14		#phi_{l}\n");
    Output_VariableList_mm.write("# v_mt								20			0		400			mT^{W}_{l}_(GeV)\n");
    Output_VariableList_mm.write("# pfMET							28			0		560			MET[GeV]\n");
    Output_VariableList_mm.write("# pfMETpuppi						28			0		560			MET[GeV]\n");
    Output_VariableList_mm.write("# pfMETpuppi_Phi					20   -3.15      3.15	  #phi_{Puppi MET}\n");
    Output_VariableList_mm.write("# pfMET_Phi						30   -3.14      3.14	  #phi_{MET}\n");
    Output_VariableList_mm.write("# ungroomed_jet_phi				30    -3.14     3.14     #phi^{AK8}\n");
    Output_VariableList_mm.write("# ungroomed_PuppiAK8_jet_pt		32    100       740      pT^{puppi AK8}_(GeV)\n");
    Output_VariableList_mm.write("# ungroomed_PuppiAK8_jet_eta		25    -2.5      2.5        #eta^{puppi AK8}\n");
    Output_VariableList_mm.write("# ungroomed_PuppiAK8_jet_phi		30    -3.14     3.14     #phi^{puppi AK8}\n");
    Output_VariableList_mm.write("# jet_mass_pr						22      40       150    Jet_Pruned_Mass_(GeV)\n");
    Output_VariableList_mm.write("# jet_mass_so						22      40       150    Jet_Softdrop_Mass_(GeV/c^{2})\n");
    Output_VariableList_mm.write("# PuppiAK8_jet_mass_pr			22      40       150    puppiAK8_Jet_Pruned_Mass_(GeV/c^{2})\n");
    Output_VariableList_mm.write("# PuppiAK8_jet_mass_so			22      40       150    puppiAK8_Jet_Softdrop_Mass_(GeV/c^{2})\n");
    Output_VariableList_mm.write("# mass_lvj_type0					40    0       3000    M_{WW}_(GeV/c^{2})\n");
    Output_VariableList_mm.write("# mass_lvj_type2					40    0       3000    M_{WW}_(GeV/c^{2})\n");
    Output_VariableList_mm.write("# mass_lvj_type0_PuppiAK8			40    0       3000    M_{WW}_(GeV/c^{2})\n");
    Output_VariableList_mm.write("# mass_lvj_type2_PuppiAK8			40    0       3000    M_{WW}_(GeV/c^{2})\n");
    Output_VariableList_mm.write("# mass_lvj_type0_met				56    200       3000    M_{WW}_(GeV/c^{2})\n");
    Output_VariableList_mm.write("# mass_lvj_type2_met				56    200       3000    M_{WW}_(GeV/c^{2})\n");
    Output_VariableList_mm.write("# nu_pz_type0						30   -500      500        pZ^{#nu}[GeV]\n");
    Output_VariableList_mm.write("# nu_pz_type2                   30   -500      500        pZ^{#nu}[GeV]\n");
    Output_VariableList_mm.write("# nu_pz_type0_met                   60   -500      500        pZ^{#nu}[GeV]\n");
    Output_VariableList_mm.write("# nu_pz_type2_met                   60   -500      500        pZ^{#nu}[GeV]\n");
    Output_VariableList_mm.write("# nbjets_csvl_veto                  5      0       5        N_{bjet}^{csvl}\n");
    Output_VariableList_mm.write("# nbjets_csvm_veto                  5      0       5        N_{bjet}^{csvm}\n");
    Output_VariableList_mm.write("# nbjets_csvt_veto                  5      0       5        N_{bjet}^{csvt}\n");
    Output_VariableList_mm.write("# numberJetBin                      5      0       5        N_{jets}\n");
    Output_VariableList_mm.write("# PuppiAK8_jet_tau2tau1                     25     0.      1.       puppiAK8_#tau_{2}/#tau_{1}\n");
    Output_VariableList_mm.write("# jet2_pt				 25	0	500	 pT^{AK4}_{1}_(GeV)\n");
    Output_VariableList_mm.write("# jet2_btag				 25	0	1	 btag^{AK4}_{1}_(GeV)\n");
    Output_VariableList_mm.write("# jet3_pt				 25	0	500	 pT^{AK4}_{1}_(GeV)\n");
    Output_VariableList_mm.write("# jet3_btag				 25	0	1	 btag^{AK4}_{1}_(GeV)\n");
    Output_VariableList_mm.write("# jet_tau2tau1_exkT                30     0.1      1.      #tau_{2}/#tau_{1}_extkT\n");
    Output_VariableList_mm.write("# jet_tau2tau1_pr                  30     0.1      1.      #tau_{2}/#tau_{1}_pruned\n");
    Output_VariableList_mm.write("# jet_massdrop_pr                  35     0.1      1.      Pruned_Mass_Drop_(GeV/c^{2})\n");
    Output_VariableList_mm.write("# jet_qjetvol                      35     0        1.         QjetVolatility\n");
    Output_VariableList_mm.write("# jet_charge                       50     -2.5     2.5       Jet_Charge\n");
    Output_VariableList_mm.write("# jet_charge_k05                       50     -2.0     2.0       Jet_Charge_k05\n");
    Output_VariableList_mm.write("# jet_charge_k07                       50     -1.5     1.5       Jet_Charge_k07\n");
    Output_VariableList_mm.write("# jet_charge_k10                       45     -0.8     0.8       Jet_Charge_k10\n");
    Output_VariableList_mm.write("# jet_GeneralizedECF                   35     0.     0.6       Jet_Generalized_ECF\n");
    Output_VariableList_mm.write("# ttb_ca8_mass_pr                   25      40      130      Jet_Pruned_Mass_(GeV/c^{2})\n");
    Output_VariableList_mm.write("# ttb_ht                            35     0      700       \n");
    Output_VariableList_mm.write("# ttb_ca8_ungroomed_pt              30   200      600       pT^{AK8}[GeV]\n");
    Output_VariableList_mm.write("# ttb_ca8_tau2tau1_exkT             30    0.1      1.0      #tau_{2}/#tau_{1}_exkT\n");
    Output_VariableList_mm.write("# ttb_ca8_tau2tau1_pr               30    0.1      1.0       #tau_{2}/#tau_{1}_pruned\n");
    Output_VariableList_mm.write("# ttb_ca8_tau2tau1                  30    0.1      1.0       #tau_{2}/#tau_{1}\n");
    Output_VariableList_mm.write("# ttb_ca8_charge                    50     -2.5     2.5       Jet_Charge\n");
    Output_VariableList_mm.write("# ttb_ca8_charge_k05                50     -2.0     2.0       Jet_Charge_k05\n");
    Output_VariableList_mm.write("# ttb_ca8_charge_k07                50     -1.5     1.5       Jet_Charge_k07\n");
    Output_VariableList_mm.write("# ttb_ca8_charge_k10                45     -0.8     0.8       Jet_Charge_k10\n");
    Output_VariableList_mm.write("# ttb_ca8_GeneralizedECF            30     0.     0.5       Jet_Generalized_ECF\n");
    Output_VariableList_mm.write("# ttb_ca8_mu                        20    0.1      0.7       Pruned_Mass_Drop_(GeV/c^{2})\n");
    Output_VariableList_mm.write("# ttb_mlvj                          40   400     1400       M_{WW}(GeV/c^{2})\n");
    Output_VariableList_mm.write("# vbf_maxpt_j1_QGLikelihood       50      0       1          j1_QGLikelihood\n");
    Output_VariableList_mm.write("# vbf_maxpt_j2_QGLikelihood       50      0       1          j2_QGLikelihood\n");
    Output_VariableList_mm.write("# mass_ungroomedjet_closerjet      30      80     400         M_{top}^{had}\n");
    Output_VariableList_mm.write("# mass_leptonic_closerjet          30      100     400   	    M_{top}^{lep}\n");
    Output_VariableList_mm.write("#jet_tau2tau1                    30       0.1       1.0          #tau_{2}/#tau_{1}\n");
    Output_VariableList_mm.write("vbf_maxpt_jj_m                  40      0       1500        M_{jj}_(GeV/c^{2})\n");
    Output_VariableList_mm.write("abs(vbf_maxpt_j1_eta-vbf_maxpt_j2_eta) 35    0       9     #Delta#eta_{jj}\n");

    if not (float(DEtaCut_value)):
       if not (float(MjjCut_value)):
           Output_VariableList_mm.write("deltaR_lak8jet                 50        0.1       5          #DeltaR\n");
           Output_VariableList_mm.write("deltaphi_METak8jet             50			-3.14	3.14		#Delta#phi_{met}\n");
           Output_VariableList_mm.write("deltaphi_Vak8jet               50			-3.14	3.14		#Delta#phi_{Wlep}\n");
           Output_VariableList_mm.write("vbf_maxpt_jj_phi                50      -3.14   3.14       #phi_{jj}\n");
           Output_VariableList_mm.write("vbf_maxpt_jj_eta                30      -4.7       4.7     #eta_{jj}\n");
           Output_VariableList_mm.write("vbf_maxpt_j2_bDiscriminatorCSV  50      0       1          j2_bDiscriminator\n");
           Output_VariableList_mm.write("vbf_maxpt_j2_eta                50      -5      5          #eta_{j2}\n");
           Output_VariableList_mm.write("vbf_maxpt_j2_pt                 50      0       300        pT_{j2}_(GeV)\n");
           Output_VariableList_mm.write("vbf_maxpt_j1_bDiscriminatorCSV  50      0       1          j1_bDiscriminator\n");
           Output_VariableList_mm.write("vbf_maxpt_j1_eta                50      -5      5          #eta_{j1}\n");
           Output_VariableList_mm.write("vbf_maxpt_j1_pt                 50      0       300        pT_{j1}_(GeV)\n");
           Output_VariableList_mm.write("jet_tau2tau1                     25     0.      1.       #tau_{2}/#tau_{1}\n");
           Output_VariableList_mm.write("jet_mass_pr						15      65       105     Jet_Pruned_Mass_(GeV/c^{2})\n");
           Output_VariableList_mm.write("ungroomed_jet_pt				32    100       740      pT^{AK8}_(GeV)\n");
           Output_VariableList_mm.write("ungroomed_jet_eta				25    -2.5      2.5        #eta^{AK8}\n");
           Output_VariableList_mm.write("pfMET							50      0       1000      MET[GeV]\n");
           Output_VariableList_mm.write("v_pt							25			200		700			pT^{W}_{l}_(GeV)\n");
           Output_VariableList_mm.write("l_pt							50			0		1000		pT_{l}_(GeV)\n");
    
    Output_VariableList_mm.close();
    # Make InputFile and SampleListFile
    Ntuple_mm=options.ntuple;       
    Sample_Counter=0;
    
            
    for line in sampleValue:
        Sample_Counter=Sample_Counter+1;

    
    
    # Make SampleListFile     
    Sample_Total_Number_mm=Sample_Counter;
    Sample_Counter_mm=i=j=k=0;
    Cfg_FileName_Table_mm=[[[0 for k in range(2*Sample_Total_Number_mm)]for j in range(Cuts_Total_Number_mm)]for i in range(2)]
    for Sample_Counter_mm in range(Sample_Total_Number_mm):
    
        Sample_mm=sampleValue[Sample_Counter_mm][0];
        Mass_mm=sampleValue[Sample_Counter_mm][2];
        Mass_str_mm=str("%.0f"%Mass_mm);
            
        FileName_Sample_mm="cfg/DataMCComparison_InputCfgFile/MATTEO_SampleList_%s%s_SR_%s_%s_%s_%s.txt"%(Sample_mm,Mass_str_mm,options.channel,DEtaCut_value,MjjCut_value,nJetsCut_value);
    
    
        Output_SampleFile_mm=open(FileName_Sample_mm,'w+');
        
        Output_SampleFile_mm.write("####################################################################################################\n");
        Output_SampleFile_mm.write("###   Sample Name				Reduced Name	Color		XSec (pb)		NumEntriesBefore\n");
        Output_SampleFile_mm.write("####################################################################################################\n");        
        
        Output_SampleFile_mm.write("WWTree_data_golden_2p1			DATA			1			1				1\n");
        Output_SampleFile_mm.write("#WWTree_data_muonPhys			DATA             1                  1               1\n");
        Output_SampleFile_mm.write("#WWTree_WJets					Jets           2                  61526.7         24184766\n");
        Output_SampleFile_mm.write("WWTree_WJets100					W+Jets           2                  1347            10152718\n");
        Output_SampleFile_mm.write("WWTree_WJets200					W+Jets           2                  360.           5221599\n");
        Output_SampleFile_mm.write("WWTree_WJets400					W+Jets           2                  48.9            1745914\n");
        Output_SampleFile_mm.write("#WWTree_WJets600				W+Jets           2                  18.77            1039152\n");
        Output_SampleFile_mm.write("WWTree_WJets600bis				W+Jets           2                  12.8            4041997\n");
        Output_SampleFile_mm.write("WWTree_WJets800					W+Jets           2                  5.26            1574633\n");
        Output_SampleFile_mm.write("WWTree_WJets1200				W+Jets           2                  1.33            255637\n");
        Output_SampleFile_mm.write("WWTree_WJets2500				W+Jets           2                  0.03089         253036\n");
        Output_SampleFile_mm.write("#WWTree_WW						WW               4                  118.7           993640\n");
        Output_SampleFile_mm.write("#WWTree_WZ						WZ               4                  47.13            978512\n");
        Output_SampleFile_mm.write("#WWTree_ZZ						ZZ               4                   16.523            996944\n");
        Output_SampleFile_mm.write("WWTree_WW_excl					WW               4                  49.997           1951600\n");
        Output_SampleFile_mm.write("WWTree_WZ_excl					WZ               4                  10.71           14346866\n");
        Output_SampleFile_mm.write("#WWTree_WZ_excl					WZ               4                  10.71           24714550\n");
        Output_SampleFile_mm.write("WWTree_ZZ_excl					ZZ               4                 3.22            18790122\n");
        Output_SampleFile_mm.write("#WWTree_ZZ_excl					ZZ               4                 3.22           11863244\n");
        Output_SampleFile_mm.write("#WWTree_sch						STop             7                  3.65792         984400\n");
        Output_SampleFile_mm.write("WWTree_sch						STop             7                  3.65792         613384\n");
        Output_SampleFile_mm.write("WWTree_tch_bar					STop             7                  26.0659         1680200\n");
        Output_SampleFile_mm.write("WWTree_tch						STop             7                  43.79844        3299800\n");
        Output_SampleFile_mm.write("WWTree_tWch						STop             7                  35.6            995600\n");
        Output_SampleFile_mm.write("WWTree_tWch_bar					STop             7                  35.6             988500\n");
        Output_SampleFile_mm.write("#WWTree_TTbar_amcatnlo			tt_bar           210                831.76          42784971\n");
        Output_SampleFile_mm.write("#WWTree_TTbar_madgraph			tt_bar           210                831.76          11344206\n");
        Output_SampleFile_mm.write("WWTree_TTbar					tt_bar           210                831.76          19757190\n");
        
        
        if Sample_mm=="BulkGraviton":
           SignalName_mm="WWTree_BulkGraviton"+Mass_str_mm;
           SignalName_VBF_mm="WWTree_VBFBulkGraviton"+Mass_str_mm;
                
        else:
           SignalName_mm="WWTree_Higgs"+Mass_str_mm;
           SignalName_VBF_mm="WWTree_VBFHiggs"+Mass_str_mm;
        
        ReducedName_mm=sampleValue[Sample_Counter_mm][1]
        ReducedName_VBF_mm=sampleValue_VBF[Sample_Counter_mm][1]
        
        Color_VBF_mm=1;
        Color_mm=13;
        
        Xsec_mm=sampleValue[Sample_Counter_mm][3];
        Xsec_VBF_mm=sampleValue_VBF[Sample_Counter_mm][3];
        
        NumberEntriesBefore_mm=sampleValue[Sample_Counter_mm][4];
        NumberEntriesBefore_VBF_mm=sampleValue_VBF[Sample_Counter_mm][4];
        
        ScaleFactor_mm=sampleValue[Sample_Counter_mm][5];
        
        Output_SampleFile_mm.write("%s\t\t\t\t\t%s\t\t\t%.0f\t\t%f\t\t%f\n"%(SignalName_mm,ReducedName_mm,Color_mm,Xsec_mm,NumberEntriesBefore_mm));
        Output_SampleFile_mm.write("%s\t\t\t\t\t%s\t\t\t%.0f\t\t%f\t\t%f\n"%(SignalName_VBF_mm,ReducedName_VBF_mm,Color_VBF_mm,Xsec_VBF_mm,NumberEntriesBefore_VBF_mm));
    
        Output_SampleFile_mm.close();
        
        tmp_string=["SAMPLE LIST File Making ",
                    "%s"%FileName_Sample_mm];
        print_lined_string_File(tmp_string,summaryF_mm);
        
        
        if Channel_global=="mu":
           leptonT="muon";
        
        elif Channel_global=="el":
           leptonT="el";   
        
        else:
           leptonT="em";
    
        
        if options.nodata:
           print_boxed_string_File(["NO DATA"],summaryF_mm);
           withData="true";
        else:
           print_boxed_string_File(["WITH DATA"],summaryF_mm);
           withData="false";

    
        Cut_Number_mm=0;
        CutType_mm=0;
        for CutType_mm in range(2):
          for Cut_Number_mm in range(Cuts_Total_Number_mm):
          
            
            Cuts_FileName_mm=Cuts_filename_table[CutType_mm][Cut_Number_mm];
            Cut_Type_String_mm=str("%.0f"%(CutType_mm+1));
            Cut_Number_String_mm=str("%.0f"%(Cut_Number_mm+1));
            if Sample_mm=="BulkGraviton":
               LetterName_mm="G";
            else:
               LetterName_mm="H";
            Dir_Data_Saved_mm="output/run2/MCDATAComparisonPlot_SR_%s_%s%s_%s_%s_%s_%s_%s"%(Channel_global,Sample_mm,Mass_mm,Cut_Type_String_mm,Cut_Number_String_mm,DEtaCut_value,MjjCut_value,nJetsCut_value);
       
            Cfg_Input_FileName_mm="cfg/DataMCComparison_InputCfgFile/MATTEO_DataMCComparison_InputCfgFile_%s%s_SR_%s_%s_%s_%s_%s_%s.cfg"%(Sample_mm,Mass_str_mm,options.channel,Cut_Type_String_mm,Cut_Number_String_mm,DEtaCut_value,MjjCut_value,nJetsCut_value);
            Output_SampleFile_mm_sample=open(Cfg_Input_FileName_mm,'w+');
            Output_SampleFile_mm_sample.write("[Input]\n\n");
            Output_SampleFile_mm_sample.write(("InputDirectory = /afs/cern.ch/user/l/lbrianza/work/public/%s/WWTree_%s\n")%(Ntuple_mm,Channel_global));
            Output_SampleFile_mm_sample.write("TreeName = otree\n");
            Output_SampleFile_mm_sample.write(("LeptonType = %s\n")%leptonT);
            Output_SampleFile_mm_sample.write(("InputSampleList = %s\n")%(FileName_Sample_mm));
            Output_SampleFile_mm_sample.write("InputVariableList = %s\n"%FileName_VariableList_mm);
            Output_SampleFile_mm_sample.write(("InputCutList = %s\n")%Cuts_FileName_mm);
            Output_SampleFile_mm_sample.write(("SignalqqHName = %s\n")%ReducedName_VBF_mm);
            Output_SampleFile_mm_sample.write(("SignalggHName = %s\n")%ReducedName_mm);
            Output_SampleFile_mm_sample.write(("SignalGraviton = grav\n"));
            Output_SampleFile_mm_sample.write(("WithoutData = %s\n\n\n")%withData);    
            Output_SampleFile_mm_sample.write("[Option]\n\n");    
            Output_SampleFile_mm_sample.write("BackgroundWeight = genWeight*eff_and_pu_Weight\n");
            Output_SampleFile_mm_sample.write("BackgroundWeightMCatNLO = 1\n");
            Output_SampleFile_mm_sample.write("SignalggHWeight = 1\n");
            Output_SampleFile_mm_sample.write("SignalqqHWeight = 1\n");
            #Output_SampleFile_mm_sample.write("SignalGravitonWeight = genWeight\n");
            Output_SampleFile_mm_sample.write(("Lumi = %f\n")%Lumi_mm);
            Output_SampleFile_mm_sample.write("ttbarControlplots = false\n");
            Output_SampleFile_mm_sample.write("SignalScaleFactor = %f\n"%(ScaleFactor_mm));
            Output_SampleFile_mm_sample.write("NormalizeSignalToData = false\n");
            Output_SampleFile_mm_sample.write("NormalizeBackgroundToData = false\n");
            Output_SampleFile_mm_sample.write("Mass = %s\n"%Mass_str_mm);
            Output_SampleFile_mm_sample.write("Sample = %s\n"%Sample_mm);
            Output_SampleFile_mm_sample.write("LetterName = %s \n\n\n"%LetterName_mm);
            Output_SampleFile_mm_sample.write("[Output]\n\n");
            Output_SampleFile_mm_sample.write(("OutputRootDirectory = %s\n"%(Dir_Data_Saved_mm)));
            Output_SampleFile_mm_sample.write("OutputRootFile = Run2_MCDataComparisonRSGraviton2000_%s.root\n"%Channel_global);
            Output_SampleFile_mm_sample.write("\n");
            Output_SampleFile_mm_sample.close();
            
            tmp_string=["MAKING Cfg File",
                        "%s"%Cfg_Input_FileName_mm];
            print_boxed_string_File(tmp_string,summaryF_mm);
            Cfg_FileName_Table_mm[CutType_mm][Cut_Number_mm][Sample_Counter_mm]=Cfg_Input_FileName_mm;
            Cfg_FileName_Table_mm[CutType_mm][Cut_Number_mm][Sample_Total_Number_mm+Sample_Counter_mm]=Dir_Data_Saved_mm+"/";
    
    
        
    
    print "\n\n----------- Check CFG name ----------------\n"
    i=j=k=0;
    for i in range(2):
        for j in range(Cuts_Total_Number_mm):
            for k in range(Sample_Total_Number_mm):
                print "\nInputFilename: %s\t Directory: %s\n"%(Cfg_FileName_Table_mm[i][j][k],Cfg_FileName_Table_mm[i][j][Sample_Total_Number_mm+k])
    print "\n\n-------------------------------------------\n"
    i=j=k=0;
    Significance_Table_mm=[[[[0 for z in range(number_Events_type+5) ]for k in range(Sample_Total_Number_mm)]for j in range(Cuts_Total_Number_mm)]for i in range(2)];
    
    




    
    
    
    

       
   










    #########################################################
    ######### MAKE CONTROL PLOTS
    #########################################################
    
    
    TTBar_Scale_Factor_mm=Scale_T_Factor_global;
    TTBar_Scale_Factor_mm_str=str(TTBar_Scale_Factor_mm);
    
    Cut_Number_mm=0
    for Cut_Number_mm in range(Cuts_Total_Number_mm):
        
        # Make directory
        Plus_Cut_Counter=Cut_Number_mm+1;
        Plus_Cut_Counter_str=str("%.0f"%(Plus_Cut_Counter));
        control_cuts1_dir=Control_Plots_Dir_mm+"/Consecutive_Cuts_%s"%(str(Plus_Cut_Counter));
        if not os.path.isdir(control_cuts1_dir):
               pd8 = subprocess.Popen(['mkdir',control_cuts1_dir]);
               pd8.wait();
    
        control_cuts2_dir=Control_Plots_Dir_mm+"/Single_Cuts_%s"%(str(Plus_Cut_Counter));
        if not os.path.isdir(control_cuts2_dir):
               pd9 = subprocess.Popen(['mkdir',control_cuts2_dir]);
               pd9.wait();
           
        cuts_file1=Cuts_filename_table[0][Cut_Number_mm];
        cuts_file2=Cuts_filename_table[1][Cut_Number_mm];
        
        
        resume_controPlotsMaking=["Making Control Plots",
                                  "Processing Cuts %0.f of %0.f"%(Plus_Cut_Counter,Cuts_Total_Number_mm),
                                  " ",
                                  "Using Cuts File 1:\t%s"%(cuts_file1),
                                  "Using Cuts File 2:\t%s"%(cuts_file2)];
        
        #print_lined_string(resume_controPlotsMaking)
        print_lined_string_File(resume_controPlotsMaking,summaryF_mm);

        
        
        
        
        # Run ControPlots code
        n_sample=0;
        for n_sample in range(Sample_Total_Number_mm):
            

            
            sample=sampleValue[n_sample][0];
            mass=sampleValue[n_sample][2];
            mass_str=str("%.0f"%mass);       
            
          
            
            final_dir1=control_cuts1_dir+"/"+sample+mass_str;
            if not os.path.isdir(final_dir1):
               pd10 = subprocess.Popen(['mkdir',final_dir1]);
               pd10.wait();
                 
            final_dir2=control_cuts2_dir+"/"+sample+mass_str;
            if not os.path.isdir(final_dir2):
               pd11 = subprocess.Popen(['mkdir',final_dir2]);
               pd11.wait();
            

            resume_processing_string=[" ",
                                      "PROCESSING:\t%s%s"%(sample,mass_str),
                                      " ",
                                      "FinalDir1: %s"%(final_dir1),
                                      "FinalDir2: %s"%(final_dir2)];
                                      
            
            
            #print_lined_string(resume_processing_string)
            print_lined_string_File(resume_processing_string,summaryF_mm);
            
        # Run ControPlots code
        n_sample=0;
        for n_sample in range(Sample_Total_Number_mm):
            

            
            sample=sampleValue[n_sample][0];
            mass=sampleValue[n_sample][2];
            mass_str=str("%.0f"%mass);       
            

            final_dir1=control_cuts1_dir+"/"+sample+mass_str;
            if not os.path.isdir(final_dir1):
               pd10 = subprocess.Popen(['mkdir',final_dir1]);
               pd10.wait();
                 
            final_dir2=control_cuts2_dir+"/"+sample+mass_str;
            if not os.path.isdir(final_dir2):
               pd11 = subprocess.Popen(['mkdir',final_dir2]);
               pd11.wait();
            

            resume_processing_string=[" ",
                                      "PROCESSING:\t%s%s"%(sample,mass_str),
                                      " ",
                                      "FinalDir1: %s"%(final_dir1),
                                      "FinalDir2: %s"%(final_dir2)];
                                      
            
            
          
            print_lined_string_File(resume_processing_string,summaryF_mm);
            
           
            
            if (Cuts_Total_Number_mm-1):
               
               print_lined_string_File([" ","CONSECUTIVE CUTS"],summaryF_mm);
               
               cfg_file_1=[Cfg_FileName_Table_mm[0][Cut_Number_mm][n_sample],Cfg_FileName_Table_mm[0][Cut_Number_mm][Sample_Total_Number_mm+n_sample]];
               # Vector with parameters for run_log function
               tmp1_InValue_runLog=[n_sample,Cut_Number_mm,1,Cuts_Total_Number_mm,Significance_Table_mm,cfg_file_1,summaryF_mm,final_dir1,TTBar_Scale_Factor_mm,sampleValue,options.channel,Scale_W_Factor_global_str,number_Events_type,total_sample_value,Channel_global]
               Significance_Table_mm=run_log(tmp1_InValue_runLog);
               
            
            
            
                          
               print_lined_string_File([" ","SINGLE CUT"],summaryF_mm);
               
               cfg_file_2=[Cfg_FileName_Table_mm[1][Cut_Number_mm][n_sample],Cfg_FileName_Table_mm[1][Cut_Number_mm][Sample_Total_Number_mm+n_sample]];               
               # Vector with parameters for run_log function
               tmp2_InValue_runLog=[n_sample,Cut_Number_mm,2,Cuts_Total_Number_mm,Significance_Table_mm,cfg_file_2,summaryF_mm,final_dir2,TTBar_Scale_Factor_mm,sampleValue,options.channel,Scale_W_Factor_global_str,number_Events_type,total_sample_value,Channel_global];
               # Make Control Plot
               Significance_Table_mm=run_log(tmp2_InValue_runLog);
              
            
            
            
            
            
            
            
            else:
               
               tmp_string=["ONLY ONE CUT"];
               print_boxed_string_File(tmp_string,summaryF_mm);
              
               cfg_file_1=[Cfg_FileName_Table_mm[0][Cut_Number_mm][n_sample],Cfg_FileName_Table_mm[0][Cut_Number_mm][Sample_Total_Number_mm+n_sample]];
               # Vector with parameters for run_log function
               tmp_OnlyOneCut_VectorValue=[n_sample,Cut_Number_mm,1,Cuts_Total_Number_mm,Significance_Table_mm,cfg_file_1,summaryF_mm,final_dir1,TTBar_Scale_Factor_mm,sampleValue,options.channel,Scale_W_Factor_global_str,number_Events_type,total_sample_value,Channel_global];
               # Make Control Plot
               Significance_Table_mm=run_log(tmp_OnlyOneCut_VectorValue);
    
    
    
    
    
    
    
    
    
    
    
    
    #########################################################
    ######### MAKE BEAMER OUTPUT
    #########################################################
    
    # Beamer Settings
    Output_Beamer_Latex_File_mm.write("\documentclass{beamer}\n");
    Output_Beamer_Latex_File_mm.write("\usetheme{Boadilla}\n");
    Output_Beamer_Latex_File_mm.write("\usecolortheme{seahorse}\n");
    Output_Beamer_Latex_File_mm.write("\\title{ControlPlots}\n");
    Output_Beamer_Latex_File_mm.write("\\author{Matteo Rappo}\n");
    Output_Beamer_Latex_File_mm.write("\setbeamertemplate{navigation symbols}{}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage[latin1]{inputenc}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage[english,italian]{babel}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage{amsmath}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage{enumerate}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage{amsfonts}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage{amssymb}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage{float}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage{placeins}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage{subfig}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage{multirow,makecell}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage{array,booktabs}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage{comment}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage{scrextend}\n");
    Output_Beamer_Latex_File_mm.write("\usepackage{verbatim,longtable}\n");
    Output_Beamer_Latex_File_mm.write("\setbeamertemplate{caption}[numbered]\n");
    Output_Beamer_Latex_File_mm.write("\\newcolumntype{P}[1]{>{\centering\\arraybackslash}p{#1}}\n");
    Output_Beamer_Latex_File_mm.write("\\newcolumntype{M}[1]{>{\centering\\arraybackslash}m{#1}}\n");
    Output_Beamer_Latex_File_mm.write("\\newcolumntype{D}[1]{>{\\arraybackslash}m{#1}}\n");
    Output_Beamer_Latex_File_mm.write("\\newcolumntype{C}[1]{>{\centering\let\\newline\\\\arraybackslash\hspace{0pt}}m{#1}}\n");
    Output_Beamer_Latex_File_mm.write("\n");
    Output_Beamer_Latex_File_mm.write("\n");
    Output_Beamer_Latex_File_mm.write("\changefontsizes{9pt}\n");
    Output_Beamer_Latex_File_mm.write("\\begin{document}\n");
    Output_Beamer_Latex_File_mm.write("\n");
    Output_Beamer_Latex_File_mm.write("\n");
     


    # Ntuple Name in \texttt{} environment
    tmp_ntuple_texttt=replace_latex(options.ntuple);
    Ntuple_Name_texttt="\\texttt{"+tmp_ntuple_texttt+"}";
    
    
    if Channel_global=="mu":
       channel_latex_mm="$\mu$";
    
    elif Channel_global=="em":
       channel_latex_mm="e$\mu$";
    
    else:
       channel_latex_mm="e" 
    Frame_tmp="\\framesubtitle{%s-channel \hspace{6pt} Ntuple: "%(channel_latex_mm)+Ntuple_Name_texttt+" \hspace{6pt} W+Jets ScaleFactor: %s"%(Scale_W_Factor_global_str)+" \hspace{6pt} TTBar ScaleFactor: %s"%(TTBar_Scale_Factor_mm_str);
    latex_FrameSubtitle=Frame_tmp+frameSubTitle_AD_string+"}\n";
    Output_Beamer_Latex_File_mm.write("\\begin{frame}\n");
    Output_Beamer_Latex_File_mm.write("\\frametitle{Control Plots - Settings }\n");   
    Output_Beamer_Latex_File_mm.write(latex_FrameSubtitle);
    Output_Beamer_Latex_File_mm.write("\changefontsizes{11pt}\n");
    Output_Beamer_Latex_File_mm.write("\\begin{itemize}\n");
    Output_Beamer_Latex_File_mm.write("\item Luminosit\`a:%.0f ${fb}^{-1}$\n"%Lumi_mm);
    Output_Beamer_Latex_File_mm.write("\item Ntuple: %s\n"%Ntuple_Name_texttt);
    Output_Beamer_Latex_File_mm.write("\item Channel: %s\n"%channel_latex_mm);
    Output_Beamer_Latex_File_mm.write("\item W+Jets Scale Factor: %s\n"%Scale_W_Factor_global_str);
    Output_Beamer_Latex_File_mm.write("\item TTBar Scale Factor: %s\n"%TTBar_Scale_Factor_mm_str);
    Output_Beamer_Latex_File_mm.write("\end{itemize}\n");
    Output_Beamer_Latex_File_mm.write("\end{frame}\n");
    Output_Beamer_Latex_File_mm.write("\n");
    Output_Beamer_Latex_File_mm.write("\n");
    Output_Beamer_Latex_File_mm.write("\n");
    Output_Beamer_Latex_File_mm.write("\n");
    Output_Beamer_Latex_File_mm.write("\n");
    Output_Beamer_Latex_File_mm.write("\n");
    Output_Beamer_Latex_File_mm.write("\n");
    
    
    ### Slides with Plots
    nsample=0;
    for nsample in range(Sample_Total_Number_mm):
        
        Frame_tmp="\\framesubtitle{%s-channel \hspace{6pt} Ntuple: "%(channel_latex_mm)+Ntuple_Name_texttt+" \hspace{6pt} W+Jets ScaleFactor: %s"%(Scale_W_Factor_global_str)+" \hspace{6pt} TTBar ScaleFactor: %s"%(TTBar_Scale_Factor_mm_str);
        latex_FrameSubtitle=Frame_tmp+frameSubTitle_AD_string+"}\n";
    
        latex_FrameTitle="Basic Cuts and TWO b-Tagging";
        Output_Beamer_Latex_File_mm.write("\graphicspath{{/home/matteo/Tesi/LxPlus_Matteo/ControlPlots/20gen/SignalRegion/Consecutive_Cuts_%.0f/}}\n"%(Cuts_Total_Number_mm));
        latex_graph_include(sampleValue[nsample][0],sampleValue[nsample][2],sampleValue[nsample][5],Output_Beamer_Latex_File_mm,latex_FrameSubtitle,latex_FrameTitle,Channel_global);
        



        

        
        
        
        #####################
        ### CALCOLO INCERTEZZE MEDIANTE PROPAGAZIONE DEGLI ERRORI ASSUMENDO SQRT(N) COME ERRORE SUI CONTEGGI
        #####################        
        
        efficence_result_string=["FINAL CONTROL PLOTS",
                                 " ",
                                 " ",
                                 "Sample: %s"%sampleValue[nsample][0],
                                 " ",
                                 "Mass: %.0f"%sampleValue[nsample][2],
                                 " ",
                                 "Ended SignalRegion ControlPlots For SIGNIFICANCE"];
        
     
        print_boxed_string_File(efficence_result_string,summaryF_mm);
        
        
        
        
    # Slides with Cuts
    
    ## Consecutive Cuts
    Output_Beamer_Latex_File_mm.write("\n\n\n");
    Output_Beamer_Latex_File_mm.write("\changefontsizes{9pt}\n");
    Output_Beamer_Latex_File_mm.write("\\begin{frame}[t,allowframebreaks]\n");
    Output_Beamer_Latex_File_mm.write("\\frametitle{Control Plots - Consecutive Cuts }\n");   
    Output_Beamer_Latex_File_mm.write(latex_FrameSubtitle);
    Output_Beamer_Latex_File_mm.write("\changefontsizes{7pt}\n");
    Output_Beamer_Latex_File_mm.write("\\begin{longtable}{|M{10pt}|D{310pt}|}\n");
    Output_Beamer_Latex_File_mm.write("\hline \multicolumn{2}{|c|}{Consecutive Cuts} \\\ \n");
    
    
    j=0;
    for j in range(Cuts_Total_Number_mm):
        cn=j+1;
        tmp=replace_latex(cuts_table_main[0][j]);
        Output_Beamer_Latex_File_mm.write("\hline %.0f & %s \\\ \n"%(cn,tmp));
         
            
    Output_Beamer_Latex_File_mm.write("\hline\n");
    Output_Beamer_Latex_File_mm.write("\end{longtable}\n");
    Output_Beamer_Latex_File_mm.write("\end{frame}\n");
    
    if (Cuts_Total_Number_mm-1):
       ## Single Cut
       Output_Beamer_Latex_File_mm.write("\n\n\n");
       Output_Beamer_Latex_File_mm.write("\changefontsizes{9pt}\n");
       Output_Beamer_Latex_File_mm.write("\\begin{frame}\n");
       Output_Beamer_Latex_File_mm.write("\\frametitle{Control Plots - Single Cut }\n");   
       Output_Beamer_Latex_File_mm.write(latex_FrameSubtitle);
       Output_Beamer_Latex_File_mm.write("\changefontsizes{7pt}\n");
       Output_Beamer_Latex_File_mm.write("\\begin{table}[H]\n");
       Output_Beamer_Latex_File_mm.write("\\begin{center}\n");
       Output_Beamer_Latex_File_mm.write("\\begin{tabular}{|M{10pt}|D{310pt}|}\n");
       Output_Beamer_Latex_File_mm.write("\hline \multicolumn{2}{|c|}{Single Cut} \\\ \n");
    
       j=0;
       for j in range(Cuts_Total_Number_mm):
           cn=j+1;
           tmp=replace_latex(cuts_table_main[1][j]);
           Output_Beamer_Latex_File_mm.write("\hline %.0f & %s \\\ \n"%(cn,tmp));
          
            
    
       Output_Beamer_Latex_File_mm.write("\hline\n");
       Output_Beamer_Latex_File_mm.write("\end{tabular}\n");
       Output_Beamer_Latex_File_mm.write("\end{center}\n");
       Output_Beamer_Latex_File_mm.write("\end{table}\n");
       Output_Beamer_Latex_File_mm.write("\end{frame}\n");




            


    
    
    # Significance slides
    nsample=0;
    for nsample in range(Sample_Total_Number_mm):
        
        if (Cuts_Total_Number_mm-1): 
           # Consecutive Cuts
           
           tmp1_Latex_InValueVector=[Cuts_Total_Number_mm,Significance_Table_mm,1,nsample,Output_Beamer_Latex_File_mm,Ntuple_Name_texttt,latex_FrameSubtitle,sampleValue,number_Events_type,Channel_global];
           make_latex_table(tmp1_Latex_InValueVector);
        
           # Single Cut
           tmp2_Latex_InValueVector=[Cuts_Total_Number_mm,Significance_Table_mm,2,nsample,Output_Beamer_Latex_File_mm,Ntuple_Name_texttt,latex_FrameSubtitle,sampleValue,number_Events_type,Channel_global];
           make_latex_table(tmp2_Latex_InValueVector)
          
        else:
           # Consecutive Cuts
           tmpOnlyOneCut_Latex_InValueVector=[Cuts_Total_Number_mm,Significance_Table_mm,1,nsample,Output_Beamer_Latex_File_mm,Ntuple_Name_texttt,latex_FrameSubtitle,sampleValue,number_Events_type,Channel_global];
           make_latex_table(tmpOnlyOneCut_Latex_InValueVector);
    
    Output_Beamer_Latex_File_mm.write("\end{document}\n");

    Output_Beamer_Latex_File_mm.close();  
    
    
