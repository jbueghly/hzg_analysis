#!/usr/bin/env python

# based on TMVAClassification.C and modified for pyroot

import ROOT as r
from ROOT import TMVA as t

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

    inputFilesDir = 'data/step2_kin_bdt'
    outputWeightsDir = 'trained_bdts'

    print('training combined dijet MVA')
    print('setting up TMVA')
    
    outFileName = 'trained_bdts/vbf_bdt_combined_james_output_file.root'
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


    factory = t.Factory('vbf_bdt_combined_james_current', outputFile, '!V:!Silent:Color:DrawProgressBar:Transformations=I;D;G,D:AnalysisType=Classification')
    factory.Print()
    
    t.gConfig().GetIONames().fWeightFileDir = outputWeightsDir
    dataloader = t.DataLoader(".")

    dataloader.AddVariable('dijetDEta', 'dijetDEta', 'dijetDEta', 'F')
    dataloader.AddVariable('dijetDPhi', 'dijetDPhi', 'dijetDPhi', 'F')
    dataloader.AddVariable('llgJJDPhi', 'llgJJDPhi', 'llgJJDPhi', 'F')
    dataloader.AddVariable('jPhotonDRMin', 'jPhotonDRMin', 'jPhotonDRMin', 'F')
    dataloader.AddVariable('ptt', 'ptt', 'ptt', 'F')
    dataloader.AddVariable('jetOnePt', 'jetOnePt', 'jetOnePt', 'F')
    dataloader.AddVariable('jetTwoPt', 'jetTwoPt', 'jetTwoPt', 'F')
    dataloader.AddVariable('kin_bdt_james', 'kin_bdt_james', 'kin_bdt_james', 'F')
    dataloader.AddVariable('vbfPtBalance', 'vbfPtBalance', 'vbfPtBalance', 'F')
    dataloader.AddVariable('photonZepp', 'photonZepp', 'photonZepp', 'F')

    # trees for training
    inputFile = r.TFile('{0}/output_combined.root'.format(inputFilesDir))

    sig_vbf_16 = inputFile.Get('hzg_vbf_M125_2016')
    bkg_zjets_16 = inputFile.Get('zjets_M50_2016') 
    bkg_zg_16 = inputFile.Get('zg_llg_2016')
    bkg_zg_ewk_16 = inputFile.Get('zg_ewk_2016')
    bkg_ttjets_16 = inputFile.Get('ttjets_2016')
    bkg_ggH_16 = inputFile.Get('hzg_gluglu_M125_2016')
    
    sig_vbf_17 = inputFile.Get('hzg_vbf_M125_2017')
    bkg_zjets_17 = inputFile.Get('zjets_M50_2017') 
    bkg_zg_17 = inputFile.Get('zg_llg_2017')
    bkg_zg_ewk_17 = inputFile.Get('zg_ewk_2017')
    bkg_ttjets_17 = inputFile.Get('ttjets_2017')
    bkg_ggH_17 = inputFile.Get('hzg_gluglu_M125_2017')
    
    sig_vbf_18 = inputFile.Get('hzg_vbf_M125_2018')
    bkg_zjets_18 = inputFile.Get('zjets_M50_2018') 
    bkg_zg_18 = inputFile.Get('zg_llg_2018')
    bkg_zg_ewk_18 = inputFile.Get('zg_ewk_2018')
    bkg_ttjets_18 = inputFile.Get('ttjets_2018')
    bkg_ggH_18 = inputFile.Get('hzg_gluglu_M125_2018') 
    
    dataloader.AddSignalTree(sig_vbf_16)
    dataloader.AddBackgroundTree(bkg_zjets_16)
    dataloader.AddBackgroundTree(bkg_zg_16)
    dataloader.AddBackgroundTree(bkg_zg_ewk_16)
    dataloader.AddBackgroundTree(bkg_ttjets_16)
    dataloader.AddBackgroundTree(bkg_ggH_16)
    
    dataloader.AddSignalTree(sig_vbf_17)
    dataloader.AddBackgroundTree(bkg_zjets_17)
    dataloader.AddBackgroundTree(bkg_zg_17)
    dataloader.AddBackgroundTree(bkg_zg_ewk_17)
    dataloader.AddBackgroundTree(bkg_ttjets_17)
    dataloader.AddBackgroundTree(bkg_ggH_17)
    
    dataloader.AddSignalTree(sig_vbf_18)
    dataloader.AddBackgroundTree(bkg_zjets_18)
    dataloader.AddBackgroundTree(bkg_zg_18)
    dataloader.AddBackgroundTree(bkg_zg_ewk_18)
    dataloader.AddBackgroundTree(bkg_ttjets_18)
    dataloader.AddBackgroundTree(bkg_ggH_18)


    dataloader.SetSignalWeightExpression('eventWeight*genWeight*mc_sf*pt_weight*isDijetTag*jetOneMatched*jetTwoMatched*useTMVA')
    dataloader.SetBackgroundWeightExpression('eventWeight*genWeight*mc_sf*pt_weight*isDijetTag*useTMVA')
    dataloader.PrepareTrainingAndTestTree(r.TCut(''), r.TCut(''), 'SplitMode=Random:NormMode=NumEvents:!V')

    print('booking the methods')

    if Use['BDTG']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDTG', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:BoostType=Grad:Shrinkage=0.10:UseBaggedGrad:GradBaggingFraction=0.5:nCuts=20:NNodesMax=5')

    if Use['BDT']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDT', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:nEventsMin=40:MaxDepth=4:BoostType=AdaBoost:AdaBoostBeta=0.6:SeparationType=GiniIndex:nCuts=20:PruningValFraction=0.6')

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
