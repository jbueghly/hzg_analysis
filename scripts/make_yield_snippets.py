#!/usr/bin/env python
import pandas as pd
import ROOT as r
from rootpy.tree import Tree
from rootpy.io import root_open
import array 
import numpy as np
from tqdm import tqdm, trange
from root_pandas import read_root
import itertools

if __name__ == '__main__':
    
    #mc_16 = ['ttbar_inclusive', 'zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wplush', 'hzg_wminush', 'hzg_zh']
    mc_16 = ['zjets_m-50_amc_16', 'zg_llg_16', 'hzg_gluglu_M125_16', 'hzg_tth_M125_16', 'hzg_vbf_M125_16', 'hzg_wplush_M125_16', 'hzg_wminush_M125_16', 'hzg_zh_M125_16']
    muon_data_16 = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
                 'muon_2016F', 'muon_2016G', 'muon_2016H']
    electron_data_16 = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                     'electron_2016F', 'electron_2016G', 'electron_2016H']

    mc_17 = ['hzg_gluglu_2017', 'hzg_tth_2017', 'hzg_vbf_2017', 'hzg_wplush_2017', 'hzg_wminush_2017', 'hzg_zh_2017'] 
    muon_data_17 = ['muon_2017B', 'muon_2017C', 'muon_2017D', 'muon_2017E', 'muon_2017F']
    electron_data_17 = ['electron_2017B', 'electron_2017C', 'electron_2017D', 'electron_2017E', 'electron_2017F'] 

    samples = {
                2016: {'mmg': mc_16 + muon_data_16, 'eeg': mc_16 + electron_data_16, 'lepton': mc_16 + muon_data_16 + electron_data_16},
                2017: {'mmg': mc_17 + muon_data_17, 'eeg': mc_17 + electron_data_17, 'lepton': mc_17 + muon_data_17 + electron_data_17} 
                }

    category_scheme = 'optimal'
    #category_scheme = 'nominal'

    channels = ['mmg', 'eeg', 'lepton']
    periods = [2016, 2017]

    if category_scheme == 'nominal':
        categories = ['lepton', 'dijet', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
        cat_num = [6789, 5, 1, 2, 3, 4]
    elif category_scheme == 'optimal':
        categories = ['lepton', 'dijet_1', 'dijet_2', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
        cat_num = [6789, 51, 52, 1, 2, 3, 4]

    for period, channel in itertools.product(periods, channels):
        yield_dict = {}
        datasets = samples[period][channel]
        if datasets == []:
            continue
        print('running over: {0}, {1}'.format(period, channel))
        for dataset in tqdm(datasets):
            for cat in categories:
                df = read_root('data/step4_cats/output_{0}_{1}_yields.root'.format(channel, period), '{0}_{1}'.format(dataset, cat)).astype('float')
                df.query('115. < CMS_hzg_mass < 170.', inplace=True)
                #yield_dict['{0}_{1}'.format(dataset, cat)] = np.sum(df.eventWeight*df.genWeight*df.mc_sf) 
                yield_dict['{0}_{1}'.format(dataset, cat)] = np.sum(df.eventWeight) 
               
        # make datacard snippets
        for i, cat in enumerate(categories):
            num = cat_num[i]
            snippet = 'bin     cat{0}       cat{0}      cat{0}       cat{0}       cat{0}      cat{0} cat{0}\n'.format(num)
            snippet += 'process     ttH_hzg     ZH_hzg      WplusH_hzg      WminusH_hzg      qqH_hzg     ggH_hzg     bgr\n'
            snippet += 'process     -5      -4      -3      -2      -1      0       1\n'
            snippet += 'rate '
            if period == 2016:
                snippet += '{0:.6f}     '.format(yield_dict['hzg_tth_M125_16_{0}'.format(cat)])
                snippet += '{0:.6f}     '.format(yield_dict['hzg_zh_M125_16_{0}'.format(cat)])
                snippet += '{0:.6f}     '.format(yield_dict['hzg_wplush_M125_16_{0}'.format(cat)])
                snippet += '{0:.6f}     '.format(yield_dict['hzg_wminush_M125_16_{0}'.format(cat)])
                snippet += '{0:.6f}     '.format(yield_dict['hzg_vbf_M125_16_{0}'.format(cat)])
                snippet += '{0:.6f}     '.format(yield_dict['hzg_gluglu_M125_16_{0}'.format(cat)])
            elif period == 2017:
                snippet += '{0:.6f}     '.format(yield_dict['hzg_tth_2017_{0}'.format(cat)])
                snippet += '{0:.6f}     '.format(yield_dict['hzg_zh_2017_{0}'.format(cat)])
                snippet += '{0:.6f}     '.format(yield_dict['hzg_wplush_2017_{0}'.format(cat)])
                snippet += '{0:.6f}     '.format(yield_dict['hzg_wminush_2017_{0}'.format(cat)])
                snippet += '{0:.6f}     '.format(yield_dict['hzg_vbf_2017_{0}'.format(cat)])
                snippet += '{0:.6f}     '.format(yield_dict['hzg_gluglu_2017_{0}'.format(cat)])
            snippet += '1.000000\n'
            snippet += '-------------------------------------------------------------\n'
            text_file = open('yields/rate_snippets/{0}_{1}_{2}.txt'.format(channel, cat, period), 'w')
            text_file.write(snippet)
            text_file.close()
