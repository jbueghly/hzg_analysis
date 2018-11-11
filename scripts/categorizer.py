#!/usr/bin/env python

import ROOT as r
from rootpy.tree import Tree
from rootpy.io import root_open
import array 
import numpy as np
from tqdm import tqdm, trange

if __name__ == '__main__':
    
    channels = ['mumug', 'elelg']

    mc = ['zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wh', 'hzg_zh']
    muon_data = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
                 'muon_2016F', 'muon_2016G', 'muon_2016H']
    electron_data = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                     'electron_2016F', 'electron_2016G', 'electron_2016H']

    #datasets = ['zjets_m-50_amc', 'zg_llg', 
    #            'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wh', 'hzg_zh',
    #            'muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
    #            'muon_2016F', 'muon_2016G', 'muon_2016H']
    data_dict = {'mumug': mc + muon_data, 'elelg': mc + electron_data}

    #categories = ['lepton', 'dijet', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
    categories = ['lepton', 'dijet_1', 'dijet_2', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
    #categories = ['lepton', 'dijet_1', 'dijet_2', 'untagged_11', 'untagged_12', 'untagged_2', 'untagged_21', 'untagged_22', 'untagged_3', 'untagged_4']
    #kin_bdt_cut_dict = {'mumug': [-0.03, 0.0095, 0.045, 0.115], 'elelg': [0.03, 0.042, 0.074, 0.1235]}
    kin_bdt_cut_dict = {'mumug': [-0.085, -0.0665, -0.02, 0.019], 'elelg': [-0.075, -0.06, -0.016, 0.022]}
    
    #inputFile = root_open('data/step2_kin_bdt/output_mumug_2016_flat.root')
    #outputFile = root_open('data/step4_cats/output_mmg_2016.root', 'recreate')

    # This is how we need to organize the data for limits
    print('categorizing for limits')
    for channel in channels:
        inputFile = root_open('data/step3_vbf_bdt/output_{0}_2016_flat.root'.format(channel))
        outputFile = root_open('data/step4_cats_new/output_{0}_2016.root'.format(channel), 'recreate')
        datasets = data_dict[channel]
        kin_bdt_cutvals = kin_bdt_cut_dict[channel]

        outTree_dict = {}
        for cat in categories:
            outTree_dict['sig_{0}'.format(cat)] = Tree('sig_{0}'.format(cat))
            outTree_dict['data_{0}'.format(cat)] = Tree('data_{0}'.format(cat))
            outTree_dict['sig_{0}'.format(cat)].create_branches({'three_body_mass': 'F'})
            outTree_dict['data_{0}'.format(cat)].create_branches({'three_body_mass': 'F'})
            outTree_dict['sig_{0}'.format(cat)].create_branches({'eventWeight': 'F'})
            outTree_dict['data_{0}'.format(cat)].create_branches({'eventWeight': 'F'})
        for dataset in tqdm(datasets):
            tree = inputFile[dataset]
            sig_tag = 'sig'
            if channel == 'mumug':
                if dataset[:4] == 'muon':
                    sig_tag = 'data'
            elif channel == 'elelg':
                if dataset[:4] == 'elec':
                    sig_tag = 'data'
            #tree.create_buffer()
            #outTree_dict['sig_{0}'.format(cat)].set_buffer(tree._buffer, create_branches=True)
            #outTree_dict['data_{0}'.format(cat)].set_buffer(tree._buffer, create_branches=True)
            #outTree_dict = {}
            #for cat in categories:
            #    outTree_dict[cat] = Tree('{0}_{1}'.format(dataset, cat))
            #    outTree_dict[cat].set_buffer(tree._buffer, create_branches=True)
            for evt in tree:
                if dataset == 'zjets_m-50_amc' and evt.vetoDY:
                    continue
                kin_bdt = evt.kin_bdt
                vbf_bdt = evt.vbf_bdt
                if kin_bdt < kin_bdt_cutvals[0]:
                    continue
                else:
                    if evt.isLeptonTag:
                        #outTree_dict['lepton'].Fill()
                        outTree_dict['{0}_lepton'.format(sig_tag)].three_body_mass = evt.llgM
                        outTree_dict['{0}_lepton'.format(sig_tag)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_lepton'.format(sig_tag)].Fill()
                    #elif evt.isDijetTag:
                    #    outTree_dict['{0}_dijet'.format(sig_tag)].three_body_mass = evt.llgM
                    #    outTree_dict['{0}_dijet'.format(sig_tag)].eventWeight = evt.eventWeight
                    #    outTree_dict['{0}_dijet'.format(sig_tag)].Fill()
                    elif vbf_bdt > 0.1: 
                        outTree_dict['{0}_dijet_1'.format(sig_tag)].three_body_mass = evt.llgM
                        outTree_dict['{0}_dijet_1'.format(sig_tag)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_dijet_1'.format(sig_tag)].Fill()
                    elif -0.01 < vbf_bdt <= 0.1:
                        outTree_dict['{0}_dijet_2'.format(sig_tag)].three_body_mass = evt.llgM
                        outTree_dict['{0}_dijet_2'.format(sig_tag)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_dijet_2'.format(sig_tag)].Fill()
                    elif kin_bdt_cutvals[0] <= kin_bdt < kin_bdt_cutvals[1]:
                        outTree_dict['{0}_untagged_1'.format(sig_tag)].three_body_mass = evt.llgM
                        outTree_dict['{0}_untagged_1'.format(sig_tag)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_untagged_1'.format(sig_tag)].Fill()
                        #if evt.photonOnePt < 25.:
                        #    outTree_dict['{0}_untagged_11'.format(sig_tag)].three_body_mass = evt.llgM
                        #    outTree_dict['{0}_untagged_11'.format(sig_tag)].eventWeight = evt.eventWeight
                        #    outTree_dict['{0}_untagged_11'.format(sig_tag)].Fill()
                        #else:
                        #    outTree_dict['{0}_untagged_12'.format(sig_tag)].three_body_mass = evt.llgM
                        #    outTree_dict['{0}_untagged_12'.format(sig_tag)].eventWeight = evt.eventWeight
                        #    outTree_dict['{0}_untagged_12'.format(sig_tag)].Fill()

                    elif kin_bdt_cutvals[1] <= kin_bdt < kin_bdt_cutvals[2]:
                        outTree_dict['{0}_untagged_2'.format(sig_tag)].three_body_mass = evt.llgM
                        outTree_dict['{0}_untagged_2'.format(sig_tag)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_untagged_2'.format(sig_tag)].Fill()
                        #if evt.photonOnePt < 25.:
                        #    outTree_dict['{0}_untagged_21'.format(sig_tag)].three_body_mass = evt.llgM
                        #    outTree_dict['{0}_untagged_21'.format(sig_tag)].eventWeight = evt.eventWeight
                        #    outTree_dict['{0}_untagged_21'.format(sig_tag)].Fill()
                        #else:
                        #    outTree_dict['{0}_untagged_22'.format(sig_tag)].three_body_mass = evt.llgM
                        #    outTree_dict['{0}_untagged_22'.format(sig_tag)].eventWeight = evt.eventWeight
                        #    outTree_dict['{0}_untagged_22'.format(sig_tag)].Fill()

                    elif kin_bdt_cutvals[2] <= kin_bdt < kin_bdt_cutvals[3]:
                        outTree_dict['{0}_untagged_3'.format(sig_tag)].three_body_mass = evt.llgM
                        outTree_dict['{0}_untagged_3'.format(sig_tag)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_untagged_3'.format(sig_tag)].Fill()
                    elif kin_bdt >= kin_bdt_cutvals[3]:
                        outTree_dict['{0}_untagged_4'.format(sig_tag)].three_body_mass = evt.llgM
                        outTree_dict['{0}_untagged_4'.format(sig_tag)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_untagged_4'.format(sig_tag)].Fill()
            for cat in categories:
                #outTree_dict[cat].Write()
                outTree_dict['sig_{0}'.format(cat)].Write()
                outTree_dict['data_{0}'.format(cat)].Write()
        
        outputFile.Close()
        inputFile.Close()

    # We should also save the categories by dataset for yields
    print('saving categories by dataset for yields')
    for channel in channels:
        inputFile = root_open('data/step3_vbf_bdt/output_{0}_2016_flat.root'.format(channel))
        outputFile = root_open('data/step4_cats_new/output_{0}_2016_yields.root'.format(channel), 'recreate')
        datasets = data_dict[channel]
        kin_bdt_cutvals = kin_bdt_cut_dict[channel]

        for dataset in tqdm(datasets):
            outTree_dict = {}
            for cat in categories:
                outTree_dict['{0}_{1}'.format(dataset, cat)] = Tree('{0}_{1}'.format(dataset, cat))
                outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'three_body_mass': 'F'})
                outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'eventWeight': 'F'})

            tree = inputFile[dataset]
            #sig_tag = 'sig'
            #if channel == 'mumug':
            #    if dataset[:4] == 'muon':
            #        sig_tag = 'data'
            #elif channel == 'elelg':
            #    if dataset[:4] == 'elec':
            #        sig_tag = 'data'
            #tree.create_buffer()
            #outTree_dict['sig_{0}'.format(cat)].set_buffer(tree._buffer, create_branches=True)
            #outTree_dict['data_{0}'.format(cat)].set_buffer(tree._buffer, create_branches=True)
            #outTree_dict = {}
            #for cat in categories:
            #    outTree_dict[cat] = Tree('{0}_{1}'.format(dataset, cat))
            #    outTree_dict[cat].set_buffer(tree._buffer, create_branches=True)
            for evt in tree:
                if dataset == 'zjets_m-50_amc' and evt.vetoDY:
                    continue
                kin_bdt = evt.kin_bdt
                vbf_bdt = evt.vbf_bdt
                if kin_bdt < kin_bdt_cutvals[0]:
                    continue
                else:
                    if evt.isLeptonTag:
                        outTree_dict['{0}_lepton'.format(dataset)].three_body_mass = evt.llgM
                        outTree_dict['{0}_lepton'.format(dataset)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_lepton'.format(dataset)].Fill()
                    #elif evt.isDijetTag:
                    #    outTree_dict['{0}_dijet'.format(dataset)].three_body_mass = evt.llgM
                    #    outTree_dict['{0}_dijet'.format(dataset)].eventWeight = evt.eventWeight
                    #    outTree_dict['{0}_dijet'.format(dataset)].Fill()
                    elif vbf_bdt > 0.1: 
                        outTree_dict['{0}_dijet_1'.format(dataset)].three_body_mass = evt.llgM
                        outTree_dict['{0}_dijet_1'.format(dataset)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_dijet_1'.format(dataset)].Fill()
                    elif -0.01 < vbf_bdt <= 0.1:
                        outTree_dict['{0}_dijet_2'.format(dataset)].three_body_mass = evt.llgM
                        outTree_dict['{0}_dijet_2'.format(dataset)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_dijet_2'.format(dataset)].Fill()
                    elif kin_bdt_cutvals[0] <= kin_bdt < kin_bdt_cutvals[1]:
                        outTree_dict['{0}_untagged_1'.format(dataset)].three_body_mass = evt.llgM
                        outTree_dict['{0}_untagged_1'.format(dataset)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_untagged_1'.format(dataset)].Fill()
                        #if evt.photonOnePt < 25.:
                        #    outTree_dict['{0}_untagged_11'.format(dataset)].three_body_mass = evt.llgM
                        #    outTree_dict['{0}_untagged_11'.format(dataset)].eventWeight = evt.eventWeight
                        #    outTree_dict['{0}_untagged_11'.format(dataset)].Fill()
                        #else:
                        #    outTree_dict['{0}_untagged_12'.format(dataset)].three_body_mass = evt.llgM
                        #    outTree_dict['{0}_untagged_12'.format(dataset)].eventWeight = evt.eventWeight
                        #    outTree_dict['{0}_untagged_12'.format(dataset)].Fill()
                    elif kin_bdt_cutvals[1] <= kin_bdt < kin_bdt_cutvals[2]:
                        outTree_dict['{0}_untagged_2'.format(dataset)].three_body_mass = evt.llgM
                        outTree_dict['{0}_untagged_2'.format(dataset)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_untagged_2'.format(dataset)].Fill()
                        #if evt.photonOnePt < 25.:
                        #    outTree_dict['{0}_untagged_21'.format(dataset)].three_body_mass = evt.llgM
                        #    outTree_dict['{0}_untagged_21'.format(dataset)].eventWeight = evt.eventWeight
                        #    outTree_dict['{0}_untagged_21'.format(dataset)].Fill()
                        #else:
                        #    outTree_dict['{0}_untagged_22'.format(dataset)].three_body_mass = evt.llgM
                        #    outTree_dict['{0}_untagged_22'.format(dataset)].eventWeight = evt.eventWeight
                        #    outTree_dict['{0}_untagged_22'.format(dataset)].Fill()
                    elif kin_bdt_cutvals[2] <= kin_bdt < kin_bdt_cutvals[3]:
                        outTree_dict['{0}_untagged_3'.format(dataset)].three_body_mass = evt.llgM
                        outTree_dict['{0}_untagged_3'.format(dataset)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_untagged_3'.format(dataset)].Fill()
                    elif kin_bdt >= kin_bdt_cutvals[3]:
                        outTree_dict['{0}_untagged_4'.format(dataset)].three_body_mass = evt.llgM
                        outTree_dict['{0}_untagged_4'.format(dataset)].eventWeight = evt.eventWeight
                        outTree_dict['{0}_untagged_4'.format(dataset)].Fill()
            for cat in categories:
                #outTree_dict[cat].Write()
                outTree_dict['{0}_{1}'.format(dataset, cat)].Write()
        
        outputFile.Close()
        inputFile.Close()
