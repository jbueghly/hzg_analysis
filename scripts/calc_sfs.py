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

    channels = ['mumug', 'elelg']

    mc_16 = ['ttbar_inclusive', 'zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wplush', 'hzg_wminush', 'hzg_zh']
    muon_data_16 = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
                 'muon_2016F', 'muon_2016G', 'muon_2016H']
    electron_data_16 = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                     'electron_2016F', 'electron_2016G', 'electron_2016H']

    mc_17 = [] # not yet available
    muon_data_17 = ['muon_2017B', 'muon_2017C', 'muon_2017D', 'muon_2017E', 'muon_2017F']
    electron_data_17 = [] # not yet available

    samples = {
                2016: {'mumug': mc_16 + muon_data_16, 'elelg': mc_16 + electron_data_16},
                2017: {'mumug': mc_17 + muon_data_17, 'elelg': mc_17 + electron_data_17} 
                }
 
    br_zg_m125 = 1.533e-3
    br_zll = 0.033658*3
    pho_conv = 0.969

    # most updated Higgs values
    xsec = {'zjets_m-50_amc': 5943.2, 'zg_llg': 117.864, 'ttbar_inclusive': 831.76, # these from MY
            'hzg_gluglu': 48.61/pho_conv, 'hzg_tth': 0.5071/pho_conv, 'hzg_vbf': 3.766/pho_conv, 
            'hzg_wh': 1.358/pho_conv, 'hzg_wplush': 0.831/pho_conv, 'hzg_wminush': 0.527/pho_conv,'hzg_zh': 0.88/pho_conv,
            'muon_2016B': 1., 'muon_2016C': 1., 'muon_2016D': 1., 'muon_2016E': 1., 
            'muon_2016F': 1., 'muon_2016G': 1., 'muon_2016H': 1.,
            'muon_2017B': 1., 'muon_2017C': 1., 'muon_2017D': 1., 'muon_2017E': 1., 'muon_2017F': 1.,
            'electron_2016B': 1., 'electron_2016C': 1., 'electron_2016D': 1., 'electron_2016E': 1., 
            'electron_2016F': 1., 'electron_2016G': 1., 'electron_2016H': 1.,
            'electron_2017B': 1., 'electron_2017C': 1., 'electron_2017D': 1., 'electron_2017E': 1., 'electron_2017F': 1}
    
    br =   {'zjets_m-50_amc': 1., 'zg_llg': 1., 'ttbar_inclusive': 1., # these from MY
            'hzg_gluglu': br_zg_m125*br_zll, 'hzg_tth': br_zg_m125, 'hzg_vbf': br_zg_m125*br_zll, 
            'hzg_wh': br_zg_m125, 'hzg_wplush': br_zg_m125, 'hzg_wminush': br_zg_m125,'hzg_zh': br_zg_m125,
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
        outputFile = root_open('data/step1_phores/output_{0}_{1}.root'.format(channel, period), 'recreate')

        for dataset in tqdm(datasets):
            tree = inputFile['tree_{0}'.format(dataset)]
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
                if dataset == 'zjets_m-50_amc':
                    if evt.vetoDY:
                        continue

                outTree.Fill()
            outTree.Write()
        outputFile.Close()
        inputFile.Close()
