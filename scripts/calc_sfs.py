#!/usr/bin/env python

# calculate MC SFs 
import ROOT as r
from ROOT import TMVA as t
from rootpy.tree import Tree
from rootpy.io import root_open
import uproot as ur
import numpy as np
import pandas as pd
from tqdm import tqdm, trange
import itertools
import pickle
import os

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
 
    br_hzg_m120 = 1.100e-3
    br_hzg_m125 = 1.533e-3
    br_hzg_m130 = 1.941e-3
    br_hmumu_m120 = 2.423e-4
    br_hmumu_m125 = 2.176e-4
    br_hmumu_m130 = 1.877e-4
    br_zll = 0.033658*3
    br_htautau = 0.06272
    pho_conv_16 = 0.969
    pho_conv_17 = 0.97
    pho_conv_18 = 0.97

    # most updated Higgs values
    xsec = {'zjets_M50_2016': 6225.42, 'zjets_M50_2017': 6225.42, 'zjets_M50_2018': 6225.42, 
            'zg_llg_2016': 117.864/pho_conv_16, 'zg_llg_2017': 117.864/pho_conv_17, 'zg_llg_2018': 117.864/pho_conv_18, 
            'zg_ewk_2016': 0.1097, 'zg_ewk_2017': 0.1097, 'zg_ewk_2018': 0.1097,
            'ttjets_2016': 831.76, 'ttjets_2017': 831.76, 'ttjets_2018': 831.76, # these from MY
            #'htautau_gluglu': 48.61/pho_conv, 'htautau_vbf': 3.766/pho_conv,

            'hzg_gluglu_M120_2016': 52.22/pho_conv_16, 'hzg_tth_M120_2016': 0.5697/pho_conv_16, 'hzg_vbf_M120_2016': 3.935/pho_conv_16, 
            'hzg_wplush_M120_2016': 0.9558/pho_conv_16, 'hzg_wminush_M120_2016': 0.6092/pho_conv_16, 'hzg_zh_M120_2016': 0.9939/pho_conv_16, 
            'hzg_gluglu_M120_2017': 52.22/pho_conv_17, 'hzg_tth_M120_2017': 0.5697/pho_conv_17, 'hzg_vbf_M120_2017': 3.935/pho_conv_17, 
            'hzg_wplush_M120_2017': 0.9558/pho_conv_17, 'hzg_wminush_M120_2017': 0.6092/pho_conv_17, 'hzg_zh_M120_2017': 0.9939/pho_conv_17,
            'hzg_gluglu_M120_2018': 52.22/pho_conv_18, 'hzg_tth_M120_2018': 0.5697/pho_conv_18, 'hzg_vbf_M120_2018': 3.935/pho_conv_18, 
            'hzg_wplush_M120_2018': 0.9558/pho_conv_18, 'hzg_wminush_M120_2018': 0.6092/pho_conv_18, 'hzg_zh_M120_2018': 0.9939/pho_conv_18, 

            'hzg_gluglu_M125_2016': 48.58/pho_conv_16, 'hzg_tth_M125_2016': 0.5071/pho_conv_16, 'hzg_vbf_M125_2016': 3.782/pho_conv_16, 
            'hzg_wplush_M125_2016': 0.84/pho_conv_16, 'hzg_wminush_M125_2016': 0.532/pho_conv_16, 'hzg_zh_M125_2016': 0.8839/pho_conv_16,
            'hzg_gluglu_M125_2017': 48.58/pho_conv_17, 'hzg_tth_M125_2017': 0.5071/pho_conv_17, 'hzg_vbf_M125_2017': 3.782/pho_conv_17, 
            'hzg_wplush_M125_2017': 0.84/pho_conv_17, 'hzg_wminush_M125_2017': 0.532/pho_conv_17, 'hzg_zh_M125_2017': 0.8839/pho_conv_17,
            'hzg_gluglu_M125_2018': 48.58/pho_conv_18, 'hzg_tth_M125_2018': 0.5071/pho_conv_18, 'hzg_vbf_M125_2018': 3.782/pho_conv_18, 
            'hzg_wplush_M125_2018': 0.84/pho_conv_18, 'hzg_wminush_M125_2018': 0.532/pho_conv_18, 'hzg_zh_M125_2018': 0.8839/pho_conv_18,
            
            'hzg_gluglu_M130_2016': 45.31/pho_conv_16, 'hzg_tth_M130_2016': 0.4539/pho_conv_16, 'hzg_vbf_M130_2016': 3.637/pho_conv_16, 
            'hzg_wplush_M130_2016': 0.7414/pho_conv_16, 'hzg_wminush_M130_2016': 0.4676/pho_conv_16, 'hzg_zh_M130_2016': 0.7899/pho_conv_16, 
            'hzg_gluglu_M130_2017': 45.31/pho_conv_17, 'hzg_tth_M130_2017': 0.4539/pho_conv_17, 'hzg_vbf_M130_2017': 3.637/pho_conv_17, 
            'hzg_wplush_M130_2017': 0.7414/pho_conv_17, 'hzg_wminush_M130_2017': 0.4676/pho_conv_17, 'hzg_zh_M130_2017': 0.7899/pho_conv_17,
            'hzg_gluglu_M130_2018': 45.31/pho_conv_18, 'hzg_tth_M130_2018': 0.4539/pho_conv_18, 'hzg_vbf_M130_2018': 3.637/pho_conv_18, 
            'hzg_wplush_M130_2018': 0.7414/pho_conv_18, 'hzg_wminush_M130_2018': 0.4676/pho_conv_18, 'hzg_zh_M130_2018': 0.7899/pho_conv_18,
            
            'hmumu_gluglu_M120_2016': 52.22, 'hmumu_tth_M120_2016': 0.5697, 'hmumu_vbf_M120_2016': 3.935, 
            'hmumu_wplush_M120_2016': 0.9558, 'hmumu_wminush_M120_2016': 0.6092, 'hmumu_zh_M120_2016': 0.9939, 
            'hmumu_gluglu_M120_2017': 52.22, 'hmumu_tth_M120_2017': 0.5697, 'hmumu_vbf_M120_2017': 3.935, 
            'hmumu_wplush_M120_2017': 0.9558, 'hmumu_wminush_M120_2017': 0.6092, 'hmumu_zh_M120_2017': 0.9939,
            'hmumu_gluglu_M120_2018': 52.22, 'hmumu_tth_M120_2018': 0.5697, 'hmumu_vbf_M120_2018': 3.935, 
            'hmumu_wplush_M120_2018': 0.9558, 'hmumu_wminush_M120_2018': 0.6092, 'hmumu_zh_M120_2018': 0.9939, 

            'hmumu_gluglu_M125_2016': 48.58, 'hmumu_tth_M125_2016': 0.5071, 'hmumu_vbf_M125_2016': 3.782, 
            'hmumu_wplush_M125_2016': 0.84, 'hmumu_wminush_M125_2016': 0.532, 'hmumu_zh_M125_2016': 0.8839,
            'hmumu_gluglu_M125_2017': 48.58, 'hmumu_tth_M125_2017': 0.5071, 'hmumu_vbf_M125_2017': 3.782, 
            'hmumu_wplush_M125_2017': 0.84, 'hmumu_wminush_M125_2017': 0.532, 'hmumu_zh_M125_2017': 0.8839,
            'hmumu_gluglu_M125_2018': 48.58, 'hmumu_tth_M125_2018': 0.5071, 'hmumu_vbf_M125_2018': 3.782, 
            'hmumu_wplush_M125_2018': 0.84, 'hmumu_wminush_M125_2018': 0.532, 'hmumu_zh_M125_2018': 0.8839,
            
            'hmumu_gluglu_M130_2016': 45.31, 'hmumu_tth_M130_2016': 0.4539, 'hmumu_vbf_M130_2016': 3.637, 
            'hmumu_wplush_M130_2016': 0.7414, 'hmumu_wminush_M130_2016': 0.4676, 'hmumu_zh_M130_2016': 0.7899, 
            'hmumu_gluglu_M130_2017': 45.31, 'hmumu_tth_M130_2017': 0.4539, 'hmumu_vbf_M130_2017': 3.637, 
            'hmumu_wplush_M130_2017': 0.7414, 'hmumu_wminush_M130_2017': 0.4676, 'hmumu_zh_M130_2017': 0.7899,
            'hmumu_gluglu_M130_2018': 45.31, 'hmumu_tth_M130_2018': 0.4539, 'hmumu_vbf_M130_2018': 3.637, 
            'hmumu_wplush_M130_2018': 0.7414, 'hmumu_wminush_M130_2018': 0.4676, 'hmumu_zh_M130_2018': 0.7899,

            'muon_2016B': 1., 'muon_2016C': 1., 'muon_2016D': 1., 'muon_2016E': 1., 
            'muon_2016F': 1., 'muon_2016G': 1., 'muon_2016H': 1.,
            'muon_2017B': 1., 'muon_2017C': 1., 'muon_2017D': 1., 'muon_2017E': 1., 'muon_2017F': 1.,
            'muon_2018A': 1., 'muon_2018B': 1., 'muon_2018C': 1., 'muon_2018D': 1.,

            'electron_2016B': 1., 'electron_2016C': 1., 'electron_2016D': 1., 'electron_2016E': 1., 
            'electron_2016F': 1., 'electron_2016G': 1., 'electron_2016H': 1.,
            'electron_2017B': 1., 'electron_2017C': 1., 'electron_2017D': 1., 'electron_2017E': 1., 'electron_2017F': 1.,
            'electron_2018A': 1., 'electron_2018B': 1., 'electron_2018C': 1., 'electron_2018D': 1.}
    
    br =   {'zjets_M50_2016': 1., 'zjets_M50_2017': 1., 'zjets_M50_2018': 1., 
            'zg_llg_2016': 1., 'zg_llg_2017': 1., 'zg_llg_2018': 1., #'ttbar_inclusive': 1., # these from MY
            'zg_ewk_2016': 1., 'zg_ewk_2017': 1., 'zg_ewk_2018': 1.,
            'ttjets_2016': 1., 'ttjets_2017': 1., 'ttjets_2018': 1., # these from MY
            #'htautau_gluglu': br_htautau, 'htautau_vbf': br_htautau,
            
            'hzg_gluglu_M120_2016': br_hzg_m120*br_zll, 'hzg_tth_M120_2016': br_hzg_m120*br_zll, 'hzg_vbf_M120_2016': br_hzg_m120*br_zll, 
            'hzg_wplush_M120_2016': br_hzg_m120*br_zll, 'hzg_wminush_M120_2016': br_hzg_m120*br_zll, 'hzg_zh_M120_2016': br_hzg_m120*br_zll,
            'hzg_gluglu_M120_2017': br_hzg_m120*br_zll, 'hzg_tth_M120_2017': br_hzg_m120*br_zll, 'hzg_vbf_M120_2017': br_hzg_m120*br_zll, 
            'hzg_wplush_M120_2017': br_hzg_m120*br_zll, 'hzg_wminush_M120_2017': br_hzg_m120*br_zll, 'hzg_zh_M120_2017': br_hzg_m120*br_zll,
            'hzg_gluglu_M120_2018': br_hzg_m120*br_zll, 'hzg_tth_M120_2018': br_hzg_m120*br_zll, 'hzg_vbf_M120_2018': br_hzg_m120*br_zll, 
            'hzg_wplush_M120_2018': br_hzg_m120*br_zll, 'hzg_wminush_M120_2018': br_hzg_m120*br_zll, 'hzg_zh_M120_2018': br_hzg_m120*br_zll,

            'hzg_gluglu_M125_2016': br_hzg_m125*br_zll, 'hzg_tth_M125_2016': br_hzg_m125*br_zll, 'hzg_vbf_M125_2016': br_hzg_m125*br_zll, 
            'hzg_wplush_M125_2016': br_hzg_m125*br_zll, 'hzg_wminush_M125_2016': br_hzg_m125*br_zll, 'hzg_zh_M125_2016': br_hzg_m125*br_zll,
            'hzg_gluglu_M125_2017': br_hzg_m125*br_zll, 'hzg_tth_M125_2017': br_hzg_m125*br_zll, 'hzg_vbf_M125_2017': br_hzg_m125*br_zll, 
            'hzg_wplush_M125_2017': br_hzg_m125*br_zll, 'hzg_wminush_M125_2017': br_hzg_m125*br_zll, 'hzg_zh_M125_2017': br_hzg_m125*br_zll,
            'hzg_gluglu_M125_2018': br_hzg_m125*br_zll, 'hzg_tth_M125_2018': br_hzg_m125*br_zll, 'hzg_vbf_M125_2018': br_hzg_m125*br_zll, 
            'hzg_wplush_M125_2018': br_hzg_m125*br_zll, 'hzg_wminush_M125_2018': br_hzg_m125*br_zll, 'hzg_zh_M125_2018': br_hzg_m125*br_zll,
            
            'hzg_gluglu_M130_2016': br_hzg_m130*br_zll, 'hzg_tth_M130_2016': br_hzg_m130*br_zll, 'hzg_vbf_M130_2016': br_hzg_m130*br_zll, 
            'hzg_wplush_M130_2016': br_hzg_m130*br_zll, 'hzg_wminush_M130_2016': br_hzg_m130*br_zll, 'hzg_zh_M130_2016': br_hzg_m130*br_zll,
            'hzg_gluglu_M130_2017': br_hzg_m130*br_zll, 'hzg_tth_M130_2017': br_hzg_m130*br_zll, 'hzg_vbf_M130_2017': br_hzg_m130*br_zll, 
            'hzg_wplush_M130_2017': br_hzg_m130*br_zll, 'hzg_wminush_M130_2017': br_hzg_m130*br_zll, 'hzg_zh_M130_2017': br_hzg_m130*br_zll,
            'hzg_gluglu_M130_2018': br_hzg_m130*br_zll, 'hzg_tth_M130_2018': br_hzg_m130*br_zll, 'hzg_vbf_M130_2018': br_hzg_m130*br_zll, 
            'hzg_wplush_M130_2018': br_hzg_m130*br_zll, 'hzg_wminush_M130_2018': br_hzg_m130*br_zll, 'hzg_zh_M130_2018': br_hzg_m130*br_zll,
            
            'hmumu_gluglu_M120_2016': br_hmumu_m120, 'hmumu_tth_M120_2016': br_hmumu_m120, 'hmumu_vbf_M120_2016': br_hmumu_m120, 
            'hmumu_wplush_M120_2016': br_hmumu_m120, 'hmumu_wminush_M120_2016': br_hmumu_m120, 'hmumu_zh_M120_2016': br_hmumu_m120,
            'hmumu_gluglu_M120_2017': br_hmumu_m120, 'hmumu_tth_M120_2017': br_hmumu_m120, 'hmumu_vbf_M120_2017': br_hmumu_m120, 
            'hmumu_wplush_M120_2017': br_hmumu_m120, 'hmumu_wminush_M120_2017': br_hmumu_m120, 'hmumu_zh_M120_2017': br_hmumu_m120,
            'hmumu_gluglu_M120_2018': br_hmumu_m120, 'hmumu_tth_M120_2018': br_hmumu_m120, 'hmumu_vbf_M120_2018': br_hmumu_m120, 
            'hmumu_wplush_M120_2018': br_hmumu_m120, 'hmumu_wminush_M120_2018': br_hmumu_m120, 'hmumu_zh_M120_2018': br_hmumu_m120,

            'hmumu_gluglu_M125_2016': br_hmumu_m125, 'hmumu_tth_M125_2016': br_hmumu_m125, 'hmumu_vbf_M125_2016': br_hmumu_m125, 
            'hmumu_wplush_M125_2016': br_hmumu_m125, 'hmumu_wminush_M125_2016': br_hmumu_m125, 'hmumu_zh_M125_2016': br_hmumu_m125,
            'hmumu_gluglu_M125_2017': br_hmumu_m125, 'hmumu_tth_M125_2017': br_hmumu_m125, 'hmumu_vbf_M125_2017': br_hmumu_m125, 
            'hmumu_wplush_M125_2017': br_hmumu_m125, 'hmumu_wminush_M125_2017': br_hmumu_m125, 'hmumu_zh_M125_2017': br_hmumu_m125,
            'hmumu_gluglu_M125_2018': br_hmumu_m125, 'hmumu_tth_M125_2018': br_hmumu_m125, 'hmumu_vbf_M125_2018': br_hmumu_m125, 
            'hmumu_wplush_M125_2018': br_hmumu_m125, 'hmumu_wminush_M125_2018': br_hmumu_m125, 'hmumu_zh_M125_2018': br_hmumu_m125,
            
            'hmumu_gluglu_M130_2016': br_hmumu_m130, 'hmumu_tth_M130_2016': br_hmumu_m130, 'hmumu_vbf_M130_2016': br_hmumu_m130, 
            'hmumu_wplush_M130_2016': br_hmumu_m130, 'hmumu_wminush_M130_2016': br_hmumu_m130, 'hmumu_zh_M130_2016': br_hmumu_m130,
            'hmumu_gluglu_M130_2017': br_hmumu_m130, 'hmumu_tth_M130_2017': br_hmumu_m130, 'hmumu_vbf_M130_2017': br_hmumu_m130, 
            'hmumu_wplush_M130_2017': br_hmumu_m130, 'hmumu_wminush_M130_2017': br_hmumu_m130, 'hmumu_zh_M130_2017': br_hmumu_m130,
            'hmumu_gluglu_M130_2018': br_hmumu_m130, 'hmumu_tth_M130_2018': br_hmumu_m130, 'hmumu_vbf_M130_2018': br_hmumu_m130, 
            'hmumu_wplush_M130_2018': br_hmumu_m130, 'hmumu_wminush_M130_2018': br_hmumu_m130, 'hmumu_zh_M130_2018': br_hmumu_m130,

            'muon_2016B': 1., 'muon_2016C': 1., 'muon_2016D': 1., 'muon_2016E': 1., 
            'muon_2016F': 1., 'muon_2016G': 1., 'muon_2016H': 1.,
            'muon_2017B': 1., 'muon_2017C': 1., 'muon_2017D': 1., 'muon_2017E': 1., 'muon_2017F': 1., 
            'muon_2018A': 1., 'muon_2018B': 1., 'muon_2018C': 1., 'muon_2018D': 1.,

            'electron_2016B': 1., 'electron_2016C': 1., 'electron_2016D': 1., 'electron_2016E': 1., 
            'electron_2016F': 1., 'electron_2016G': 1., 'electron_2016H': 1.,    
            'electron_2017B': 1., 'electron_2017C': 1., 'electron_2017D': 1., 'electron_2017E': 1., 'electron_2017F': 1.,
            'electron_2018A': 1., 'electron_2018B': 1., 'electron_2018C': 1., 'electron_2018D': 1.}

    periods = [2016, 2017, 2018]
    luminosity = {2016: 35.9e3, 2017: 41.5e3, 2018: 59.8e3}
    channels = ['mmg', 'eeg']

    sf_dict = {}

    #mingyan_data = pd.read_csv('data/mingyan_final_data/all_data.csv')
    mingyan_data = pd.read_csv('data/mingyan_final_data/all_data_no_cuts.csv')

    for period, channel in itertools.product(periods, channels):
        datasets = samples[period][channel]
        if datasets == []:
            continue
        print('running over: {0}, {1}'.format(period, channel))
        sf_dict[period] = {}
        inputFile = root_open('data/bltuples/output_{0}_{1}.root'.format(channel, period))
        outputFile = root_open('data/step1_sfs/output_{0}_{1}.root'.format(channel, period), 'recreate')

        if period == 2017 or period == 2018:
            pt_weights = ur.open('data/from_ming-yan/pt_weights/pt_weights_{0}_{1}.root'.format(channel, period))['hd']

        for dataset in tqdm(datasets):
            tree = inputFile['signal/tree_{0}'.format(dataset)]
            hist = inputFile['TotalEvents_{0}'.format(dataset)]
            tree.create_buffer()
            outTree = Tree(dataset)
            outTree.set_buffer(tree._buffer, create_branches=True)
            outTree.create_branches({'mc_sf': 'F'})
            outTree.create_branches({'pt_weight': 'F'})
            outTree.create_branches({'useTMVA': 'F'})
            outTree.create_branches({'corrPhotonMVA': 'F'})
            outTree.create_branches({'llgMKinMY': 'F'})
            outTree.create_branches({'isMingYanData': 'I'})

            # compute the MC scale factor
            n_gen = inputFile['TotalEvents_{0}'.format(dataset)].GetBinContent(1)
            n_neg = inputFile['TotalEvents_{0}'.format(dataset)].GetBinContent(30)
            sf = luminosity[period]*xsec[dataset]*br[dataset]/(float(n_gen) - 2.*float(n_neg))
            sf_dict[period][dataset] = sf
            
            #print(dataset)
            #print(n_gen)
            #print(n_neg)
            #print(sf)
            #print('without the negative weights!!')
            #print(sf*(n_gen - 2.*n_neg)/float(n_gen))

            for evt in tree:
                run = evt.runNumber
                lumi = evt.lumiSection
                event = evt.evtNumber

                outTree.mc_sf = sf

                outTree.llgMKinMY = evt.llgMKin # by default use my own kin fit result
                outTree.isMingYanData = 0
               
                # DY veto
                if 'zjets' in dataset:
                    if evt.vetoDY:
                        continue

                # ZH lepton tag cleaning
                if (('hzg_zh' in dataset) and evt.isLeptonTag and not (evt.leptonOneMatched and evt.leptonTwoMatched)):
                    continue
                
                # split signal in half for MVA training
                useTMVA = 1.
                #if 'hzg' in dataset:
                if (dataset in mc_16 or dataset in mc_17 or dataset in mc_18):
                    if event % 2 != 0:
                        useTMVA = 0.
                outTree.useTMVA = useTMVA

                # fix system balance and photon Zeppenfeld variables
                outTree.vbfPtBalance = abs(evt.vbfPtBalance)
                outTree.photonZepp = abs(evt.photonZepp)

                # llg pt reweighting
                #pt_weight = 1.
                #if (period == 2017 and dataset in mc_17):
                #    for i in range(len(pt_bin_edges_17)-1):
                #        if pt_bin_edges_17[i] < evt.llgPt and evt.llgPt < pt_bin_edges_17[i+1]:
                #            pt_weight = pt_weights_17[i]
                #            break
                #elif (period == 2018 and dataset in mc_18):
                #    for i in range(len(pt_bin_edges_18)-1):
                #        if pt_bin_edges_18[i] < evt.llgPt and evt.llgPt < pt_bin_edges_18[i+1]:
                #            pt_weight = pt_weights_18[i]
                #            break
                #outTree.pt_weight = pt_weight

                # using Ming-Yan weights
                pt_weight = 1.
                if (dataset in mc_17 or dataset in mc_18) and not ('hzg' in dataset or 'hmumu' in dataset):
                    for i in range(len(pt_weights.alledges)-1):
                        if pt_weights.alledges[i] < evt.llgPt and evt.llgPt < pt_weights.alledges[i+1]:
                            pt_weight = pt_weights.allvalues[i]
                            break
                outTree.pt_weight = pt_weight

                outTree.corrPhotonMVA = evt.photonMVA
                if 0.97 <= evt.photonMVAWeight <= 1.03:
                    outTree.corrPhotonMVA *= evt.photonMVAWeight 

                if 'muon' in dataset or 'electron' in dataset:
                    this_evt_mingyan = mingyan_data.query('run == {0} and lumi == {1} and evt == {2}'.format(evt.runNumber, evt.lumiSection, evt.evtNumber))
                    if this_evt_mingyan.shape[0] > 0:
                        this_mass = this_evt_mingyan['CMS_hzg_mass'].values[0]
                        outTree.llgMKinMY = this_mass
                        outTree.isMingYanData = 1
                    else:
                        this_mass_mingyan = mingyan_data.query('run == {0} and lumi == {1} and abs(llgMRaw - {2}) <= 0.001'.format(evt.runNumber, evt.lumiSection, evt.llgM))
                        if this_mass_mingyan.shape[0] > 0:
                            this_mass = this_mass_mingyan['CMS_hzg_mass'].values[0]
                            outTree.llgMKinMY = this_mass
                            outTree.evtNumber = this_mass_mingyan['evt'].values[0]
                            outTree.isMingYanData = 1
 
                outTree.Fill()

            outTree.Write()
            hist.Write()
        outputFile.Close()
        inputFile.Close()

    pickle.dump(sf_dict, open('data/mc_sfs/mc_sfs.pkl', 'wb'))
