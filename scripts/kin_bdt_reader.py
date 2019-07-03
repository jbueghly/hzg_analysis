#!/usr/bin/env python

# based on TMVAClassificationApplication.C and modified for pyroot

import ROOT as r
from ROOT import TMVA as t
from rootpy.tree import Tree
from rootpy.io import root_open
import array 
import numpy as np
from tqdm import tqdm, trange
import itertools

if __name__ == '__main__':

    mc_16 = ['ttbar_inclusive', 'zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wplush', 'hzg_wminush', 'hzg_zh']
    muon_data_16 = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
                 'muon_2016F', 'muon_2016G', 'muon_2016H']
    electron_data_16 = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                     'electron_2016F', 'electron_2016G', 'electron_2016H']

    mc_17 = ['hzg_gluglu_2017', 'hzg_tth_2017', 'hzg_vbf_2017', 'hzg_wplus_2017', 'hzg_wminus_2017', 'hzg_zh_2017'] # not yet available
    muon_data_17 = ['muon_2017B', 'muon_2017C', 'muon_2017D', 'muon_2017E', 'muon_2017F']
    electron_data_17 = [] # not yet available

    samples = {
                2016: {'mumug': mc_16 + muon_data_16, 'elelg': mc_16 + electron_data_16},
                #2017: {'mumug': mc_17 + muon_data_17, 'elelg': mc_17 + electron_data_17} 
                2017: {'mumug': mc_17 + muon_data_17, 'elelg': electron_data_17} 
                }

    kinWeightsFile = 'trained_bdts/discr_BDT.weights.xml'

    # kinematic BDT
    kin_reader = t.Reader("!Color:Silent")
 
    zgLittleThetaJames = array.array('f', [-999])
    zgBigThetaJames = array.array('f', [-999])
    llgPtOverM = array.array('f', [-999])
    leptonOneEta = array.array('f', [-999])
    leptonTwoEta = array.array('f', [-999])
    photonOneEta = array.array('f', [-999])
    zgPhiJames = array.array('f', [-999])
    photonOneR9 = array.array('f', [-999])
    photonOneMVA = array.array('f', [-999])
    lPhotonDRMin = array.array('f', [-999])
    lPhotonDRMax = array.array('f', [-999])

    kin_reader.AddVariable('zgLittleThetaJames', zgLittleThetaJames)
    kin_reader.AddVariable('zgBigThetaJames', zgBigThetaJames)
    kin_reader.AddVariable('llgPtOverM', llgPtOverM)
    kin_reader.AddVariable('leptonOneEta', leptonOneEta)
    kin_reader.AddVariable('leptonTwoEta', leptonTwoEta)
    kin_reader.AddVariable('photonOneEta', photonOneEta)
    kin_reader.AddVariable('zgPhiJames', zgPhiJames)
    kin_reader.AddVariable('photonOneR9', photonOneR9)
    kin_reader.AddVariable('photonOneMVA', photonOneMVA)
    kin_reader.AddVariable('lPhotonDRMin', lPhotonDRMin)
    kin_reader.AddVariable('lPhotonDRMax', lPhotonDRMax)
 
    kin_reader.BookMVA('BDT method', kinWeightsFile)
    
    channels = ['mumug', 'elelg']
    periods = [2016, 2017]
    
    for period, channel in itertools.product(periods, channels):
        datasets = samples[period][channel]
        if datasets == []:
            continue
        print('running over: {0}, {1}'.format(period, channel))
        inputFile = root_open('data/step1_sfs/output_{0}_{1}.root'.format(channel, period))
        outputFile = root_open('data/step2_kin_bdt/output_{0}_{1}.root'.format(channel, period), 'recreate')

        for dataset in tqdm(datasets):
            tree = inputFile[dataset]
            tree.create_buffer()
            outTree = Tree(dataset)
            outTree.set_buffer(tree._buffer, create_branches=True)
            outTree.create_branches({'kin_bdt': 'F'})
            for evt in tree:

                zgLittleThetaJames[0] = evt.zgLittleThetaJames
                zgBigThetaJames[0] = evt.zgBigThetaJames
                llgPtOverM[0] = evt.llgPtOverM
                leptonOneEta[0] = evt.leptonOneEta
                leptonTwoEta[0] = evt.leptonTwoEta
                photonOneEta[0] = evt.photonOneEta
                zgPhiJames[0] = evt.zgPhiJames
                photonOneR9[0] = evt.photonOneR9
                photonOneMVA[0] = evt.photonOneMVA
                lPhotonDRMin[0] = evt.lPhotonDRMin
                lPhotonDRMax[0] = evt.lPhotonDRMax

                bdt_score = kin_reader.EvaluateMVA('BDT method')
                outTree.kin_bdt = bdt_score
                outTree.Fill()

            outTree.Write()

        outputFile.Close()
        inputFile.Close()

