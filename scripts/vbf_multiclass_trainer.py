#!/usr/bin/env python

# based on TMVAClassification.C and modified for pyroot

import ROOT as r
from ROOT import TMVA as t

if __name__ == '__main__':
    inputFilesDir = 'data/step2_kin_bdt'
    outputWeightsDir = 'trained_bdts'

    print('setting up TMVA')

    # ggf, vbf, tth, zh, w+h, w-h, z+jets, zg_llg, tt2l2nu
    mcwei = [0.0007090, 0.0001082, 0.0001495, 0.0001910, 0.0001763, 0.0001148, 2.6446207, 0.4315552]

    outFileName = 'trained_bdts/vbf_multiclass_output_file.root'
    outputFile = r.TFile(outFileName, 'RECREATE')

    t.Tools.Instance() # what does this do ?????? 
    
    Use =   {
            'BDT': 0,
            'BDTG': 1,
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


    factory = t.Factory('vbf_multiclass_discr', outputFile, '!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=multiclass')
    factory.Print()
    
    t.gConfig().GetIONames().fWeightFileDir = outputWeightsDir
    dataloader = t.DataLoader(".")

    dataloader.AddVariable('dijetM', 'dijetM', 'dijetM', 'F')
    dataloader.AddVariable('zepp', 'zepp', 'zepp', 'F')
    dataloader.AddVariable('dijetDEta', 'dijetDEta', 'dijetDEta', 'F')
    dataloader.AddVariable('dijetDPhi', 'dijetDPhi', 'dijetDPhi', 'F')
    dataloader.AddVariable('llgJJDPhi', 'llgJJDPhi', 'llgJJDPhi', 'F')
    dataloader.AddVariable('jPhotonDRMin', 'jPhotonDRMin', 'jPhotonDRMin', 'F')
    dataloader.AddVariable('ptt', 'ptt', 'ptt', 'F')
    dataloader.AddVariable('jetOnePt', 'jetOnePt', 'jetOnePt', 'F')
    dataloader.AddVariable('jetTwoPt', 'jetTwoPt', 'jetTwoPt', 'F')
    dataloader.AddVariable('kin_bdt', 'kin_bdt', 'kin_bdt', 'F')

    # trees for training
    inputFile = r.TFile('{0}/output_combined_2016.root'.format(inputFilesDir))
    ggf = inputFile.Get('hzg_gluglu') 
    vbf = inputFile.Get('hzg_vbf')
    #sig_tth = inputFile.Get('hzg_tth')
    #sig_zh = inputFile.Get('hzg_zh')
    #sig_wplush = inputFile.Get('hzg_wplush')
    #sig_wminush = inputFile.Get('hzg_wminush')
    bkg1 = inputFile.Get('zjets_m-50_amc') 
    bkg2 = inputFile.Get('zg_llg')

    dataloader.AddTree(bkg1, 'bkg', mcwei[6])
    dataloader.AddTree(bkg2, 'bkg', mcwei[7])
    dataloader.AddTree(ggf, 'sig0', mcwei[0])
    dataloader.AddTree(vbf, 'sig1', mcwei[1])
   
    dataloader.SetWeightExpression('eventWeight*genWeight*isDijetTag', 'sig0')
    dataloader.SetWeightExpression('eventWeight*genWeight*isDijetTag', 'sig1')
    dataloader.SetWeightExpression('eventWeight*genWeight*isDijetTag', 'bkg')

    dataloader.PrepareTrainingAndTestTree(r.TCut(''), 'SplitMode=Random:NormMode=NumEvents:!V')

    print('booking the methods')

    if Use['BDTG']:
        factory.BookMethod(dataloader, t.Types.kBDT, 'BDTG', '!H:!V:IgnoreNegWeightsInTraining:NTrees=1000:BoostType=Grad:Shrinkage=0.10:UseBaggedGrad:GradBaggingFraction=0.5:nCuts=20:NNodesMax=5')

    if Use['MLP']:
        factory.BookMethod(dataloader, t.Types.kMLP, 'MLP', '!H:!V:NeuronType=tanh:NCycles=1000:HiddenLayers=N+5:TestRate=5:EstimatorType=MSE')

    print('training the methods')

    factory.TrainAllMethods()

    print('evaluating the methods')
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    outputFile.Close()

    print('wrote the output root file')
    print('TMVA training is done!')

    del factory
