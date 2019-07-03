#!/usr/bin/env python

import ROOT as r
from rootpy.tree import Tree
from rootpy.io import root_open
import array 
import numpy as np
from tqdm import tqdm, trange
import itertools

r.gStyle.SetOptStat(0)

def fill_cat_tree(tree_dict, tag, cat, event, useKinFit=False):
    if useKinFit:
        tree_dict['{0}_{1}'.format(tag, cat)].three_body_mass = event.llgMKin
    else:
        tree_dict['{0}_{1}'.format(tag, cat)].three_body_mass = event.llgM
    tree_dict['{0}_{1}'.format(tag, cat)].eventWeight = event.eventWeight
    tree_dict['{0}_{1}'.format(tag, cat)].Fill()

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
    
    category_scheme = 'optimal'
    #category_scheme = 'nominal'
    
    channels = ['mumug', 'elelg']
    periods = [2016, 2017]
    channels_rename = {'mumug': 'mmg', 'elelg': 'eeg'}

    if category_scheme == 'nominal':
        categories = ['lepton', 'dijet', 'boosted', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']

    elif category_scheme == 'optimal':
        categories = ['lepton', 'dijet_1', 'dijet_2', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
        kin_bdt_cut_dict = {'mumug': [-0.085, -0.0665, -0.02, 0.019], 'elelg': [-0.075, -0.06, -0.016, 0.022]}
 
    # This is how we need to organize the data for limits
    print('categorizing for limits')
    
    for period, channel in itertools.product(periods, channels):
        datasets = samples[period][channel]
        if datasets == []:
            continue
        print('running over: {0}, {1}'.format(period, channel))
        inputFile = root_open('data/step3_vbf_bdt/output_{0}_{1}.root'.format(channel, period))
        outputFile = root_open('data/step4_cats/output_{0}_{1}.root'.format(channel, period), 'recreate')

        if category_scheme == 'optimal':
            kin_bdt_cutvals = kin_bdt_cut_dict[channel]

        outTree_dict = {}
        for cat in categories:
            outTree_dict['sig_{0}'.format(cat)] = Tree('sig_{0}'.format(cat))
            outTree_dict['data_{0}'.format(cat)] = Tree('data_{0}'.format(cat))
            outTree_dict['bkg_{0}'.format(cat)] = Tree('bkg_{0}'.format(cat))
            outTree_dict['sig_{0}'.format(cat)].create_branches({'three_body_mass': 'F'})
            outTree_dict['data_{0}'.format(cat)].create_branches({'three_body_mass': 'F'})
            outTree_dict['bkg_{0}'.format(cat)].create_branches({'three_body_mass': 'F'})
            outTree_dict['sig_{0}'.format(cat)].create_branches({'eventWeight': 'F'})
            outTree_dict['data_{0}'.format(cat)].create_branches({'eventWeight': 'F'})
            outTree_dict['bkg_{0}'.format(cat)].create_branches({'eventWeight': 'F'})

        for dataset in tqdm(datasets):
            tree = inputFile[dataset]
            sig_tag = 'sig'
            if dataset == 'zjets_m-50_amc' or dataset == 'zg_llg':
                sig_tag = 'bkg'
            if channel == 'mumug':
                if dataset[:4] == 'muon':
                    sig_tag = 'data'
            elif channel == 'elelg':
                if dataset[:4] == 'elec':
                    sig_tag = 'data'

            for evt in tree:
                if dataset == 'zjets_m-50_amc' and evt.vetoDY:
                    continue
                kin_bdt = evt.kin_bdt
                vbf_bdt = evt.vbf_bdt
                if category_scheme == 'optimal' and kin_bdt < kin_bdt_cutvals[0]:
                    continue
                if category_scheme == 'optimal' and (evt.llgMKin < 115. or evt.llgMKin > 170.):
                    continue
                if category_scheme == 'nominal' and (evt.llgM < 115. or evt.llgM > 170.):
                    continue
                if evt.photonOnePt < 15. or evt.photonOnePt > 100.:
                    continue
                if category_scheme == 'nominal': 
                    if evt.isLeptonTag:
                        fill_cat_tree(outTree_dict, sig_tag, 'lepton', evt, useKinFit=False)
                    elif evt.isDijetTag:
                        fill_cat_tree(outTree_dict, sig_tag, 'dijet', evt, useKinFit=False)
                    elif evt.llgPt >= 60.0:
                        fill_cat_tree(outTree_dict, sig_tag, 'boosted', evt, useKinFit=False)
                    else:
                        if channel == 'mumug':
                            if abs(evt.photonOneEta) < 1.4442:
                                if ((abs(evt.leptonOneEta) < 2.1 and abs(evt.leptonTwoEta) < 2.1) and
                                   (abs(evt.leptonOneEta) < 0.9 or  abs(evt.leptonTwoEta) < 0.9)):
                                    if evt.photonOneR9 > 0.94:
                                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_1',
                                                      evt, useKinFit=False)
                                    else:
                                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_2', 
                                                      evt, useKinFit=False)
                                else:
                                    fill_cat_tree(outTree_dict, sig_tag, 'untagged_3', 
                                                  evt, useKinFit=False)
                            else:
                                fill_cat_tree(outTree_dict, sig_tag, 'untagged_4', 
                                              evt, useKinFit=False)
                        elif channel == 'elelg':
                            if abs(evt.photonOneEta) < 1.4442:
                                if (abs(evt.leptonOneEta) < 1.4442 and 
                                    abs(evt.leptonTwoEta) < 1.4442):
                                    if evt.photonOneR9 > 0.94: 
                                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_1',
                                                      evt, useKinFit=False)
                                    else:
                                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_2',
                                                      evt, useKinFit=False)
                                else:
                                    fill_cat_tree(outTree_dict, sig_tag, 'untagged_3', 
                                                  evt, useKinFit=False)
                            else:
                                fill_cat_tree(outTree_dict, sig_tag, 'untagged_4', 
                                              evt, useKinFit=False)
                
                elif category_scheme == 'optimal':
                    if evt.isLeptonTag:
                        fill_cat_tree(outTree_dict, sig_tag, 'lepton', evt, useKinFit=True)
                    elif vbf_bdt > 0.1: 
                        fill_cat_tree(outTree_dict, sig_tag, 'dijet_1', evt, useKinFit=True)
                    elif -0.01 < vbf_bdt <= 0.1:
                        fill_cat_tree(outTree_dict, sig_tag, 'dijet_2', evt, useKinFit=True)
                    elif kin_bdt_cutvals[0] <= kin_bdt < kin_bdt_cutvals[1]:
                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_1', evt, useKinFit=True)
                    elif kin_bdt_cutvals[1] <= kin_bdt < kin_bdt_cutvals[2]:
                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_2', evt, useKinFit=True)
                    elif kin_bdt_cutvals[2] <= kin_bdt < kin_bdt_cutvals[3]:
                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_3', evt, useKinFit=True)
                    elif kin_bdt >= kin_bdt_cutvals[3]:
                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_4', evt, useKinFit=True)

        for cat in categories:
            outTree_dict['sig_{0}'.format(cat)].Write()
            outTree_dict['data_{0}'.format(cat)].Write()
            outTree_dict['bkg_{0}'.format(cat)].Write()
        
        outputFile.Close()
        inputFile.Close()

    # We should also save the categories by dataset for yields
    print('saving categories by dataset for yields')
    for period, channel in itertools.product(periods, channels):
        datasets = samples[period][channel]
        if datasets == []:
            continue
        print('running over: {0}, {1}'.format(period, channel))
        inputFile = root_open('data/step3_vbf_bdt/output_{0}_{1}.root'.format(channel, period))
        outputFile = root_open('data/step4_cats/output_{0}_{1}_yields.root'.format(channel, period), 'recreate')

        if category_scheme == 'optimal':
            kin_bdt_cutvals = kin_bdt_cut_dict[channel]

        for dataset in tqdm(datasets):
            outTree_dict = {}
            tree = inputFile[dataset]
            tree.create_buffer()
            for cat in categories:
                outTree_dict['{0}_{1}'.format(dataset, cat)] = Tree('{0}_{1}'.format(dataset, cat))
                outTree_dict['{0}_{1}'.format(dataset, cat)].set_buffer(tree._buffer, create_branches=True)
                outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'three_body_mass': 'F'})

            for evt in tree:
                if dataset == 'zjets_m-50_amc' and evt.vetoDY:
                    continue
                kin_bdt = evt.kin_bdt
                vbf_bdt = evt.vbf_bdt
                if category_scheme == 'optimal' and kin_bdt < kin_bdt_cutvals[0]:
                    continue
                if category_scheme == 'optimal' and kin_bdt < kin_bdt_cutvals[0]:
                    continue
                if category_scheme == 'optimal' and (evt.llgMKin < 115. or evt.llgMKin > 170.):
                    continue
                if category_scheme == 'nominal' and (evt.llgM < 115. or evt.llgM > 170.):
                    continue
                if evt.photonOnePt < 15. or evt.photonOnePt > 100.:
                    continue
                
                if evt.isLeptonTag:
                    fill_cat_tree(outTree_dict, dataset, 'lepton', evt, useKinFit=False)

                if category_scheme == 'nominal': 
                    if evt.isDijetTag:
                        fill_cat_tree(outTree_dict, dataset, 'dijet', evt, useKinFit=False)
                    elif evt.llgPt >= 60.0:
                        fill_cat_tree(outTree_dict, dataset, 'boosted', evt, useKinFit=False)
                    else:
                        if channel == 'mumug':
                            if abs(evt.photonOneEta) < 1.4442:
                                if ((abs(evt.leptonOneEta) < 2.1 and abs(evt.leptonTwoEta) < 2.1) and
                                    (abs(evt.leptonOneEta) < 0.9 or  abs(evt.leptonTwoEta) < 0.9)):
                                    if evt.photonOneR9 > 0.94:
                                        fill_cat_tree(outTree_dict, dataset, 'untagged_1',
                                                      evt, useKinFit=False)
                                    else:
                                        fill_cat_tree(outTree_dict, dataset, 'untagged_2', 
                                                      evt, useKinFit=False)
                                else:
                                    fill_cat_tree(outTree_dict, dataset, 'untagged_3', 
                                                  evt, useKinFit=False)
                            else:
                                fill_cat_tree(outTree_dict, dataset, 'untagged_4', 
                                              evt, useKinFit=False)
                        elif channel == 'elelg':
                            if abs(evt.photonOneEta) < 1.4442:
                                if (abs(evt.leptonOneEta) < 1.4442 and 
                                    abs(evt.leptonTwoEta) < 1.4442):
                                    if evt.photonOneR9 > 0.94: 
                                        fill_cat_tree(outTree_dict, dataset, 'untagged_1',
                                                      evt, useKinFit=False)
                                    else:
                                        fill_cat_tree(outTree_dict, dataset, 'untagged_2',
                                                      evt, useKinFit=False)
                                else:
                                    fill_cat_tree(outTree_dict, dataset, 'untagged_3', 
                                                  evt, useKinFit=False)
                            else:
                                fill_cat_tree(outTree_dict, dataset, 'untagged_4', 
                                              evt, useKinFit=False)
                
                elif category_scheme == 'optimal':
                    if vbf_bdt > 0.1: 
                        fill_cat_tree(outTree_dict, dataset, 'dijet_1', evt, useKinFit=True)
                    elif -0.01 < vbf_bdt <= 0.1:
                        fill_cat_tree(outTree_dict, dataset, 'dijet_2', evt, useKinFit=True)
                    elif kin_bdt_cutvals[0] <= kin_bdt < kin_bdt_cutvals[1]:
                        fill_cat_tree(outTree_dict, dataset, 'untagged_1', evt, useKinFit=True)
                    elif kin_bdt_cutvals[1] <= kin_bdt < kin_bdt_cutvals[2]:
                        fill_cat_tree(outTree_dict, dataset, 'untagged_2', evt, useKinFit=True)
                    elif kin_bdt_cutvals[2] <= kin_bdt < kin_bdt_cutvals[3]:
                        fill_cat_tree(outTree_dict, dataset, 'untagged_3', evt, useKinFit=True)
                    elif kin_bdt >= kin_bdt_cutvals[3]:
                        fill_cat_tree(outTree_dict, dataset, 'untagged_4', evt, useKinFit=True)

            for cat in categories:
                outTree_dict['{0}_{1}'.format(dataset, cat)].Write()
        
        outputFile.Close()
        inputFile.Close()
