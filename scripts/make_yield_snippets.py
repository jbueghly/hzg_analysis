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
    
    #mc_16 = ['zjets_M50_2016', 'zg_llg_2016', 'hzg_gluglu_M125_2016', 'hzg_tth_M125_2016', 'hzg_vbf_M125_2016', 'hzg_wplush_M125_2016', 'hzg_wminush_M125_2016', 'hzg_zh_M125_2016']
    signal_16_M120 = ['hzg_gluglu_M120_2016', 'hzg_tth_M120_2016', 'hzg_vbf_M120_2016', 'hzg_wplush_M120_2016', 'hzg_wminush_M120_2016', 'hzg_zh_M120_2016']
    signal_16_M125 = ['hzg_gluglu_M125_2016', 'hzg_tth_M125_2016', 'hzg_vbf_M125_2016', 'hzg_wplush_M125_2016', 'hzg_wminush_M125_2016', 'hzg_zh_M125_2016']
    signal_16_M130 = ['hzg_gluglu_M130_2016', 'hzg_tth_M130_2016', 'hzg_vbf_M130_2016', 'hzg_wplush_M130_2016', 'hzg_wminush_M130_2016', 'hzg_zh_M130_2016']
    mc_16 = signal_16_M120 + signal_16_M125 + signal_16_M130

    muon_data_16 = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
                 'muon_2016F', 'muon_2016G', 'muon_2016H']
    electron_data_16 = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                     'electron_2016F', 'electron_2016G', 'electron_2016H']
    
    signal_17_M120 = ['hzg_gluglu_M120_2017', 'hzg_tth_M120_2017', 'hzg_vbf_M120_2017', 'hzg_wplush_M120_2017', 'hzg_wminush_M120_2017', 'hzg_zh_M120_2017']
    signal_17_M125 = ['hzg_gluglu_M125_2017', 'hzg_tth_M125_2017', 'hzg_vbf_M125_2017', 'hzg_wplush_M125_2017', 'hzg_wminush_M125_2017', 'hzg_zh_M125_2017']
    signal_17_M130 = ['hzg_gluglu_M130_2017', 'hzg_tth_M130_2017', 'hzg_vbf_M130_2017', 'hzg_wplush_M130_2017', 'hzg_wminush_M130_2017', 'hzg_zh_M130_2017']
    mc_17 = signal_17_M120 + signal_17_M125 + signal_17_M130

    muon_data_17 = ['muon_2017B', 'muon_2017C', 'muon_2017D', 'muon_2017E', 'muon_2017F']
    electron_data_17 = ['electron_2017B', 'electron_2017C', 'electron_2017D', 'electron_2017E', 'electron_2017F'] 

    signal_18_M120 = ['hzg_gluglu_M120_2018', 'hzg_tth_M120_2018', 'hzg_vbf_M120_2018', 'hzg_wplush_M120_2018', 'hzg_wminush_M120_2018', 'hzg_zh_M120_2018']
    signal_18_M125 = ['hzg_gluglu_M125_2018', 'hzg_tth_M125_2018', 'hzg_vbf_M125_2018', 'hzg_wplush_M125_2018', 'hzg_wminush_M125_2018', 'hzg_zh_M125_2018']
    signal_18_M130 = ['hzg_gluglu_M130_2018', 'hzg_tth_M130_2018', 'hzg_vbf_M130_2018', 'hzg_wplush_M130_2018', 'hzg_wminush_M130_2018', 'hzg_zh_M130_2018']
    mc_18 = signal_18_M120 + signal_18_M125 + signal_18_M130
    
    muon_data_18 = ['muon_2018A', 'muon_2018B', 'muon_2018C', 'muon_2018D']
    electron_data_18 = ['electron_2018A', 'electron_2018B', 'electron_2018C', 'electron_2018D'] 
    
    samples = {
                2016: {'mmg': mc_16, 'eeg': mc_16, 'lepton': mc_16},
                2017: {'mmg': mc_17, 'eeg': mc_17, 'lepton': mc_17},
                2018: {'mmg': mc_18, 'eeg': mc_18, 'lepton': mc_18} 
                }

    fudge_factor = {
                    2016: {'mmg': 1.08765, 'eeg': 1.},
                    2017: {'mmg': 1., 'eeg': 1.},
                    2018: {'mmg': 1., 'eeg': 1.06938}
                    }

    category_scheme = 'optimal'
    #category_scheme = 'nominal'

    #channels = ['mmg', 'eeg', 'lepton']
    channels = ['mmg', 'eeg', 'lepton']
    #channels = ['lepton']
    periods = [2016, 2017, 2018]

    if category_scheme == 'nominal':
        categories = ['lepton', 'dijet', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
        cat_num = [6789, 5, 1, 2, 3, 4]
    elif category_scheme == 'optimal':
        categories = ['lepton', 'dijet_1', 'dijet_2', 'dijet_3', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
        #categories = ['lepton']
        cat_num = [6789, 51, 52, 53, 1, 2, 3, 4]

    yield_dict = {}
    for period, channel in itertools.product(periods, channels):
        datasets = samples[period][channel]
        if datasets == []:
            continue
        print('running over: {0}, {1}'.format(period, channel))
        for dataset in tqdm(datasets):
            for cat in categories:
                if (channel == 'mmg' or channel == 'eeg') and cat == 'lepton':
                    continue
                if channel == 'eeg' and dataset == 'hzg_tth_M120_2017':
                    yield_dict['{0}_{1}_{2}'.format(dataset, channel, cat)] = 0.
                    continue
                #if channel == 'eeg' and dataset == 'hzg_tth_M125_2018':
                #    yield_dict['{0}_{1}_{2}'.format(dataset, channel, cat)] = 0.
                #    continue
                #if channel == 'mmg' and dataset == 'hzg_tth_M120_2017':
                #    yield_dict['{0}_{1}_{2}'.format(dataset, channel, cat)] = 0.
                #    continue
                #if channel == 'eeg' and dataset == 'hzg_tth_M130_2018':
                #    yield_dict['{0}_{1}_{2}'.format(dataset, channel, cat)] = 0.
                #    continue
                df = read_root('data/step4_cats/output_{0}_{1}_yields.root'.format(channel, period), '{0}_{1}'.format(dataset, cat)).astype('float')
                df.query('115. < CMS_hzg_mass < 170.', inplace=True)
                #yield_dict['{0}_{1}'.format(dataset, cat)] = np.sum(df.eventWeight*df.genWeight*df.mc_sf) 
                yield_dict['{0}_{1}_{2}'.format(dataset, channel, cat)] = np.sum(df.eventWeight)#*fudge_factor[period][channel]

    # interpolation
    for period, channel in itertools.product(periods, channels):
        for pm in ['hzg_gluglu', 'hzg_vbf', 'hzg_tth', 'hzg_zh', 'hzg_wplush', 'hzg_wminush']:
            for i, cat in enumerate(categories):
                if (channel == 'mmg' or channel == 'eeg') and cat == 'lepton':
                    continue
                yield_120 = yield_dict[f'{pm}_M120_{period}_{channel}_{cat}']
                yield_125 = yield_dict[f'{pm}_M125_{period}_{channel}_{cat}']
                yield_130 = yield_dict[f'{pm}_M130_{period}_{channel}_{cat}']
                for interp_mass in [121, 122, 123, 124]:
                    interp_yield = yield_120 + (interp_mass-120)*(yield_125-yield_120)/5.
                    yield_dict[f'{pm}_M{interp_mass}_{period}_{channel}_{cat}'] = interp_yield
                for interp_mass in [125.38, 126, 127, 128, 129]:
                    interp_yield = yield_125 + (interp_mass-125)*(yield_130-yield_125)/5.
                    yield_dict[f'{pm}_M{interp_mass}_{period}_{channel}_{cat}'] = interp_yield
               
    # make datacard snippets

    for i, cat in enumerate(categories):
        if cat == 'lepton':
            continue
        num = cat_num[i]

        for mass in [120, 121, 122, 123, 124, 125, 125.38, 126, 127, 128, 129, 130]:
            snippet = 'bin     cat{0}       cat{0}      cat{0}       cat{0}       cat{0}      cat{0} cat{0}\n'.format(num)
            snippet += 'process     ggH_hzg     qqH_hzg      ttH_hzg      ZH_hzg      WplusH_hzg    bgr\n'
            snippet += 'process     -4      -3      -2      -1      0       1\n'
            snippet += 'rate '

            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_gluglu_M{mass}_2016_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_vbf_M{mass}_2016_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_tth_M{mass}_2016_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_zh_M{mass}_2016_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_wplush_M{mass}_2016_eeg_{cat}']+yield_dict[f'hzg_wminush_M{mass}_2016_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_gluglu_M{mass}_2016_mmg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_vbf_M{mass}_2016_mmg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_tth_M{mass}_2016_mmg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_zh_M{mass}_2016_mmg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_wplush_M{mass}_2016_mmg_{cat}']+yield_dict[f'hzg_wminush_M{mass}_2016_mmg_{cat}'])
            
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_gluglu_M{mass}_2017_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_vbf_M{mass}_2017_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_tth_M{mass}_2017_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_zh_M{mass}_2017_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_wplush_M{mass}_2017_eeg_{cat}']+yield_dict[f'hzg_wminush_M{mass}_2017_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_gluglu_M{mass}_2017_mmg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_vbf_M{mass}_2017_mmg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_tth_M{mass}_2017_mmg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_zh_M{mass}_2017_mmg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_wplush_M{mass}_2017_mmg_{cat}']+yield_dict[f'hzg_wminush_M{mass}_2017_mmg_{cat}'])
            
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_gluglu_M{mass}_2018_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_vbf_M{mass}_2018_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_tth_M{mass}_2018_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_zh_M{mass}_2018_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_wplush_M{mass}_2018_eeg_{cat}']+yield_dict[f'hzg_wminush_M{mass}_2018_eeg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_gluglu_M{mass}_2018_mmg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_vbf_M{mass}_2018_mmg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_tth_M{mass}_2018_mmg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_zh_M{mass}_2018_mmg_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hzg_wplush_M{mass}_2018_mmg_{cat}']+yield_dict[f'hzg_wminush_M{mass}_2018_mmg_{cat}'])
        

            snippet += '1.000000\n'
            snippet += '-------------------------------------------------------------\n'
            text_file = open('yields/rate_snippets/{0}_inclusive_{1}.txt'.format(cat, mass), 'w')
            text_file.write(snippet)
            text_file.close()



    #lepton tag
    for mass in [120, 121, 122, 123, 124, 125, 125.38, 126, 127, 128, 129, 130]:

        snippet = 'bin     cat6789       cat6789      cat6789       cat6789       cat6789      cat6789 cat6789\n'
        snippet += 'process     ggH_hzg     qqH_hzg      ttH_hzg      ZH_hzg      WplusH_hzg    bgr\n'
        snippet += 'process     -4      -3      -2      -1      0       1\n'
        snippet += 'rate '

        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_gluglu_M{mass}_2016_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_vbf_M{mass}_2016_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_tth_M{mass}_2016_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_zh_M{mass}_2016_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_wplush_M{mass}_2016_lepton_lepton']+yield_dict[f'hzg_wminush_M{mass}_2016_lepton_lepton'])
        
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_gluglu_M{mass}_2017_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_vbf_M{mass}_2017_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_tth_M{mass}_2017_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_zh_M{mass}_2017_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_wplush_M{mass}_2017_lepton_lepton']+yield_dict[f'hzg_wminush_M{mass}_2017_lepton_lepton'])
        
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_gluglu_M{mass}_2018_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_vbf_M{mass}_2018_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_tth_M{mass}_2018_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_zh_M{mass}_2018_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hzg_wplush_M{mass}_2018_lepton_lepton']+yield_dict[f'hzg_wminush_M{mass}_2018_lepton_lepton'])  

        snippet += '1.000000\n'
        snippet += '-------------------------------------------------------------\n'
        text_file = open('yields/rate_snippets/lepton_inclusive_{0}.txt'.format(mass), 'w')
        text_file.write(snippet)
        text_file.close()
