#!/usr/bin/env python
import pandas as pd
import ROOT as r
from rootpy.tree import Tree
from rootpy.io import root_open
import array 
import numpy as np
from tqdm import tqdm, trange
from root_pandas import read_root
import uproot as ur
import itertools
import re

if __name__ == '__main__':
    
    signal_16_M120 = ['hzg_gluglu_M120_2016', 'hzg_tth_M120_2016', 'hzg_vbf_M120_2016', 'hzg_wplush_M120_2016', 'hzg_wminush_M120_2016', 'hzg_zh_M120_2016', 
                      'hmumu_gluglu_M120_2016', 'hmumu_tth_M120_2016', 'hmumu_vbf_M120_2016', 'hmumu_wplush_M120_2016', 'hmumu_wminush_M120_2016', 'hmumu_zh_M120_2016']
    signal_16_M125 = ['hzg_gluglu_M125_2016', 'hzg_tth_M125_2016', 'hzg_vbf_M125_2016', 'hzg_wplush_M125_2016', 'hzg_wminush_M125_2016', 'hzg_zh_M125_2016', 
                      'hmumu_gluglu_M125_2016', 'hmumu_tth_M125_2016', 'hmumu_vbf_M125_2016', 'hmumu_wplush_M125_2016', 'hmumu_wminush_M125_2016', 'hmumu_zh_M125_2016']
    signal_16_M130 = ['hzg_gluglu_M130_2016', 'hzg_tth_M130_2016', 'hzg_vbf_M130_2016', 'hzg_wplush_M130_2016', 'hzg_wminush_M130_2016', 'hzg_zh_M130_2016', 
                      'hmumu_gluglu_M130_2016', 'hmumu_tth_M130_2016', 'hmumu_vbf_M130_2016', 'hmumu_wplush_M130_2016', 'hmumu_wminush_M130_2016', 'hmumu_zh_M130_2016']
    mc_16 = signal_16_M120 + signal_16_M125 + signal_16_M130

    muon_data_16 = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
                 'muon_2016F', 'muon_2016G', 'muon_2016H']
    electron_data_16 = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                     'electron_2016F', 'electron_2016G', 'electron_2016H']
    
    signal_17_M120 = ['hzg_gluglu_M120_2017', 'hzg_tth_M120_2017', 'hzg_vbf_M120_2017', 'hzg_wplush_M120_2017', 'hzg_wminush_M120_2017', 'hzg_zh_M120_2017', 
                      'hmumu_gluglu_M120_2017', 'hmumu_tth_M120_2017', 'hmumu_vbf_M120_2017', 'hmumu_wplush_M120_2017', 'hmumu_wminush_M120_2017', 'hmumu_zh_M120_2017']
    signal_17_M125 = ['hzg_gluglu_M125_2017', 'hzg_tth_M125_2017', 'hzg_vbf_M125_2017', 'hzg_wplush_M125_2017', 'hzg_wminush_M125_2017', 'hzg_zh_M125_2017', 
                      'hmumu_gluglu_M125_2017', 'hmumu_tth_M125_2017', 'hmumu_vbf_M125_2017', 'hmumu_wplush_M125_2017', 'hmumu_wminush_M125_2017', 'hmumu_zh_M125_2017']
    signal_17_M130 = ['hzg_gluglu_M130_2017', 'hzg_tth_M130_2017', 'hzg_vbf_M130_2017', 'hzg_wplush_M130_2017', 'hzg_wminush_M130_2017', 'hzg_zh_M130_2017', 
                      'hmumu_gluglu_M130_2017', 'hmumu_tth_M130_2017', 'hmumu_vbf_M130_2017', 'hmumu_wplush_M130_2017', 'hmumu_wminush_M130_2017', 'hmumu_zh_M130_2017']
    mc_17 = signal_17_M120 + signal_17_M125 + signal_17_M130

    muon_data_17 = ['muon_2017B', 'muon_2017C', 'muon_2017D', 'muon_2017E', 'muon_2017F']
    electron_data_17 = ['electron_2017B', 'electron_2017C', 'electron_2017D', 'electron_2017E', 'electron_2017F'] 

    signal_18_M120 = ['hzg_gluglu_M120_2018', 'hzg_tth_M120_2018', 'hzg_vbf_M120_2018', 'hzg_wplush_M120_2018', 'hzg_wminush_M120_2018', 'hzg_zh_M120_2018', 
                      'hmumu_gluglu_M120_2018', 'hmumu_tth_M120_2018', 'hmumu_vbf_M120_2018', 'hmumu_wplush_M120_2018', 'hmumu_wminush_M120_2018', 'hmumu_zh_M120_2018']
    signal_18_M125 = ['hzg_gluglu_M125_2018', 'hzg_tth_M125_2018', 'hzg_vbf_M125_2018', 'hzg_wplush_M125_2018', 'hzg_wminush_M125_2018', 'hzg_zh_M125_2018', 
                      'hmumu_gluglu_M125_2018', 'hmumu_tth_M125_2018', 'hmumu_vbf_M125_2018', 'hmumu_wplush_M125_2018', 'hmumu_wminush_M125_2018', 'hmumu_zh_M125_2018']
    signal_18_M130 = ['hzg_gluglu_M130_2018', 'hzg_tth_M130_2018', 'hzg_vbf_M130_2018', 'hzg_wplush_M130_2018', 'hzg_wminush_M130_2018', 'hzg_zh_M130_2018', 
                      'hmumu_gluglu_M130_2018', 'hmumu_tth_M130_2018', 'hmumu_vbf_M130_2018', 'hmumu_wplush_M130_2018', 'hmumu_wminush_M130_2018', 'hmumu_zh_M130_2018']
    mc_18 = signal_18_M120 + signal_18_M125 + signal_18_M130
    
    muon_data_18 = ['muon_2018A', 'muon_2018B', 'muon_2018C', 'muon_2018D']
    electron_data_18 = ['electron_2018A', 'electron_2018B', 'electron_2018C', 'electron_2018D'] 
    
    samples = {
                2016: {'mmg': mc_16, 'eeg': mc_16, 'lepton': mc_16},
                2017: {'mmg': mc_17, 'eeg': mc_17, 'lepton': mc_17},
                2018: {'mmg': mc_18, 'eeg': mc_18, 'lepton': mc_18} 
                }

    category_scheme = 'optimal'
    channels = ['mmg', 'eeg', 'lepton']
    periods = [2016, 2017, 2018]

    if category_scheme == 'nominal':
        categories = ['lepton', 'dijet', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
        cat_num = [6789, 5, 1, 2, 3, 4]
    elif category_scheme == 'optimal':
        categories = ['lepton', 'dijet_1', 'dijet_2', 'dijet_3', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
        cat_num = [6789, 501, 502, 503, 1, 2, 3, 4]

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
                this_file = ur.open(f'data/step4_cats/output_{channel}_{period}_yields.root')
                this_tree = this_file[f'{dataset}_{cat}']
                if this_tree.numentries == 0:
                    yield_dict['{0}_{1}_{2}'.format(dataset, channel, cat)] = 0.
                else:
                    df = this_tree.pandas.df()
                    df.query('105. < CMS_hzg_mass < 170.', inplace=True)
                    yield_dict['{0}_{1}_{2}'.format(dataset, channel, cat)] = np.sum(df.eventWeight)

    # interpolation

    xsec = {'hzg_gluglu':       {120: 52.22, 121: 51.46, 122: 50.71, 123: 49.98, 124: 49.27, 125: 48.58, 125.38: 48.3, 126: 47.89, 127: 47.23, 128: 46.58, 129: 45.94, 130: 45.31},
            'hzg_vbf':          {120: 3.935, 121: 3.904, 122: 3.873, 123: 3.842, 124: 3.812, 125: 3.782, 125.38: 3.770, 126: 3.752, 127: 3.723, 128: 3.694, 129: 3.665, 130: 3.637},
            'hzg_tth':          {120: 0.5697, 121: 0.5658, 122: 0.5438, 123: 0.5315, 124: 0.5193, 125: 0.5071, 125.38: 0.5033, 126: 0.4964, 127: 0.5851, 128: 0.4742, 129: 0.4639, 130: 0.4539},
            'hzg_zh':           {120: 0.9939, 121: 0.9705, 122: 0.9485, 123: 0.9266, 124: 0.9051, 125: 0.8839, 125.38: 0.8767, 126: 0.8649, 127: 0.8446, 128: 0.8255, 129: 0.8073, 130: 0.7899},
            'hzg_wplush':       {120: 0.9558, 121: 0.9320, 122: 0.9091, 123: 0.8843, 124: 0.8611, 125: 0.8400, 125.38: 0.8313, 126: 0.8184, 127: 0.7987, 128: 0.7785, 129: 0.7593, 130: 0.7414},
            'hzg_wminush':      {120: 0.6092, 121: 0.5925, 122: 0.5765, 123: 0.5618, 124: 0.5466, 125: 0.5328, 125.38: 0.5272, 126: 0.5187, 127: 0.5051, 128: 0.4924, 129: 0.4801, 130: 0.4676}, 
            'hmumu_gluglu':       {120: 52.22, 121: 51.46, 122: 50.71, 123: 49.98, 124: 49.27, 125: 48.58, 125.38: 48.3, 126: 47.89, 127: 47.23, 128: 46.58, 129: 45.94, 130: 45.31},
            'hmumu_vbf':          {120: 3.935, 121: 3.904, 122: 3.873, 123: 3.842, 124: 3.812, 125: 3.782, 125.38: 3.770, 126: 3.752, 127: 3.723, 128: 3.694, 129: 3.665, 130: 3.637},
            'hmumu_tth':          {120: 0.5697, 121: 0.5658, 122: 0.5438, 123: 0.5315, 124: 0.5193, 125: 0.5071, 125.38: 0.5033, 126: 0.4964, 127: 0.5851, 128: 0.4742, 129: 0.4639, 130: 0.4539},
            'hmumu_zh':           {120: 0.9939, 121: 0.9705, 122: 0.9485, 123: 0.9266, 124: 0.9051, 125: 0.8839, 125.38: 0.8767, 126: 0.8649, 127: 0.8446, 128: 0.8255, 129: 0.8073, 130: 0.7899},
            'hmumu_wplush':       {120: 0.9558, 121: 0.9320, 122: 0.9091, 123: 0.8843, 124: 0.8611, 125: 0.8400, 125.38: 0.8313, 126: 0.8184, 127: 0.7987, 128: 0.7785, 129: 0.7593, 130: 0.7414},
            'hmumu_wminush':      {120: 0.6092, 121: 0.5925, 122: 0.5765, 123: 0.5618, 124: 0.5466, 125: 0.5328, 125.38: 0.5272, 126: 0.5187, 127: 0.5051, 128: 0.4924, 129: 0.4801, 130: 0.4676}}
    br_hzg = {120: 1.100e-3, 121: 1.186e-3, 122: 1.272e-3, 123: 1.359e-3, 124: 1.447e-3, 125: 1.533e-3, 125.38: 1.567e-3, 126: 1.618e-3, 127: 1.702e-3, 128: 1.785e-3, 129: 1.864e-3, 130: 1.941e-3}
    br_hmm = {120: 2.423e-4, 121: 2.378e-4, 122: 2.331e-4, 123: 2.282e-4, 124: 2.230e-4, 125: 2.176e-4, 125.38: 2.153e-4, 126: 2.119e-4, 127: 2.061e-4, 128: 2.002e-4, 129: 1.940e-4, 130: 1.877e-4}
    for period, channel in itertools.product(periods, channels):
        for pm in ['hzg_gluglu', 'hzg_vbf', 'hzg_tth', 'hzg_zh', 'hzg_wplush', 'hzg_wminush', 
                   'hmumu_gluglu', 'hmumu_vbf', 'hmumu_tth', 'hmumu_zh', 'hmumu_wplush', 'hmumu_wminush']:
            for i, cat in enumerate(categories):
                if (channel == 'mmg' or channel == 'eeg') and cat == 'lepton':
                    continue
                yield_120 = yield_dict[f'{pm}_M120_{period}_{channel}_{cat}']
                yield_125 = yield_dict[f'{pm}_M125_{period}_{channel}_{cat}']
                yield_130 = yield_dict[f'{pm}_M130_{period}_{channel}_{cat}']
                if 'hzg' in pm:
                    br_dict = br_hzg
                elif 'hmumu' in pm:
                    br_dict = br_hmm
                    
                yield_120_no_xbr = yield_120 / (xsec[pm][120]*br_dict[120])
                yield_125_no_xbr = yield_125 / (xsec[pm][125]*br_dict[125])
                yield_130_no_xbr = yield_130 / (xsec[pm][130]*br_dict[130])

                for interp_mass in [121, 122, 123, 124]:
                    interp_yield = (yield_120_no_xbr + (interp_mass-120)*(yield_125_no_xbr-yield_120_no_xbr)/5.)*xsec[pm][interp_mass]*br_dict[interp_mass]
                    yield_dict[f'{pm}_M{interp_mass}_{period}_{channel}_{cat}'] = interp_yield
                for interp_mass in [125.38, 126, 127, 128, 129]:
                    interp_yield = (yield_125_no_xbr + (interp_mass-125)*(yield_130_no_xbr-yield_125_no_xbr)/5.)*xsec[pm][interp_mass]*br_dict[interp_mass]
                    yield_dict[f'{pm}_M{interp_mass}_{period}_{channel}_{cat}'] = interp_yield
               
    # make datacard snippets

    for i, cat in enumerate(categories):
        if cat == 'lepton':
            continue

        for mass in [120, 121, 122, 123, 124, 125, 125.38, 126, 127, 128, 129, 130]:
            #snippet = 'bin'
            #snippet += f'    cat{cat_num[i]}'*46
            #snippet += '\n'

            #snippet += 'process'
            #snippet += '    ggH_hzg_16_ele  qqH_hzg_16_ele  ttH_zg_16_ele   ZH_hzg_16_ele   WH_hzg_16_ele'
            #snippet += '    ggH_hzg_16_mu  qqH_hzg_16_mu  ttH_zg_16_mu   ZH_hzg_16_mu   WH_hzg_16_mu'
            #snippet += '    ggH_hzg_17_ele  qqH_hzg_17_ele  ttH_zg_17_ele   ZH_hzg_17_ele   WH_hzg_17_ele'
            #snippet += '    ggH_hzg_17_mu  qqH_hzg_17_mu  ttH_zg_17_mu   ZH_hzg_17_mu   WH_hzg_17_mu'
            #snippet += '    ggH_hzg_18_ele  qqH_hzg_18_ele  ttH_zg_18_ele   ZH_hzg_18_ele   WH_hzg_18_ele'
            #snippet += '    ggH_hzg_18_mu  qqH_hzg_18_mu  ttH_zg_18_mu   ZH_hzg_18_mu   WH_hzg_18_mu'
            #snippet += '    bkg_ggH_hmm_16  bkg_qqH_hmm_16  bkg_ttH_hmm_16  bkg_ZH_hmm_16   bkg_WH_hmm_16'
            #snippet += '    bkg_ggH_hmm_17  bkg_qqH_hmm_17  bkg_ttH_hmm_17  bkg_ZH_hmm_17   bkg_WH_hmm_17'
            #snippet += '    bkg_ggH_hmm_18  bkg_qqH_hmm_18  bkg_ttH_hmm_18  bkg_ZH_hmm_18   bkg_WH_hmm_18'
            #snippet += '    bgr\n'

            #snippet += 'process'
            #num_list = np.linspace(-44, 1, num=46, dtype='int')
            #for num in num_list:
            #    snippet += f'   {num}'
            #snippet += '\n'

            snippet = 'rate    '

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

            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_gluglu_M{mass}_2016_lepton_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_vbf_M{mass}_2016_lepton_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_tth_M{mass}_2016_lepton_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_zh_M{mass}_2016_lepton_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_wplush_M{mass}_2016_lepton_{cat}']+yield_dict[f'hmumu_wminush_M{mass}_2016_lepton_{cat}'])
            
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_gluglu_M{mass}_2017_lepton_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_vbf_M{mass}_2017_lepton_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_tth_M{mass}_2017_lepton_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_zh_M{mass}_2017_lepton_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_wplush_M{mass}_2017_lepton_{cat}']+yield_dict[f'hmumu_wminush_M{mass}_2017_lepton_{cat}'])
            
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_gluglu_M{mass}_2018_lepton_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_vbf_M{mass}_2018_lepton_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_tth_M{mass}_2018_lepton_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_zh_M{mass}_2018_lepton_{cat}'])
            snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_wplush_M{mass}_2018_lepton_{cat}']+yield_dict[f'hmumu_wminush_M{mass}_2018_lepton_{cat}'])
        

            snippet += '1.000000\n'
            #snippet += '-------------------------------------------------------------\n'
            #text_file = open('yields/rate_snippets/{0}_inclusive_{1}.txt'.format(cat, mass), 'w')
            #text_file.write(snippet)
            #text_file.close()
            output_datacard = open(f'datacards/card_run2_comb_{cat_num[i]}_{mass}_m105_mod.txt', 'w')
            with open(f'datacard_examples/card_run2_comb_{cat_num[i]}_{mass}_m105.txt') as ref_datacard:
                line = ref_datacard.readline()
                while line:
                    if 'rate' in line:
                        #print(line)
                        line = snippet
                    output_datacard.write(line)
                    #output_datacard.write('\n')
                    line = ref_datacard.readline()
            output_datacard.close()
                        
    #lepton tag
    for mass in [120, 121, 122, 123, 124, 125, 125.38, 126, 127, 128, 129, 130]:
        #snippet = 'bin'
        #snippet += f'    cat{cat_num[i]}'*31
        #snippet += '\n'

        #snippet += 'process'
        #snippet += '    ggH_hzg_16_ele_mu  qqH_hzg_16_ele_mu  ttH_zg_16_ele_mu   ZH_hzg_16_ele_mu   WH_hzg_16_ele_mu'
        #snippet += '    ggH_hzg_17_ele_mu  qqH_hzg_17_ele_mu  ttH_zg_17_ele_mu   ZH_hzg_17_ele_mu   WH_hzg_17_ele_mu'
        #snippet += '    ggH_hzg_18_ele_mu  qqH_hzg_18_ele_mu  ttH_zg_18_ele_mu   ZH_hzg_18_ele_mu   WH_hzg_18_ele_mu'
        #snippet += '    bkg_ggH_hmm_16  bkg_qqH_hmm_16  bkg_ttH_hmm_16  bkg_ZH_hmm_16   bkg_WH_hmm_16'
        #snippet += '    bkg_ggH_hmm_17  bkg_qqH_hmm_17  bkg_ttH_hmm_17  bkg_ZH_hmm_17   bkg_WH_hmm_17'
        #snippet += '    bkg_ggH_hmm_18  bkg_qqH_hmm_18  bkg_ttH_hmm_18  bkg_ZH_hmm_18   bkg_WH_hmm_18'
        #snippet += '    bgr\n'

        #snippet += 'process'
        #num_list = np.linspace(-29, 1, num=31, dtype='int')
        #for num in num_list:
        #    snippet += f'   {num}'
        #snippet += '\n'

        snippet = 'rate    '

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
            
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_gluglu_M{mass}_2016_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_vbf_M{mass}_2016_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_tth_M{mass}_2016_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_zh_M{mass}_2016_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_wplush_M{mass}_2016_lepton_lepton']+yield_dict[f'hmumu_wminush_M{mass}_2016_lepton_lepton'])
        
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_gluglu_M{mass}_2017_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_vbf_M{mass}_2017_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_tth_M{mass}_2017_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_zh_M{mass}_2017_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_wplush_M{mass}_2017_lepton_lepton']+yield_dict[f'hmumu_wminush_M{mass}_2017_lepton_lepton'])
        
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_gluglu_M{mass}_2018_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_vbf_M{mass}_2018_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_tth_M{mass}_2018_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_zh_M{mass}_2018_lepton_lepton'])
        snippet += '{0:.6f}     '.format(yield_dict[f'hmumu_wplush_M{mass}_2018_lepton_lepton']+yield_dict[f'hmumu_wminush_M{mass}_2018_lepton_lepton'])
        

        snippet += '1.000000\n'
        #snippet += '-------------------------------------------------------------\n'

        output_datacard = open(f'datacards/card_run2_comb_6789_{mass}_m105_mod.txt', 'w')
        with open(f'datacard_examples/card_run2_comb_6789_{mass}_m105.txt') as ref_datacard:
            line = ref_datacard.readline()
            while line:
                if 'rate' in line:
                    #print(line)
                    line = snippet
                output_datacard.write(line)
                output_datacard.write('\n')
                line = ref_datacard.readline()
        output_datacard.close()
        
        #text_file = open('yields/rate_snippets/lepton_inclusive_{0}.txt'.format(mass), 'w')
        #text_file.write(snippet)
        #text_file.close()
