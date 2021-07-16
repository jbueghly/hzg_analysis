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

    mc_16 = ['zjets_M50_2016', 'zg_llg_2016', 'zg_ewk_2016', 'ttjets_2016',
             'hzg_gluglu_M120_2016', 'hzg_tth_M120_2016', 'hzg_vbf_M120_2016', 'hzg_wplush_M120_2016', 'hzg_wminush_M120_2016', 'hzg_zh_M120_2016',
             'hzg_gluglu_M125_2016', 'hzg_tth_M125_2016', 'hzg_vbf_M125_2016', 'hzg_wplush_M125_2016', 'hzg_wminush_M125_2016', 'hzg_zh_M125_2016',
             'hzg_gluglu_M130_2016', 'hzg_tth_M130_2016', 'hzg_vbf_M130_2016', 'hzg_wplush_M130_2016', 'hzg_wminush_M130_2016', 'hzg_zh_M130_2016',
             'hmumu_gluglu_M120_2016', 'hmumu_tth_M120_2016', 'hmumu_vbf_M120_2016', 'hmumu_wplush_M120_2016', 'hmumu_wminush_M120_2016', 'hmumu_zh_M120_2016',
             'hmumu_gluglu_M125_2016', 'hmumu_tth_M125_2016', 'hmumu_vbf_M125_2016', 'hmumu_wplush_M125_2016', 'hmumu_wminush_M125_2016', 'hmumu_zh_M125_2016',
             'hmumu_gluglu_M130_2016', 'hmumu_tth_M130_2016', 'hmumu_vbf_M130_2016', 'hmumu_wplush_M130_2016', 'hmumu_wminush_M130_2016', 'hmumu_zh_M130_2016'
             ]
    muon_data_16 = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
                 'muon_2016F', 'muon_2016G', 'muon_2016H']
    electron_data_16 = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                     'electron_2016F', 'electron_2016G', 'electron_2016H']

    mc_17 = ['zjets_M50_2017', 'zg_llg_2017', 'zg_ewk_2017', 'ttjets_2017',
             'hzg_gluglu_M120_2017', 'hzg_tth_M120_2017', 'hzg_vbf_M120_2017', 'hzg_wplush_M120_2017', 'hzg_wminush_M120_2017', 'hzg_zh_M120_2017',
             'hzg_gluglu_M125_2017', 'hzg_tth_M125_2017', 'hzg_vbf_M125_2017', 'hzg_wplush_M125_2017', 'hzg_wminush_M125_2017', 'hzg_zh_M125_2017',
             'hzg_gluglu_M130_2017', 'hzg_tth_M130_2017', 'hzg_vbf_M130_2017', 'hzg_wplush_M130_2017', 'hzg_wminush_M130_2017', 'hzg_zh_M130_2017',
             'hmumu_gluglu_M120_2017', 'hmumu_tth_M120_2017', 'hmumu_vbf_M120_2017', 'hmumu_wplush_M120_2017', 'hmumu_wminush_M120_2017', 'hmumu_zh_M120_2017',
             'hmumu_gluglu_M125_2017', 'hmumu_tth_M125_2017', 'hmumu_vbf_M125_2017', 'hmumu_wplush_M125_2017', 'hmumu_wminush_M125_2017', 'hmumu_zh_M125_2017',
             'hmumu_gluglu_M130_2017', 'hmumu_tth_M130_2017', 'hmumu_vbf_M130_2017', 'hmumu_wplush_M130_2017', 'hmumu_wminush_M130_2017', 'hmumu_zh_M130_2017'
            ] 
    muon_data_17 = ['muon_2017B', 'muon_2017C', 'muon_2017D', 'muon_2017E', 'muon_2017F']
    electron_data_17 = ['electron_2017B', 'electron_2017C', 'electron_2017D', 'electron_2017E', 'electron_2017F'] 
    
    mc_18 = ['zjets_M50_2018', 'zg_llg_2018', 'zg_ewk_2018', 'ttjets_2018',
             'hzg_gluglu_M120_2018', 'hzg_tth_M120_2018', 'hzg_vbf_M120_2018', 'hzg_wplush_M120_2018', 'hzg_wminush_M120_2018', 'hzg_zh_M120_2018',
             'hzg_gluglu_M125_2018', 'hzg_tth_M125_2018', 'hzg_vbf_M125_2018', 'hzg_wplush_M125_2018', 'hzg_wminush_M125_2018', 'hzg_zh_M125_2018',
             'hzg_gluglu_M130_2018', 'hzg_tth_M130_2018', 'hzg_vbf_M130_2018', 'hzg_wplush_M130_2018', 'hzg_wminush_M130_2018', 'hzg_zh_M130_2018',
             'hmumu_gluglu_M120_2018', 'hmumu_tth_M120_2018', 'hmumu_vbf_M120_2018', 'hmumu_wplush_M120_2018', 'hmumu_wminush_M120_2018', 'hmumu_zh_M120_2018',
             'hmumu_gluglu_M125_2018', 'hmumu_tth_M125_2018', 'hmumu_vbf_M125_2018', 'hmumu_wplush_M125_2018', 'hmumu_wminush_M125_2018', 'hmumu_zh_M125_2018',
             'hmumu_gluglu_M130_2018', 'hmumu_tth_M130_2018', 'hmumu_vbf_M130_2018', 'hmumu_wplush_M130_2018', 'hmumu_wminush_M130_2018', 'hmumu_zh_M130_2018'
            ] 
    muon_data_18 = ['muon_2018A', 'muon_2018B', 'muon_2018C', 'muon_2018D']
    electron_data_18 = ['electron_2018A', 'electron_2018B', 'electron_2018C', 'electron_2018D'] 

    samples = {
                2016: {'mmg': mc_16 + muon_data_16, 'eeg': mc_16 + electron_data_16},
                2017: {'mmg': mc_17 + muon_data_17, 'eeg': mc_17 + electron_data_17},
                2018: {'mmg': mc_18 + muon_data_18, 'eeg': mc_18 + electron_data_18} 
                }
 
    channels = ['mmg', 'eeg']
    periods = [2016, 2017, 2018]
    
    for period, channel in itertools.product(periods, channels):
 
        zgLittleTheta = array.array('f', [-999])
        zgBigTheta = array.array('f', [-999])
        llgPtOverM = array.array('f', [-999])
        leptonOneEta = array.array('f', [-999])
        leptonTwoEta = array.array('f', [-999])
        photonEta = array.array('f', [-999])
        zgPhi = array.array('f', [-999])
        photonMVA = array.array('f', [-999])
        corrPhotonMVA = array.array('f', [-999])
        photonERes = array.array('f', [-999])
        lPhotonDRMin = array.array('f', [-999])
        lPhotonDRMax = array.array('f', [-999])
        
        kinWeightsFile = 'trained_bdts/kin_bdt_combined_ming-yan_current.xml'
        kin_reader = t.Reader("!Color:Silent")

        kin_reader.AddVariable('zgLittleTheta', zgLittleTheta)
        kin_reader.AddVariable('zgBigTheta', zgBigTheta)
        kin_reader.AddVariable('llgPtOverM', llgPtOverM)
        kin_reader.AddVariable('leptonOneEta', leptonOneEta)
        kin_reader.AddVariable('leptonTwoEta', leptonTwoEta)
        kin_reader.AddVariable('photonEta', photonEta)
        kin_reader.AddVariable('zgPhi', zgPhi)
        kin_reader.AddVariable('photonMVA', corrPhotonMVA)
        kin_reader.AddVariable('photonERes', photonERes)
        kin_reader.AddVariable('lPhotonDRMin', lPhotonDRMin)
        kin_reader.AddVariable('lPhotonDRMax', lPhotonDRMax)
     
        kin_reader.BookMVA('BDT method', kinWeightsFile)
        
        kinWeightsFileJames = 'trained_bdts/kin_bdt_combined_james_current_BDT.weights.xml'
        kin_reader_james = t.Reader("!Color:Silent")

        kin_reader_james.AddVariable('zgLittleTheta', zgLittleTheta)
        kin_reader_james.AddVariable('zgBigTheta', zgBigTheta)
        kin_reader_james.AddVariable('llgPtOverM', llgPtOverM)
        kin_reader_james.AddVariable('leptonOneEta', leptonOneEta)
        kin_reader_james.AddVariable('leptonTwoEta', leptonTwoEta)
        kin_reader_james.AddVariable('photonEta', photonEta)
        kin_reader_james.AddVariable('zgPhi', zgPhi)
        kin_reader_james.AddVariable('corrPhotonMVA', corrPhotonMVA)
        kin_reader_james.AddVariable('photonERes', photonERes)
        kin_reader_james.AddVariable('lPhotonDRMin', lPhotonDRMin)
        kin_reader_james.AddVariable('lPhotonDRMax', lPhotonDRMax)
     
        kin_reader_james.BookMVA('BDT method', kinWeightsFileJames)

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
            outTree.create_branches({'kin_bdt_james': 'F'})
            for evt in tree:
                
                zgLittleTheta[0] = evt.zgLittleTheta
                zgBigTheta[0] = evt.zgBigTheta
                llgPtOverM[0] = evt.llgPtOverM
                leptonOneEta[0] = evt.leptonOneEta
                leptonTwoEta[0] = evt.leptonTwoEta
                photonEta[0] = evt.photonEta
                zgPhi[0] = evt.zgPhi
                corrPhotonMVA[0] = evt.corrPhotonMVA
                #photonMVA[0] = evt.photonMVA
                photonERes[0] = evt.photonERes
                lPhotonDRMin[0] = evt.lPhotonDRMin
                lPhotonDRMax[0] = evt.lPhotonDRMax

                bdt_score = kin_reader.EvaluateMVA('BDT method')
                bdt_score_james = kin_reader_james.EvaluateMVA('BDT method')
                
                outTree.kin_bdt = bdt_score
                outTree.kin_bdt_james = bdt_score_james
                
                outTree.Fill()

            outTree.Write()

        outputFile.Close()
        inputFile.Close()

