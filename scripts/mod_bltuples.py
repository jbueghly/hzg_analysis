#!/usr/bin/env python

# add photon resolution variable to the bltuples
import ROOT as r
from ROOT import TMVA as t
from rootpy.tree import Tree
from rootpy.io import root_open
import numpy as np
import pandas as pd
from tqdm import tqdm, trange

if __name__ == '__main__':

    #channels = ['mumug', 'elelg']
    channels = ['mumug']

    mc = ['ttbar_inclusive', 'zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wh', 'hzg_zh']
    muon_data = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
                 'muon_2016F', 'muon_2016G', 'muon_2016H']
    electron_data = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                     'electron_2016F', 'electron_2016G', 'electron_2016H']

    #datasets = ['zjets_m-50_amc', 'zg_llg', 
    #            'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wh', 'hzg_zh',
    #            'muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
    #            'muon_2016F', 'muon_2016G', 'muon_2016H']

    data_dict = {'mumug': mc + muon_data, 'elelg': mc + electron_data}

    #sf_dict = {'zjets_m-50_amc': 2.6467566, 'zg_llg': 0.4507267, 'ttbar_inclusive': 0.479329,
    #        'hzg_gluglu': 0.0007087, 'hzg_tth': 0.0001937, 'hzg_vbf': 0.0001087, 'hzg_wh': 0.0001490, 'hzg_zh': 0.0001510,
    #        'muon_2016B': 1., 'muon_2016C': 1., 'muon_2016D': 1., 'muon_2016E': 1., 
    #        'muon_2016F': 1., 'muon_2016G': 1., 'muon_2016H': 1.,
    #        'electron_2016B': 1., 'electron_2016C': 1., 'electron_2016D': 1., 'electron_2016E': 1., 
    #        'electron_2016F': 1., 'electron_2016G': 1., 'electron_2016H': 1.}
   
    # Ming-Yan's mc weights, except for wh, which she has split into W+ and W-; need to fix that
    sf_dict = {'zjets_m-50_amc': 2.6089713, 'zg_llg': 0.4303657, 'ttbar_inclusive': 0.479329,
            'hzg_gluglu': 0.0006731, 'hzg_tth': 0.0001448, 'hzg_vbf': 0.0001032, 'hzg_wh': 0.0001490, 'hzg_zh': 0.0001754,
            'muon_2016B': 1., 'muon_2016C': 1., 'muon_2016D': 1., 'muon_2016E': 1., 
            'muon_2016F': 1., 'muon_2016G': 1., 'muon_2016H': 1.,
            'electron_2016B': 1., 'electron_2016C': 1., 'electron_2016D': 1., 'electron_2016E': 1., 
            'electron_2016F': 1., 'electron_2016G': 1., 'electron_2016H': 1.}
            

    #inputFile = root_open('data/bltuples/output_mumug_2016_flat.root')
    #outputFile = root_open('data/step1_phores/output_mumug_2016_flat.root', 'recreate')

    for channel in channels:
        print('running over {0} datasets'.format(channel))
        inputFile = root_open('data/bltuples/output_{0}_2016_flat.root'.format(channel))
        outputFile = root_open('data/step1_phores/output_{0}_2016_flat.root'.format(channel), 'recreate')
        datasets = data_dict[channel]

        for dataset in tqdm(datasets):
            tree = inputFile['tree_{0}'.format(dataset)]
            tree.create_buffer()
            outTree = Tree(dataset)
            outTree.set_buffer(tree._buffer, create_branches=True)
            #outTree.create_branches({'phores': 'F'})
            if dataset != 'ttbar_inclusive':
                outTree.create_branches({'cosTheta': 'F', 'costheta': 'F', 'mllgptdmllg': 'F', 
                                         'lepEta1': 'F', 'lepEta2': 'F', 'phoEta': 'F', 
                                         'Phi': 'F', 'phoR9': 'F', 'phores': 'F', 
                                         'dRlg': 'F', 'maxdRlg': 'F'})
            if channel == 'mumug' and dataset != 'ttbar_inclusive':
                if dataset[:4] == 'muon':
                    #df_phores = pd.read_csv('data/phores/data_mu.csv')
                    df_phores = pd.read_csv('data/from_ming-yan/data_mu.csv')
                elif dataset[0] == 'z':
                    #df_phores = pd.read_csv('data/phores/{0}_mu.csv'.format(dataset))
                    df_phores = pd.read_csv('data/from_ming-yan/{0}_mu.csv'.format(dataset))
                else:
                    #df_phores = pd.read_csv('data/phores/{0}_125_mu.csv'.format(dataset))
                    df_phores = pd.read_csv('data/from_ming-yan/{0}_125_mu.csv'.format(dataset))
            elif channel == 'elelg' and dataset != 'ttbar_inclusive':
                if dataset[:4] == 'elec':
                    #df_phores = pd.read_csv('data/phores/data_ele.csv')
                    df_phores = pd.read_csv('data/from_ming-yan/data_ele.csv')
                elif dataset[0] == 'z':
                    #df_phores = pd.read_csv('data/phores/{0}_ele.csv'.format(dataset))
                    df_phores = pd.read_csv('data/from_ming-yan/{0}_ele.csv'.format(dataset))
                else:
                    #df_phores = pd.read_csv('data/phores/{0}_125_ele.csv'.format(dataset))
                    df_phores = pd.read_csv('data/from_ming-yan/{0}_125_ele.csv'.format(dataset))
            for evt in tree:
                run = evt.runNumber
                lumi = evt.lumiSection
                event = evt.evtNumber
                outTree.eventWeight = evt.eventWeight * sf_dict[dataset]
                if dataset == 'ttbar_inclusive':
                    outTree.Fill()
                    continue
                df_phores_cut = df_phores.query('run == {0} and lumi == {1} and evt == {2}'.format(run, lumi, event))
                if df_phores_cut.shape[0] > 0:
                    if dataset[0] == 'z':
                        outTree.phores = df_phores_cut.phores.values[0]
                        outTree.Fill() # only filling the tree if the event overlaps with Ming-Yan
                    else:
                        outTree.cosTheta = df_phores_cut.cosTheta.values[0]
                        outTree.costheta = df_phores_cut.costheta.values[0]
                        outTree.mllgptdmllg = df_phores_cut.mllgptdmllg.values[0]
                        outTree.lepEta1 = df_phores_cut.lepEta1.values[0]
                        outTree.lepEta2 = df_phores_cut.lepEta2.values[0]
                        outTree.phoEta = df_phores_cut.phoEta.values[0]
                        outTree.Phi = df_phores_cut.Phi.values[0]
                        outTree.phoR9 = df_phores_cut.phoR9.values[0]
                        outTree.phores = df_phores_cut.phores.values[0]
                        outTree.dRlg = df_phores_cut.dRlg.values[0]
                        outTree.maxdRlg = df_phores_cut.maxdRlg.values[0]
                        outTree.Fill() # only filling the tree if the event overlaps with Ming-Yan
                #else:
                #    phores = -999.

            outTree.Write()
        outputFile.Close()
        inputFile.Close()
