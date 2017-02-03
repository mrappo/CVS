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

from ROOT import gROOT, TPaveLabel, gStyle, gSystem, TGaxis, TStyle, TLatex, TString, TF1,TFile,TLine, TLegend, TH1D,TH2D,THStack,TChain, TCanvas, TMatrixDSym, TMath, TText, TPad, RooFit, RooArgSet, RooArgList, RooArgSet, RooAbsData, RooAbsPdf, RooAddPdf, RooWorkspace, RooExtendPdf,RooCBShape, RooLandau, RooFFTConvPdf, RooGaussian, RooBifurGauss, RooArgusBG,RooDataSet, RooExponential,RooBreitWigner, RooVoigtian, RooNovosibirsk, RooRealVar,RooFormulaVar, RooDataHist, RooHist,RooCategory, RooChebychev, RooSimultaneous, RooGenericPdf,RooConstVar, RooKeysPdf, RooHistPdf, RooEffProd, RooProdPdf, TIter, kTRUE, kFALSE, kGray, kRed, kDashed, kGreen,kAzure, kOrange, kBlack,kBlue,kYellow,kCyan, kMagenta, kWhite



def SumSquareRelErrors(sigma_rel_vector):

    i=j=0;

    for j in sigma_rel_vector:
        i=i+1;
    
    Number_sigma=i;
 
    Square_Error_rel=0;
    i=0;
    for i in range(Number_sigma):
        Square_Error_rel=Square_Error_rel+TMath.Power(sigma_rel_vector[i],2);

    Error_rel=TMath.Sqrt(Square_Error_rel);

    return Error_rel;












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
    if total_lenght > 120:
       total_lenght=120;


        
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









def print_boxed_string_File(in_string_vector,out_fileName):
    
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
    if total_lenght > 120:
       total_lenght=120;
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
    
    out_file=open(out_fileName,'a');
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















#def make_latex_table(Cuts_Total_Number_tk,Sig_Data_Table_tk,ctype_tk,Sample_Number_tk,Output_File_tk,NtupleTTName_tk,frameSubTitle_tk,sampleValue_tk,number_Events_type_tk,Channel_global_tk):

def make_latex_table(in_tk_VectorValue):
   
    Cuts_Total_Number_tk=in_tk_VectorValue[0];
    Sig_Data_Table_tk=in_tk_VectorValue[1];
    ctype_tk=in_tk_VectorValue[2];
    Sample_Number_tk=in_tk_VectorValue[3];
    Output_File_tk=in_tk_VectorValue[4];
    NtupleTTName_tk=in_tk_VectorValue[5];
    frameSubTitle_tk=in_tk_VectorValue[6];
    sampleValue_tk=in_tk_VectorValue[7];
    number_Events_type_tk=in_tk_VectorValue[8];
    Channel_global_tk=in_tk_VectorValue[9];
    
    
    Cut_Type_tk=ctype_tk-1;
    Sample_tk=sampleValue_tk[Sample_Number_tk][0];
    Mass_Str_tk=str(sampleValue_tk[Sample_Number_tk][2]);
    
    Output_File_tk.write("\n\n\n\n");
    Output_File_tk.write("\changefontsizes{9pt}\n");
    Output_File_tk.write("\\begin{frame}[allowframebreaks]\n");
    Output_File_tk.write("\changefontsizes{8pt}\n");
    
    if Cut_Type_tk:
           Output_File_tk.write("\\frametitle{%s %s - Control Plots - Single Cut }\n"%(Sample_tk,Mass_Str_tk));   
           Output_File_tk.write(frameSubTitle_tk);
    else:
           Output_File_tk.write("\\frametitle{%s %s - Control Plots - Consecutive Cuts }\n"%(Sample_tk,Mass_Str_tk));   
           Output_File_tk.write(frameSubTitle_tk);
    
    
    latex_table=[[0 for i in range(number_Events_type_tk+5)] for j in range(Cuts_Total_Number_tk+1)];
    latex_table[0][0]="Cut";
    latex_table[0][1]="W+Jet Py";
    latex_table[0][2]="W+JetHe";
    latex_table[0][3]="TTbarPo";
    latex_table[0][4]="TTbarMC";
    latex_table[0][5]="VVqcd";
    latex_table[0][6]="WWewk";
    latex_table[0][7]="Stop";
    latex_table[0][8]="AllBkgPy";
    latex_table[0][9]="AllBkgHe";
    latex_table[0][10]="Signalgg";
    latex_table[0][11]="SignalVBF";
    latex_table[0][12]="SigPy";
    latex_table[0][13]="SigHe";
    latex_table[0][14]="$\\frac{S_j}{S_{j-1}}$ Pythia";
    latex_table[0][15]="$\\frac{S_j}{S_{j-1}}$ Herwig";
    
        
    
    n_cut=0;
    for n_cut in range(Cuts_Total_Number_tk):
        latex_table[n_cut+1][0]=n_cut+1;
        ev=0;
        for ev in range(number_Events_type_tk):
            latex_table[n_cut+1][ev+1]=Sig_Data_Table_tk[Cut_Type_tk][n_cut][Sample_Number_tk][ev];
            #print "Cut_Type_tk: %.0f\t CutNumber:%.0f\t SampleNumber:%.0f\t Line:%.0f\t VALUE:%f"%(Cut_Type_tk,c,Sample_Number_tk,ev+2,latex_table[c+1][ev+1])

        sig_n_py=Sig_Data_Table_tk[Cut_Type_tk][n_cut][Sample_Number_tk][number_Events_type_tk]
        sig_n_he=Sig_Data_Table_tk[Cut_Type_tk][n_cut][Sample_Number_tk][number_Events_type_tk+1]
        latex_table[n_cut+1][12]=sig_n_py;
        latex_table[n_cut+1][13]=sig_n_he;
        
        #latex_table[c+1][12]=latex_table[c+1][11]/(1+TMath.Sqrt(latex_table[c+1][8]));
        #latex_table[c+1][13]=latex_table[c+1][11]/(1+TMath.Sqrt(latex_table[c+1][9]));
    
        
        if n_cut:
           sig_n_1_py=Sig_Data_Table_tk[Cut_Type_tk][n_cut-1][Sample_Number_tk][number_Events_type_tk];
           sig_n_1_he=Sig_Data_Table_tk[Cut_Type_tk][n_cut-1][Sample_Number_tk][number_Events_type_tk+1];
           
           if (sig_n_1_py and sig_n_1_he):
              sig_rel_py=sig_n_py/sig_n_1_py;
              sig_rel_he=sig_n_he/sig_n_1_he;
           else:
              sig_rel_py=0;
              sig_rel_he=0;
        else:
           sig_rel_py=sig_n_py;
           sig_rel_he=sig_n_he;
           
        latex_table[n_cut+1][14]=sig_rel_py;
        latex_table[n_cut+1][15]=sig_rel_he;
        
       
    if Cut_Type_tk:
       table_string_name="Single Cut %s%s"%(Sample_tk,Mass_Str_tk);
    else:
       table_string_name="Consecutive Cuts %s%s"%(Sample_tk,Mass_Str_tk);
       

    Output_File_tk.write("\n\n\n");
    Output_File_tk.write("\\begin{table}[H]\n");
    Output_File_tk.write("\\begin{center}\n");
    Output_File_tk.write("\\begin{tabular}{|c|c|c|c|c|c|c|}\n");
    Output_File_tk.write("\hline \multicolumn{7}{|c|}{%s} \\\ \n"%(table_string_name));
    
    '''
    for r in range(Cuts_Total_Number_tk+1):
        for c in range(number_Events_type+3):
            if not r:
                   print "Riga:%.0f\tColonna:%.0f\tVALUE:%s\n"%(r,c,latex_table[r][c])
            else:
                   print "Riga:%.0f\tColonna:%.0f\tVALUE:%f\n"%(r,c,latex_table[r][c])
    '''
    for r in range(Cuts_Total_Number_tk+1):
        if r:
           Output_File_tk.write("\hline %.0f & %.4f & %.5f & %.5f & %.5f & %.4f & %.5f \\\ \n"%(latex_table[r][0],latex_table[r][1],latex_table[r][3],latex_table[r][4],latex_table[r][5],latex_table[r][6],latex_table[r][7]));
        else:
           Output_File_tk.write("\hline %s & %s & %s & %s & %s & %s & %s \\\ \n"%(latex_table[r][0],latex_table[r][1],latex_table[r][3],latex_table[r][4],latex_table[r][5],latex_table[r][6],latex_table[r][7]));
        
            
    
    Output_File_tk.write("\hline\n");
    Output_File_tk.write("\end{tabular}\n");
    #Output_File_tk.write("\\caption{Significanza in funzione delle Input Variables for Cut Optimization per diversi valori di risonanza}\n");
    Output_File_tk.write("\end{center}\n");
    Output_File_tk.write("\end{table}\n");
    
    Output_File_tk.write("\\framebreak\n");
    
    
                
    if Cut_Type_tk:
       Output_File_tk.write("\n\n\n");
       Output_File_tk.write("\\begin{table}[H]\n");
       Output_File_tk.write("\\begin{center}\n");
       Output_File_tk.write("\\begin{tabular}{|c|c|c|c|c|c|c|}\n");
       Output_File_tk.write("\hline \multicolumn{7}{|c|}{%s} \\\ \n"%(table_string_name));
    
    
       r=0;  
       for r in range(Cuts_Total_Number_tk+1):
           if r:
              Output_File_tk.write("\hline %.0f & %f & %f & %f & %f & %f & %f \\\ \n"%(latex_table[r][0],latex_table[r][8],latex_table[r][9],latex_table[r][10],latex_table[r][11],latex_table[r][12],latex_table[r][13]));
           else:
              Output_File_tk.write("\hline %s & %s & %s & %s & %s & %s & %s \\\ \n"%(latex_table[r][0],latex_table[r][8],latex_table[r][9],latex_table[r][10],latex_table[r][11],latex_table[r][12],latex_table[r][13]));
        
            
    
       Output_File_tk.write("\hline\n");
       Output_File_tk.write("\end{tabular}\n");
       #Output_File_tk.write("\\caption{Significanza in funzione delle Input Variables for Cut Optimization per diversi valori di risonanza}\n");
       Output_File_tk.write("\end{center}\n");
       Output_File_tk.write("\end{table}\n");
       
    else:
       Output_File_tk.write("\n\n\n");
       Output_File_tk.write("\\begin{table}[H]\n");
       Output_File_tk.write("\\begin{center}\n");
       Output_File_tk.write("\\begin{tabular}{|c|c|c|c|c|c|c|}\n");
       Output_File_tk.write("\hline \multicolumn{7}{|c|}{%s} \\\ \n"%(table_string_name));
    
    
       r=0;
       for r in range(Cuts_Total_Number_tk+1):
           if r:
              Output_File_tk.write("\hline %.0f & %f & %f & %f & %f & %f & %f \\\ \n"%(latex_table[r][0],latex_table[r][8],latex_table[r][9],latex_table[r][10],latex_table[r][11],latex_table[r][12],latex_table[r][13]));
           else:
              Output_File_tk.write("\hline %s & %s & %s & %s & %s & %s & %s \\\ \n"%(latex_table[r][0],latex_table[r][8],latex_table[r][9],latex_table[r][10],latex_table[r][11],latex_table[r][12],latex_table[r][13]));
        
            
    
       Output_File_tk.write("\hline\n");
       Output_File_tk.write("\end{tabular}\n");
       #Output_File_tk.write("\\caption{Significanza in funzione delle Input Variables for Cut Optimization per diversi valori di risonanza}\n");
       Output_File_tk.write("\end{center}\n");
       Output_File_tk.write("\end{table}\n");
       
       Output_File_tk.write("\\framebreak\n");
       
       Output_File_tk.write("\n\n\n");
       Output_File_tk.write("\\begin{table}[H]\n");
       Output_File_tk.write("\\begin{center}\n");
       Output_File_tk.write("\\begin{tabular}{|c|c|c|}\n");
       Output_File_tk.write("\hline \multicolumn{3}{|c|}{%s} \\\ \n"%(table_string_name));
    
    
       r=0;
       for r in range(Cuts_Total_Number_tk+1):
           if r:
              Output_File_tk.write("\hline %.0f & %f & %f  \\\ \n"%(latex_table[r][0],latex_table[r][14],latex_table[r][15]));
           else:
              Output_File_tk.write("\hline %s & %s & %s \\\ \n"%(latex_table[r][0],latex_table[r][14],latex_table[r][15]));
        
            
    
       Output_File_tk.write("\hline\n");
       Output_File_tk.write("\end{tabular}\n");
       #Output_File_tk.write("\\caption{Significanza in funzione delle Input Variables for Cut Optimization per diversi valori di risonanza}\n");
       Output_File_tk.write("\end{center}\n");
       Output_File_tk.write("\end{table}\n");       
       
    Output_File_tk.write("\end{frame}\n");


def replace_latex(in_string):
    out1=in_string.replace("&&", "\&\&");
    out2=out1.replace("_", "\_");
    out3=out2.replace(">", "\\texttt{>}");
    out4=out3.replace("<", "\\texttt{<}");
    out5=out4.replace("||", "$||$")
    return out5


    
def latex_graph_include(Sample_gi,Mass_gi,ScaleFactor_gi,ofile_gi,FrameSubTitle_gi,FrameTitle_gi,Channel_global_tk):




    SampleMass_gi=Sample_gi+str("%.0f"%Mass_gi);
    ofile_gi.write("\\begin{frame}[allowframebreaks]\n");
    ofile_gi.write("\\frametitle{Control Plots: %s %.0f - SignalScaleFactor %.0f - %s }\n"%(Sample_gi,Mass_gi,ScaleFactor_gi,FrameTitle_gi));
    ofile_gi.write(FrameSubTitle_gi);

    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{$\Delta\eta_{jj}$}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/abs_vbf_maxpt_j1_eta-vbf_maxpt_j2_eta__0.pdf}} \quad\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{$\Delta\eta_{jj}$ Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/abs_vbf_maxpt_j1_eta-vbf_maxpt_j2_eta__0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    #ofile_gi.write("\%\caption{$\mu$-channel: Input Variables for Cut Optimization.}\n");
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");

    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{$M_{jj}$}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/vbf_maxpt_jj_m_0.pdf}} \quad\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{$M_{jj}$ Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/vbf_maxpt_jj_m_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    #ofile_gi.write("\%\caption{$\mu$-channel: Input Variables for Cut Optimization.}\n"%SampleMass_gi);
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");
    

    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{$pfMET$}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/pfMET_0.pdf}} \quad \n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{$pfMET$ Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/pfMET_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");

    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{Lepton $P_{t}$}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/l_pt_0.pdf}} \quad \n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{Lepton $P_{t}$ Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/l_pt_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");




    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{\\texttt{ungroomed\_jet\_pt\_0}}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/ungroomed_jet_pt_0.pdf}} \quad \n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{\\texttt{ungroomed\_jet\_pt\_0} Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/ungroomed_jet_pt_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");

    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{\\texttt{v\_pt\_0}}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/v_pt_0.pdf}} \quad \n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{\\texttt{v\_pt\_0} Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/v_pt_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");

    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{\\texttt{vbf\_maxpt\_j1\_eta\_0}}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/vbf_maxpt_j1_eta_0.pdf}} \quad \n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{\\texttt{vbf\_maxpt\_j1\_eta\_0} Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/vbf_maxpt_j1_eta_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");






    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{\\texttt{vbf\_maxpt\_j2\_eta}}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/vbf_maxpt_j2_eta_0.pdf}}  \quad \n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{\\texttt{vbf\_maxpt\_j2\_eta} Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/vbf_maxpt_j2_eta_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");
    
    
    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{\\texttt{vbf\_maxpt\_j1\_bDiscriminatorCSV}}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/vbf_maxpt_j1_bDiscriminatorCSV_0.pdf}}  \quad \n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{\\texttt{vbf\_maxpt\_j1\_bDiscriminatorCSV} Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/vbf_maxpt_j1_bDiscriminatorCSV_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");
    
    
    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{\\texttt{vbf\_maxpt\_j2\_bDiscriminatorCSV}}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/vbf_maxpt_j2_bDiscriminatorCSV_0.pdf}}  \quad \n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{\\texttt{vbf\_maxpt\_j2\_bDiscriminatorCSV} Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/vbf_maxpt_j2_bDiscriminatorCSV_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");
    
    
    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{$\\frac{\\tau_2}{\\tau_1}$}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/jet_tau2tau1_0.pdf}}  \quad \n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{$\\frac{\\tau_2}{\\tau_1}$ Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/jet_tau2tau1_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");
    
    
    
    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{\\texttt{deltaR\_lak8jet}}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/deltaR_lak8jet_0.pdf}}  \quad \n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{\\texttt{deltaR\_lak8jet} Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/deltaR_lak8jet_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");
    
  
    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{\\texttt{deltaphi\_METak8jet}}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/deltaphi_METak8jet_0.pdf}}  \quad \n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{\\texttt{deltaphi\_METak8jet} Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/deltaphi_METak8jet_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");
    
    
    ofile_gi.write("\\framebreak\n");
    ofile_gi.write("\setcounter{subfigure}{0}\n");
    ofile_gi.write("\\begin{figure}[h]\n");
    ofile_gi.write("\\begin{center}\n");
    ofile_gi.write("\subfloat[][\emph{\\texttt{deltaphi\_Vak8jet}}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/deltaphi_Vak8jet_0.pdf}}  \quad \n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\subfloat[][\emph{\\texttt{deltaphi\_Vak8jet} Log Scale}]\n");
    ofile_gi.write("{\includegraphics[width=.45\columnwidth]{%s/data/Run2_MCDataComparisonRSGraviton2000_%s_plot/deltaphi_Vak8jet_0_Log.pdf}}\n"%(SampleMass_gi,Channel_global_tk));
    ofile_gi.write("\label{}\n");
    ofile_gi.write("\end{center}\n");
    ofile_gi.write("\end{figure}\n");
        
     
 
  
    

    ofile_gi.write("\end{frame}\n");
    
    
   
    
    








def run_log(in_vector_value_ll):
    
    Sample_Number_ll=in_vector_value_ll[0];
    Cut_Number_ll=in_vector_value_ll[1];
    C_Type_ll=in_vector_value_ll[2];
    Cut_Total_Number_ll=in_vector_value_ll[3];
    Significance_Table_ll=in_vector_value_ll[4];
    Input_Cfg_File_ll=in_vector_value_ll[5];
    Summary_Output_FileName_ll=in_vector_value_ll[6];
    Directory_Path_ll=in_vector_value_ll[7];
    TTB_ScaleFactor_ll=in_vector_value_ll[8];
    sampleValue_ll=in_vector_value_ll[9];
    channel_ll=in_vector_value_ll[10];
    Scale_ww_ll=in_vector_value_ll[11];
    number_Events_type_ll=in_vector_value_ll[12];
    total_sample_value_ll=in_vector_value_ll[13];
    Channel_global_ll=in_vector_value_ll[14];
    
    
    
    TTB_ScaleFactor_ll_str=str(TTB_ScaleFactor_ll);
    Cut_Type_ll=C_Type_ll-1;
    Sample_ll=sampleValue_ll[Sample_Number_ll][0];
    Mass_ll=sampleValue_ll[Sample_Number_ll][2];        
    Mass_ll_str=str("%.0f"%Mass_ll);
    process_name=Sample_ll+Mass_ll_str;
    
    
    Summary_Output_File_ll=open(Summary_Output_FileName_ll,'a');
    
           
    Log_Dir_ll=Directory_Path_ll+"/log";
    if not os.path.isdir(Log_Dir_ll):
           pdl1 = subprocess.Popen(['mkdir',Log_Dir_ll]);
           pdl1.wait();
            
    Data_Dir_ll=Directory_Path_ll+"/data";
    if not os.path.isdir(Data_Dir_ll):
           pdl2 = subprocess.Popen(['mkdir',Data_Dir_ll]);
           pdl2.wait();
    
    cn_print=Cut_Number_ll+1; 
    if Cut_Type_ll:
       print_string=("\tSingle CUT: %.0f of %.0f")%(cn_print,Cut_Total_Number_ll);     
    else:
       print_string=("\tRecursive CUTS: %.0f of %.0f")%(cn_print,Cut_Total_Number_ll);
    
    log_file1=Log_Dir_ll+"/Log_ControlPlots_%s_%s%s.txt"%(channel_ll,Sample_ll,Mass_ll_str)
    log_file2=Log_Dir_ll+"/Error_Log_ControlPlots_%s_%s%s.txt"%(channel_ll,Sample_ll,Mass_ll_str)
     
          
    output_log1=open(log_file1,'w+')
    output_log1.write("\n\n--------------------------------\n\n")
    output_log1.write("STARTING\t\t")
    output_log1.write(process_name)
    output_log1.write(print_string)
    output_log1.write("\n\n--------------------------------\n\n")
            
    output_log2=open(log_file2,'w+')
    output_log2.write("\n\n--------------------------------\n\n")
    output_log2.write("STARTING\t\t")
    output_log2.write(process_name)
    output_log2.write(print_string)
    output_log2.write("\n\n--------------------------------\n\n")
          
    sys.stdout.write("\n\n\n\n-------------------------------------------------------------------------------------------------------\n\n")
    sys.stdout.write("STARTING\t\t")
    sys.stdout.write(process_name)
    sys.stdout.write(print_string)
    sys.stdout.write("\n\n")
    
    #Summary_Output_File_ll.write("\n\n--------------------------------\n\n")
    Summary_Output_File_ll.write("\n-------------------------------------------------------------------------------------------------------\n\n")
    Summary_Output_File_ll.write("STARTING\t\t")
    Summary_Output_File_ll.write(process_name)
    Summary_Output_File_ll.write(print_string)
    #Summary_Output_File_ll.write("\n\n--------------------------------\n\n")                
    
    Wjets_Pythia_Events_d="Jets Pythia  Events:           ";
    Wjets_Herwig_Events_d="Jets Herwig  Events:           ";
    TTbar_Powegh_Events_d="Tbar Powegh Events:           ";
    TTbar_MC_Events_d="Tbar mc@nlo Events:           ";
    VV_QCD_Events_d="V Events QCD:              ";
    WW_EWK_Events_d="W Events EWK:              ";
    STop_Events_d="Top Events:            ";
    All_bkg_Pythia_d="l Backgrounds Events Pythia: ";
    All_bkg_Herwig_d="l Backgrounds Events Herwig: ";
    Signal_gg_d="ignal ggH:             ";
    Signal_VBF_d="ignal qqH:             ";
    
     

    
    Events_type=[Wjets_Pythia_Events_d,Wjets_Herwig_Events_d,TTbar_Powegh_Events_d,TTbar_MC_Events_d,VV_QCD_Events_d,WW_EWK_Events_d,STop_Events_d,All_bkg_Pythia_d,All_bkg_Herwig_d,Signal_gg_d,Signal_VBF_d];
    
    
    #Scale_ww_ll=Scale_W_Factor_global_str;
    pdl3 = subprocess.Popen(['./bin/DataMCComparisonPlot.exe',Input_Cfg_File_ll[0],Scale_ww_ll,"1",TTB_ScaleFactor_ll_str],stdout=subprocess.PIPE,stderr=output_log2)
    ev=0;
    #ev_ttb=0;
    #ev_counter=0;
    TTB_data=0;
    TTB_check1=0;
    TTB_check2=0;
    TTB_check3=0;
    #start=0;
    for line in pdl3.stdout:
        #sys.stdout.write(line)
        output_log1.write(line)
        
        
        if line.find('WWTree_data_golden_2p1.root') !=-1:
           TTB_check1=TTB_check1+1;
           
           
           
        if TTB_check2:
           cut_string1=line.split("ata Entries ");
           t1=cut_string1[1];
           cut_string2=t1.split(" weigthed events ");
           t2=cut_string2[0];
           TTB_data=float(t2);
           Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll+2]=TTB_data;
           
           Summary_Output_File_ll.write("\n");   
           Summary_Output_File_ll.write(line);
           Summary_Output_File_ll.write("\n DATA Number of Events: %f\n"%TTB_data);
           Summary_Output_File_ll.write("\n--------------------------------------------------\n\n\n");
           
           print line
           print "\n DATA Number of Events: %f"%TTB_data
           print "\n--------------------------------------------------\n\n"
           TTB_check2=0;
              
        if TTB_check1==1: 
           
           Summary_Output_File_ll.write("\n\n-------------- Read DATA Events Number NOT WEIGHTED: -----------------\n");
           Summary_Output_File_ll.write(line);  

           
           print "\n\n-------------- Read DATA Events Number NOT WEIGHTED: -----------------\n"
           print line  
           TTB_check1=TTB_check1+1;
           TTB_check2=1;
              
        if line.find("Event Scaled To Lumi") !=-1:
           TTB_check3=1;

        if TTB_check3:
           print line
           Summary_Output_File_ll.write("\n"+line);
           #TTB_check3=TTB_check3+1;
        
        
        
        
        #if line.find('Event Scaled To Lumi') !=-1:
        #   start=1;
        #if start:   
        #   Summary_Output_File_ll.write("\n"+line);
        counter_events_type=0;
        for ev in Events_type:
            if line.find(ev) !=-1:
               cut_string = line.split(ev);
               new_string = cut_string[1]
               #print line
               #Summary_Output_File_ll.write("\n"+line);
               val=float(new_string);
               Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][counter_events_type]=val;
               #print "Cut_Type_ll: %.0f\t Cut_Number_ll:%.0f\t Sample_Number_ll:%.0f\t Line:%.0f\t VALUE:%f"%(Cut_Type_ll,cnumber,k,cn+2,val)
            
               
            counter_events_type=counter_events_type+1;
    pdl3.wait();    
    
    
    
    
    
    
    
    
    
    
    
    
    sig_Pytia=Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll-1]/(1+TMath.Sqrt(Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll-4]));
    sig_Herwig=Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll-1]/(1+TMath.Sqrt(Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll-3]));
    Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll]=sig_Pytia;
    Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll+1]=sig_Herwig;
    Summary_Output_File_ll.close();
    Significance_result_string=["Calculate Significance",
                                " ",
                                "qq signal: %f"% Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll-1],
                                " ",
                                "Pythia Bkg: %f"% Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll-4],
                                " ",
                                "Hewig Bkg: %f"% Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll-3],
                                " ",
                                "Sig Pythia: %f"% sig_Pytia,
                                " ",
                                "Sig Herwig: %f"% sig_Herwig]

    print_boxed_string_File(Significance_result_string,Summary_Output_FileName_ll);



    
    Data_ll=Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll+2];
    TTBar_MC_ll=Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][2];
    STop_MC_ll=Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][6];
    WJets_MC_ll=Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][0];
    VV_MC_ll=Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][4]+Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][5];
    
    #TTBar_data_ll=Data_ll-WJets_MC_ll-VV_MC_ll;
    #Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll+3]=TTBar_data_ll;
    
    
    
    result_string=["DATA READED FROM ANALYSIS",
                   " ",
                   "Wjets_Pythia MC Events: %f"%Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][0], # 0
                   " ",
                   "Wjets_Herwig MC Events: %f"%Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][1],# 1
                   " ",
                   "TTbar_Powegh MC Events: %f"%Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][2], # 2
                   " ",
                   "TTbar_MC MC Events: %f"%Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][3], # 3
                   " ",
                   "VV_QCD MC Events: %f"%Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][4], # 4
                   " ",
                   "WW_EWK MC Events: %f"%Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][5], # 5
                   " ",
                   "STop MC Events: %f"%Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][6], # 6
                   " ",
                   "All_bkg_Pythia MC Events: %f"%Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][7], # 7
                   " ",
                   "All_bkg_Herwig MC Events: %f"%Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][8], # 8
                   " ",
                   "Signal_gg MC Events: %f"%Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][9], # 9
                   " ",
                   "Signal_VBF MC Events: %f"%Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][10], # 10
                   " ",
                   "Data: %f"%Significance_Table_ll[Cut_Type_ll][Cut_Number_ll][Sample_Number_ll][number_Events_type_ll+2]]; #13
    
 
    print_boxed_string_File(result_string,Summary_Output_FileName_ll);
 
    

    
    
    print "\nInputFile: %s"%Input_Cfg_File_ll[0]   
    print "\nOutputDirectory: %s"%Input_Cfg_File_ll[1]
    
    Summary_Output_File_ll=open(Summary_Output_FileName_ll,'a');
    Summary_Output_File_ll.write("\n\nInputFile: %s"%Input_Cfg_File_ll[0]);
    Summary_Output_File_ll.write("\n\nOutputDirectory: %s"%Input_Cfg_File_ll[1]);
    
    
    print "\nVBF_Sample: %s \tReducedName: %s \tMass: %.0f \txSec: %f \tNumbEntBefore: %.0f \tScaleFactor: %.0f\n"%(total_sample_value_ll[1][Sample_Number_ll][0],total_sample_value_ll[1][Sample_Number_ll][1],total_sample_value_ll[1][Sample_Number_ll][2],total_sample_value_ll[1][Sample_Number_ll][3],total_sample_value_ll[1][Sample_Number_ll][4],total_sample_value_ll[1][Sample_Number_ll][5])
    
    print "\nNormal_Sample: %s \tReducedName: %s \tMass: %.0f \txSec: %f \tNumbEntBefore: %.0f \tScaleFactor: %.0f\n"%(total_sample_value_ll[0][Sample_Number_ll][0],total_sample_value_ll[0][Sample_Number_ll][1],total_sample_value_ll[0][Sample_Number_ll][2],total_sample_value_ll[0][Sample_Number_ll][3],total_sample_value_ll[0][Sample_Number_ll][4],total_sample_value_ll[0][Sample_Number_ll][5])
    
    Summary_Output_File_ll.write("\n\nVBF_Sample: %s \tReducedName: %s \tMass: %.0f \txSec: %f \tNumbEntBefore: %.0f \tScaleFactor: %.0f\n"%(total_sample_value_ll[1][Sample_Number_ll][0],total_sample_value_ll[1][Sample_Number_ll][1],total_sample_value_ll[1][Sample_Number_ll][2],total_sample_value_ll[1][Sample_Number_ll][3],total_sample_value_ll[1][Sample_Number_ll][4],total_sample_value_ll[1][Sample_Number_ll][5]));
    
    Summary_Output_File_ll.write("\nNormal_Sample: %s \tReducedName: %s \tMass: %.0f \txSec: %f \tNumbEntBefore: %.0f \tScaleFactor: %.0f\n"%(total_sample_value_ll[0][Sample_Number_ll][0],total_sample_value_ll[0][Sample_Number_ll][1],total_sample_value_ll[0][Sample_Number_ll][2],total_sample_value_ll[0][Sample_Number_ll][3],total_sample_value_ll[0][Sample_Number_ll][4],total_sample_value_ll[0][Sample_Number_ll][5]));
    
    path_dir_in_tmp=Input_Cfg_File_ll[1];
    path_dir_in=path_dir_in_tmp+"Run2_MCDataComparisonRSGraviton2000_%s_plot"%Channel_global_ll; 
    #path_dir_in="output/run2/MCDATAComparisonPlot_mu_22sep_%s/Run2_MCDataComparisonRSGraviton2000_mu_plot"%process_name;
    path_dir_out=Directory_Path_ll;
    pdl4 = subprocess.Popen(['cp','-r',path_dir_in,path_dir_out])
    pdl4.wait()

    print "\n\nCopy DATA from: %s"%path_dir_in
    print "\nCopy DATA to: %s"%path_dir_out
    
    Summary_Output_File_ll.write("\n\nCopy DATA from: %s"%path_dir_in);
    Summary_Output_File_ll.write("\nCopy DATA to: %s"%path_dir_out);

    data_in=Directory_Path_ll+"/Run2_MCDataComparisonRSGraviton2000_%s_plot/"%Channel_global_ll;
    data_out=Directory_Path_ll+"/data/";
    pdl5 = subprocess.Popen(['mv',data_in,data_out])
    pdl5.wait()
    print "\n\nMove DATA from: %s"%data_in
    print "\nMove DATA to: %s\n\n"%data_out
    
    
    Summary_Output_File_ll.write("\n\nMove DATA from: %s"%data_in);
    Summary_Output_File_ll.write("\nMove DATA to: %s\n\n"%data_out);

    root_in=path_dir_in_tmp+"Run2_MCDataComparisonRSGraviton2000_%s.root"%Channel_global_ll;
    root_out=data_out+"/Root_ControlPlots_out_%s.root"%process_name;
    pdl6 = subprocess.Popen(['cp',root_in,root_out])
    pdl6.wait()

    if os.path.isdir(data_in):
       pdl7=subprocess.Popen(['rm','-r',data_in])
       pdl7.wait()
                     
    
            
    output_log1.write("\n\n--------------------------------\n\n");
    output_log1.write("ENDED\t\t");
    output_log1.write(process_name);
    output_log1.write(print_string);
    output_log1.write("\n\n--------------------------------\n\n");
    output_log1.close();
            
    output_log2.write("\n\n--------------------------------\n\n");
    output_log2.write("ENDED\t\t")
    output_log2.write(process_name);
    output_log2.write(print_string);
    output_log2.write("\n\n--------------------------------\n\n");
    output_log2.close();
            
                        
    #sys.stdout.write("\n\n------------------------------------------------------------------\n\n")
    sys.stdout.write("\nENDED\t\t")
    sys.stdout.write(process_name)
    sys.stdout.write(print_string)
    sys.stdout.write("\n\n-------------------------------------------------------------------------------------------------------\n\n\n\n")
    
    #Summary_Output_File_ll.write("\n\n--------------------------------\n\n")
    Summary_Output_File_ll.write("\nENDED\t\t");
    Summary_Output_File_ll.write(process_name);
    Summary_Output_File_ll.write(print_string);
    Summary_Output_File_ll.write("\n\n-------------------------------------------------------------------------------------------------------\n\n\n\n");
    Summary_Output_File_ll.close();
    
    return Significance_Table_ll;






def GetDataFromFile(filename):
    
    f = open(filename,'r');
    lines=f.readlines();
    
    return lines;


