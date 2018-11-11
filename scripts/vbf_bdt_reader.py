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
    #outputFile = root_open('data/step2_bdt/output_mumug_2016_flat.root')

    vbfWeightsFile = 'trained_bdts/vbf_bdt_ming-yan.weights.xml'

    ## VBF BDT
    vbf_reader = t.Reader("!Color:Silent")

    dijetM = array.array('f', [-999])
    absZepp = array.array('f', [-999])
    dijetDEta = array.array('f', [-999])
    dijetDPhi = array.array('f', [-999])
    llgJJDPhi = array.array('f', [-999])
    jPhotonDRMin = array.array('f', [-999])
    ptt = array.array('f', [-999]) 
    jetOnePt = array.array('f', [-999])
    jetTwoPt = array.array('f', [-999])
    kin_bdt = array.array('f', [-999])


    vbf_reader.AddVariable('mjj', dijetM)  
    vbf_reader.AddVariable('absZeppen', absZepp)  
    vbf_reader.AddVariable('absdEta_jj', dijetDEta)   
    vbf_reader.AddVariable('absdPhi_jj', dijetDPhi)   
    vbf_reader.AddVariable('absdPhi_Zgjj', llgJJDPhi)   
    vbf_reader.AddVariable('dR_phojet', jPhotonDRMin)   
    vbf_reader.AddVariable('ZgPTt', ptt)   
    vbf_reader.AddVariable('VBFPt1', jetOnePt)   
    vbf_reader.AddVariable('VBFPt2', jetTwoPt)   
    vbf_reader.AddVariable('HZgMVA', kin_bdt)   

    vbf_reader.BookMVA('BDTRT method', vbfWeightsFile)

    for channel in channels:
        inputFile = root_open('data/step2_kin_bdt/output_{0}_2016_flat.root'.format(channel))
        outputFile = root_open('data/step3_vbf_bdt/output_{0}_2016_flat.root'.format(channel), 'recreate')
        #inputFile = root_open('data/step2_kin_bdt_james/output_{0}_2016_flat.root'.format(channel))
        #outputFile = root_open('data/step3_vbf_bdt_james/output_{0}_2016_flat.root'.format(channel), 'recreate')
        datasets = data_dict[channel]
        
        for dataset in tqdm(datasets):
            tree = inputFile[dataset]
            tree.create_buffer()
            outTree = Tree(dataset)
            outTree.set_buffer(tree._buffer, create_branches=True)
            outTree.create_branches({'vbf_bdt': 'F'})
            for evt in tree:
                dijetM[0] = evt.dijetM
                absZepp[0] = abs(evt.zepp)
                dijetDEta[0] = evt.dijetDEta
                dijetDPhi[0] = evt.dijetDPhi
                llgJJDPhi[0] = evt.llgJJDPhi
                jPhotonDRMin[0] = evt.jPhotonDRMin
                ptt[0] = evt.ptt
                jetOnePt[0] = evt.jetOnePt
                jetTwoPt[0] = evt.jetTwoPt
                kin_bdt[0] = evt.kin_bdt
                bdt_score = -1.
                if evt.isDijetTag:
                    bdt_score = vbf_reader.EvaluateMVA("BDTRT method")
                outTree.vbf_bdt = bdt_score
                outTree.Fill()
            outTree.Write()
        
        outputFile.Close()
        inputFile.Close()
