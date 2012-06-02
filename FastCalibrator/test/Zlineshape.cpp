#include "Zutils.h"
#include "setTDRStyle.h"
#include "ConfigParser.h"
#include "ntpleUtils.h"

#include "TROOT.h"
#include "TStyle.h"
#include "TFile.h"
#include "TF1.h"
#include "TH1.h"
#include "TH2.h"
#include "TChain.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"
#include "TPaveStats.h"
#include "TLegend.h"
#include "TTree.h"
#include "TVirtualFitter.h"

#include <iostream>
#include <string>
#include <sstream>
#include <ctime>
#include <map>
#include <algorithm>
#include <cmath>
#include <vector>
#include <fstream>


int main(int argc, char **argv){

   //set the style
  setTDRStyle();
  gROOT->Reset();
  gROOT->SetStyle("Plain");
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  gStyle->SetOptTitle(0); 
  gStyle->SetOptStat(1110); 


 /// Acquisition from cfg file
 
 if(argc != 2){
 std::cerr << " >>>>> analysis.cpp::usage: " << argv[0] << " configFileName" << std::endl ;
 return 1;
 }

 parseConfigFile (argv[1]) ;
 
 std::string treeNameDATA  = gConfigParser -> readStringOption("Input::treeNameDATA");
 std::cout<<" Input Tree Name DATA = "<<treeNameDATA<<std::endl;
 std::string treeNameMC  = gConfigParser -> readStringOption("Input::treeNameMC");
 std::cout<<" Input Tree Name MC = "<<treeNameMC<<std::endl;
 std::string inputDataFile =  gConfigParser -> readStringOption("Input::inputDataFile");
 std::cout<<" Input Data File = "<<inputDataFile<<std::endl;
 std::string inputMCFile =  gConfigParser -> readStringOption("Input::inputMCFile");
 std::cout<<" Input MC File = "<<inputMCFile<<std::endl;
 std::string WeightforMC =  gConfigParser -> readStringOption("Input::WeightforMC");
 std::cout<<" Weights for MC = "<<WeightforMC<<std::endl;
 bool useMC =  gConfigParser -> readBoolOption("Input::useMC");
 std::cout<<" Fit also MC = "<<useMC<<std::endl;
 std::string outputFile =  gConfigParser -> readStringOption("Output::outputFile");
 std::cout<<" Output Data File = "<<outputFile<<std::endl;
 std::string outputTable =  gConfigParser -> readStringOption("Output::outputFileTable");
 std::cout<<" Output Table File = "<<outputTable<<std::endl;

 /// Input data infos

 TChain* treeDATA = new TChain(treeNameDATA.c_str());
 TChain* treeMC = new TChain(treeNameMC.c_str());

 FillChain(*treeDATA,inputDataFile.c_str());
 FillChain(*treeMC,inputMCFile.c_str());

 std::cout << " MC: " << std::setw(8) << treeMC->GetEntries() << " entries" << std::endl; 
 std::cout << " DATA: " << std::setw(8) << treeDATA->GetEntries() << " entries" << std::endl;
  
 if (treeDATA->GetEntries() == 0 || treeMC->GetEntries() == 0 ){
    std::cout << ">>>recalibZ::Error: at least one file is empty" << std::endl; 
    return -1;
  }

 std::vector<std::string> FitCategories;
 FitCategories = gConfigParser -> readStringListOption("Input::FitCategories");

 std::cout << " >>>>> Input::FitCategories size = " << FitCategories.size() << std::endl;  
 std::cout << " >>>>> >>>>>  "; 
 for (unsigned int iCat = 0; iCat < FitCategories.size(); iCat++){
  std::cout << " " << FitCategories.at(iCat) << ", ";
 }
 std::cout << std::endl; 
 
 //--- weights for MC
 TFile weightsFile (WeightforMC.c_str(),"READ"); 
 TH1F* hweights = (TH1F*)weightsFile.Get("hweights");
 float w[100];
 for (int ibin = 1; ibin < hweights->GetNbinsX()+1; ibin++){
    w[ibin-1] = hweights->GetBinContent(ibin);  // bin 1 --> nvtx = 0 
  }
 weightsFile.Close();

 /// Output infos
 TFile* outputTFile = new TFile(outputFile.c_str(),"RECREATE");

 /// option Infos
 int nbinZ  = gConfigParser -> readIntOption("Option::nbinZ");
 std::cout<<" nbinZ = "<<nbinZ<<std::endl;
 double mZ_Max =  gConfigParser -> readDoubleOption("Option::mZMax");
 std::cout<<" mZ_Max = "<<mZ_Max<<std::endl;
 double mZ_Min =  gConfigParser -> readDoubleOption("Option::mZMin");
 std::cout<<" mZ_Min = "<<mZ_Min<<std::endl;
 double scaleEB = gConfigParser -> readDoubleOption("Option::scaleEB");
 std::cout<<" scaleEB = "<<scaleEB<<std::endl;
 double scaleEE = gConfigParser -> readDoubleOption("Option::scaleEE");
 std::cout<<" scaleEE = "<<scaleEE<<std::endl;
 int nPoints  = gConfigParser -> readIntOption("Option::nPoints");
 std::cout<<" nPoints = "<<nPoints<<std::endl;


 ///**** Book histos

 std::map<std::string,TH1F*> ZmassDATA;
 std::map<std::string,TH1F*> ZmassDATA_regression;
 std::map<std::string,TH1F*> ZmassMC;
 std::map<std::string,TH1F*> ZmassMC_regression;


 for(unsigned int i = 0; i < FitCategories.size(); ++i){
   std::string category = FitCategories.at(i);
   std::string histoName1 = "h_ZmassDATA_"+category;
   ZmassDATA[category] = new TH1F(histoName1.c_str(),"",nbinZ,mZ_Min,mZ_Max);
   ZmassDATA[category] -> Sumw2();

   std::string histoName2 = "h_ZmassDATA_regression_"+category;
   ZmassDATA_regression[category] = new TH1F(histoName2.c_str(),"",nbinZ,mZ_Min,mZ_Max);
   ZmassDATA_regression[category] -> Sumw2();

   std::string histoName3 = "h_ZmassMC_"+category;
   ZmassMC[category] = new TH1F(histoName3.c_str(),"",nbinZ,mZ_Min,mZ_Max);
   ZmassMC[category] -> Sumw2();

   std::string histoName4 = "h_ZmassMC_regression_"+category;
   ZmassMC_regression[category] = new TH1F(histoName4.c_str(),"",nbinZ,mZ_Min,mZ_Max);
   ZmassMC_regression[category] -> Sumw2();

  }

 /// Set branch addresses
 int isZ;
 float ele1ele2_scM,ele1ele2_scM_regression;
 int ele1_isEB,ele2_isEB;
 float ele1_scEta,ele2_scEta,ele1_scE,ele2_scE,ele1_es,ele2_es,ele1_scERaw,ele2_scERaw, ele1_scE_regression,
       ele2_scE_regression,ele1_e3x3,ele2_e3x3;
 int ele1_seedIeta,ele1_seedIphi,ele2_seedIeta,ele2_seedIphi,ele1_seedIx,ele2_seedIx,ele1_seedIy,ele2_seedIy,ele1_seedZside,ele2_seedZside;
 int PUit_NumInteractions;
 
 treeDATA->SetBranchAddress("isZ", &isZ);
 treeDATA->SetBranchAddress("ele1ele2_scM", &ele1ele2_scM);
 treeDATA->SetBranchAddress("ele1ele2_scM_regression", &ele1ele2_scM_regression);
 treeDATA->SetBranchAddress("ele1_isEB",  &ele1_isEB);
 treeDATA->SetBranchAddress("ele2_isEB",  &ele2_isEB);

 treeMC->SetBranchAddress("isZ", &isZ);
 treeMC->SetBranchAddress("ele1ele2_scM", &ele1ele2_scM);
 treeMC->SetBranchAddress("ele1_isEB",  &ele1_isEB);
 treeMC->SetBranchAddress("ele2_isEB",  &ele2_isEB);
 treeMC->SetBranchAddress("PUit_NumInteractions", &PUit_NumInteractions);

 treeDATA->SetBranchAddress("ele1_scEta", &ele1_scEta);
 treeDATA->SetBranchAddress("ele2_scEta", &ele2_scEta);

 treeMC->SetBranchAddress("ele1_scEta", &ele1_scEta);
 treeMC->SetBranchAddress("ele2_scEta", &ele2_scEta);

 treeDATA->SetBranchAddress("ele1_seedIeta", &ele1_seedIeta);
 treeDATA->SetBranchAddress("ele1_seedIphi", &ele1_seedIphi);
 treeDATA->SetBranchAddress("ele2_seedIeta", &ele2_seedIeta);
 treeDATA->SetBranchAddress("ele2_seedIphi",  &ele2_seedIphi);
 treeDATA->SetBranchAddress("ele1_seedIx",  &ele1_seedIx);
 treeDATA->SetBranchAddress("ele2_seedIx",  &ele2_seedIx);
 treeDATA->SetBranchAddress("ele1_seedIy",  &ele1_seedIy);
 treeDATA->SetBranchAddress("ele2_seedIy",  &ele2_seedIy);
 treeDATA->SetBranchAddress("ele1_seedZside",  &ele1_seedZside);
 treeDATA->SetBranchAddress("ele2_seedZside",  &ele2_seedZside);

 treeMC->SetBranchAddress("ele1_seedIeta", &ele1_seedIeta);
 treeMC->SetBranchAddress("ele1_seedIphi", &ele1_seedIphi);
 treeMC->SetBranchAddress("ele2_seedIeta", &ele2_seedIeta);
 treeMC->SetBranchAddress("ele2_seedIphi",  &ele2_seedIphi);
 treeMC->SetBranchAddress("ele1_seedIx",  &ele1_seedIx);
 treeMC->SetBranchAddress("ele2_seedIx",  &ele2_seedIx);
 treeMC->SetBranchAddress("ele1_seedIy",  &ele1_seedIy);
 treeMC->SetBranchAddress("ele2_seedIy",  &ele2_seedIy);
 treeMC->SetBranchAddress("ele1_seedZside",  &ele1_seedZside);
 treeMC->SetBranchAddress("ele2_seedZside",  &ele2_seedZside);


 treeDATA->SetBranchAddress("ele1_scE", &ele1_scE);
 treeDATA->SetBranchAddress("ele1_e3x3", &ele1_e3x3);
 treeDATA->SetBranchAddress("ele1_scE_regression", &ele1_scE_regression);
 treeDATA->SetBranchAddress("ele2_scE_regression", &ele2_scE_regression);
 treeDATA->SetBranchAddress("ele2_scE", &ele2_scE);
 treeDATA->SetBranchAddress("ele1_scERaw", &ele1_scERaw);
 treeDATA->SetBranchAddress("ele2_e3x3", &ele2_e3x3);
 treeDATA->SetBranchAddress("ele1_es", &ele1_es);
 treeDATA->SetBranchAddress("ele2_scERaw", &ele2_scERaw);
 treeDATA->SetBranchAddress("ele2_es", &ele2_es);

 treeMC->SetBranchAddress("ele1_scE", &ele1_scE);
 treeMC->SetBranchAddress("ele1_e3x3", &ele1_e3x3);
 treeMC->SetBranchAddress("ele1_scE_regression", &ele1_scE_regression);
 treeMC->SetBranchAddress("ele2_scE_regression", &ele2_scE_regression);
 treeMC->SetBranchAddress("ele1_scERaw", &ele1_scERaw);
 treeMC->SetBranchAddress("ele1_es", &ele1_es);
 treeMC->SetBranchAddress("ele2_scE", &ele2_scE);
 treeMC->SetBranchAddress("ele2_e3x3", &ele2_e3x3);
 treeMC->SetBranchAddress("ele2_scERaw", &ele2_scERaw);
 treeMC->SetBranchAddress("ele2_es", &ele2_es);
   
 //*** Loop on MC **//
 std::cout <<" Fill with MC Events "<<std::endl;
 int nEntriesMC = treeMC-> GetEntries();
 std::cout <<" MC Events =  "<<nEntriesMC<<std::endl;
 for(int iEntry = 0; iEntry < nEntriesMC; ++iEntry){

  if( (iEntry%100000 == 0) ) std::cout << " reading saved entry " << iEntry << std::endl;
  treeMC -> GetEntry(iEntry);
  double weight = w[PUit_NumInteractions];
   //only the Z
   if (isZ != 1) continue;
   if( (ele1_seedZside== 0) && (ele2_seedZside == 0) ){
	  ZmassMC["EB-EB"] ->  Fill( ele1ele2_scM * sqrt(scaleEB*scaleEB),weight );
	  ZmassMC_regression["EB-EB"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEB*scaleEB),weight);
	}    
   else if( fabs(ele1_seedZside)== 1 && fabs(ele2_seedZside)== 1 ){
	  ZmassMC["EE-EE"] ->  Fill( ele1ele2_scM * sqrt(scaleEE*scaleEE),weight );
	  ZmassMC_regression["EE-EE"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEE*scaleEE),weight );

	}    
   else{
	  ZmassMC["EB-EE"] ->  Fill( ele1ele2_scM * sqrt(scaleEB*scaleEE),weight );
	  ZmassMC_regression["EB-EE"] ->  Fill( ele1ele2_scM* sqrt(scaleEB*scaleEE)* sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)),weight );
       }

  if((ele1_seedZside== 0) && (ele2_seedZside == 0) && ele1_scEta>0. && ele2_scEta>0. ){
	  ZmassMC["EBp"] ->  Fill( ele1ele2_scM * sqrt(scaleEB*scaleEB),weight );
	  ZmassMC_regression["EBp"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEB*scaleEB),weight);
   }
  else if((ele1_seedZside== 0) && (ele2_seedZside == 0) && ele1_scEta<0. && ele2_scEta<0. ){
          ZmassMC["EBm"] ->  Fill( ele1ele2_scM * sqrt(scaleEB*scaleEB),weight );
	  ZmassMC_regression["EBm"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEB*scaleEB),weight);
  }
  
  if((ele1_seedZside== 1) && (ele2_seedZside == 1)){
          ZmassMC["EEp"] ->  Fill( ele1ele2_scM * sqrt(scaleEE*scaleEE),weight );
	  ZmassMC_regression["EEp"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEE*scaleEE),weight);
  }
  else if((ele1_seedZside== -1) && (ele2_seedZside == -1)){
          ZmassMC["EEm"] ->  Fill( ele1ele2_scM * sqrt(scaleEE*scaleEE),weight );
	  ZmassMC_regression["EEm"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEE*scaleEE),weight);
  }

 if((ele1_seedZside!=0) && (ele2_seedZside !=0) && ele1_e3x3/ele1_scERaw>0.94 && ele2_e3x3/ele2_scERaw>0.94){
          ZmassMC["EE_R9_g"] ->  Fill( ele1ele2_scM * sqrt(scaleEE*scaleEE),weight );
	  ZmassMC_regression["EE_R9_g"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEE*scaleEE),weight);
  }

 else if((ele1_seedZside!=0) && (ele2_seedZside !=0) && ele1_e3x3/ele1_scERaw<0.94 && ele2_e3x3/ele2_scERaw<0.94){
          ZmassMC["EE_R9_l"] ->  Fill( ele1ele2_scM * sqrt(scaleEE*scaleEE),weight );
	  ZmassMC_regression["EE_R9_l"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEE*scaleEE),weight);
  }

 if((ele1_seedZside==0) && (ele2_seedZside ==0) && (ele1_e3x3/ele1_scERaw)>0.94 && (ele2_e3x3/ele2_scERaw)>0.94){
          ZmassMC["EB_R9_g"] ->  Fill( ele1ele2_scM * sqrt(scaleEB*scaleEB),weight );
	  ZmassMC_regression["EB_R9_g"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEB*scaleEB),weight);
  }

 else if((ele1_seedZside==0) && (ele2_seedZside==0) && (ele1_e3x3/ele1_scERaw)<0.94 && (ele2_e3x3/ele2_scERaw)<0.94){
          ZmassMC["EB_R9_l"] ->  Fill( ele1ele2_scM * sqrt(scaleEB*scaleEB),weight );
	  ZmassMC_regression["EB_R9_l"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEB*scaleEB),weight);
  }

 }

 //*** Loop over Data **//
 int nEntriesDATA = treeDATA -> GetEntries();
 std::cout <<" Fill with DATA Events "<<std::endl;
 std::cout <<" DATA Events =  "<<nEntriesDATA<<std::endl;
 
 for(int iEntry = 0; iEntry < nEntriesDATA; ++iEntry){

 if( (iEntry%100000 == 0) ) std::cout << " reading saved entry " << iEntry << std::endl;
 treeDATA -> GetEntry(iEntry);
   //only the Z
  if (isZ != 1) continue;
      
  if( (ele1_seedZside== 0) && (ele2_seedZside== 0) ){
	  ZmassDATA["EB-EB"] ->  Fill( ele1ele2_scM * sqrt(scaleEB*scaleEB) );
	  ZmassDATA_regression["EB-EB"] ->  Fill( ele1ele2_scM* sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE))* sqrt(scaleEB*scaleEB));
	}    
  else if( fabs(ele1_seedZside)== 1 && fabs(ele2_seedZside)== 1 ){
	  ZmassDATA["EE-EE"] ->  Fill( ele1ele2_scM * sqrt(scaleEE*scaleEE) );
	  ZmassDATA_regression["EE-EE"] ->  Fill( ele1ele2_scM* sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEE*scaleEE) );

	}    
  else{
	  ZmassDATA["EB-EE"] ->  Fill( ele1ele2_scM * sqrt(scaleEB*scaleEE) );
	  ZmassDATA_regression["EB-EE"] ->  Fill( ele1ele2_scM* sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEB*scaleEE) );
       }

 if((ele1_seedZside== 0) && (ele2_seedZside == 0) && ele1_scEta>0. && ele2_scEta>0. ){
	  ZmassDATA["EBp"] ->  Fill( ele1ele2_scM * sqrt(scaleEB*scaleEB));
	  ZmassDATA_regression["EBp"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEB*scaleEB));
   }
  else if((ele1_seedZside== 0) && (ele2_seedZside == 0) && ele1_scEta<0. && ele2_scEta<0. ){
          ZmassDATA["EBm"] ->  Fill( ele1ele2_scM * sqrt(scaleEB*scaleEB));
	  ZmassDATA_regression["EBm"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEB*scaleEB));
  }
 
 if((ele1_seedZside== 1) && (ele2_seedZside == 1)){
          ZmassDATA["EEp"] ->  Fill( ele1ele2_scM * sqrt(scaleEE*scaleEE));
	  ZmassDATA_regression["EEp"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEE*scaleEE));
 }

else if((ele1_seedZside== -1) && (ele2_seedZside == -1)){
          ZmassDATA["EEm"] ->  Fill( ele1ele2_scM * sqrt(scaleEE*scaleEE));
	  ZmassDATA_regression["EEm"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEE*scaleEE));
}
 

 if((ele1_seedZside!=0) && (ele2_seedZside !=0) && (ele1_e3x3/ele1_scERaw)>0.94 && (ele2_e3x3/ele2_scERaw)>0.94){
          ZmassDATA["EE_R9_g"] ->  Fill( ele1ele2_scM * sqrt(scaleEE*scaleEE));
	  ZmassDATA_regression["EE_R9_g"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEE*scaleEE));
  }

 else if((ele1_seedZside!=0) && (ele2_seedZside !=0) && (ele1_e3x3/ele1_scERaw)<0.94 && (ele2_e3x3/ele2_scERaw)<0.94){
          ZmassDATA["EE_R9_l"] ->  Fill( ele1ele2_scM * sqrt(scaleEE*scaleEE));
	  ZmassDATA_regression["EE_R9_l"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEE*scaleEE));
  }

 if((ele1_seedZside==0) && (ele2_seedZside ==0) && (ele1_e3x3/ele1_scERaw)>0.94 && (ele2_e3x3/ele2_scERaw)>0.94){
          ZmassDATA["EB_R9_g"] ->  Fill( ele1ele2_scM * sqrt(scaleEB*scaleEB));
	  ZmassDATA_regression["EB_R9_g"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEB*scaleEB));
  }

 else if((ele1_seedZside==0) && (ele2_seedZside==0) && (ele1_e3x3/ele1_scERaw)<0.94 && (ele2_e3x3/ele2_scERaw)<0.94){
          ZmassDATA["EB_R9_l"] ->  Fill( ele1ele2_scM * sqrt(scaleEB*scaleEB));
	  ZmassDATA_regression["EB_R9_l"] ->  Fill( ele1ele2_scM*sqrt((ele1_scE_regression/ele1_scE)*(ele2_scE_regression/ele2_scE)) * sqrt(scaleEB*scaleEB));
  }


 }

 /// Z Lineshape Tool
if(useMC){
  
   std::string energyType = "NoReg";

   std::ofstream outTableFile (outputTable.c_str(),std::ios::out);
 
   outTableFile<<"\\begin{table}[!htb]"<<std::endl;
   outTableFile<<"\\begin{center}"<<std::endl;

   outTableFile<<"\\begin{tabular}{c|c|c|c|c|c}"<<std::endl;

   outTableFile<<"\\hline"<<std::endl;
   outTableFile<<"\\hline"<<std::endl;


   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " Category " << " & " <<" Data Event "<<" & "<<" #Delta M_{data} "<<" & "<<" #Delta M_{MC} "<<" & "<<" #sigma_{cb}^{data} "<<" & "<<" #sigma_{cb}^{MC} "<<" \\\\ "<<std::endl;
 
   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<<"\\hline"<<std::endl;
   outTableFile<<"\\hline"<<std::endl;


   std::cout<<" Fit Z Peak EB-EB DATA and MC"<<std::endl;

   BinnedFitZPeak("EB-EB", 1, ZmassDATA["EB-EB"], ZmassMC["EB-EB"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EB-EB" <<" & "<<ZmassDATA["EB-EB"]->GetEntries() <<" & "<<ZmassDATA["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_NoReg")->GetParError(3) <<" & "<< ZmassMC["EB-EB"]->GetFunction("bw_cb_MC_EB-EB_NoReg")->GetParameter(3) <<" #pm "<<ZmassMC["EB-EB"]->GetFunction("bw_cb_MC_EB-EB_NoReg")->GetParError(3)<<" & "<<ZmassDATA["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_NoReg")->GetParameter(4)<<" #pm "<<ZmassDATA["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_NoReg")->GetParError(4) <<" & "<< ZmassMC["EB-EB"]->GetFunction("bw_cb_MC_EB-EB_NoReg")->GetParameter(4) <<" #pm "<<ZmassMC["EB-EB"]->GetFunction("bw_cb_MC_EB-EB_NoReg")->GetParError(4)<<" \\\\ "<<std::endl;


   std::cout<<" Fit Z Peak EB-EB DATA and MC Regression"<<std::endl;

   BinnedFitZPeak("EB-EB", 1, ZmassDATA_regression["EB-EB"], ZmassMC_regression["EB-EB"], nPoints, mZ_Min, mZ_Max);  


   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EB-EB" <<" & "<<ZmassDATA["EB-EB"]->GetEntries() <<" & "<<ZmassDATA_regression["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_Reg")->GetParError(3) <<" & "<< ZmassMC_regression["EB-EB"]->GetFunction("bw_cb_MC_EB-EB_Reg")->GetParameter(3) <<" #pm "<<ZmassMC_regression["EB-EB"]->GetFunction("bw_cb_MC_EB-EB_Reg")->GetParError(3)<<" & "<<ZmassDATA_regression["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_Reg")->GetParameter(4)<<" #pm "<<ZmassDATA_regression["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_Reg")->GetParError(4) <<" & "<< ZmassMC_regression["EB-EB"]->GetFunction("bw_cb_MC_EB-EB_Reg")->GetParameter(4) <<" #pm "<<ZmassMC_regression["EB-EB"]->GetFunction("bw_cb_MC_EB-EB_Reg")->GetParError(4)<<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EBp DATA and MC"<<std::endl;
 
   BinnedFitZPeak("EBp", 1, ZmassDATA["EBp"], ZmassMC["EBp"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EBp" <<" & "<<ZmassDATA["EBp"]->GetEntries() <<" & "<<ZmassDATA["EBp"]->GetFunction("bw_cb_DATA_EBp_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EBp"]->GetFunction("bw_cb_DATA_EBp_NoReg")->GetParError(3) <<" & "<< ZmassMC["EBp"]->GetFunction("bw_cb_MC_EBp_NoReg")->GetParameter(3) <<" #pm "<<ZmassMC["EBp"]->GetFunction("bw_cb_MC_EBp_NoReg")->GetParError(3)<<" & "<<ZmassDATA["EBp"]->GetFunction("bw_cb_DATA_EBp_NoReg")->GetParameter(4)<<" #pm "<<ZmassDATA["EBp"]->GetFunction("bw_cb_DATA_EBp_NoReg")->GetParError(4) <<" & "<< ZmassMC["EBp"]->GetFunction("bw_cb_MC_EBp_NoReg")->GetParameter(4) <<" #pm "<<ZmassMC["EBp"]->GetFunction("bw_cb_MC_EBp_NoReg")->GetParError(4)<<" \\\\ "<<std::endl;


   std::cout<<" Fit Z Peak EBp DATA and MC Regression"<<std::endl;

   BinnedFitZPeak("EBp", 1, ZmassDATA_regression["EBp"], ZmassMC_regression["EBp"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EBp" <<" & "<<ZmassDATA["EBp"]->GetEntries() <<" & "<<ZmassDATA_regression["EBp"]->GetFunction("bw_cb_DATA_EBp_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EBp"]->GetFunction("bw_cb_DATA_EBp_Reg")->GetParError(3) <<" & "<< ZmassMC_regression["EBp"]->GetFunction("bw_cb_MC_EBp_Reg")->GetParameter(3) <<" #pm "<<ZmassMC_regression["EBp"]->GetFunction("bw_cb_MC_EBp_Reg")->GetParError(3)<<" & "<<ZmassDATA_regression["EBp"]->GetFunction("bw_cb_DATA_EBp_Reg")->GetParameter(4)<<" #pm "<<ZmassDATA_regression["EBp"]->GetFunction("bw_cb_DATA_EBp_Reg")->GetParError(4) <<" & "<< ZmassMC_regression["EBp"]->GetFunction("bw_cb_MC_EBp_Reg")->GetParameter(4) <<" #pm "<<ZmassMC_regression["EBp"]->GetFunction("bw_cb_MC_EBp_Reg")->GetParError(4)<<" \\\\ "<<std::endl;

  
   std::cout<<" Fit Z Peak EBm DATA and MC"<<std::endl;

   BinnedFitZPeak("EBm", 1, ZmassDATA["EBm"], ZmassMC["EBm"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EBm" <<" & "<<ZmassDATA["EBm"]->GetEntries() <<" & "<<ZmassDATA["EBm"]->GetFunction("bw_cb_DATA_EBm_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EBm"]->GetFunction("bw_cb_DATA_EBm_NoReg")->GetParError(3) <<" & "<< ZmassMC["EBm"]->GetFunction("bw_cb_MC_EBm_NoReg")->GetParameter(3) <<" #pm "<<ZmassMC["EBm"]->GetFunction("bw_cb_MC_EBm_NoReg")->GetParError(3)<<" & "<<ZmassDATA["EBm"]->GetFunction("bw_cb_DATA_EBm_NoReg")->GetParameter(4)<<" #pm "<<ZmassDATA["EBm"]->GetFunction("bw_cb_DATA_EBm_NoReg")->GetParError(4) <<" & "<< ZmassMC["EBm"]->GetFunction("bw_cb_MC_EBm_NoReg")->GetParameter(4) <<" #pm "<<ZmassMC["EBm"]->GetFunction("bw_cb_MC_EBm_NoReg")->GetParError(4)<<" \\\\ "<<std::endl;

 
   std::cout<<" Fit Z Peak EBm DATA and MC Regression"<<std::endl;

   BinnedFitZPeak("EBm", 1, ZmassDATA_regression["EBm"], ZmassMC_regression["EBm"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EBm" <<" & "<<ZmassDATA["EBm"]->GetEntries() <<" & "<<ZmassDATA_regression["EBm"]->GetFunction("bw_cb_DATA_EBm_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EBm"]->GetFunction("bw_cb_DATA_EBm_Reg")->GetParError(3) <<" & "<< ZmassMC_regression["EBm"]->GetFunction("bw_cb_MC_EBm_Reg")->GetParameter(3) <<" #pm "<<ZmassMC_regression["EBm"]->GetFunction("bw_cb_MC_EBm_Reg")->GetParError(3)<<" & "<<ZmassDATA_regression["EBm"]->GetFunction("bw_cb_DATA_EBm_Reg")->GetParameter(4)<<" #pm "<<ZmassDATA_regression["EBm"]->GetFunction("bw_cb_DATA_EBm_Reg")->GetParError(4) <<" & "<< ZmassMC_regression["EBm"]->GetFunction("bw_cb_MC_EBm_Reg")->GetParameter(4) <<" #pm "<<ZmassMC_regression["EBm"]->GetFunction("bw_cb_MC_EBm_Reg")->GetParError(4)<<" \\\\ "<<std::endl;


   std::cout<<" Fit Z Peak R9 > DATA and MC "<<std::endl;

   BinnedFitZPeak("EB_R9_g", 1, ZmassDATA["EB_R9_g"], ZmassMC["EB_R9_g"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EB_R9_g" <<" & "<<ZmassDATA["EB_R9_g"]->GetEntries() <<" & "<<ZmassDATA["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_NoReg")->GetParError(3) <<" & "<< ZmassMC["EB_R9_g"]->GetFunction("bw_cb_MC_EB_R9_g_NoReg")->GetParameter(3) <<" #pm "<<ZmassMC["EB_R9_g"]->GetFunction("bw_cb_MC_EB_R9_g_NoReg")->GetParError(3)<<" & "<<ZmassDATA["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_NoReg")->GetParameter(4)<<" #pm "<<ZmassDATA["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_NoReg")->GetParError(4) <<" & "<< ZmassMC["EB_R9_g"]->GetFunction("bw_cb_MC_EB_R9_g_NoReg")->GetParameter(4) <<" #pm "<<ZmassMC["EB_R9_g"]->GetFunction("bw_cb_MC_EB_R9_g_NoReg")->GetParError(4)<<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak R9 > DATA and MC Regression"<<std::endl;
 
   BinnedFitZPeak("EB_R9_g", 1, ZmassDATA_regression["EB_R9_g"], ZmassMC_regression["EB_R9_g"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EB_R9_g" <<" & "<<ZmassDATA["EB_R9_g"]->GetEntries() <<" & "<<ZmassDATA_regression["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_Reg")->GetParError(3) <<" & "<< ZmassMC_regression["EB_R9_g"]->GetFunction("bw_cb_MC_EB_R9_g_Reg")->GetParameter(3) <<" #pm "<<ZmassMC_regression["EB_R9_g"]->GetFunction("bw_cb_MC_EB_R9_g_Reg")->GetParError(3)<<" & "<<ZmassDATA_regression["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_Reg")->GetParameter(4)<<" #pm "<<ZmassDATA_regression["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_Reg")->GetParError(4) <<" & "<< ZmassMC_regression["EB_R9_g"]->GetFunction("bw_cb_MC_EB_R9_g_Reg")->GetParameter(4) <<" #pm "<<ZmassMC_regression["EB_R9_g"]->GetFunction("bw_cb_MC_EB_R9_g_Reg")->GetParError(4)<<" \\\\ "<<std::endl;


   std::cout<<" Fit Z Peak R9 < DATA and MC "<<std::endl;
 
   BinnedFitZPeak("EB_R9_l", 1, ZmassDATA["EB_R9_l"], ZmassMC["EB_R9_l"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EB_R9_l" <<" & "<<ZmassDATA["EB_R9_l"]->GetEntries() <<" & "<<ZmassDATA["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_NoReg")->GetParError(3) <<" & "<< ZmassMC["EB_R9_l"]->GetFunction("bw_cb_MC_EB_R9_l_NoReg")->GetParameter(3) <<" #pm "<<ZmassMC["EB_R9_l"]->GetFunction("bw_cb_MC_EB_R9_l_NoReg")->GetParError(3)<<" & "<<ZmassDATA["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_NoReg")->GetParameter(4)<<" #pm "<<ZmassDATA["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_NoReg")->GetParError(4) <<" & "<< ZmassMC["EB_R9_l"]->GetFunction("bw_cb_MC_EB_R9_l_NoReg")->GetParameter(4) <<" #pm "<<ZmassMC["EB_R9_l"]->GetFunction("bw_cb_MC_EB_R9_l_NoReg")->GetParError(4)<<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak R9 < DATA and MC Regression "<<std::endl;

   BinnedFitZPeak("EB_R9_l", 1, ZmassDATA_regression["EB_R9_l"], ZmassMC_regression["EB_R9_l"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EB_R9_l" <<" & "<<ZmassDATA["EB_R9_l"]->GetEntries() <<" & "<<ZmassDATA_regression["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_Reg")->GetParError(3) <<" & "<< ZmassMC_regression["EB_R9_l"]->GetFunction("bw_cb_MC_EB_R9_l_Reg")->GetParameter(3) <<" #pm "<<ZmassMC_regression["EB_R9_l"]->GetFunction("bw_cb_MC_EB_R9_l_Reg")->GetParError(3)<<" & "<<ZmassDATA_regression["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_Reg")->GetParameter(4)<<" #pm "<<ZmassDATA_regression["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_Reg")->GetParError(4) <<" & "<< ZmassMC_regression["EB_R9_l"]->GetFunction("bw_cb_MC_EB_R9_l_Reg")->GetParameter(4) <<" #pm "<<ZmassMC_regression["EB_R9_l"]->GetFunction("bw_cb_MC_EB_R9_l_Reg")->GetParError(4)<<" \\\\ "<<std::endl;
 
   std::cout<<" Fit Z Peak EE  DATA and MC  "<<std::endl;

   BinnedFitZPeak("EE-EE", 1, ZmassDATA["EE-EE"], ZmassMC["EE-EE"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EE-EE" <<" & "<<ZmassDATA["EE-EE"]->GetEntries() <<" & "<<ZmassDATA["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_NoReg")->GetParError(3) <<" & "<< ZmassMC["EE-EE"]->GetFunction("bw_cb_MC_EE-EE_NoReg")->GetParameter(3) <<" #pm "<<ZmassMC["EE-EE"]->GetFunction("bw_cb_MC_EE-EE_NoReg")->GetParError(3)<<" & "<<ZmassDATA["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_NoReg")->GetParameter(4)<<" #pm "<<ZmassDATA["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_NoReg")->GetParError(4) <<" & "<< ZmassMC["EE-EE"]->GetFunction("bw_cb_MC_EE-EE_NoReg")->GetParameter(4) <<" #pm "<<ZmassMC["EE-EE"]->GetFunction("bw_cb_MC_EE-EE_NoReg")->GetParError(4)<<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE  DATA and MC Regression  "<<std::endl;
 
   BinnedFitZPeak("EE-EE", 2, ZmassDATA_regression["EE-EE"], ZmassMC_regression["EE-EE"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EE-EE" <<" & "<<ZmassDATA["EE-EE"]->GetEntries() <<" & "<<ZmassDATA_regression["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_Reg")->GetParError(3) <<" & "<< ZmassMC_regression["EE-EE"]->GetFunction("bw_cb_MC_EE-EE_Reg")->GetParameter(3) <<" #pm "<<ZmassMC_regression["EE-EE"]->GetFunction("bw_cb_MC_EE-EE_Reg")->GetParError(3)<<" & "<<ZmassDATA_regression["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_Reg")->GetParameter(4)<<" #pm "<<ZmassDATA_regression["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_Reg")->GetParError(4) <<" & "<< ZmassMC_regression["EE-EE"]->GetFunction("bw_cb_MC_EE-EE_Reg")->GetParameter(4) <<" #pm "<<ZmassMC_regression["EE-EE"]->GetFunction("bw_cb_MC_EE-EE_Reg")->GetParError(4)<<" \\\\ "<<std::endl;
 

   std::cout<<" Fit Z Peak EEp  DATA and MC "<<std::endl;

   BinnedFitZPeak("EEp", 2, ZmassDATA["EEp"], ZmassMC["EEp"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EEp" <<" & "<<ZmassDATA["EEp"]->GetEntries() <<" & "<<ZmassDATA["EEp"]->GetFunction("bw_cb_DATA_EEp_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EEp"]->GetFunction("bw_cb_DATA_EEp_NoReg")->GetParError(3) <<" & "<< ZmassMC["EEp"]->GetFunction("bw_cb_MC_EEp_NoReg")->GetParameter(3) <<" #pm "<<ZmassMC["EEp"]->GetFunction("bw_cb_MC_EEp_NoReg")->GetParError(3)<<" & "<<ZmassDATA["EEp"]->GetFunction("bw_cb_DATA_EEp_NoReg")->GetParameter(4)<<" #pm "<<ZmassDATA["EEp"]->GetFunction("bw_cb_DATA_EEp_NoReg")->GetParError(4) <<" & "<< ZmassMC["EEp"]->GetFunction("bw_cb_MC_EEp_NoReg")->GetParameter(4) <<" #pm "<<ZmassMC["EEp"]->GetFunction("bw_cb_MC_EEp_NoReg")->GetParError(4)<<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EEp  DATA and MC Regression "<<std::endl;

   BinnedFitZPeak("EEp", 2, ZmassDATA_regression["EEp"], ZmassMC_regression["EEp"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EEp" <<" & "<<ZmassDATA["EEp"]->GetEntries() <<" & "<<ZmassDATA_regression["EEp"]->GetFunction("bw_cb_DATA_EEp_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EEp"]->GetFunction("bw_cb_DATA_EEp_Reg")->GetParError(3) <<" & "<< ZmassMC_regression["EEp"]->GetFunction("bw_cb_MC_EEp_Reg")->GetParameter(3) <<" #pm "<<ZmassMC_regression["EEp"]->GetFunction("bw_cb_MC_EEp_Reg")->GetParError(3)<<" & "<<ZmassDATA_regression["EEp"]->GetFunction("bw_cb_DATA_EEp_Reg")->GetParameter(4)<<" #pm "<<ZmassDATA_regression["EEp"]->GetFunction("bw_cb_DATA_EEp_Reg")->GetParError(4) <<" & "<< ZmassMC_regression["EEp"]->GetFunction("bw_cb_MC_EEp_Reg")->GetParameter(4) <<" #pm "<<ZmassMC_regression["EEp"]->GetFunction("bw_cb_MC_EEp_Reg")->GetParError(4)<<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EEm  DATA and MC "<<std::endl;

   BinnedFitZPeak("EEm", 2, ZmassDATA["EEm"], ZmassMC["EEm"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EEm" <<" & "<<ZmassDATA["EEm"]->GetEntries() <<" & "<<ZmassDATA["EEm"]->GetFunction("bw_cb_DATA_EEm_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EEm"]->GetFunction("bw_cb_DATA_EEm_NoReg")->GetParError(3) <<" & "<< ZmassMC["EEm"]->GetFunction("bw_cb_MC_EEm_NoReg")->GetParameter(3) <<" #pm "<<ZmassMC["EEm"]->GetFunction("bw_cb_MC_EEm_NoReg")->GetParError(3)<<" & "<<ZmassDATA["EEm"]->GetFunction("bw_cb_DATA_EEm_NoReg")->GetParameter(4)<<" #pm "<<ZmassDATA["EEm"]->GetFunction("bw_cb_DATA_EEm_NoReg")->GetParError(4) <<" & "<< ZmassMC["EEm"]->GetFunction("bw_cb_MC_EEm_NoReg")->GetParameter(4) <<" #pm "<<ZmassMC["EEm"]->GetFunction("bw_cb_MC_EEm_NoReg")->GetParError(4)<<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EEm  DATA and MC Regression "<<std::endl;

   BinnedFitZPeak("EEm", 2, ZmassDATA_regression["EEm"], ZmassMC_regression["EEm"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EEm" <<" & "<<ZmassDATA["EEm"]->GetEntries() <<" & "<<ZmassDATA_regression["EEm"]->GetFunction("bw_cb_DATA_EEm_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EEm"]->GetFunction("bw_cb_DATA_EEm_Reg")->GetParError(3) <<" & "<< ZmassMC_regression["EEm"]->GetFunction("bw_cb_MC_EEm_Reg")->GetParameter(3) <<" #pm "<<ZmassMC_regression["EEm"]->GetFunction("bw_cb_MC_EEm_Reg")->GetParError(3)<<" & "<<ZmassDATA_regression["EEm"]->GetFunction("bw_cb_DATA_EEm_Reg")->GetParameter(4)<<" #pm "<<ZmassDATA_regression["EEm"]->GetFunction("bw_cb_DATA_EEm_Reg")->GetParError(4) <<" & "<< ZmassMC_regression["EEm"]->GetFunction("bw_cb_MC_EEm_Reg")->GetParameter(4) <<" #pm "<<ZmassMC_regression["EEm"]->GetFunction("bw_cb_MC_EEm_Reg")->GetParError(4)<<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE R9 > DATA and MC  "<<std::endl;

   BinnedFitZPeak("EE_R9_g", 2, ZmassDATA["EE_R9_g"], ZmassMC["EE_R9_g"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EE_R9_g" <<" & "<<ZmassDATA["EE_R9_g"]->GetEntries() <<" & "<<ZmassDATA["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_NoReg")->GetParError(3) <<" & "<< ZmassMC["EE_R9_g"]->GetFunction("bw_cb_MC_EE_R9_g_NoReg")->GetParameter(3) <<" #pm "<<ZmassMC["EE_R9_g"]->GetFunction("bw_cb_MC_EE_R9_g_NoReg")->GetParError(3)<<" & "<<ZmassDATA["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_NoReg")->GetParameter(4)<<" #pm "<<ZmassDATA["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_NoReg")->GetParError(4) <<" & "<< ZmassMC["EE_R9_g"]->GetFunction("bw_cb_MC_EE_R9_g_NoReg")->GetParameter(4) <<" #pm "<<ZmassMC["EE_R9_g"]->GetFunction("bw_cb_MC_EE_R9_g_NoReg")->GetParError(4)<<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE R9 > DATA and MC Regression "<<std::endl;
 
   BinnedFitZPeak("EE_R9_g", 2, ZmassDATA_regression["EE_R9_g"], ZmassMC_regression["EE_R9_g"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EE_R9_g" <<" & "<<ZmassDATA["EE_R9_g"]->GetEntries() <<" & "<<ZmassDATA_regression["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_Reg")->GetParError(3) <<" & "<< ZmassMC_regression["EE_R9_g"]->GetFunction("bw_cb_MC_EE_R9_g_Reg")->GetParameter(3) <<" #pm "<<ZmassMC_regression["EE_R9_g"]->GetFunction("bw_cb_MC_EE_R9_g_Reg")->GetParError(3)<<" & "<<ZmassDATA_regression["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_Reg")->GetParameter(4)<<" #pm "<<ZmassDATA_regression["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_Reg")->GetParError(4) <<" & "<< ZmassMC_regression["EE_R9_g"]->GetFunction("bw_cb_MC_EE_R9_g_Reg")->GetParameter(4) <<" #pm "<<ZmassMC_regression["EE_R9_g"]->GetFunction("bw_cb_MC_EE_R9_g_Reg")->GetParError(4)<<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE R9 < DATA and MC  "<<std::endl;

   BinnedFitZPeak("EE_R9_l", 2, ZmassDATA["EE_R9_l"], ZmassMC["EE_R9_l"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EE_R9_l" <<" & "<<ZmassDATA["EE_R9_l"]->GetEntries() <<" & "<<ZmassDATA["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_NoReg")->GetParError(3) <<" & "<< ZmassMC["EE_R9_l"]->GetFunction("bw_cb_MC_EE_R9_l_NoReg")->GetParameter(3) <<" #pm "<<ZmassMC["EE_R9_l"]->GetFunction("bw_cb_MC_EE_R9_l_NoReg")->GetParError(3)<<" & "<<ZmassDATA["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_NoReg")->GetParameter(4)<<" #pm "<<ZmassDATA["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_NoReg")->GetParError(4) <<" & "<< ZmassMC["EE_R9_l"]->GetFunction("bw_cb_MC_EE_R9_l_NoReg")->GetParameter(4) <<" #pm "<<ZmassMC["EE_R9_l"]->GetFunction("bw_cb_MC_EE_R9_l_NoReg")->GetParError(4)<<"\\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE R9 < DATA and MC "<<std::endl;

   BinnedFitZPeak("EE_R9_l", 2, ZmassDATA_regression["EE_R9_l"], ZmassMC_regression["EE_R9_l"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EE_R9_l" <<" & "<<ZmassDATA["EE_R9_l"]->GetEntries() <<" & "<<ZmassDATA_regression["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_Reg")->GetParError(3) <<" & "<< ZmassMC_regression["EE_R9_l"]->GetFunction("bw_cb_MC_EE_R9_l_Reg")->GetParameter(3) <<" #pm "<<ZmassMC_regression["EE_R9_l"]->GetFunction("bw_cb_MC_EE_R9_l_Reg")->GetParError(3)<<" & "<<ZmassDATA_regression["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_Reg")->GetParameter(4)<<" #pm "<<ZmassDATA_regression["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_Reg")->GetParError(4) <<" & "<< ZmassMC_regression["EE_R9_l"]->GetFunction("bw_cb_MC_EE_R9_l_Reg")->GetParameter(4) <<" #pm "<<ZmassMC_regression["EE_R9_l"]->GetFunction("bw_cb_MC_EE_R9_l_Reg")->GetParError(4)<<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE-EB DATA and MC "<<std::endl;

   BinnedFitZPeak("EB-EE", 2, ZmassDATA["EB-EE"], ZmassMC["EB-EE"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EB-EE" <<" & "<<ZmassDATA["EB-EE"]->GetEntries() <<" & "<<ZmassDATA["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_NoReg")->GetParError(3) <<" & "<< ZmassMC["EB-EE"]->GetFunction("bw_cb_MC_EB-EE_NoReg")->GetParameter(3) <<" #pm "<<ZmassMC["EB-EE"]->GetFunction("bw_cb_MC_EB-EE_NoReg")->GetParError(3)<<" & "<<ZmassDATA["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_NoReg")->GetParameter(4)<<" #pm "<<ZmassDATA["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_NoReg")->GetParError(4) <<" & "<< ZmassMC["EB-EE"]->GetFunction("bw_cb_MC_EB-EE_NoReg")->GetParameter(4) <<" #pm "<<ZmassMC["EB-EE"]->GetFunction("bw_cb_MC_EB-EE_NoReg")->GetParError(4)<<" \\\\ "<<std::endl;


   std::cout<<" Fit Z Peak EE-EB DATA and MC Regression "<<std::endl;

   BinnedFitZPeak("EB-EE", 2, ZmassDATA_regression["EB-EE"], ZmassMC_regression["EB-EE"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EB-EE" <<" & "<<ZmassDATA["EB-EE"]->GetEntries() <<" & "<<ZmassDATA_regression["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_Reg")->GetParError(3) <<" & "<< ZmassMC_regression["EB-EE"]->GetFunction("bw_cb_MC_EB-EE_Reg")->GetParameter(3) <<" #pm "<<ZmassMC_regression["EB-EE"]->GetFunction("bw_cb_MC_EB-EE_Reg")->GetParError(3)<<" & "<<ZmassDATA_regression["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_Reg")->GetParameter(4)<<" #pm "<<ZmassDATA_regression["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_Reg")->GetParError(4) <<" & "<< ZmassMC_regression["EB-EE"]->GetFunction("bw_cb_MC_EB-EE_Reg")->GetParameter(4) <<" #pm "<<ZmassMC_regression["EB-EE"]->GetFunction("bw_cb_MC_EB-EE_Reg")->GetParError(4)<<" \\\\ "<<std::endl;

   outTableFile<< " \\hline "<<std::endl;
   outTableFile<< " \\hline "<<std::endl;

   outTableFile<< " \\end{tabular} "<<std::endl;
   outTableFile<< " \\end{center} "<<std::endl;
   outTableFile<< " \\end{table} "<<std::endl;
}

else{
  
   std::string energyType = "NoReg";

   std::ofstream outTableFile (outputTable.c_str(),std::ios::out);
 
   outTableFile<<"\\begin{table}[!htb]"<<std::endl;
   outTableFile<<"\\begin{center}"<<std::endl;

   outTableFile<<"\\begin{tabular}{c|c|c|c}"<<std::endl;

   outTableFile<<"\\hline"<<std::endl;
   outTableFile<<"\\hline"<<std::endl;

   outTableFile<< " & " <<" & "<<" & "<<" \\\\"<<std::endl;

   outTableFile<< " Category " << " & " <<" Data Event "<<" & "<<" #Delta M_{data} "<<" #sigma_{cb}^{data} "<<" \\\\ "<<std::endl;

   outTableFile<<"\\hline"<<std::endl;
   outTableFile<<"\\hline"<<std::endl;

   outTableFile<< " & " <<" & "<<" &  "<<" \\\\ "<<std::endl;


   std::cout<<" Fit Z Peak EB-EB DATA and MC"<<std::endl;

   BinnedFitZPeak("EB-EB", 1, ZmassDATA["EB-EB"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EB-EB" <<" & "<<ZmassDATA["EB-EB"]->GetEntries() <<" & "<<ZmassDATA["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_NoReg")->GetParError(3) <<" & "<< ZmassDATA["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_NoReg")->GetParameter(4) <<" #pm "<< ZmassDATA["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_NoReg")->GetParError(4) <<" \\\\ "<<std::endl;


   std::cout<<" Fit Z Peak EB-EB DATA and MC Regression"<<std::endl;

   BinnedFitZPeak("EB-EB", 1, ZmassDATA_regression["EB-EB"],  nPoints, mZ_Min, mZ_Max);  


   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EB-EB" <<" & "<<ZmassDATA_regression["EB-EB"]->GetEntries() <<" & "<<ZmassDATA_regression["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_Reg")->GetParError(3) <<" & "<< ZmassDATA_regression["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_Reg")->GetParameter(4) <<" #pm "<< ZmassDATA_regression["EB-EB"]->GetFunction("bw_cb_DATA_EB-EB_Reg")->GetParError(4) <<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EBp DATA and MC"<<std::endl;
 
   BinnedFitZPeak("EBp", 1, ZmassDATA["EBp"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EBp" <<" & "<<ZmassDATA["EBp"]->GetEntries() <<" & "<<ZmassDATA["EBp"]->GetFunction("bw_cb_DATA_EBp_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EBp"]->GetFunction("bw_cb_DATA_EBp_NoReg")->GetParError(3) <<" & "<< ZmassDATA["EBp"]->GetFunction("bw_cb_DATA_EBp_NoReg")->GetParameter(4) <<" #pm "<< ZmassDATA["EBp"]->GetFunction("bw_cb_DATA_EBp_NoReg")->GetParError(4) <<" \\\\ "<<std::endl;


   std::cout<<" Fit Z Peak EBp DATA and MC Regression"<<std::endl;

   BinnedFitZPeak("EBp", 1, ZmassDATA_regression["EBp"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EBp" <<" & "<<ZmassDATA_regression["EBp"]->GetEntries() <<" & "<<ZmassDATA_regression["EBp"]->GetFunction("bw_cb_DATA_EBp_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EBp"]->GetFunction("bw_cb_DATA_EBp_Reg")->GetParError(3) <<" & "<< ZmassDATA_regression["EBp"]->GetFunction("bw_cb_DATA_EBp_Reg")->GetParameter(4) <<" #pm "<< ZmassDATA_regression["EBp"]->GetFunction("bw_cb_DATA_EBp_Reg")->GetParError(4) <<" \\\\ "<<std::endl;

  
   std::cout<<" Fit Z Peak EBm DATA and MC"<<std::endl;

   BinnedFitZPeak("EBm", 1, ZmassDATA["EBm"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EBm" <<" & "<<ZmassDATA["EBm"]->GetEntries() <<" & "<<ZmassDATA["EBm"]->GetFunction("bw_cb_DATA_EBm_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EBm"]->GetFunction("bw_cb_DATA_EBm_NoReg")->GetParError(3) <<" & "<< ZmassDATA["EBm"]->GetFunction("bw_cb_DATA_EBm_NoReg")->GetParameter(4) <<" #pm "<< ZmassDATA["EBm"]->GetFunction("bw_cb_DATA_EBm_NoReg")->GetParError(4) <<" \\\\"<<std::endl;


   std::cout<<" Fit Z Peak EBm DATA and MC Regression"<<std::endl;

   BinnedFitZPeak("EBm", 1, ZmassDATA_regression["EBm"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EBm" <<" & "<<ZmassDATA_regression["EBm"]->GetEntries() <<" & "<<ZmassDATA_regression["EBm"]->GetFunction("bw_cb_DATA_EBm_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EBm"]->GetFunction("bw_cb_DATA_EBm_Reg")->GetParError(3) <<" & "<< ZmassDATA_regression["EBm"]->GetFunction("bw_cb_DATA_EBm_Reg")->GetParameter(4) <<" #pm "<< ZmassDATA_regression["EBm"]->GetFunction("bw_cb_DATA_EBm_Reg")->GetParError(4) <<" \\\\ "<<std::endl;


   std::cout<<" Fit Z Peak R9 > DATA and MC "<<std::endl;

   BinnedFitZPeak("EB_R9_g", 1, ZmassDATA["EB_R9_g"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EB_R9_g" <<" & "<<ZmassDATA["EB_R9_g"]->GetEntries() <<" & "<<ZmassDATA["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_NoReg")->GetParError(3) <<" & "<< ZmassDATA["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_NoReg")->GetParameter(4) <<" #pm "<< ZmassDATA["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_NoReg")->GetParError(4) <<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak R9 > DATA and MC Regression"<<std::endl;
 
   BinnedFitZPeak("EB_R9_g", 1, ZmassDATA_regression["EB_R9_g"],nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EB_R9_g" <<" & "<<ZmassDATA_regression["EB_R9_g"]->GetEntries() <<" & "<<ZmassDATA_regression["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_Reg")->GetParError(3) <<" & "<< ZmassDATA_regression["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_Reg")->GetParameter(4) <<" #pm "<< ZmassDATA_regression["EB_R9_g"]->GetFunction("bw_cb_DATA_EB_R9_g_Reg")->GetParError(4) <<" \\\\"<<std::endl;


   std::cout<<" Fit Z Peak R9 < DATA and MC "<<std::endl;
 
   BinnedFitZPeak("EB_R9_l", 1, ZmassDATA["EB_R9_l"],  nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< " EB_R9_l" <<" & "<<ZmassDATA["EB_R9_l"]->GetEntries() <<" & "<<ZmassDATA["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_NoReg")->GetParError(3) <<" & "<< ZmassDATA["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_NoReg")->GetParameter(4) <<" #pm "<< ZmassDATA["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_NoReg")->GetParError(4) <<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak R9 < DATA and MC Regression "<<std::endl;

   BinnedFitZPeak("EB_R9_l", 1, ZmassDATA_regression["EB_R9_l"],  nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EB_R9_l" <<" & "<<ZmassDATA_regression["EB_R9_l"]->GetEntries() <<" & "<<ZmassDATA_regression["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_Reg")->GetParError(3) <<" & "<< ZmassDATA_regression["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_Reg")->GetParameter(4) <<" #pm "<< ZmassDATA_regression["EB_R9_l"]->GetFunction("bw_cb_DATA_EB_R9_l_Reg")->GetParError(4) <<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE  DATA and MC  "<<std::endl;

   BinnedFitZPeak("EE-EE", 1, ZmassDATA["EE-EE"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EE-EE" <<" & "<<ZmassDATA["EE-EE"]->GetEntries() <<" & "<<ZmassDATA["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_NoReg")->GetParError(4) <<" & "<< ZmassDATA["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_NoReg")->GetParameter(4) <<" #pm "<< ZmassDATA["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_NoReg")->GetParError(4) <<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE  DATA and MC Regression  "<<std::endl;
 
   BinnedFitZPeak("EE-EE", 2, ZmassDATA_regression["EE-EE"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EE-EE" <<" & "<<ZmassDATA_regression["EE-EE"]->GetEntries() <<" & "<<ZmassDATA_regression["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_Reg")->GetParError(3) <<" & "<< ZmassDATA_regression["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_Reg")->GetParameter(4) <<" #pm "<< ZmassDATA_regression["EE-EE"]->GetFunction("bw_cb_DATA_EE-EE_Reg")->GetParError(4) <<" \\\\ "<<std::endl;


   std::cout<<" Fit Z Peak EEp  DATA and MC "<<std::endl;

   BinnedFitZPeak("EEp", 2, ZmassDATA["EEp"],nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EEp" <<" & "<<ZmassDATA["EEp"]->GetEntries() <<" & "<<ZmassDATA["EEp"]->GetFunction("bw_cb_DATA_EEp_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EEp"]->GetFunction("bw_cb_DATA_EEp_NoReg")->GetParError(3) <<" & "<< ZmassDATA["EEp"]->GetFunction("bw_cb_DATA_EEp_NoReg")->GetParameter(4) <<" #pm "<< ZmassDATA["EEp"]->GetFunction("bw_cb_DATA_EEp_NoReg")->GetParError(4) <<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EEp  DATA and MC Regression "<<std::endl;

   BinnedFitZPeak("EEp", 2, ZmassDATA_regression["EEp"],  nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EEp" <<" & "<<ZmassDATA_regression["EEp"]->GetEntries() <<" & "<<ZmassDATA_regression["EEp"]->GetFunction("bw_cb_DATA_EEp_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EEp"]->GetFunction("bw_cb_DATA_EEp_Reg")->GetParError(3) <<" & "<< ZmassDATA_regression["EEp"]->GetFunction("bw_cb_DATA_EEp_Reg")->GetParameter(4) <<" #pm "<< ZmassDATA_regression["EEp"]->GetFunction("bw_cb_DATA_EEp_Reg")->GetParError(4) <<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EEm  DATA and MC "<<std::endl;

   BinnedFitZPeak("EEm", 2, ZmassDATA["EEm"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EEm" <<" & "<<ZmassDATA["EEm"]->GetEntries() <<" & "<<ZmassDATA["EEm"]->GetFunction("bw_cb_DATA_EEm_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EEm"]->GetFunction("bw_cb_DATA_EEm_NoReg")->GetParError(3) <<" & "<< ZmassDATA["EEm"]->GetFunction("bw_cb_DATA_EEm_NoReg")->GetParameter(4) <<" #pm "<< ZmassDATA["EEm"]->GetFunction("bw_cb_DATA_EEm_NoReg")->GetParError(4) <<" \\\\"<<std::endl;

   std::cout<<" Fit Z Peak EEm  DATA and MC Regression "<<std::endl;

   BinnedFitZPeak("EEm", 2, ZmassDATA_regression["EEm"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EEm" <<" & "<<ZmassDATA_regression["EEm"]->GetEntries() <<" & "<<ZmassDATA_regression["EEm"]->GetFunction("bw_cb_DATA_EEm_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EEm"]->GetFunction("bw_cb_DATA_EEm_Reg")->GetParError(3) <<" & "<< ZmassDATA_regression["EEm"]->GetFunction("bw_cb_DATA_EEm_Reg")->GetParameter(4) <<" #pm "<< ZmassDATA_regression["EEm"]->GetFunction("bw_cb_DATA_EEm_Reg")->GetParError(4) <<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE R9 > DATA and MC  "<<std::endl;

   BinnedFitZPeak("EE_R9_g", 2, ZmassDATA["EE_R9_g"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EE_R9_g" <<" & "<<ZmassDATA["EE_R9_g"]->GetEntries() <<" & "<<ZmassDATA["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_NoReg")->GetParError(3) <<" & "<< ZmassDATA["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_NoReg")->GetParameter(4) <<" #pm "<< ZmassDATA["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_NoReg")->GetParError(4) <<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE R9 > DATA and MC Regression "<<std::endl;
 
   BinnedFitZPeak("EE_R9_g", 2, ZmassDATA_regression["EE_R9_g"], nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EE_R9_g" <<" & "<<ZmassDATA_regression["EE_R9_g"]->GetEntries() <<" & "<<ZmassDATA_regression["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_Reg")->GetParError(3) <<" & "<< ZmassDATA_regression["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_Reg")->GetParameter(4) <<" #pm "<< ZmassDATA_regression["EE_R9_g"]->GetFunction("bw_cb_DATA_EE_R9_g_Reg")->GetParError(4) <<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE R9 < DATA and MC  "<<std::endl;

   BinnedFitZPeak("EE_R9_l", 2, ZmassDATA["EE_R9_l"], nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EE_R9_l" <<" & "<<ZmassDATA["EE_R9_l"]->GetEntries() <<" & "<<ZmassDATA["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_NoReg")->GetParError(3) <<" & "<< ZmassDATA["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_NoReg")->GetParameter(4) <<" #pm "<< ZmassDATA["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_NoReg")->GetParError(4) <<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE R9 < DATA and MC "<<std::endl;

   BinnedFitZPeak("EE_R9_l", 2, ZmassDATA_regression["EE_R9_l"], nPoints, mZ_Min, mZ_Max);

  outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EE_R9_l" <<" & "<<ZmassDATA_regression["EE_R9_l"]->GetEntries() <<" & "<<ZmassDATA_regression["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_Reg")->GetParError(3) <<" & "<< ZmassDATA_regression["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_Reg")->GetParameter(4) <<" #pm "<< ZmassDATA_regression["EE_R9_l"]->GetFunction("bw_cb_DATA_EE_R9_l_Reg")->GetParError(4) <<" \\\\ "<<std::endl;

   std::cout<<" Fit Z Peak EE-EB R9  DATA and MC "<<std::endl;

   BinnedFitZPeak("EB-EE", 2, ZmassDATA["EB-EE"],  nPoints, mZ_Min, mZ_Max,energyType);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EB-EE" <<" & "<<ZmassDATA["EB-EE"]->GetEntries() <<" & "<<ZmassDATA["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_NoReg")->GetParameter(3)<<" #pm "<<ZmassDATA["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_NoReg")->GetParError(3) <<" & "<< ZmassDATA["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_NoReg")->GetParameter(4) <<" #pm "<< ZmassDATA["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_NoReg")->GetParError(4) <<" \\\\ "<<std::endl;


   std::cout<<" Fit Z Peak EE-EB R9  DATA and MC Regression "<<std::endl;

   BinnedFitZPeak("EB-EE", 2, ZmassDATA_regression["EB-EE"],  nPoints, mZ_Min, mZ_Max);

   outTableFile<< " & " <<" & "<<" & "<<" \\\\ "<<std::endl;

   outTableFile<< "EB-EE" <<" & "<<ZmassDATA_regression["EB-EE"]->GetEntries() <<" & "<<ZmassDATA_regression["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_Reg")->GetParameter(3)<<" #pm "<<ZmassDATA_regression["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_Reg")->GetParError(3) <<" & "<< ZmassDATA_regression["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_Reg")->GetParameter(4) <<" #pm "<< ZmassDATA_regression["EB-EE"]->GetFunction("bw_cb_DATA_EB-EE_Reg")->GetParError(4) <<" \\\\ "<<std::endl;

   outTableFile<< " \\hline "<<std::endl;
   outTableFile<< " \\hline "<<std::endl;

   outTableFile<< " \\end{tabular} "<<std::endl;
   outTableFile<< " \\end{center} "<<std::endl;
   outTableFile<< " \\end{table} "<<std::endl;

}


 /// Output save 
 std::cout << "recalibZ::Saving and Closing" << std::endl;

 ZmassDATA["EB-EB"]->Write();
 ZmassDATA["EB-EE"]->Write();
 ZmassDATA["EE-EE"]->Write();
 ZmassDATA["EBp"]->Write();
 ZmassDATA["EB_R9_g"]->Write();
 ZmassDATA["EB_R9_l"]->Write();
 ZmassDATA["EEp"]->Write();
 ZmassDATA["EEm"]->Write();
 ZmassDATA["EE_R9_g"]->Write();
 ZmassDATA["EE_R9_l"]->Write();
 ZmassDATA["EB-EE"]->Write();

 ZmassMC["EB-EB"]->Write();
 ZmassMC["EB-EE"]->Write();
 ZmassMC["EE-EE"]->Write();
 ZmassMC["EBp"]->Write();
 ZmassMC["EB_R9_g"]->Write();
 ZmassMC["EB_R9_l"]->Write();
 ZmassMC["EEp"]->Write();
 ZmassMC["EEm"]->Write();
 ZmassMC["EE_R9_g"]->Write();
 ZmassMC["EE_R9_l"]->Write();
 ZmassMC["EB-EE"]->Write();

 ZmassDATA_regression["EB-EB"]->Write();
 ZmassDATA_regression["EB-EE"]->Write();
 ZmassDATA_regression["EE-EE"]->Write();

 ZmassMC_regression["EB-EB"]->Write();
 ZmassMC_regression["EB-EE"]->Write();
 ZmassMC_regression["EE-EE"]->Write();

 outputTFile -> Close();

 return 0;
}
