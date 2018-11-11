#!/usr/bin/env python

# based on TMVAClassification.C and modified for pyroot

import ROOT as r
from ROOT import TMVA as t

if __name__ == '__main__':
    inputFilesDir = 'data/step1_phores'
    outputWeightsDir = 'trained_bdts'

    print('setting up TMVA')

    # ggf, vbf, tth, zh, w+h, w-h, z+jets, zg_llg, tt2l2nu
    #mcwei = [0.0006731, 0.0001032, 0.0001448, 0.0001754, 0.0001645, 0.0001068, 2.6089713, 0.4303657, 0.0399476] # update to dict later
    #mcwei = [0.0006731, 2.6089713] # update to dict later

    mcwei = [0.0007087, 0.0001087, 0.0001937, 0.0001490, 0.0001510, 2.6467566, 0.4507267]

    # sampleNames ??????
    # outFileName ??????
    outFileName = 'trained_bdts/mva_output_file.root'

    t.Tools.Instance() # what does this do ?????? 
    
    Use =   {
            'BDT': 0,
            'BDTG': 0,
            'BDTRT': 1,
            'BDTB': 0,
            'BDTD': 0,
            'BDTF': 0,
            'MLP': 0,
            'MLPBFGS': 0,
            'MLPBNN': 0,
            'CFMlpANN': 0,
            'TMlpANN': 0
            }

    outputFile = r.TFile(outFileName, 'RECREATE')
    # classificationBaseName ??????

    factory = t.Factory('discr', outputFile, '!V:!Silent:Color:DrawProgressBar:Transformations=I;D;G,D:AnalysisType=Classification')
    #factory = t.Factory('discr', outputFile, '!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification')
    factory.Print()
    
    t.gConfig().GetIONames().fWeightFileDir = outputWeightsDir

    dataloader = t.DataLoader("dataset")

    dataloader.AddVariable('zgLittleTheta', 'costheta', 'costheta', 'F')
    dataloader.AddVariable('zgBigTheta', 'cosTheta', 'cosTheta', 'F')
    dataloader.AddVariable('llgPtOverM', 'mllgptdmllg', 'mllgptdmllg', 'F')
    dataloader.AddVariable('leptonOneEta', 'lepEta1', 'lepEta1', 'F')
    dataloader.AddVariable('leptonTwoEta', 'lepEta2', 'lepEta2', 'F')
    dataloader.AddVariable('photonOneEta', 'phoEta', 'phoEta', 'F')
    dataloader.AddVariable('zgPhi', 'Phi', 'Phi', 'F')
    dataloader.AddVariable('photonOneR9', 'phoR9', 'phoR9', 'F')
    dataloader.AddVariable('photonOneMVA', 'phoMVA', 'phoMVA', 'F')
    dataloader.AddVariable('phores', 'phores', 'phores', 'F')
    dataloader.AddVariable('lPhotonDRMin', 'dRlg', 'dRlg', 'F')
    dataloader.AddVariable('lPhotonDRMax', 'maxdRlg', 'maxdRlg', 'F')

    # trees for training
    inputFile = r.TFile('{0}/output_combined_2016_flat.root'.format(inputFilesDir))
    sig_ggf = inputFile.Get('hzg_gluglu') 
    sig_vbf = inputFile.Get('hzg_vbf')
    sig_zh = inputFile.Get('hzg_zh')
    sig_wh = inputFile.Get('hzg_wh')
    sig_tth = inputFile.Get('hzg_tth')
    #bkg_zjets = inputFile.Get('zjets_m-50_amc') 
    bkg1 = inputFile.Get('zjets_m-50_amc') 
    #r.gROOT.cd()
    #bkg1 = bkg_zjets.CopyTree("vetoDY==0")
    bkg2 = inputFile.Get('zg_llg')

    #factory.AddSignalTree(sig_ggF, mcwei[0])
    #factory.AddBackgroundTree(bkg1, mcwei[1])
    dataloader.AddSignalTree(sig_ggf, mcwei[0])
    dataloader.AddSignalTree(sig_vbf, mcwei[1])
    dataloader.AddSignalTree(sig_zh, mcwei[2])
    dataloader.AddSignalTree(sig_wh, mcwei[3])
    dataloader.AddSignalTree(sig_tth, mcwei[4])
    dataloader.AddBackgroundTree(bkg1, mcwei[5])
    #dataloader.AddBackgroundTree(bkg2, mcwei[6])

    #factory.SetSignalWeightExpression('eventWeight*genWeight')
    #factory.SetBackgroundWeightExpression('eventWeight*genWeight')
    #factory.PrepareTrainingAndTestTree(r.TCut(''), r.TCut(''), 'SplitMode=Random:NormMode=NumEvents:!V')
    dataloader.SetSignalWeightExpression('eventWeight*genWeight')
    dataloader.SetBackgroundWeightExpression('eventWeight*genWeight')
    dataloader.PrepareTrainingAndTestTree(r.TCut(''), r.TCut(''), 'SplitMode=Random:NormMode=NumEvents:!V')

    print('booking the methods')

    if Use['BDTG']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDTG', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:BoostType=Grad:Shrinkage=0.10:UseBaggedGrad:GradBaggingFraction=0.5:nCuts=20:NNodesMax=5')

    if Use['BDT']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDT', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:nEventsMin=40:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=1:SeparationType=GiniIndex:nCuts=20')

    if Use['BDTRT']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDTRT', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:nEventsMin=40:MaxDepth=4:UseRandomisedTrees=True:BoostType=AdaBoost:AdaBoostBeta=1:SeparationType=GiniIndex:nCuts=20:NNodesMax=5')

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
