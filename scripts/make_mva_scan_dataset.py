#!/usr/bin/env python

import ROOT as r
from rootpy.tree import Tree
from rootpy.io import root_open
import array 
import numpy as np
from tqdm import tqdm, trange
import itertools

if __name__ == '__main__':

    data = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 'muon_2016F', 'muon_2016G', 'muon_2016H',
            'electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 'electron_2016F', 'electron_2016G', 'electron_2016H']
    
    signal = ['hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wplush', 'hzg_wminush', 'hzg_zh']

    inputFile = root_open('data/step3_vbf_bdt/output_combined_2016.root')
    outputFile = root_open('data/step3_vbf_bdt/output_mva_scan_2016.root', 'recreate')
    
    data_tree = Tree('data') 
    sig_tree = Tree('sig')
    data_tree.create_branches({'CMS_hzg_mass': 'F', 'eventWeight': 'F', 'vbf_bdt': 'F', 'kin_bdt': 'F'})
    sig_tree.create_branches({'CMS_hzg_mass': 'F', 'eventWeight': 'F', 'vbf_bdt': 'F', 'kin_bdt': 'F'})

    sig_tree_dict = {}
    for sig_sample in signal:
        sig_tree_dict[sig_sample] = Tree(sig_sample)
        sig_tree_dict[sig_sample].create_branches({'CMS_hzg_mass': 'F', 'eventWeight': 'F', 'vbf_bdt': 'F', 'kin_bdt': 'F'})

    for sample in signal + data:
        tree = inputFile[sample]
        for evt in tree:
            if sample in signal:
                # all signal
                sig_tree.CMS_hzg_mass = evt.llgMKin
                sig_tree.eventWeight = evt.eventWeight*evt.mc_sf
                sig_tree.vbf_bdt = evt.vbf_bdt
                sig_tree.kin_bdt = evt.kin_bdt
                sig_tree.Fill()
                # specific signal process
                sig_tree_dict[sample].CMS_hzg_mass = evt.llgMKin
                sig_tree_dict[sample].eventWeight = evt.eventWeight*evt.mc_sf
                sig_tree_dict[sample].vbf_bdt = evt.vbf_bdt
                sig_tree_dict[sample].kin_bdt = evt.kin_bdt
                sig_tree_dict[sample].Fill()
            elif sample in data:
                data_tree.CMS_hzg_mass = evt.llgMKin
                data_tree.eventWeight = 1
                data_tree.vbf_bdt = evt.vbf_bdt
                data_tree.kin_bdt = evt.kin_bdt
                data_tree.Fill()

    sig_tree.Write()
    data_tree.Write()

    for sig_sample in signal:
        sig_tree_dict[sig_sample].Write()

    outputFile.Close()
    inputFile.Close()


                


