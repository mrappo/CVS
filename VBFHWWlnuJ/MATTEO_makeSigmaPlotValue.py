import os
import glob
import math
import array
import ROOT
import ntpath
import sys
import subprocess
from subprocess import Popen
from optparse import OptionParser
#import CMS_lumi, tdrstyle
from array import array
from datetime import datetime

from ROOT import TColor, gROOT, TPaveLabel, gStyle, gSystem, TGaxis, TStyle, TLatex, TString, TF1,TFile,TLine, TLegend, TH1D,TH2D,THStack,TChain, TCanvas, TMatrixDSym, TMath, TText, TPad, RooFit, RooArgSet, RooArgList, RooArgSet, RooAbsData, RooAbsPdf, RooAddPdf, RooWorkspace, RooExtendPdf,RooCBShape, RooLandau, RooFFTConvPdf, RooGaussian, RooBifurGauss, RooArgusBG,RooDataSet, RooExponential,RooBreitWigner, RooVoigtian, RooNovosibirsk, RooRealVar,RooFormulaVar, RooDataHist, RooHist,RooCategory, RooChebychev, RooSimultaneous, RooGenericPdf,RooConstVar, RooKeysPdf, RooHistPdf, RooEffProd, RooProdPdf, TIter, kTRUE, kFALSE, kGray, kRed, kDashed, kGreen,kAzure, kOrange, kBlack,kBlue,kYellow,kCyan, kMagenta, kWhite, gPad





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
Deta=[0.0,1.0,1.5,2.0,2.5,3.0,3.5,4.0];
Mjj=[0.0,100.0,150.0,200.0,250.0,300.0,350.0,400.0];

######################################################
##### FUNCTION DEFINITION
######################################################
def set_palette(name,ncontours):
    """Set a color palette from a given RGB list
    stops, red, green and blue should all be lists of the same length
    see set_decent_colors for an example"""

    if name == "gray" or name == "grayscale":
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [1.00, 0.84, 0.61, 0.34, 0.00]
        green = [1.00, 0.84, 0.61, 0.34, 0.00]
        blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
    # elif name == "whatever":
        # (define more palettes)
    else:
        # default palette, looks cool
        stops = [0.00, 0.34, 0.61, 0.84, 0.90]
        red   = [0.35, 0.00, 0.87, 1.00, 0.61]
        green = [0.10, 0.81, 1.00, 0.20, 0.00]
        blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

    s = array('d', stops)
    r = array('d', red)
    g = array('d', green)
    b = array('d', blue)

    npoints = len(s)
    TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    gStyle.SetNumberContours(ncontours)

def readVBFCutsFile(in_VBFCutsFile):
    '''
    textName="VBF_CutListFile.txt";
    if options.pseudodata:
       
       if options.vbf:
          in_VBFCutsFile="../../../CMSSW_5_3_13/src/EXOVVFitter/Ntuple_%s/pseudoData/Lumi_%s_VBF/"%(options.ntuple,str("%.0f"%options.lumi))+textName;
       else:
          in_VBFCutsFile="../../../CMSSW_5_3_13/src/EXOVVFitter/Ntuple_%s/pseudoData/Lumi_%s/"%(options.ntuple,str("%.0f"%options.lumi))+textName;
    
    else:
       if options.vbf:
          in_VBFCutsFile="../../../CMSSW_5_3_13/src/EXOVVFitter/Ntuple_%s/trueData/Lumi_%s_VBF/"%(options.ntuple,str("%.0f"%options.lumi))+textName;
       else:
          in_VBFCutsFile="../../../CMSSW_5_3_13/src/EXOVVFitter/Ntuple_%s/trueData/Lumi_%s/"%(options.ntuple,str("%.0f"%options.lumi))+textName;    
    '''
    tmp_VBFCutsFile=open(in_VBFCutsFile, 'r');
    readedLines=tmp_VBFCutsFile.readlines();
    
    i=j=0;
    for i in readedLines:
        j=j+1;
    
    totalLineNumber=j;
    
    i=j=0;
    
    tmp_Cuts_Vector= [0 for i in range(totalLineNumber)];
    i=j=0;
    
    for i in range(totalLineNumber):
        tmp_Cuts_Vector[i]=[float((readedLines[i]).split(" ")[0]),float((readedLines[i]).split(" ")[1])];
        print tmp_Cuts_Vector[i]
    
    tmp_VBFCutsFile.close();
    return [totalLineNumber,tmp_Cuts_Vector];
    
    
    
    
def GetDataFromFile(filename):
    
    f = open(filename,'r');
    lines=f.readlines();
    
    i=j=0;
    for i in lines:
        j=j+1;
    
    out=[int(j),lines]
    return out;  
    




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
    
    Ntuple_Dir_mm="output/Ntuple_%s"%(options.ntuple);
    if not os.path.isdir(Ntuple_Dir_mm):
           print "\nError!!! Missing directory:%s \n EXIT"%Ntuple_Dir_mm
           sys.exit();


    Lumi_Dir_mm=Ntuple_Dir_mm+"/Lumi_%.0f"%(options.lumi);
    if not os.path.isdir(Lumi_Dir_mm):
           print "\nError!!! Missing directory:%s \n EXIT"%Lumi_Dir_mm
           sys.exit();
       

    ControlP_Dir_1=Lumi_Dir_mm+"/ControlPlots";
    if not os.path.isdir(ControlP_Dir_1):
           print "\nError!!! Missing directory:%s \n EXIT"%ControlP_Dir_1
           sys.exit();
    
    
    
    ControlP_Dir_2=ControlP_Dir_1+"/%s_Channel"%options.channel;
    if not os.path.isdir(ControlP_Dir_2):
           print "\nError!!! Missing directory:%s \n EXIT"%ControlP_Dir_2
           sys.exit();
           
    outputFileName=ControlP_Dir_2+"/Total_TTB_SF_Value.txt";
    outputFile=open(outputFileName,'w');
    outputFile.write("\nTTBar Scale Factor Total");
    outputFile.close();
           
    InputCutFileName=ControlP_Dir_2+"/CutValues.txt";
    print "\nLoad CutsInputFile: %s"%InputCutFileName
    
    readed_input_cuts=readVBFCutsFile(InputCutFileName);
    
    CutNumber=readed_input_cuts[0];
    CutValueVector=readed_input_cuts[1];
    
    i=0;
    ScaleFactorVector=[0.0 for i in range(CutNumber)];
    
    i=j=0;
    
    for i in range(CutNumber):
        
        i=int(i);
        tmp=CutValueVector[i];
        DEta_local=float("%1.3f"%tmp[0]);
        Mjj_local=float("%.1f"%tmp[1]);
        
        if (DEta_local==0.0 and Mjj_local==0.0):
           nJetsCut_value=0.0;
        else:
           nJetsCut_value=1.0;
        
        ControlP_Dir_3=ControlP_Dir_2+"/Deta%1.3f_Mjj%.0f_NJ%.0f"%(DEta_local,Mjj_local,nJetsCut_value);
        
        #print ControlP_Dir_3
        tmp_in_FileName=ControlP_Dir_3+"/Summary_CP_for_datacard.txt";
        tmp_Cut_Value_Vector=GetDataFromFile(tmp_in_FileName);
        
        error_value=[0.0,0.0,DEta_local,Mjj_local];
        if tmp_Cut_Value_Vector[0]<15:
           ScaleFactorVector[i]=error_value;
        
        else:
           tmp_CutVector=tmp_Cut_Value_Vector[1];
        
           tmp_TTB_SF=tmp_CutVector[14];
           tmp_TTB_SF_Sigma=tmp_CutVector[15];
        
           if (((tmp_TTB_SF).find('nan') != -1) or  (tmp_TTB_SF < 0.0)):
              ScaleFactorVector[i]=error_value;
           
           elif (((tmp_TTB_SF_Sigma).find('nan') != -1) or (tmp_TTB_SF_Sigma < 0.0)):
              ScaleFactorVector[i]=error_value;
           
           else:
              ScaleFactorVector[i]=[float(tmp_TTB_SF),float(tmp_TTB_SF_Sigma),DEta_local,Mjj_local];
           
           tmp_print_string=["READED TTB Value form File",
                             " ",
                             "file: %s"%ControlP_Dir_3,
                             " ",
                             "TTB ScaleFactor: %f"%ScaleFactorVector[i][0],
                             " ",
                             "Sigma TTB SF: %f"%ScaleFactorVector[i][1]];
           
           print_boxed_string_File(tmp_print_string,outputFileName);
    
    #TH2D (const char *name, const char *title, Int_t nbinsx, Double_t xlow, Double_t xup, Int_t nbinsy, Double_t ylow, Double_t yup)
    # x --> DEta
    # y --> Mjj
    #TCanvas (const char *name, const char *title="", Int_t form=1)
    canvas=TCanvas ("Plot","Plot", 1000,600);
    i=j=0;
    for i in Deta:
        j=j+1;
    
    Total_bin_deta=j;
    i=j=0;
    for i in Mjj:
        j=j+1;
    Total_bin_mjj=j;
    
    graph_val=ROOT.TH2D("graph_val","graph_val",Total_bin_mjj,Mjj[0],Mjj[Total_bin_mjj-1],Total_bin_deta,Deta[0],Deta[Total_bin_deta-1]);
    #graph_val.SetCanExtend(ROOT.TH1.kAllAxes);
    
    i=j=0;
    
    
    
        
    check_zero=1;
    for i in range(CutNumber):
        DEta_tmp=ScaleFactorVector[i][2];
        Mjj_tmp=ScaleFactorVector[i][3];
        TTB_SF_tmp=ScaleFactorVector[i][0];
        Sigma_TTB_SF_tmp=ScaleFactorVector[i][1];
        if TTB_SF_tmp==0:
           Sigma_rel=3.0;
        else:
           Sigma_rel=Sigma_TTB_SF_tmp/TTB_SF_tmp;
        print "\nUsed Value: %1.3f %.0f %f"%(DEta_tmp,Mjj_tmp,TTB_SF_tmp)
        j=k=0;
        for j in Deta:
            if DEta_tmp==Deta[k]:
               n_bin_deta=k;
            k=k+1;
            
        j=k=0;
        for j in Mjj:
            if Mjj_tmp==Mjj[k]:
               n_bin_mjj=k;
            k=k+1;
        
        '''
        if (DEta_tmp==0.0 and Mjj_tmp==0.0):
           DEta_tmp_zero=DEta_tmp;
           Mjj_tmp_zero=Mjj_tmp;
           TTB_SF_tmp_zero=TTB_SF_tmp;
           
        if (int(n_bin_mjj+1)==1 and int(n_bin_deta+1)==1):
           DEta_tmp=DEta_tmp_zero;
           Mjj_tmp=Mjj_tmp_zero;
           TTB_SF_tmp=TTB_SF_tmp_zero;
        
        if (DEta_tmpl!=0.0 and Mjj_tmp!=0.0 and int(n_bin_mjj+1)==1 and int(n_bin_deta+1)==1):
           DEta_tmp=DEta_tmp_zer;
           Mjj_tmp=Mjj_tmp_zero;
           TTB_SF_tmp=TTB_SF_tmp_zero;
        '''
           
        
        print "BIN: Mjj %.0f \tDEta %.0f \tValue %f "%(int(n_bin_mjj+1),int(n_bin_deta+1),TTB_SF_tmp)   
        graph_val.SetBinContent(n_bin_mjj+1,n_bin_deta+1,Sigma_rel);
        
        
           
        
    #SetBinContent (Int_t binx, Int_t biny, Double_t content)
    #gStyle.SetOptStat("ne");
    gStyle.SetOptStat(0);
    canvasFileName=ControlP_Dir_2+"/Sigma_Graph.pdf";
    #graph_val.SetFillColor(29);
    graph_val.GetXaxis().CenterLabels(kTRUE);
    graph_val.GetYaxis().CenterLabels(kTRUE);
    
    
    i=j=0;
    for i in range(Total_bin_mjj):
         	
        graph_val.GetXaxis().SetBinLabel(i+1,str("%.0f"%(Mjj[i])));
        
   
    
    i=j=0;
    for i in range(Total_bin_deta):
        
        graph_val.GetYaxis().SetBinLabel(i+1,str("%1.3f"%(Deta[i])));
    
    
    graph_val.GetXaxis().SetTitle("M_{jj}");
    graph_val.GetXaxis().CenterTitle(kTRUE);
    graph_val.GetXaxis().SetTitleOffset(1.5);
    graph_val.GetYaxis().SetTitle("#Delta#eta_{jj}");
    graph_val.GetYaxis().CenterTitle(kTRUE);
    graph_val.GetYaxis().SetTitleOffset(1.5);
    #graph_val.LabelsDeflate("X");
    #graph_val.LabelsDeflate("Y");
    #graph_val.LabelsOption("v");
    
    #gStyle.SetPalette(1,0.0);
    #graph_val.GetYaxis().SetNdivisions(7);
    #graph_val.GetYaxis().SetTickLength(1);
    #graph_val.SetNdivisions(7);
    #graph_val.SetTickLength(1);
    #ROOT.gPad.Modified();
    #ROOT.gPad.Update();
    
    #gStyle.SetPalette(57);
    set_palette("palette",99);
    #gStyle.SetNumberContours(99);
    gPad.SetTheta(30); # default is 30
    #gPad.SetPhi(170); # default is 30
    gPad.Update();
    graph_val.SetTitle("Sigma Relativa TTBar ScaleFactor for DataCard")
    graph_val.Draw("LEGO2Z");
    #graph_val.Draw("SURF3");
    
    #graph_val.Draw("b lego1");
    canvas.SaveAs(canvasFileName);
    raw_input('Press Enter to exit')
    
