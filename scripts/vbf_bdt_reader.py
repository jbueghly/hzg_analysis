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
                #2016: {'mmg': mc_16, 'eeg': mc_16},
                #2017: {'mmg': mc_17, 'eeg': mc_17},
                #2018: {'mmg': mc_18, 'eeg': mc_18} 
                }

    channels = ['mmg', 'eeg']
    periods = [2016, 2017, 2018]
    
    for period, channel in itertools.product(periods, channels):
        dijetDEta = array.array('f', [-999])
        dijetDPhi = array.array('f', [-999])
        llgJJDPhi = array.array('f', [-999])
        jPhotonDRMin = array.array('f', [-999])
        ptt = array.array('f', [-999]) 
        jetOnePt = array.array('f', [-999])
        jetTwoPt = array.array('f', [-999])
        kin_bdt = array.array('f', [-999])
        vbfPtBalance = array.array('f', [-999])
        photonZepp = array.array('f', [-999])
        
        kin_bdt_james = array.array('f', [-999])
        
        vbfWeightsFile = 'trained_bdts/vbf_bdt_combined_ming-yan_current.xml'
        vbf_reader = t.Reader("!Color:Silent")
 
        vbf_reader.AddVariable('dijetDEta', dijetDEta)   
        vbf_reader.AddVariable('dijetDPhi', dijetDPhi)   
        vbf_reader.AddVariable('llgJJDPhi', llgJJDPhi)   
        vbf_reader.AddVariable('jPhotonDRMin', jPhotonDRMin)   
        vbf_reader.AddVariable('ptt', ptt)   
        vbf_reader.AddVariable('jetOnePt', jetOnePt)   
        vbf_reader.AddVariable('jetTwoPt', jetTwoPt)   
        vbf_reader.AddVariable('kin_bdt', kin_bdt)   
        vbf_reader.AddVariable('vbfPtBalance', vbfPtBalance)   
        vbf_reader.AddVariable('photonZepp', photonZepp)   

        vbf_reader.BookMVA('BDT method', vbfWeightsFile)
        
        #vbfWeightsFileJames = 'trained_bdts/vbf_bdt_combined_james_current_half_signal_BDT.weights.xml'
        #vbfWeightsFileJames = 'trained_bdts/WPMingyanV2/vbf_bdt_combined_james_current_half_signal_BDT.weights.xml'
        #vbfWeightsFileJames = 'trained_bdts/golden_1/vbf_bdt_combined_james_current_half_signal_half_background_BDT.weights.xml'
        vbfWeightsFileJames = 'trained_bdts/vbf_bdt_combined_james_current_BDT.weights.xml'
        #vbfWeightsFileJames = 'trained_bdts/vbf_bdt_combined_james_current_all_samples_BDT.weights.xml'
        vbf_reader_james = t.Reader("!Color:Silent")
 
        vbf_reader_james.AddVariable('dijetDEta', dijetDEta)   
        vbf_reader_james.AddVariable('dijetDPhi', dijetDPhi)   
        vbf_reader_james.AddVariable('llgJJDPhi', llgJJDPhi)   
        vbf_reader_james.AddVariable('jPhotonDRMin', jPhotonDRMin)   
        vbf_reader_james.AddVariable('ptt', ptt)   
        vbf_reader_james.AddVariable('jetOnePt', jetOnePt)   
        vbf_reader_james.AddVariable('jetTwoPt', jetTwoPt)   
        vbf_reader_james.AddVariable('kin_bdt_james', kin_bdt_james)   
        vbf_reader_james.AddVariable('vbfPtBalance', vbfPtBalance)   
        vbf_reader_james.AddVariable('photonZepp', photonZepp)   

        vbf_reader_james.BookMVA('BDT method', vbfWeightsFileJames)
        
        datasets = samples[period][channel]
        if datasets == []:
            continue
        print('running over: {0}, {1}'.format(period, channel))
        inputFile = root_open('data/step2_kin_bdt/output_{0}_{1}.root'.format(channel, period))
        outputFile = root_open('data/step3_vbf_bdt/output_{0}_{1}.root'.format(channel, period), 'recreate')
    
        
        for dataset in tqdm(datasets):
            tree = inputFile[dataset]
            tree.create_buffer()
            outTree = Tree(dataset)
            outTree.set_buffer(tree._buffer, create_branches=True)
            outTree.create_branches({'vbf_bdt': 'F'})
            outTree.create_branches({'vbf_bdt_james': 'F'})
            for evt in tree:
                
                dijetDEta[0] = evt.dijetDEta
                dijetDPhi[0] = evt.dijetDPhi
                llgJJDPhi[0] = evt.llgJJDPhi
                jPhotonDRMin[0] = evt.jPhotonDRMin
                ptt[0] = evt.ptt
                jetOnePt[0] = evt.jetOnePt
                jetTwoPt[0] = evt.jetTwoPt
                kin_bdt[0] = evt.kin_bdt
                vbfPtBalance[0] = evt.vbfPtBalance
                photonZepp[0] = evt.photonZepp
                
                kin_bdt_james[0] = evt.kin_bdt_james

                bdt_score = -1.
                bdt_score_james = -1.

                if evt.isDijetTag:
                    bdt_score = vbf_reader.EvaluateMVA("BDT method")
                    bdt_score_james = vbf_reader_james.EvaluateMVA("BDT method")

                outTree.vbf_bdt = bdt_score
                outTree.vbf_bdt_james = bdt_score
                
                outTree.Fill()

            outTree.Write()
        
        outputFile.Close()
        inputFile.Close()
