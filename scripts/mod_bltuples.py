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

    #mc_17 = ['ttbar_inclusive', 'zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wplush', 'hzg_wminush', 'hzg_zh']
    mc_17 = []
    muon_data_17 = ['muon_2017B', 'muon_2017C', 'muon_2017D', 'muon_2017E', 'muon_2017F']
    #electron_data_17 = ['electron_2017B', 'electron_2017C', 'electron_2017D', 'electron_2017E', 'electron_2017F']
    electron_data_17 = []

    samples = {
                2016: {'mumug': mc_16 + muon_data_16, 'elelg': mc_16 + electron_data_16},
                2017: {'mumug': mc_17 + muon_data_17, 'elelg': mc_17 + electron_data_17} 
                }
 
    br_zg_m125 = 1.533e-3
    br_zll = 0.033658*3
    #br_wlnu = 0.1086*3 #PDG
    #br_wlnu = 0.108*3 #MY
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

    #for channel in channels:
        #print('running over {0} datasets'.format(channel))
        #inputFile = root_open('data/bltuples/output_{0}_2016_flat.root'.format(channel))
        #outputFile = root_open('data/step1_phores/output_{0}_2016_flat.root'.format(channel), 'recreate')
        #datasets = samples[channel]

        for dataset in tqdm(datasets):

            tree = inputFile['tree_{0}'.format(dataset)]
            tree.create_buffer()
            outTree = Tree(dataset)
            outTree.set_buffer(tree._buffer, create_branches=True)
            outTree.create_branches({'mc_sf': 'F'})
            #outTree.create_branches({'sync_status': 'I'})

            # compute the MC scale factor
            n_gen = inputFile['TotalEvents_{0}'.format(dataset)].GetBinContent(1)
            n_neg = inputFile['TotalEvents_{0}'.format(dataset)].GetBinContent(30)
            sf = luminosity[period]*xsec[dataset]*br[dataset]/(float(n_gen) - 2.*float(n_neg))
            
            #if dataset != 'ttbar_inclusive':
            #    outTree.create_branches({'cosTheta': 'F', 'costheta': 'F', 'mllgptdmllg': 'F', 
            #                             'lepEta1': 'F', 'lepEta2': 'F', 'phoEta': 'F', 
            #                             'Phi': 'F', 'phoR9': 'F', 'phores': 'F', 
            #                             'dRlg': 'F', 'maxdRlg': 'F'})

            #if channel == 'mumug' and dataset != 'ttbar_inclusive':
            #    if dataset[:4] == 'muon':
            #        df_phores = pd.read_csv('data/from_ming-yan/data_mu.csv')
            #    elif dataset[0] == 'z':
            #        df_phores = pd.read_csv('data/from_ming-yan/{0}_mu.csv'.format(dataset))
            #    else:
            #        df_phores = pd.read_csv('data/from_ming-yan/{0}_125_mu.csv'.format(dataset))
            #elif channel == 'elelg' and dataset != 'ttbar_inclusive':
            #    if dataset[:4] == 'elec':
            #        df_phores = pd.read_csv('data/from_ming-yan/data_ele.csv')
            #    elif dataset[0] == 'z':
            #        df_phores = pd.read_csv('data/from_ming-yan/{0}_ele.csv'.format(dataset))
            #    else:
            #        df_phores = pd.read_csv('data/from_ming-yan/{0}_125_ele.csv'.format(dataset))

            #sync_file = open('data/sync/james_evts_{0}_{1}.csv'.format(dataset, channel), 'w')
            #sync_file.write('run,lumi,evt,lepton1_pt,lepton1_eta,lepton1_phi,lepton2_pt,lepton2_eta,lepton2_phi,photon_pt,photon_eta,photon_phi,dilepton_pt,dilepton_eta,dilepton_phi,dilepton_m,llg_pt,llg_eta,llg_phi,llg_m\n')
            for evt in tree:
                run = evt.runNumber
                lumi = evt.lumiSection
                event = evt.evtNumber
                outTree.mc_sf = sf
                #sync_file.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19}\n'.format(
                #    run,lumi,event,evt.leptonOnePt,evt.leptonOneEta,evt.leptonOnePhi,evt.leptonTwoPt,evt.leptonTwoEta,evt.leptonTwoPhi,
                #    evt.photonOnePt,evt.photonOneEta,evt.photonOnePhi,evt.dileptonPt,evt.dileptonEta,evt.dileptonPhi,evt.dileptonM,
                #    evt.llgPt,evt.llgEta,evt.llgPhi,evt.llgM))
                if dataset == 'zjets_m-50_amc':
                    #outTree.eventWeight *= (1. - evt.vetoDY)
                    if evt.vetoDY:
                        continue

                #if dataset == 'ttbar_inclusive':
                #    outTree.Fill()
                #    continue

                #df_phores_cut = df_phores.query('run == {0} and lumi == {1} and evt == {2}'.format(run, lumi, event))
                #if df_phores_cut.shape[0] > 0:
                #    outTree.sync_status = 1 # overlap
                #    outTree.cosTheta = df_phores_cut.cosTheta.values[0]
                #    outTree.costheta = df_phores_cut.costheta.values[0]
                #    outTree.mllgptdmllg = df_phores_cut.mllgptdmllg.values[0]
                #    outTree.lepEta1 = df_phores_cut.lepEta1.values[0]
                #    outTree.lepEta2 = df_phores_cut.lepEta2.values[0]
                #    outTree.phoEta = df_phores_cut.phoEta.values[0]
                #    outTree.Phi = df_phores_cut.Phi.values[0]
                #    outTree.phoR9 = df_phores_cut.phoR9.values[0]
                #    outTree.phores = df_phores_cut.phores.values[0]
                #    outTree.dRlg = df_phores_cut.dRlg.values[0]
                #    outTree.maxdRlg = df_phores_cut.maxdRlg.values[0]
                #    outTree.Fill() # only filling the tree if the event overlaps with Ming-Yan
                ##else:
                ##    continue
                #else:
                #    #outTree.eventWeight = 0.
                #    outTree.sync_status = 0 # James only
                #    #outTree.phores = -999.
                #    #outTree.cosTheta = -999.
                #    #outTree.costheta = -999.
                #    #outTree.mllgptdmllg = -999.
                #    #outTree.lepEta1 = -999.
                #    #outTree.lepEta2 = -999.
                #    #outTree.phoEta = -999.
                #    #outTree.Phi = -999.
                #    #outTree.phoR9 = -999.
                #    #outTree.phores = -999.
                #    #outTree.dRlg = -999.
                #    #outTree.maxdRlg = -999.
                #    outTree.Fill()

            #sync_file.close()
                outTree.Fill()
            outTree.Write()
        outputFile.Close()
        inputFile.Close()
