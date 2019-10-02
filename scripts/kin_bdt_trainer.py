#!/usr/bin/env python

# based on TMVAClassification.C and modified for pyroot

import ROOT as r
from ROOT import TMVA as t

if __name__ == '__main__':
    inputFilesDir = 'data/step1_sfs'
    outputWeightsDir = 'trained_bdts'

    print('setting up TMVA')

    # ggf, vbf, tth, zh, w+h, w-h, z+jets, zg_llg, tt2l2nu
    mcwei = [0.0007090, 0.0001082, 0.0001495, 0.0001910, 0.0001763, 0.0001148, 2.6446207, 0.4315552]

    outFileName = 'trained_bdts/mva_output_file.root'
    outputFile = r.TFile(outFileName, 'RECREATE')

    t.Tools.Instance() # what does this do ?????? 
    
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


    factory = t.Factory('kin_discr', outputFile, '!V:!Silent:Color:DrawProgressBar:Transformations=I;D;G,D:AnalysisType=Classification')
    factory.Print()
    
    t.gConfig().GetIONames().fWeightFileDir = outputWeightsDir
    dataloader = t.DataLoader(".")

    dataloader.AddVariable('zgLittleThetaJames', 'zgLittleThetaJames', 'zgLittleThetaJames', 'F')
    dataloader.AddVariable('zgBigThetaJames', 'zgBigThetaJames', 'zgBigThetaJames', 'F')
    dataloader.AddVariable('llgPtOverM', 'llgPtOverM', 'llgPtOverM', 'F')
    dataloader.AddVariable('leptonOneEta', 'leptonOneEta', 'leptonOneEta', 'F')
    dataloader.AddVariable('leptonTwoEta', 'leptonTwoEta', 'leptonTwoEta', 'F')
    dataloader.AddVariable('photonOneEta', 'photonOneEta', 'photonOneEta', 'F')
    dataloader.AddVariable('zgPhiJames', 'zgPhiJames', 'zgPhiJames', 'F')
    dataloader.AddVariable('photonOneR9', 'photonOneR9', 'photonOneR9', 'F')
    dataloader.AddVariable('photonOneMVA', 'photonOneMVA', 'photonOneMVA', 'F')
    dataloader.AddVariable('photonOneERes', 'photonOneERes', 'photonOneERes', 'F')
    dataloader.AddVariable('lPhotonDRMin', 'lPhotonDRMin', 'lPhotonDRMin', 'F')
    dataloader.AddVariable('lPhotonDRMax', 'lPhotonDRMax', 'lPhotonDRMax', 'F')

    # trees for training
    inputFile = r.TFile('{0}/output_combined_2016.root'.format(inputFilesDir))
    sig_ggf = inputFile.Get('hzg_gluglu_M125_16') 
    sig_vbf = inputFile.Get('hzg_vbf_M125_16')
    sig_tth = inputFile.Get('hzg_tth_M125_16')
    sig_zh = inputFile.Get('hzg_zh_M125_16')
    sig_wplush = inputFile.Get('hzg_wplush_M125_16')
    sig_wminush = inputFile.Get('hzg_wminush_M125_16')
    bkg1 = inputFile.Get('zjets_m-50_amc_16') 
    bkg2 = inputFile.Get('zg_llg_16')
    
    dataloader.AddSignalTree(sig_ggf, mcwei[0])
    dataloader.AddSignalTree(sig_vbf, mcwei[1])
    dataloader.AddSignalTree(sig_tth, mcwei[2])
    dataloader.AddSignalTree(sig_zh, mcwei[3])
    dataloader.AddSignalTree(sig_wplush, mcwei[4])
    dataloader.AddSignalTree(sig_wminush, mcwei[5])
    dataloader.AddBackgroundTree(bkg1, mcwei[6])
    dataloader.AddBackgroundTree(bkg2, mcwei[7])

    dataloader.SetSignalWeightExpression('eventWeight*genWeight')
    dataloader.SetBackgroundWeightExpression('eventWeight*genWeight')
    dataloader.PrepareTrainingAndTestTree(r.TCut(''), r.TCut(''), 'SplitMode=Random:NormMode=NumEvents:!V')

    print('booking the methods')

    if Use['BDTG']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDTG', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:BoostType=Grad:Shrinkage=0.10:UseBaggedGrad:GradBaggingFraction=0.5:nCuts=20:NNodesMax=5')

    if Use['BDT']:
        #factory.BookMethod(dataloader, t.Types.kBDT, 'BDT', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:nEventsMin=40:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=1:SeparationType=GiniIndex:nCuts=20')
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDT', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:nEventsMin=40:MaxDepth=5:BoostType=AdaBoost:AdaBoostBeta=0.6:SeparationType=GiniIndex:nCuts=20')
        #factory.BookMethod(dataloader, t.Types.kBDT, 'BDT', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:MinNodeSize=0.0230303%:MaxDepth=5:BoostType=AdaBoost:AdaBoostBeta=0.6:SeparationType=GiniIndex:nCuts=20')

    if Use['BDTRT']:
        #factory.BookMethod(dataloader, t.Types.kBDT, 'BDTRT', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:nEventsMin=40:MaxDepth=4:UseRandomisedTrees=True:BoostType=AdaBoost:AdaBoostBeta=1:SeparationType=GiniIndex:nCuts=20:NNodesMax=5')
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
