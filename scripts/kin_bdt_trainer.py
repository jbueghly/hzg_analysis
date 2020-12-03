#!/usr/bin/env python

# based on TMVAClassification.C and modified for pyroot

import ROOT as r
from ROOT import TMVA as t
import pickle

if __name__ == '__main__':

    mc_16 = {'hzg_gluglu_M125_2016': 'hzg_gluglu_M125_2016', 'hzg_vbf_M125': 'hzg_vbf_M125_2016', 'hzg_tth_M125': 'hzg_tth_M125_2016',
             'hzg_zh_M125_2016': 'hzg_zh_M125_2016', 'hzg_wplush_M125': 'hzg_wplush_M125_2016', 'hzg_wminush_M125': 'hzg_wminush_M125_2016',
             'zjets_M50_2016': 'zjets_m-50_amc_2016', 'zg_llg': 'zg_llg_2016', 'ewk_zg': 'zg_ewk_2016', 'ttjets': 'ttjets_2016'}
    
    mc_17 = {'hzg_gluglu_m125_2017': 'hzg_gluglu_m125_2017', 'hzg_vbf_m125': 'hzg_vbf_m125_2017', 'hzg_tth_m125': 'hzg_tth_m125_2017',
             'hzg_zh_m125_2017': 'hzg_zh_m125_2017', 'hzg_wplush_m125': 'hzg_wplush_m125_2017', 'hzg_wminush_m125': 'hzg_wminush_m125_2017',
             'zjets_m50_2017': 'zjets_m-50_amc_2017', 'zg_llg': 'zg_llg_2017', 'ewk_zg': 'zg_ewk_2017', 'ttjets': 'ttjets_2017'}
    
    mc_18 = {'hzg_gluglu_M125_2018': 'hzg_gluglu_M125_2018', 'hzg_vbf_M125': 'hzg_vbf_M125_2018', 'hzg_tth_M125': 'hzg_tth_M125_2018',
             'hzg_zh_M125_2018': 'hzg_zh_M125_2018', 'hzg_wplush_M125': 'hzg_wplush_M125_2018', 'hzg_wminush_M125': 'hzg_wminush_M125_2018',
             'zjets_M50_2018': 'zjets_m-50_amc_2018', 'zg_llg': 'zg_llg_2018', 'ewk_zg': 'zg_ewk_2018', 'ttjets': 'ttjets_2018'}
    
    mc = {2016: mc_16, 2017: mc_17, 2018: mc_18}

    inputFilesDir = 'data/step1_sfs'
    #inputFilesDir = 'data/step1_sfs/WPMingyanV2'
    outputWeightsDir = 'trained_bdts/reanalysis_2'
 
    print('training combined kinematic BDT')
    print('setting up TMVA')

    #outFileName = 'trained_bdts/kin_bdt_combined_james_output_file_half_signal.root' 
    #outFileName = 'trained_bdts/kin_bdt_combined_james_output_file_half_signal_half_background.root'
    outFileName = 'trained_bdts/reanalysis_2/kin_bdt_combined_james_output_file.root'
    #outFileName = 'trained_bdts/kin_bdt_2016_with_obj_match.root'
    outputFile = r.TFile(outFileName, 'RECREATE')

    t.Tools.Instance() 
    
    Use =   {
            'BDT': 1,
            'BDTG': 0,
            'BDTRT': 0,
            'BDTB': 0,
            'BDTD': 0,
            'BDTF': 0,
            'MLP': 0,
            'MLPBFGS': 0,
            'MLPBNN': 0,
            'CFMlpANN': 0,
            'TMlpANN': 0
            }


    #factory = t.Factory('kin_bdt_combined_james_current_half_signal', outputFile, '!V:!Silent:Color:DrawProgressBar:Transformations=I;D;G,D:AnalysisType=Classification')
    #factory = t.Factory('kin_bdt_combined_james_current_half_signal_half_background', outputFile, '!V:!Silent:Color:DrawProgressBar:Transformations=I;D;G,D:AnalysisType=Classification')
    factory = t.Factory('kin_bdt_combined_james_current', outputFile, '!V:!Silent:Color:DrawProgressBar:Transformations=I;D;G,D:AnalysisType=Classification')
    factory.Print()
        
    t.gConfig().GetIONames().fWeightFileDir = outputWeightsDir
    dataloader = t.DataLoader(".")

    #dataloader.AddVariable('zgLittleThetaMY', 'zgLittleThetaMY', 'zgLittleThetaMY', 'F')
    dataloader.AddVariable('zgLittleTheta', 'zgLittleTheta', 'zgLittleTheta', 'F')
    dataloader.AddVariable('zgBigTheta', 'zgBigTheta', 'zgBigTheta', 'F')
    dataloader.AddVariable('llgPtOverM', 'llgPtOverM', 'llgPtOverM', 'F')
    dataloader.AddVariable('leptonOneEta', 'leptonOneEta', 'leptonOneEta', 'F')
    dataloader.AddVariable('leptonTwoEta', 'leptonTwoEta', 'leptonTwoEta', 'F')
    dataloader.AddVariable('photonEta', 'photonEta', 'photonEta', 'F')
    dataloader.AddVariable('zgPhi', 'zgPhi', 'zgPhi', 'F')
    dataloader.AddVariable('photonMVA', 'photonMVA', 'photonMVA', 'F')
    #dataloader.AddVariable('corrPhotonMVA', 'corrPhotonMVA', 'corrPhotonMVA', 'F')
    dataloader.AddVariable('photonERes', 'photonERes', 'photonERes', 'F')
    dataloader.AddVariable('lPhotonDRMin', 'lPhotonDRMin', 'lPhotonDRMin', 'F')
    dataloader.AddVariable('lPhotonDRMax', 'lPhotonDRMax', 'lPhotonDRMax', 'F')

    # trees for training
    inputFile = r.TFile('{0}/output_combined.root'.format(inputFilesDir))
        
    sig_ggf_16 = inputFile.Get('hzg_gluglu_M125_2016') 
    sig_vbf_16 = inputFile.Get('hzg_vbf_M125_2016')
    sig_tth_16 = inputFile.Get('hzg_tth_M125_2016')
    sig_zh_16 = inputFile.Get('hzg_zh_M125_2016')
    sig_wplush_16 = inputFile.Get('hzg_wplush_M125_2016')
    sig_wminush_16 = inputFile.Get('hzg_wminush_M125_2016')
    bkg_zjets_16 = inputFile.Get('zjets_M50_2016') 
    bkg_zg_16 = inputFile.Get('zg_llg_2016')
    bkg_zg_ewk_16 = inputFile.Get('zg_ewk_2016')
    bkg_ttjets_16 = inputFile.Get('ttjets_2016')
    
    sig_ggf_17 = inputFile.Get('hzg_gluglu_M125_2017') 
    sig_vbf_17 = inputFile.Get('hzg_vbf_M125_2017')

    sig_tth_17 = inputFile.Get('hzg_tth_M125_2017')
    sig_zh_17 = inputFile.Get('hzg_zh_M125_2017')
    sig_wplush_17 = inputFile.Get('hzg_wplush_M125_2017')
    sig_wminush_17 = inputFile.Get('hzg_wminush_M125_2017')
    bkg_zjets_17 = inputFile.Get('zjets_M50_2017') 
    bkg_zg_17 = inputFile.Get('zg_llg_2017')
    bkg_zg_ewk_17 = inputFile.Get('zg_ewk_2017')
    bkg_ttjets_17 = inputFile.Get('ttjets_2017')
    
    sig_ggf_18 = inputFile.Get('hzg_gluglu_M125_2018') 
    sig_vbf_18 = inputFile.Get('hzg_vbf_M125_2018')
    sig_tth_18 = inputFile.Get('hzg_tth_M125_2018')
    sig_zh_18 = inputFile.Get('hzg_zh_M125_2018')
    sig_wplush_18 = inputFile.Get('hzg_wplush_M125_2018')
    sig_wminush_18 = inputFile.Get('hzg_wminush_M125_2018')
    bkg_zjets_18 = inputFile.Get('zjets_M50_2018') 
    bkg_zg_18 = inputFile.Get('zg_llg_2018') 
    bkg_zg_ewk_18 = inputFile.Get('zg_ewk_2018')
    bkg_ttjets_18 = inputFile.Get('ttjets_2018')

    #mc_sfs = pickle.load(open('data/mc_sfs/golden_1/mc_sfs.pkl', 'rb'))
    #print(mc_sfs)
  
    #dataloader.AddSignalTree(sig_ggf_16, mc_sfs[2016]['hzg_gluglu_M125_2016'])
    #dataloader.AddSignalTree(sig_vbf_16, mc_sfs[2016]['hzg_vbf_M125_2016'])
    #dataloader.AddSignalTree(sig_tth_16, mc_sfs[2016]['hzg_tth_M125_2016'])
    #dataloader.AddSignalTree(sig_zh_16, mc_sfs[2016]['hzg_zh_M125_2016'])
    #dataloader.AddSignalTree(sig_wplush_16, mc_sfs[2016]['hzg_wplush_M125_2016'])
    #dataloader.AddSignalTree(sig_wminush_16, mc_sfs[2016]['hzg_wminush_M125_2016'])
    #dataloader.AddBackgroundTree(bkg_zjets_16, mc_sfs[2016]['zjets_M50_2016'])
    #dataloader.AddBackgroundTree(bkg_zg_16, mc_sfs[2016]['zg_llg_2016'])
    #
    #dataloader.AddSignalTree(sig_ggf_17, mc_sfs[2017]['hzg_gluglu_M125_2017'])
    #dataloader.AddSignalTree(sig_vbf_17, mc_sfs[2017]['hzg_vbf_M125_2017'])
    #dataloader.AddSignalTree(sig_tth_17, mc_sfs[2017]['hzg_tth_M125_2017'])
    #dataloader.AddSignalTree(sig_zh_17, mc_sfs[2017]['hzg_zh_M125_2017'])
    #dataloader.AddSignalTree(sig_wplush_17, mc_sfs[2017]['hzg_wplush_M125_2017'])
    #dataloader.AddSignalTree(sig_wminush_17, mc_sfs[2017]['hzg_wminush_M125_2017'])
    #dataloader.AddBackgroundTree(bkg_zjets_17, mc_sfs[2017]['zjets_M50_2017'])
    #dataloader.AddBackgroundTree(bkg_zg_17, mc_sfs[2017]['zg_llg_2017'])
    
    #dataloader.AddSignalTree(sig_ggf_18, mc_sfs[2018]['hzg_gluglu_M125_2018'])
    #dataloader.AddSignalTree(sig_vbf_18, mc_sfs[2018]['hzg_vbf_M125_2018'])
    #dataloader.AddSignalTree(sig_tth_18, mc_sfs[2018]['hzg_tth_M125_2018'])
    #dataloader.AddSignalTree(sig_zh_18, mc_sfs[2018]['hzg_zh_M125_2018'])
    #dataloader.AddSignalTree(sig_wplush_18, mc_sfs[2018]['hzg_wplush_M125_2018'])
    #dataloader.AddSignalTree(sig_wminush_18, mc_sfs[2018]['hzg_wminush_M125_2018'])
    #dataloader.AddBackgroundTree(bkg_zjets_18, mc_sfs[2018]['zjets_M50_2018'])
    #dataloader.AddBackgroundTree(bkg_zg_18, mc_sfs[2018]['zg_llg_2018'])
    

    dataloader.AddSignalTree(sig_ggf_16)
    dataloader.AddSignalTree(sig_vbf_16)
    dataloader.AddSignalTree(sig_tth_16)
    dataloader.AddSignalTree(sig_zh_16)
    dataloader.AddSignalTree(sig_wplush_16)
    dataloader.AddSignalTree(sig_wminush_16)
    dataloader.AddBackgroundTree(bkg_zjets_16)
    dataloader.AddBackgroundTree(bkg_zg_16)
    ###dataloader.AddBackgroundTree(bkg_zg_ewk_16)
    ###dataloader.AddBackgroundTree(bkg_ttjets_16)

    dataloader.AddSignalTree(sig_ggf_17)
    dataloader.AddSignalTree(sig_vbf_17)
    dataloader.AddSignalTree(sig_tth_17)
    dataloader.AddSignalTree(sig_zh_17)
    dataloader.AddSignalTree(sig_wplush_17)
    dataloader.AddSignalTree(sig_wminush_17)
    dataloader.AddBackgroundTree(bkg_zjets_17)
    dataloader.AddBackgroundTree(bkg_zg_17)
    ###dataloader.AddBackgroundTree(bkg_zg_ewk_17)
    ###dataloader.AddBackgroundTree(bkg_ttjets_17)
    #
    dataloader.AddSignalTree(sig_ggf_18)
    dataloader.AddSignalTree(sig_vbf_18)
    dataloader.AddSignalTree(sig_tth_18)
    dataloader.AddSignalTree(sig_zh_18)
    dataloader.AddSignalTree(sig_wplush_18)
    dataloader.AddSignalTree(sig_wminush_18)
    dataloader.AddBackgroundTree(bkg_zjets_18)
    dataloader.AddBackgroundTree(bkg_zg_18)
    ##dataloader.AddBackgroundTree(bkg_zg_ewk_18)
    ##dataloader.AddBackgroundTree(bkg_ttjets_18)
 
    dataloader.SetSignalWeightExpression('eventWeight*genWeight*mc_sf*pt_weight*useTMVA')
    #dataloader.SetSignalWeightExpression('eventWeight*genWeight*pt_weight*useTMVA')
    #dataloader.SetSignalWeightExpression('genWeight*mc_sf*useTMVA')
    dataloader.SetBackgroundWeightExpression('eventWeight*genWeight*mc_sf*pt_weight*useTMVA')
    #dataloader.SetBackgroundWeightExpression('eventWeight*genWeight*pt_weight*useTMVA')
    #dataloader.SetBackgroundWeightExpression('genWeight*mc_sf*useTMVA')
    dataloader.PrepareTrainingAndTestTree(r.TCut(''), r.TCut(''), 'SplitMode=Random:NormMode=NumEvents:!V')

    print('booking the methods')

    if Use['BDTG']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDTG', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:BoostType=Grad:Shrinkage=0.10:UseBaggedGrad:GradBaggingFraction=0.5:nCuts=20:NNodesMax=5')

    if Use['BDT']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDT', '!H:!V:IgnoreNegWeightsInTraining:NTrees=3500:nEventsMin=40:MaxDepth=4:BoostType=AdaBoost:AdaBoostBeta=0.6:SeparationType=GiniIndex:nCuts=20')
    #if Use['BDT']:
    #    factory.BookMethod(dataloader, t.Types.kBDT, 'BDT', '!H:!V:IgnoreNegWeightsInTraining:NTrees=800:MinNodeSize=0.005:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.6:SeparationType=GiniIndex:nCuts=20')

    if Use['BDTRT']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDTRT', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:nEventsMin=40:MaxDepth=5:UseRandomisedTrees=True:BoostType=AdaBoost:AdaBoostBeta=0.6:SeparationType=GiniIndex:nCuts=20:NNodesMax=5')

    if Use['BDTB']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDTB', '!H:!V:NTrees=400:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning')

    if Use['BDTD']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDTD', '!H:!V:NTrees=400:nEventsMin=400:MaxDepth=3:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning:VarTransform=Decorrelate')

    if Use['BDTF']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDTMitFisher', '!H:!V:NTrees=50:nEventsMin=150:UseFisherCuts:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning')

    if Use['MLP']:
        factory.BookMethod(dataloader, t.Types.kMLP, 'MLP', '!H:!V:NeuronType=tanh:VarTransform=N:NCycles=500:HiddenLayers=N:TestRate=10')

    if Use['MLPBFGS']:
        factory.BookMethod(dataloader, t.Types.kMLP, 'MLPBFGS', 'H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:TrainingMethod=BFGS:!UseRegulator')

    if Use['MLPBNN']:
        factory.BookMethod(dataloader, t.Types.kMLP, 'MLPBNN', 'H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:TrainingMethod=BFGS:UseRegulator')

    if Use['CFMlpANN']:
        factory.BookMethod(dataloader, t.Types.kCFMlpANN, 'CFMlpANN', '!H:!V:NCycles=2000:HiddenLayers=N+1,N')

    if Use['TMlpANN']:
        factory.BookMethod(dataloader, t.Types.kTMlpANN, 'TMlpANN', '!H:!V:NCycles=200:HiddenLayers=N+1,N:LearningMethod=BFGS:ValidationFraction=0.3')

    print('training the methods')

    factory.TrainAllMethods()

    print('evaluating the methods')
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    outputFile.Close()

    print('wrote the output root file')
    print('TMVA training is done!')

    del factory
