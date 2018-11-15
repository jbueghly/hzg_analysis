#!/usr/bin/env python

# based on TMVAClassificationApplication.C and modified for pyroot

import ROOT as r
from ROOT import TMVA as t
from rootpy.tree import Tree
from rootpy.io import root_open
import array 
import numpy as np
from tqdm import tqdm, trange

if __name__ == '__main__':

    channels = ['mumug', 'elelg']

    #mc = ['ttbar_inclusive', 'zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wh', 'hzg_zh']
    mc = ['zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wh', 'hzg_zh']
    #mc = ['hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wh', 'hzg_zh']
    muon_data = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
                 'muon_2016F', 'muon_2016G', 'muon_2016H']
    electron_data = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                     'electron_2016F', 'electron_2016G', 'electron_2016H']

    #datasets = ['zjets_m-50_amc', 'zg_llg', 
    #            'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wh', 'hzg_zh',
    #            'muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
    #            'muon_2016F', 'muon_2016G', 'muon_2016H']
    
    data_dict = {'mumug': mc + muon_data, 'elelg': mc + electron_data}

    #inputFile = root_open('data/step1_phores/output_mumug_2016_flat.root')
    #outputFile = root_open('data/step2_kin_bdt/output_mumug_2016_flat.root', 'recreate')
    
    kinWeightsFile = 'trained_bdts/kin_bdt_ming-yan.weights.xml'
    #kinWeightsFile = 'trained_bdts/discr_BDTRT.weights.xml'

    # kinematic BDT
    kin_reader = t.Reader("!Color:Silent")

    zgLittleTheta = array.array('f', [-999])
    zgBigTheta = array.array('f', [-999])
    llgPtOverM = array.array('f', [-999])
    leptonOneEta = array.array('f', [-999])
    leptonTwoEta = array.array('f', [-999])
    photonOneEta = array.array('f', [-999])
    zgPhi = array.array('f', [-999])
    photonOneR9 = array.array('f', [-999])
    photonOneMVA = array.array('f', [-999])
    phores = array.array('f', [-999])
    lPhotonDRMin = array.array('f', [-999])
    lPhotonDRMax = array.array('f', [-999])

    kin_reader.AddVariable('costheta', zgLittleTheta)
    kin_reader.AddVariable('cosTheta', zgBigTheta)
    kin_reader.AddVariable('mllgptdmllg', llgPtOverM)
    kin_reader.AddVariable('lepEta1', leptonOneEta)
    kin_reader.AddVariable('lepEta2', leptonTwoEta)
    kin_reader.AddVariable('phoEta', photonOneEta)
    kin_reader.AddVariable('Phi', zgPhi)
    kin_reader.AddVariable('phoR9', photonOneR9)
    kin_reader.AddVariable('phoMVA', photonOneMVA)
    kin_reader.AddVariable('phores', phores)
    kin_reader.AddVariable('dRlg', lPhotonDRMin)
    kin_reader.AddVariable('maxdRlg', lPhotonDRMax)
    
    kin_reader.BookMVA('BDTRT method', kinWeightsFile)
    
    for channel in channels:
        print('running over {0} datasets'.format(channel))
        inputFile = root_open('data/step1_phores/output_{0}_2016_flat.root'.format(channel))
        outputFile = root_open('data/step2_kin_bdt/output_{0}_2016_flat.root'.format(channel), 'recreate')
        #outputFile = root_open('data/step2_kin_bdt_james/output_{0}_2016_flat.root'.format(channel), 'recreate')
        datasets = data_dict[channel]
    
        for dataset in tqdm(datasets):
            tree = inputFile[dataset]
            tree.create_buffer()
            outTree = Tree(dataset)
            outTree.set_buffer(tree._buffer, create_branches=True)
            outTree.create_branches({'kin_bdt': 'F'})
            for evt in tree:
                zgLittleTheta[0] = evt.zgLittleTheta
                zgBigTheta[0] = evt.zgBigTheta
                llgPtOverM[0] = evt.llgPtOverM
                leptonOneEta[0] = evt.leptonOneEta
                leptonTwoEta[0] = evt.leptonTwoEta
                photonOneEta[0] = evt.photonOneEta
                zgPhi[0] = evt.zgPhi
                photonOneR9[0] = evt.photonOneR9
                photonOneMVA[0] = evt.photonOneMVA
                phores[0] = evt.phores
                lPhotonDRMin[0] = evt.lPhotonDRMin
                lPhotonDRMax[0] = evt.lPhotonDRMax
                #zgLittleTheta[0] = evt.costheta
                #zgBigTheta[0] = evt.cosTheta
                #llgPtOverM[0] = evt.mllgptdmllg
                #leptonOneEta[0] = evt.lepEta1
                #leptonTwoEta[0] = evt.lepEta2
                #photonOneEta[0] = evt.phoEta
                #zgPhi[0] = evt.Phi
                #photonOneR9[0] = evt.phoR9
                #photonOneMVA[0] = evt.photonOneMVA
                #phores[0] = evt.phores
                #lPhotonDRMin[0] = evt.dRlg
                #lPhotonDRMax[0] = evt.maxdRlg
                bdt_score = kin_reader.EvaluateMVA('BDTRT method')
                outTree.kin_bdt = bdt_score
                outTree.Fill()
            outTree.Write()

        outputFile.Close()
        inputFile.Close()

