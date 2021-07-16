#!/usr/bin/env python

import pickle
import ROOT as r
from rootpy.tree import Tree
from rootpy.io import root_open
import array 
import numpy as np
import pandas as pd
from tqdm import tqdm, trange
import itertools

r.gStyle.SetOptStat(0)

def fill_cat_tree(tree_dict, tag, cat, event, useKinFit=False):
    if useKinFit:
        #tree_dict['{0}_{1}'.format(tag, cat)].CMS_hzg_mass = event.llgMKin
        tree_dict['{0}_{1}'.format(tag, cat)].CMS_hzg_mass = event.llgMKinMY
    else:
        tree_dict['{0}_{1}'.format(tag, cat)].CMS_hzg_mass = event.llgM

    tree_dict['{0}_{1}'.format(tag, cat)].mll = event.dileptonM
    tree_dict['{0}_{1}'.format(tag, cat)].llgMRaw = event.llgM
    tree_dict['{0}_{1}'.format(tag, cat)].REFIT_mll = event.dileptonMKin
    tree_dict['{0}_{1}'.format(tag, cat)].eventWeight = event.eventWeight*event.genWeight*event.mc_sf*event.pt_weight
    tree_dict['{0}_{1}'.format(tag, cat)].vbf_bdt = event.vbf_bdt
    tree_dict['{0}_{1}'.format(tag, cat)].kin_bdt = event.kin_bdt
    #tree_dict['{0}_{1}'.format(tag, cat)].evt = event.evtNumber
    #tree_dict['{0}_{1}'.format(tag, cat)].run = event.runNumber
    #tree_dict['{0}_{1}'.format(tag, cat)].lumi = event.lumiSection
    tree_dict['{0}_{1}'.format(tag, cat)].Fill()

if __name__ == '__main__':

    signal_16_M120 = ['hzg_gluglu_M120_2016', 'hzg_tth_M120_2016', 'hzg_vbf_M120_2016', 'hzg_wplush_M120_2016', 'hzg_wminush_M120_2016', 'hzg_zh_M120_2016']
    signal_16_M125 = ['hzg_gluglu_M125_2016', 'hzg_tth_M125_2016', 'hzg_vbf_M125_2016', 'hzg_wplush_M125_2016', 'hzg_wminush_M125_2016', 'hzg_zh_M125_2016']
    signal_16_M130 = ['hzg_gluglu_M130_2016', 'hzg_tth_M130_2016', 'hzg_vbf_M130_2016', 'hzg_wplush_M130_2016', 'hzg_wminush_M130_2016', 'hzg_zh_M130_2016']
    background_16 = ['zjets_M50_2016', 'zg_llg_2016']
    hmumu_background_16_M120 = ['hmumu_gluglu_M120_2016', 'hmumu_tth_M120_2016', 'hmumu_vbf_M120_2016', 'hmumu_wplush_M120_2016', 'hmumu_wminush_M120_2016', 'hmumu_zh_M120_2016']
    hmumu_background_16_M125 = ['hmumu_gluglu_M125_2016', 'hmumu_tth_M125_2016', 'hmumu_vbf_M125_2016', 'hmumu_wplush_M125_2016', 'hmumu_wminush_M125_2016', 'hmumu_zh_M125_2016']
    hmumu_background_16_M130 = ['hmumu_gluglu_M130_2016', 'hmumu_tth_M130_2016', 'hmumu_vbf_M130_2016', 'hmumu_wplush_M130_2016', 'hmumu_wminush_M130_2016', 'hmumu_zh_M130_2016']
    muon_data_16 = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
                 'muon_2016F', 'muon_2016G', 'muon_2016H']
    electron_data_16 = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                     'electron_2016F', 'electron_2016G', 'electron_2016H']

    signal_17_M120 = ['hzg_gluglu_M120_2017', 'hzg_tth_M120_2017', 'hzg_vbf_M120_2017', 'hzg_wplush_M120_2017', 'hzg_wminush_M120_2017', 'hzg_zh_M120_2017']
    signal_17_M125 = ['hzg_gluglu_M125_2017', 'hzg_tth_M125_2017', 'hzg_vbf_M125_2017', 'hzg_wplush_M125_2017', 'hzg_wminush_M125_2017', 'hzg_zh_M125_2017']
    signal_17_M130 = ['hzg_gluglu_M130_2017', 'hzg_tth_M130_2017', 'hzg_vbf_M130_2017', 'hzg_wplush_M130_2017', 'hzg_wminush_M130_2017', 'hzg_zh_M130_2017']
    background_17 = ['zjets_M50_2017', 'zg_llg_2017'] 
    hmumu_background_17_M120 = ['hmumu_gluglu_M120_2017', 'hmumu_tth_M120_2017', 'hmumu_vbf_M120_2017', 'hmumu_wplush_M120_2017', 'hmumu_wminush_M120_2017', 'hmumu_zh_M120_2017']
    hmumu_background_17_M125 = ['hmumu_gluglu_M125_2017', 'hmumu_tth_M125_2017', 'hmumu_vbf_M125_2017', 'hmumu_wplush_M125_2017', 'hmumu_wminush_M125_2017', 'hmumu_zh_M125_2017']
    hmumu_background_17_M130 = ['hmumu_gluglu_M130_2017', 'hmumu_tth_M130_2017', 'hmumu_vbf_M130_2017', 'hmumu_wplush_M130_2017', 'hmumu_wminush_M130_2017', 'hmumu_zh_M130_2017']
    muon_data_17 = ['muon_2017B', 'muon_2017C', 'muon_2017D', 'muon_2017E', 'muon_2017F']
    electron_data_17 = ['electron_2017B', 'electron_2017C', 'electron_2017D', 'electron_2017E', 'electron_2017F'] 
    
    signal_18_M120 = ['hzg_gluglu_M120_2018', 'hzg_tth_M120_2018', 'hzg_vbf_M120_2018', 'hzg_wplush_M120_2018', 'hzg_wminush_M120_2018', 'hzg_zh_M120_2018']
    signal_18_M125 = ['hzg_gluglu_M125_2018', 'hzg_tth_M125_2018', 'hzg_vbf_M125_2018', 'hzg_wplush_M125_2018', 'hzg_wminush_M125_2018', 'hzg_zh_M125_2018']
    signal_18_M130 = ['hzg_gluglu_M130_2018', 'hzg_tth_M130_2018', 'hzg_vbf_M130_2018', 'hzg_wplush_M130_2018', 'hzg_wminush_M130_2018', 'hzg_zh_M130_2018']
    background_18 = ['zjets_M50_2018', 'zg_llg_2018'] 
    hmumu_background_18_M120 = ['hmumu_gluglu_M120_2018', 'hmumu_tth_M120_2018', 'hmumu_vbf_M120_2018', 'hmumu_wplush_M120_2018', 'hmumu_wminush_M120_2018', 'hmumu_zh_M120_2018']
    hmumu_background_18_M125 = ['hmumu_gluglu_M125_2018', 'hmumu_tth_M125_2018', 'hmumu_vbf_M125_2018', 'hmumu_wplush_M125_2018', 'hmumu_wminush_M125_2018', 'hmumu_zh_M125_2018']
    hmumu_background_18_M130 = ['hmumu_gluglu_M130_2018', 'hmumu_tth_M130_2018', 'hmumu_vbf_M130_2018', 'hmumu_wplush_M130_2018', 'hmumu_wminush_M130_2018', 'hmumu_zh_M130_2018']
    muon_data_18 = ['muon_2018A', 'muon_2018B', 'muon_2018C', 'muon_2018D']
    electron_data_18 = ['electron_2018A', 'electron_2018B', 'electron_2018C', 'electron_2018D'] 

    samples = {
                2016: { 'mmg': signal_16_M120 + signal_16_M125 + signal_16_M130 + 
                               background_16 + hmumu_background_16_M120 + hmumu_background_16_M125 + hmumu_background_16_M130 + muon_data_16, 
                        'eeg': signal_16_M120 + signal_16_M125 + signal_16_M130 + 
                               background_16 + hmumu_background_16_M120 + hmumu_background_16_M125 + hmumu_background_16_M130 + electron_data_16},
                2017: { 'mmg': signal_17_M120 + signal_17_M125 + signal_17_M130 + 
                               background_17 + hmumu_background_17_M120 + hmumu_background_17_M125 + hmumu_background_17_M130 + muon_data_17, 
                        'eeg': signal_17_M120 + signal_17_M125 + signal_17_M130 + 
                               background_17 + hmumu_background_17_M120 + hmumu_background_17_M125 + hmumu_background_17_M130 + electron_data_17},
                2018: { 'mmg': signal_18_M120 + signal_18_M125 + signal_18_M130 + 
                               background_18 + hmumu_background_18_M120 + hmumu_background_18_M125 + hmumu_background_18_M130 + muon_data_18, 
                        'eeg': signal_18_M120 + signal_18_M125 + signal_18_M130 + 
                               background_18 + hmumu_background_18_M120 + hmumu_background_18_M125 + hmumu_background_18_M130 + electron_data_18}
                }

    signal_samples = {
                        2016: {120: signal_16_M120, 125: signal_16_M125, 130: signal_16_M130}, 
                        2017: {120: signal_17_M120, 125: signal_17_M125, 130: signal_17_M130}, 
                        2018: {120: signal_18_M120, 125: signal_18_M125, 130: signal_18_M130}
                        }

    background_samples = {2016: background_16 + hmumu_background_16_M120 + hmumu_background_16_M125 + hmumu_background_16_M130, 
                          2017: background_17 + hmumu_background_17_M120 + hmumu_background_17_M125 + hmumu_background_17_M130,
                          2018: background_18 + hmumu_background_18_M120 + hmumu_background_18_M125 + hmumu_background_18_M130}
    data_samples = {
                    2016: muon_data_16 + electron_data_16,
                    2017: muon_data_17 + electron_data_17,
                    2018: muon_data_18 + electron_data_18
                    }
    
    category_scheme = 'optimal'
    #category_scheme = 'nominal'
    
    channels = ['mmg', 'eeg']
    periods = [2016, 2017, 2018]
    masses = [120, 125, 130]

    if category_scheme == 'nominal':
        categories = ['lepton', 'dijet', 'boosted', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']

    elif category_scheme == 'optimal':
        categories = ['lepton', 'dijet_1', 'dijet_2', 'dijet_3', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4', 'bkg_removal']
        #kin_bdt_cut_dict = pickle.load(open('data/mva_cuts/golden_1/kin_cuts.pkl', 'rb'))
        #vbf_bdt_cut_dict = pickle.load(open('data/mva_cuts/golden_1/vbf_cuts.pkl', 'rb'))
        kin_bdt_cut_dict = pickle.load(open('data/mva_cuts/kin_cuts.pkl', 'rb'))
        vbf_bdt_cut_dict = pickle.load(open('data/mva_cuts/vbf_cuts.pkl', 'rb'))
        #kin_bdt_cut_dict = pickle.load(open('data/mva_cuts/golden_1/kin_cuts.pkl', 'rb'))
        #vbf_bdt_cut_dict = pickle.load(open('data/mva_cuts/golden_1/vbf_cuts.pkl', 'rb'))
 
    # This is how we need to organize the data for limits
    print('categorizing for limits')

    #lepton_mingyan = pd.read_csv('data/mingyan_final_data/cat_leptag.csv')
    #dijet_1_mingyan = pd.read_csv('data/mingyan_final_data/dijet1.csv')
    #dijet_2_mingyan = pd.read_csv('data/mingyan_final_data/dijet2.csv')
    #dijet_3_mingyan = pd.read_csv('data/mingyan_final_data/dijet3.csv')
    #untagged_1_mingyan = pd.read_csv('data/mingyan_final_data/untag1.csv')
    #untagged_2_mingyan = pd.read_csv('data/mingyan_final_data/untag2.csv')
    #untagged_3_mingyan = pd.read_csv('data/mingyan_final_data/untag3.csv')
    #untagged_4_mingyan = pd.read_csv('data/mingyan_final_data/untag4.csv')
    #dijet_mingyan = pd.concat([dijet_1_mingyan, dijet_2_mingyan, dijet_3_mingyan])
    #untagged_mingyan = pd.concat([untagged_1_mingyan, untagged_2_mingyan, untagged_3_mingyan, untagged_4_mingyan])

    james_exclusive = pd.read_csv('unblinding_checks/data/james_exclusive.csv')
    
    #for period, channel in itertools.product(periods, channels):
    #    datasets = samples[period][channel]
    #    if datasets == []:
    #        continue
    #    print('running over: {0}, {1}'.format(period, channel))
    #    #inputFile = root_open('data/step3_vbf_bdt/output_{0}_{1}.root'.format(channel, period))
    #    #outputFile = root_open('data/step4_cats/output_{0}_{1}.root'.format(channel, period), 'recreate')
    #    inputFile = root_open('data/step3_vbf_bdt/output_{0}_{1}.root'.format(channel, period))
    #    outputFile = root_open('data/step4_cats/output_{0}_{1}.root'.format(channel, period), 'recreate')

    #    if category_scheme == 'optimal':
    #        vbf_bdt_cutvals = vbf_bdt_cut_dict['Ming-Yan']
    #        kin_bdt_cutvals = kin_bdt_cut_dict['Ming-Yan']
    #        #vbf_bdt_cutvals = vbf_bdt_cut_dict['James']
    #        #kin_bdt_cutvals = kin_bdt_cut_dict['James']
    #        
    #    outTree_dict = {}
    #    for cat in categories:
    #        outTree_dict['data_{0}'.format(cat)] = Tree('data_{0}'.format(cat))
    #        outTree_dict['bkg_{0}'.format(cat)] = Tree('bkg_{0}'.format(cat))
    #        outTree_dict['data_{0}'.format(cat)].create_branches({'CMS_hzg_mass': 'F'})
    #        outTree_dict['bkg_{0}'.format(cat)].create_branches({'CMS_hzg_mass': 'F'})
    #        outTree_dict['data_{0}'.format(cat)].create_branches({'mll': 'F'})
    #        outTree_dict['bkg_{0}'.format(cat)].create_branches({'mll': 'F'})
    #        outTree_dict['data_{0}'.format(cat)].create_branches({'llgMRaw': 'F'})
    #        outTree_dict['bkg_{0}'.format(cat)].create_branches({'llgMRaw': 'F'})
    #        outTree_dict['data_{0}'.format(cat)].create_branches({'REFIT_mll': 'F'})
    #        outTree_dict['bkg_{0}'.format(cat)].create_branches({'REFIT_mll': 'F'})
    #        outTree_dict['data_{0}'.format(cat)].create_branches({'eventWeight': 'F'})
    #        outTree_dict['bkg_{0}'.format(cat)].create_branches({'eventWeight': 'F'})
    #        outTree_dict['data_{0}'.format(cat)].create_branches({'vbf_bdt': 'F'})
    #        outTree_dict['bkg_{0}'.format(cat)].create_branches({'vbf_bdt': 'F'})
    #        outTree_dict['data_{0}'.format(cat)].create_branches({'kin_bdt': 'F'})
    #        outTree_dict['bkg_{0}'.format(cat)].create_branches({'kin_bdt': 'F'})
    #        #outTree_dict['data_{0}'.format(cat)].create_branches({'evt': 'UL'})
    #        #outTree_dict['bkg_{0}'.format(cat)].create_branches({'evt': 'UL'})
    #        #outTree_dict['data_{0}'.format(cat)].create_branches({'run': 'UI'})
    #        #outTree_dict['bkg_{0}'.format(cat)].create_branches({'run': 'UI'})
    #        #outTree_dict['data_{0}'.format(cat)].create_branches({'lumi': 'I'})
    #        #outTree_dict['bkg_{0}'.format(cat)].create_branches({'lumi': 'I'})
    #        for mass in masses:
    #            outTree_dict['sig_{0}_{1}'.format(mass, cat)] = Tree('sig_{0}_{1}'.format(mass, cat))
    #            outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'CMS_hzg_mass': 'F'})
    #            outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'mll': 'F'})
    #            outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'llgMRaw': 'F'})
    #            outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'REFIT_mll': 'F'})
    #            outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'eventWeight': 'F'})
    #            outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'vbf_bdt': 'F'})
    #            outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'kin_bdt': 'F'})
    #            #outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'evt': 'UL'})
    #            #outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'run': 'UI'})
    #            #outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'lumi': 'I'})

    #    for dataset in tqdm(datasets):
    #        tree = inputFile[dataset]
    #        #tree.create_buffer()
    #        #for cat in categories:
    #        #    #outTree_dict['data_{0}'.format(cat)] = Tree('data_{0}'.format(cat))
    #        #    outTree_dict['data_{0}'.format(cat)].set_buffer(tree._buffer, create_branches=True)
    #        #    #outTree_dict['bkg_{0}'.format(cat)] = Tree('bkg_{0}'.format(cat))
    #        #    outTree_dict['bkg_{0}'.format(cat)].set_buffer(tree._buffer, create_branches=True)
    #        #    #outTree_dict['data_{0}'.format(cat)].create_branches({'CMS_hzg_mass': 'F'})
    #        #    #outTree_dict['bkg_{0}'.format(cat)].create_branches({'CMS_hzg_mass': 'F'})
    #        #    #outTree_dict['data_{0}'.format(cat)].create_branches({'mll': 'F'})
    #        #    #outTree_dict['bkg_{0}'.format(cat)].create_branches({'mll': 'F'})
    #        #    #outTree_dict['data_{0}'.format(cat)].create_branches({'REFIT_mll': 'F'})
    #        #    #outTree_dict['bkg_{0}'.format(cat)].create_branches({'REFIT_mll': 'F'})
    #        #    #outTree_dict['data_{0}'.format(cat)].create_branches({'eventWeight': 'F'})
    #        #    #outTree_dict['bkg_{0}'.format(cat)].create_branches({'eventWeight': 'F'})
    #        #    #outTree_dict['data_{0}'.format(cat)].create_branches({'vbf_bdt': 'F'})
    #        #    #outTree_dict['bkg_{0}'.format(cat)].create_branches({'vbf_bdt': 'F'})
    #        #    #outTree_dict['data_{0}'.format(cat)].create_branches({'kin_bdt': 'F'})
    #        #    #outTree_dict['bkg_{0}'.format(cat)].create_branches({'kin_bdt': 'F'})
    #        #    for mass in masses:
    #        #        #outTree_dict['sig_{0}_{1}'.format(mass, cat)] = Tree('sig_{0}_{1}'.format(mass, cat))
    #        #        outTree_dict['sig_{0}_{1}'.format(mass, cat)].set_buffer(tree._buffer, create_branches=True)
    #        #        #outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'CMS_hzg_mass': 'F'})
    #        #        #outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'mll': 'F'})
    #        #        #outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'REFIT_mll': 'F'})
    #        #        #outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'eventWeight': 'F'})
    #        #        #outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'vbf_bdt': 'F'})
    #        #        #outTree_dict['sig_{0}_{1}'.format(mass, cat)].create_branches({'kin_bdt': 'F'})

    #        sig_tag = ''
    #        if dataset in background_samples[period]:
    #            sig_tag = 'bkg'
    #        elif dataset in data_samples[period]:
    #            sig_tag = 'data'
    #        else: 
    #            for mass in masses:
    #                if dataset in signal_samples[period][mass]:
    #                    sig_tag = 'sig_{0}'.format(mass)

    #        for evt in tree:
    #            if evt.llgMKinMY < 105. or evt.llgMKinMY > 170.:
    #                continue
    #            if dataset in data_samples[period]:
    #                this_james_exclusive = james_exclusive.query('run == {0} and lumi == {1} and evt == {2}'.format(evt.runNumber, evt.lumiSection, evt.evtNumber))
    #                if this_james_exclusive.shape[0] > 0:
    #                    continue
    #            #if evt.llgMKinMY < 116. and evt.llgMKinMY == evt.llgMKin:
    #            #    continue
    #            #if evt.llgMKin < 115. or evt.llgMKin > 170.:
    #            #    continue
    #            kin_bdt = evt.kin_bdt
    #            vbf_bdt = evt.vbf_bdt
    #            #kin_bdt = evt.kin_bdt_james
    #            #vbf_bdt = evt.vbf_bdt_james
    #            #if category_scheme == 'optimal' and kin_bdt < kin_bdt_cutvals[0]:
    #            #    continue

    #            # recategorize to Ming-Yan
    #            #if dataset in data_samples[period]:
    #            #    this_my_lepton = lepton_mingyan.query('run == {0} and lumi == {1} and evt == {2}'.format(evt.runNumber, evt.lumiSection, evt.evtNumber))
    #            #    this_my_dijet = dijet_mingyan.query('run == {0} and lumi == {1} and evt == {2}'.format(evt.runNumber, evt.lumiSection, evt.evtNumber))
    #            #    this_my_untagged = untagged_mingyan.query('run == {0} and lumi == {1} and evt == {2}'.format(evt.runNumber, evt.lumiSection, evt.evtNumber))
    #            #    if this_my_lepton.shape[0] > 0:
    #            #        evt.isLeptonTag = 1.
    #            #        evt.isDijetTag = 0.
    #            #    elif this_my_dijet.shape[0] > 0:
    #            #        evt.isLeptonTag = 0.
    #            #        evt.isDijetTag = 1.
    #            #        evt.vbf_bdt = this_my_dijet.vbf_bdt.values[0]
    #            #    elif this_my_untagged.shape[0] > 0:
    #            #        evt.isLeptonTag = 0.
    #            #        evt.isDijetTag = 0. 
    #            #        evt.kin_bdt = this_my_untagged.kin_bdt.values[0]

    #            if category_scheme == 'nominal': 
    #                if evt.isLeptonTag:
    #                    fill_cat_tree(outTree_dict, sig_tag, 'lepton', evt, useKinFit=False)
    #                elif evt.isDijetTag:
    #                    fill_cat_tree(outTree_dict, sig_tag, 'dijet', evt, useKinFit=False)
    #                elif evt.llgPt >= 60.0:
    #                    fill_cat_tree(outTree_dict, sig_tag, 'boosted', evt, useKinFit=False)
    #                else:
    #                    if channel == 'mmg':
    #                        if abs(evt.photonOneEta) < 1.4442:
    #                            if ((abs(evt.leptonOneEta) < 2.1 and abs(evt.leptonTwoEta) < 2.1) and
    #                               (abs(evt.leptonOneEta) < 0.9 or  abs(evt.leptonTwoEta) < 0.9)):
    #                                if evt.photonOneR9 > 0.94:
    #                                    fill_cat_tree(outTree_dict, sig_tag, 'untagged_1',
    #                                                  evt, useKinFit=False)
    #                                else:
    #                                    fill_cat_tree(outTree_dict, sig_tag, 'untagged_2', 
    #                                                  evt, useKinFit=False)
    #                            else:
    #                                fill_cat_tree(outTree_dict, sig_tag, 'untagged_3', 
    #                                              evt, useKinFit=False)
    #                        else:
    #                            fill_cat_tree(outTree_dict, sig_tag, 'untagged_4', 
    #                                          evt, useKinFit=False)
    #                    elif channel == 'eeg':
    #                        if abs(evt.photonOneEta) < 1.4442:
    #                            if (abs(evt.leptonOneEta) < 1.4442 and 
    #                                abs(evt.leptonTwoEta) < 1.4442):
    #                                if evt.photonOneR9 > 0.94: 
    #                                    fill_cat_tree(outTree_dict, sig_tag, 'untagged_1',
    #                                                  evt, useKinFit=False)
    #                                else:
    #                                    fill_cat_tree(outTree_dict, sig_tag, 'untagged_2',
    #                                                  evt, useKinFit=False)
    #                            else:
    #                                fill_cat_tree(outTree_dict, sig_tag, 'untagged_3', 
    #                                              evt, useKinFit=False)
    #                        else:
    #                            fill_cat_tree(outTree_dict, sig_tag, 'untagged_4', 
    #                                          evt, useKinFit=False)
    #            
    #            elif category_scheme == 'optimal':
    #                if evt.isLeptonTag:
    #                    fill_cat_tree(outTree_dict, sig_tag, 'lepton', evt, useKinFit=True)
    #                else:
    #                    if evt.isDijetTag:
    #                        if vbf_bdt > vbf_bdt_cutvals['dijet_1']: 
    #                            fill_cat_tree(outTree_dict, sig_tag, 'dijet_1', evt, useKinFit=True)
    #                        elif vbf_bdt_cutvals['dijet_2'] < vbf_bdt <= vbf_bdt_cutvals['dijet_1']:
    #                            fill_cat_tree(outTree_dict, sig_tag, 'dijet_2', evt, useKinFit=True)
    #                        else:
    #                            fill_cat_tree(outTree_dict, sig_tag, 'dijet_3', evt, useKinFit=True)
    #                    else:
    #                        if kin_bdt > kin_bdt_cutvals['untagged_1']:
    #                            fill_cat_tree(outTree_dict, sig_tag, 'untagged_1', evt, useKinFit=True)
    #                        elif kin_bdt_cutvals['untagged_2'] < kin_bdt <= kin_bdt_cutvals['untagged_1']:
    #                            fill_cat_tree(outTree_dict, sig_tag, 'untagged_2', evt, useKinFit=True)
    #                        elif kin_bdt_cutvals['untagged_3'] < kin_bdt <= kin_bdt_cutvals['untagged_2']:
    #                            fill_cat_tree(outTree_dict, sig_tag, 'untagged_3', evt, useKinFit=True)
    #                        elif kin_bdt_cutvals['untagged_4'] < kin_bdt <= kin_bdt_cutvals['untagged_3']:
    #                            fill_cat_tree(outTree_dict, sig_tag, 'untagged_4', evt, useKinFit=True)
    #                        else:
    #                            fill_cat_tree(outTree_dict, sig_tag, 'bkg_removal', evt, useKinFit=True)

    #    for cat in categories:
    #        outTree_dict['data_{0}'.format(cat)].Write()
    #        outTree_dict['bkg_{0}'.format(cat)].Write()
    #        for mass in masses:
    #            outTree_dict['sig_{0}_{1}'.format(mass, cat)].Write()
    #    
    #    outputFile.Close()
    #    inputFile.Close()

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
            #vbf_bdt_cutvals = vbf_bdt_cut_dict[period]
            #kin_bdt_cutvals = kin_bdt_cut_dict[channel][period]
            vbf_bdt_cutvals = vbf_bdt_cut_dict['Ming-Yan']
            kin_bdt_cutvals = kin_bdt_cut_dict['Ming-Yan']
            #vbf_bdt_cutvals = vbf_bdt_cut_dict['James']
            #kin_bdt_cutvals = kin_bdt_cut_dict['James']

        for dataset in tqdm(datasets):
            outTree_dict = {}
            tree = inputFile[dataset]
            tree.create_buffer()
            for cat in categories:
                outTree_dict['{0}_{1}'.format(dataset, cat)] = Tree('{0}_{1}'.format(dataset, cat))
                outTree_dict['{0}_{1}'.format(dataset, cat)].set_buffer(tree._buffer, create_branches=True)
                outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'CMS_hzg_mass': 'F'})
                outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'mll': 'F'})
                outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'llgMRaw': 'F'})
                outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'REFIT_mll': 'F'})
                outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'evt': 'F'})
                outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'run': 'F'})
                outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'lumi': 'F'})
                #outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'vbf_bdt': 'F'})
                #outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'kin_bdt': 'F'})

            for evt in tree:
                if evt.llgMKinMY < 105. or evt.llgMKinMY > 170.:
                    continue
                #if evt.llgMKinMY < 116. and evt.llgMKinMY == evt.llgMKin:
                #    continue
                #if evt.llgMKin < 115. or evt.llgMKin > 170.:
                #    continue
                kin_bdt = evt.kin_bdt
                vbf_bdt = evt.vbf_bdt
                #kin_bdt = evt.kin_bdt_james
                #vbf_bdt = evt.vbf_bdt_james
                
                if category_scheme == 'nominal': 
                    if evt.isLeptonTag:
                        fill_cat_tree(outTree_dict, dataset, 'lepton', evt, useKinFit=False)
                    if evt.isDijetTag:
                        fill_cat_tree(outTree_dict, dataset, 'dijet', evt, useKinFit=False)
                    elif evt.llgPt >= 60.0:
                        fill_cat_tree(outTree_dict, dataset, 'boosted', evt, useKinFit=False)
                    else:
                        if channel == 'mmg':
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
                        elif channel == 'eeg':
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
                    if evt.isLeptonTag:
                        fill_cat_tree(outTree_dict, dataset, 'lepton', evt, useKinFit=True)
                    else:
                        if evt.isDijetTag:
                            if vbf_bdt > vbf_bdt_cutvals['dijet_1']: 
                                fill_cat_tree(outTree_dict, dataset, 'dijet_1', evt, useKinFit=True)
                            elif vbf_bdt_cutvals['dijet_2'] < vbf_bdt <= vbf_bdt_cutvals['dijet_1']:
                                fill_cat_tree(outTree_dict, dataset, 'dijet_2', evt, useKinFit=True)
                            else:
                                fill_cat_tree(outTree_dict, dataset, 'dijet_3', evt, useKinFit=True)
                        else:
                            if kin_bdt > kin_bdt_cutvals['untagged_1']:
                                fill_cat_tree(outTree_dict, dataset, 'untagged_1', evt, useKinFit=True)
                            elif kin_bdt_cutvals['untagged_2'] < kin_bdt <= kin_bdt_cutvals['untagged_1']:
                                fill_cat_tree(outTree_dict, dataset, 'untagged_2', evt, useKinFit=True)
                            elif kin_bdt_cutvals['untagged_3'] < kin_bdt <= kin_bdt_cutvals['untagged_2']:
                                fill_cat_tree(outTree_dict, dataset, 'untagged_3', evt, useKinFit=True)
                            elif kin_bdt_cutvals['untagged_4'] < kin_bdt <= kin_bdt_cutvals['untagged_3']:
                                fill_cat_tree(outTree_dict, dataset, 'untagged_4', evt, useKinFit=True)
                            else:
                                fill_cat_tree(outTree_dict, dataset, 'bkg_removal', evt, useKinFit=True)


            for cat in categories:
                outTree_dict['{0}_{1}'.format(dataset, cat)].Write()
        
        outputFile.Close()
        inputFile.Close()
