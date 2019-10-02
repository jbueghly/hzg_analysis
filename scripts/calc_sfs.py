#!/usr/bin/env python

# calculate MC SFs 
import ROOT as r
from ROOT import TMVA as t
from rootpy.tree import Tree
from rootpy.io import root_open
import numpy as np
import pandas as pd
from tqdm import tqdm, trange
import itertools

if __name__ == '__main__':

    channels = ['mmg', 'eeg']

    #mc_16 = ['ttbar_inclusive', 'zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wplush', 'hzg_wminush', 'hzg_zh']
    mc_16 = ['zjets_m-50_amc_16', 'zg_llg_16', 'hzg_gluglu_M125_16', 'hzg_tth_M125_16', 'hzg_vbf_M125_16', 'hzg_wplush_M125_16', 'hzg_wminush_M125_16', 'hzg_zh_M125_16']
    muon_data_16 = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
                 'muon_2016F', 'muon_2016G', 'muon_2016H']
    electron_data_16 = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                     'electron_2016F', 'electron_2016G', 'electron_2016H']

    mc_17 = ['zjets_m-50_2017', 'hzg_gluglu_2017', 'hzg_tth_2017', 'hzg_vbf_2017', 'hzg_wplush_2017', 'hzg_wminush_2017', 'hzg_zh_2017'] 
    muon_data_17 = ['muon_2017B', 'muon_2017C', 'muon_2017D', 'muon_2017E', 'muon_2017F']
    electron_data_17 = ['electron_2017B', 'electron_2017C', 'electron_2017D', 'electron_2017E', 'electron_2017F'] 

    samples = {
                2016: {'mmg': mc_16 + muon_data_16, 'eeg': mc_16 + electron_data_16},
                2017: {'mmg': mc_17 + muon_data_17, 'eeg': mc_17 + electron_data_17} 
                }
 
    br_zg_m125 = 1.533e-3
    br_zll = 0.033658*3
    br_htautau = 0.06272
    pho_conv = 0.969

    # most updated Higgs values
    xsec = {'zjets_m-50_amc_16': 5943.2, 'zjets_m-50_2017': 5943.2, 'zg_llg_16': 117.864, 'ttbar_inclusive': 831.76, # these from MY
            'htautau_gluglu': 48.61/pho_conv, 'htautau_vbf': 3.766/pho_conv,
            'hzg_gluglu_M125_16': 48.61/pho_conv, 'hzg_tth_M125_16': 0.5071/pho_conv, 'hzg_vbf_M125_16': 3.766/pho_conv, 
            'hzg_wh_M125_16': 1.358/pho_conv, 'hzg_wplush_M125_16': 0.831/pho_conv, 'hzg_wminush_M125_16': 0.527/pho_conv,'hzg_zh_M125_16': 0.88/pho_conv,
            'hzg_gluglu_2017': 48.61/pho_conv, 'hzg_tth_2017': 0.5071/pho_conv, 'hzg_vbf_2017': 3.766/pho_conv, 
            'hzg_wh_2017': 1.358/pho_conv, 'hzg_wplus_2017': 0.831/pho_conv, 'hzg_wminus_2017': 0.527/pho_conv,'hzg_zh_2017': 0.88/pho_conv,
            'hzg_wplush_2017': 0.831/pho_conv, 'hzg_wminush_2017': 0.527/pho_conv,
            'muon_2016B': 1., 'muon_2016C': 1., 'muon_2016D': 1., 'muon_2016E': 1., 
            'muon_2016F': 1., 'muon_2016G': 1., 'muon_2016H': 1.,
            'muon_2017B': 1., 'muon_2017C': 1., 'muon_2017D': 1., 'muon_2017E': 1., 'muon_2017F': 1.,
            'electron_2016B': 1., 'electron_2016C': 1., 'electron_2016D': 1., 'electron_2016E': 1., 
            'electron_2016F': 1., 'electron_2016G': 1., 'electron_2016H': 1.,
            'electron_2017B': 1., 'electron_2017C': 1., 'electron_2017D': 1., 'electron_2017E': 1., 'electron_2017F': 1}
    
    br =   {'zjets_m-50_amc_16': 1., 'zjets_m-50_2017': 1., 'zg_llg_16': 1., 'ttbar_inclusive': 1., # these from MY
            'htautau_gluglu': br_htautau, 'htautau_vbf': br_htautau,
            'hzg_gluglu_M125_16': br_zg_m125*br_zll, 'hzg_tth_M125_16': br_zg_m125, 'hzg_vbf_M125_16': br_zg_m125*br_zll, 
            'hzg_wh_M125_16': br_zg_m125, 'hzg_wplush_M125_16': br_zg_m125, 'hzg_wminush_M125_16': br_zg_m125,'hzg_zh_M125_16': br_zg_m125,
            'hzg_gluglu_2017': br_zg_m125*br_zll, 'hzg_tth_2017': br_zg_m125*br_zll, 'hzg_vbf_2017': br_zg_m125*br_zll, 
            'hzg_wh_2017': br_zg_m125, 'hzg_wplus_2017': br_zg_m125, 'hzg_wminus_2017': br_zg_m125,'hzg_zh_2017': br_zg_m125,
            'hzg_wplush_2017': br_zg_m125, 'hzg_wminush_2017': br_zg_m125,
            'muon_2016B': 1., 'muon_2016C': 1., 'muon_2016D': 1., 'muon_2016E': 1., 
            'muon_2016F': 1., 'muon_2016G': 1., 'muon_2016H': 1.,
            'muon_2017B': 1., 'muon_2017C': 1., 'muon_2017D': 1., 'muon_2017E': 1., 'muon_2017F': 1., 
            'electron_2016B': 1., 'electron_2016C': 1., 'electron_2016D': 1., 'electron_2016E': 1., 
            'electron_2016F': 1., 'electron_2016G': 1., 'electron_2016H': 1.,    
            'electron_2017B': 1., 'electron_2017C': 1., 'electron_2017D': 1., 'electron_2017E': 1., 'electron_2017F': 1}

    periods = [2016, 2017]
    luminosity = {2016: 35.9e3, 2017: 44.98e3}

    for period, channel in itertools.product(periods, channels):
        datasets = samples[period][channel]
        if datasets == []:
            continue
        print('running over: {0}, {1}'.format(period, channel))
        inputFile = root_open('data/bltuples/output_{0}_{1}.root'.format(channel, period))
        outputFile = root_open('data/step1_sfs/output_{0}_{1}.root'.format(channel, period), 'recreate')

        for dataset in tqdm(datasets):
            tree = inputFile['tree_{0}'.format(dataset)]
            hist = inputFile['TotalEvents_{0}'.format(dataset)]
            tree.create_buffer()
            outTree = Tree(dataset)
            outTree.set_buffer(tree._buffer, create_branches=True)
            outTree.create_branches({'mc_sf': 'F'})

            # compute the MC scale factor
            n_gen = inputFile['TotalEvents_{0}'.format(dataset)].GetBinContent(1)
            n_neg = inputFile['TotalEvents_{0}'.format(dataset)].GetBinContent(30)
            sf = luminosity[period]*xsec[dataset]*br[dataset]/(float(n_gen) - 2.*float(n_neg))

            for evt in tree:
                run = evt.runNumber
                lumi = evt.lumiSection
                event = evt.evtNumber
                outTree.mc_sf = sf
                if 'zjets' in dataset:
                    if evt.vetoDY:
                        continue

                outTree.Fill()
            outTree.Write()
            hist.Write()
        outputFile.Close()
        inputFile.Close()
