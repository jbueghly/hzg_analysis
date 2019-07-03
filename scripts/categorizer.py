#!/usr/bin/env python

import ROOT as r
from rootpy.tree import Tree
from rootpy.io import root_open
import array 
import numpy as np
from tqdm import tqdm, trange

r.gStyle.SetOptStat(0)

def fill_cat_tree(tree_dict, tag, cat, event, useKinFit=False):
    if useKinFit:
        tree_dict['{0}_{1}'.format(tag, cat)].three_body_mass = event.llgMKin
    else:
        tree_dict['{0}_{1}'.format(tag, cat)].three_body_mass = event.llgM
    tree_dict['{0}_{1}'.format(tag, cat)].photon_pt = event.photonOnePt
    #tree_dict['{0}_{1}'.format(tag, cat)].eventWeight = event.eventWeight
    tree_dict['{0}_{1}'.format(tag, cat)].Fill()

def fill_cat_hist(hist_dict, tag, cat, event, useKinFit=False):
    if useKinFit:
        hist_dict['{0}_{1}_hist'.format(tag, cat)].Fill(event.llgMKin, event.photonOnePt, event.eventWeight)
    else:
        hist_dict['{0}_{1}_hist'.format(tag, cat)].Fill(event.llgM, event.photonOnePt, event.eventWeight)

#def fill_cat_hist(hist_dict, tag, cat, event, useKinFit=False):
#        hist_dict['{0}_{1}_hist'.format(tag, cat)].Fill(event.photonOnePt, event.eventWeight)

def update_norm(hist):
    print('updating the normalization')
    for i in range(hist.GetNbinsX()):
        integral = 0
        for j in range(hist.GetNbinsY()):
            binNum = hist.GetBin(i+1, j+1)
            integral += hist.GetBinContent(binNum)
            print('inner loop integral = {0}'.format(integral))
        if integral > 0:
            print('yay we had a good integral!!')
            for j in range(hist.GetNbinsY()):
                binNum = hist.GetBin(i+1, j+1)
                print('dividing bin content {0} by integral {1}'.format(hist.GetBinContent(binNum), integral))
                hist.SetBinContent(binNum, hist.GetBinContent(binNum)/integral)

def plot_template(h, h_name):
    c = r.TCanvas()
    h.Draw('COLZ')
    c.SetLogz()
    h.SetTitle('')
    h.GetXaxis().SetTitle('#m_{\ell\ell\gamma}# [GeV]')
    h.GetXaxis().SetTitleSize(h.GetXaxis().GetTitleSize()*2)
    #h.GetXaxis().SetTitleOffset(1.5)
    h.GetYaxis().SetTitle('#p_{T}^{\gamma}# [GeV]')
    h.GetYaxis().SetTitleSize(h.GetYaxis().GetTitleSize()*2)
    #h.GetYaxis().SetTitleOffset(1.5)
    h.GetZaxis().SetTitle('Entries / bin')
    h.GetZaxis().SetTitleSize(h.GetZaxis().GetTitleSize()*2)
    #h.GetZaxis().SetTitleOffset(1.5)
    c.SetTitle('')
    c.SetLeftMargin(0.15)
    c.SetRightMargin(0.2)
    c.SetBottomMargin(0.2)
    c.Update()
    c.SaveAs('plots/templates/{0}.png'.format(h_name))

#def plot_template(h, h_name):
#    c = r.TCanvas()
#    h.SetTitle('')
#    h.GetXaxis().SetTitle('#p_{T}^{\gamma}# [GeV]')
#    h.GetXaxis().SetTitleSize(h.GetXaxis().GetTitleSize()*2)
#    c.SetTitle('')
#    c.SetLeftMargin(0.15)
#    c.SetRightMargin(0.2)
#    c.SetBottomMargin(0.2)
#    c.Update()
#    c.SaveAs('plots/templates/{0}.png'.format(h_name))

if __name__ == '__main__':

    category_scheme = 'optimal'
    #category_scheme = 'nominal'
    
    channels = ['mumug', 'elelg']
    channels_rename = {'mumug': 'mmg', 'elelg': 'eeg'}

    #mc = ['zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wh', 'hzg_zh']
    mc = ['zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wplush', 'hzg_wminush', 'hzg_zh']
    #mc = ['zjets_m-50_amc', 'zg_llg', 'hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_zh']
    #mc = ['zjets_m-50_amc', 'zg_llg', 'hzg_gluglu']
    #mc = ['hzg_gluglu', 'hzg_tth', 'hzg_vbf', 'hzg_wh', 'hzg_zh']
    muon_data = ['muon_2016B', 'muon_2016C', 'muon_2016D', 'muon_2016E', 
                 'muon_2016F', 'muon_2016G', 'muon_2016H']
    electron_data = ['electron_2016B', 'electron_2016C', 'electron_2016D', 'electron_2016E', 
                     'electron_2016F', 'electron_2016G', 'electron_2016H']

    #mass_binning_sig = array.array('d', [115, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 170])
    mass_binning_sig = array.array('d', [115, 125, 170])
    n_mass_bins_sig = len(mass_binning_sig) - 1
    #mass_binning_bg = array.array('d', [115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 130, 135, 140, 150, 160, 170])
    mass_binning_bg = array.array('d', [115, 125, 170])
    n_mass_bins_bg = len(mass_binning_bg) - 1
    
    pt_binning_sig = array.array('d', [15, 20, 85])
    n_pt_bins_sig = len(pt_binning_sig) - 1
    #pt_binning_bg = array.array('d', [115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 130, 135, 140, 150, 160, 170])
    pt_binning_bg = array.array('d', [15, 20, 85])
    n_pt_bins_bg = len(pt_binning_bg) - 1

    data_dict = {'mumug': mc + muon_data, 'elelg': mc + electron_data}

    if category_scheme == 'nominal':
        categories = ['lepton', 'dijet', 'boosted', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']

    elif category_scheme == 'optimal':
        categories = ['lepton', 'dijet_1', 'dijet_2', 'untagged_1', 'untagged_2', 'untagged_3', 'untagged_4']
        #categories = ['lepton', 'dijet_1', 'dijet_2', 'untagged_11', 'untagged_12', 'untagged_2', 'untagged_21', 'untagged_22', 'untagged_3', 'untagged_4']
        kin_bdt_cut_dict = {'mumug': [-0.085, -0.0665, -0.02, 0.019], 'elelg': [-0.075, -0.06, -0.016, 0.022]}
 
    # This is how we need to organize the data for limits
    print('categorizing for limits')
    for channel in channels:
        inputFile = root_open('data/step3_vbf_bdt/output_{0}_2016_flat.root'.format(channel))
        outputFile = root_open('data/step4_cats/output_{0}_2016.root'.format(channels_rename[channel]), 'recreate')
        datasets = data_dict[channel]

        if category_scheme == 'optimal':
            kin_bdt_cutvals = kin_bdt_cut_dict[channel]

        outTree_dict = {}
        outHist_dict = {}
        for cat in categories:
            outTree_dict['sig_{0}'.format(cat)] = Tree('sig_{0}'.format(cat))
            outTree_dict['data_{0}'.format(cat)] = Tree('data_{0}'.format(cat))
            outTree_dict['bkg_{0}'.format(cat)] = Tree('bkg_{0}'.format(cat))
            outTree_dict['sig_{0}'.format(cat)].create_branches({'three_body_mass': 'F'})
            outTree_dict['data_{0}'.format(cat)].create_branches({'three_body_mass': 'F'})
            outTree_dict['bkg_{0}'.format(cat)].create_branches({'three_body_mass': 'F'})
            outTree_dict['sig_{0}'.format(cat)].create_branches({'photon_pt': 'F'})
            outTree_dict['data_{0}'.format(cat)].create_branches({'photon_pt': 'F'})
            outTree_dict['bkg_{0}'.format(cat)].create_branches({'photon_pt': 'F'})
            outTree_dict['sig_{0}'.format(cat)].create_branches({'eventWeight': 'F'})
            outTree_dict['data_{0}'.format(cat)].create_branches({'eventWeight': 'F'})
            outTree_dict['bkg_{0}'.format(cat)].create_branches({'eventWeight': 'F'})
            #outHist_dict['sig_{0}_hist'.format(cat)] = r.TH2F('sig_{0}_hist'.format(cat), 'sig_{0}_hist'.format(cat), 55, 115., 170., 85, 15., 100.)
            #outHist_dict['data_{0}_hist'.format(cat)] = r.TH2F('data_{0}_hist'.format(cat), 'data_{0}_hist'.format(cat), 55, 115., 170., 85, 15., 100.)
            #outHist_dict['sig_{0}_hist'.format(cat)] = r.TH2F('sig_{0}_hist'.format(cat), 'sig_{0}_hist'.format(cat), n_mass_bins_sig, mass_binning_sig, n_pt_bins_sig, pt_binning_sig)
            #outHist_dict['data_{0}_hist'.format(cat)] = r.TH2F('data_{0}_hist'.format(cat), 'data_{0}_hist'.format(cat), n_mass_bins_bg, mass_binning_bg, n_pt_bins_sig, pt_binning_sig)
            #outHist_dict['bkg_{0}_hist'.format(cat)] = r.TH2F('bkg_{0}_hist'.format(cat), 'bkg_{0}_hist'.format(cat), n_mass_bins_bg, mass_binning_bg, n_pt_bins_sig, pt_binning_sig)
            #outHist_dict['sig_{0}_hist'.format(cat)] = r.TH2F('sig_{0}_hist'.format(cat), 'sig_{0}_hist'.format(cat), 55, 115., 170., 34, 15., 100.)
            #outHist_dict['data_{0}_hist'.format(cat)] = r.TH2F('data_{0}_hist'.format(cat), 'data_{0}_hist'.format(cat), 55, 115., 170., 34, 15., 100.)
            #outHist_dict['bkg_{0}_hist'.format(cat)] = r.TH2F('bkg_{0}_hist'.format(cat), 'bkg_{0}_hist'.format(cat), 55, 115., 170., 34, 15., 100.)
            #outHist_dict['sig_{0}_hist'.format(cat)] = r.TH2F('sig_{0}_hist'.format(cat), 'sig_{0}_hist'.format(cat), 12, 115., 170., 17, 15., 100.)
            #outHist_dict['data_{0}_hist'.format(cat)] = r.TH2F('data_{0}_hist'.format(cat), 'data_{0}_hist'.format(cat), 12, 115., 170., 17, 15., 100.)
            #outHist_dict['bkg_{0}_hist'.format(cat)] = r.TH2F('bkg_{0}_hist'.format(cat), 'bkg_{0}_hist'.format(cat), 12, 115., 170., 17, 15., 100.)
            outHist_dict['sig_{0}_hist'.format(cat)] = r.TH2F('sig_{0}_hist'.format(cat), 'sig_{0}_hist'.format(cat), 1, 115., 170., 1, 15., 100.)
            outHist_dict['data_{0}_hist'.format(cat)] = r.TH2F('data_{0}_hist'.format(cat), 'data_{0}_hist'.format(cat), 1, 115., 170., 1, 15., 100.)
            outHist_dict['bkg_{0}_hist'.format(cat)] = r.TH2F('bkg_{0}_hist'.format(cat), 'bkg_{0}_hist'.format(cat), 1, 115., 170., 1, 15., 100.)
            #outHist_dict['sig_{0}_hist'.format(cat)] = r.TH1F('sig_{0}_hist'.format(cat), 'sig_{0}_hist'.format(cat), 2, 15., 100.)
            #outHist_dict['data_{0}_hist'.format(cat)] = r.TH1F('data_{0}_hist'.format(cat), 'data_{0}_hist'.format(cat), 2, 15., 100.)
            #outHist_dict['bkg_{0}_hist'.format(cat)] = r.TH1F('bkg_{0}_hist'.format(cat), 'bkg_{0}_hist'.format(cat), 2, 15., 100.)

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
                        fill_cat_hist(outHist_dict, sig_tag, 'lepton', evt, useKinFit=False)
                    elif evt.isDijetTag:
                        fill_cat_tree(outTree_dict, sig_tag, 'dijet', evt, useKinFit=False)
                        fill_cat_hist(outHist_dict, sig_tag, 'dijet', evt, useKinFit=False)
                    elif evt.llgPt >= 60.0:
                        fill_cat_tree(outTree_dict, sig_tag, 'boosted', evt, useKinFit=False)
                        fill_cat_hist(outHist_dict, sig_tag, 'boosted', evt, useKinFit=False)
                    else:
                        if channel == 'mumug':
                            if abs(evt.photonOneEta) < 1.4442:
                                if ((abs(evt.leptonOneEta) < 2.1 and abs(evt.leptonTwoEta) < 2.1) and
                                   (abs(evt.leptonOneEta) < 0.9 or  abs(evt.leptonTwoEta) < 0.9)):
                                    if evt.photonOneR9 > 0.94:
                                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_1',
                                                      evt, useKinFit=False)
                                        fill_cat_hist(outHist_dict, sig_tag, 'untagged_1',
                                                      evt, useKinFit=False)
                                    else:
                                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_2', 
                                                      evt, useKinFit=False)
                                        fill_cat_hist(outHist_dict, sig_tag, 'untagged_2',
                                                      evt, useKinFit=False)
                                else:
                                    fill_cat_tree(outTree_dict, sig_tag, 'untagged_3', 
                                                  evt, useKinFit=False)
                                    fill_cat_hist(outHist_dict, sig_tag, 'untagged_3',
                                                  evt, useKinFit=False)
                            else:
                                fill_cat_tree(outTree_dict, sig_tag, 'untagged_4', 
                                              evt, useKinFit=False)
                                fill_cat_hist(outHist_dict, sig_tag, 'untagged_4', 
                                              evt, useKinFit=False)
                        elif channel == 'elelg':
                            if abs(evt.photonOneEta) < 1.4442:
                                if (abs(evt.leptonOneEta) < 1.4442 and 
                                    abs(evt.leptonTwoEta) < 1.4442):
                                    if evt.photonOneR9 > 0.94: 
                                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_1',
                                                      evt, useKinFit=False)
                                        fill_cat_hist(outHist_dict, sig_tag, 'untagged_1',
                                                      evt, useKinFit=False)
                                    else:
                                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_2',
                                                      evt, useKinFit=False)
                                        fill_cat_hist(outHist_dict, sig_tag, 'untagged_2',
                                                      evt, useKinFit=False)
                                else:
                                    fill_cat_tree(outTree_dict, sig_tag, 'untagged_3', 
                                                  evt, useKinFit=False)
                                    fill_cat_hist(outHist_dict, sig_tag, 'untagged_3', 
                                                  evt, useKinFit=False)
                            else:
                                fill_cat_tree(outTree_dict, sig_tag, 'untagged_4', 
                                              evt, useKinFit=False)
                                fill_cat_hist(outHist_dict, sig_tag, 'untagged_4', 
                                              evt, useKinFit=False)
                
                elif category_scheme == 'optimal':
                    if evt.isLeptonTag:
                        fill_cat_tree(outTree_dict, sig_tag, 'lepton', evt, useKinFit=True)
                        fill_cat_hist(outHist_dict, sig_tag, 'lepton', evt, useKinFit=True)
                    elif vbf_bdt > 0.1: 
                        fill_cat_tree(outTree_dict, sig_tag, 'dijet_1', evt, useKinFit=True)
                        fill_cat_hist(outHist_dict, sig_tag, 'dijet_1', evt, useKinFit=True)
                    elif -0.01 < vbf_bdt <= 0.1:
                        fill_cat_tree(outTree_dict, sig_tag, 'dijet_2', evt, useKinFit=True)
                        fill_cat_hist(outHist_dict, sig_tag, 'dijet_2', evt, useKinFit=True)
                    elif kin_bdt_cutvals[0] <= kin_bdt < kin_bdt_cutvals[1]:
                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_1', evt, useKinFit=True)
                        fill_cat_hist(outHist_dict, sig_tag, 'untagged_1', evt, useKinFit=True)
                        #if evt.photonOnePt < 25.:
                        #    fill_cat_tree(outTree_dict, sig_tag, 'untagged_11', evt, useKinFit=True)
                        #else:
                        #    fill_cat_tree(outTree_dict, sig_tag, 'untagged_12', evt, useKinFit=True)
                    elif kin_bdt_cutvals[1] <= kin_bdt < kin_bdt_cutvals[2]:
                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_2', evt, useKinFit=True)
                        fill_cat_hist(outHist_dict, sig_tag, 'untagged_2', evt, useKinFit=True)
                        #if evt.photonOnePt < 25.:
                        #    fill_cat_tree(outTree_dict, sig_tag, 'untagged_21', evt, useKinFit=True)
                        #else:
                        #    fill_cat_tree(outTree_dict, sig_tag, 'untagged_22', evt, useKinFit=True)
                    elif kin_bdt_cutvals[2] <= kin_bdt < kin_bdt_cutvals[3]:
                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_3', evt, useKinFit=True)
                        fill_cat_hist(outHist_dict, sig_tag, 'untagged_3', evt, useKinFit=True)
                    elif kin_bdt >= kin_bdt_cutvals[3]:
                        fill_cat_tree(outTree_dict, sig_tag, 'untagged_4', evt, useKinFit=True)
                        fill_cat_hist(outHist_dict, sig_tag, 'untagged_4', evt, useKinFit=True)

        for cat in categories:
            outTree_dict['sig_{0}'.format(cat)].Write()
            outTree_dict['data_{0}'.format(cat)].Write()
            outTree_dict['bkg_{0}'.format(cat)].Write()
            update_norm(outHist_dict['sig_{0}_hist'.format(cat)])
            update_norm(outHist_dict['data_{0}_hist'.format(cat)])
            update_norm(outHist_dict['bkg_{0}_hist'.format(cat)])
            #plot_template(outHist_dict['sig_{0}_hist'.format(cat)], 'sig_{0}_{1}_hist'.format(channel, cat))
            #plot_template(outHist_dict['data_{0}_hist'.format(cat)], 'data_{0}_{1}_hist'.format(channel, cat))
            #plot_template(outHist_dict['bkg_{0}_hist'.format(cat)], 'bkg_{0}_{1}_hist'.format(channel, cat))
            plot_template(outHist_dict['sig_{0}_hist'.format(cat)], 'sig_{0}_{1}_hist_raw'.format(channel, cat))
            plot_template(outHist_dict['data_{0}_hist'.format(cat)], 'data_{0}_{1}_hist_raw'.format(channel, cat))
            plot_template(outHist_dict['bkg_{0}_hist'.format(cat)], 'bkg_{0}_{1}_hist_raw'.format(channel, cat))
            outHist_dict['sig_{0}_hist'.format(cat)].Write()
            outHist_dict['data_{0}_hist'.format(cat)].Write()
            outHist_dict['bkg_{0}_hist'.format(cat)].Write()
        
        outputFile.Close()
        inputFile.Close()

    # We should also save the categories by dataset for yields
    print('saving categories by dataset for yields')
    for channel in channels:
        inputFile = root_open('data/step3_vbf_bdt/output_{0}_2016_flat.root'.format(channel))
        outputFile = root_open('data/step4_cats/output_{0}_2016_yields.root'.format(channels_rename[channel]), 'recreate')
        datasets = data_dict[channel]
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
                outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'photon_pt': 'F'})
                #outTree_dict['{0}_{1}'.format(dataset, cat)].create_branches({'eventWeight': 'F'})


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
                        #if evt.photonOnePt < 25.:
                        #    fill_cat_tree(outTree_dict, dataset, 'untagged_11', evt, useKinFit=True)
                        #else:
                        #    fill_cat_tree(outTree_dict, dataset, 'untagged_12', evt, useKinFit=True)
                    elif kin_bdt_cutvals[1] <= kin_bdt < kin_bdt_cutvals[2]:
                        fill_cat_tree(outTree_dict, dataset, 'untagged_2', evt, useKinFit=True)
                        #if evt.photonOnePt < 25.:
                        #    fill_cat_tree(outTree_dict, dataset, 'untagged_21', evt, useKinFit=True)
                        #else:
                        #    fill_cat_tree(outTree_dict, dataset, 'untagged_22', evt, useKinFit=True)
                    elif kin_bdt_cutvals[2] <= kin_bdt < kin_bdt_cutvals[3]:
                        fill_cat_tree(outTree_dict, dataset, 'untagged_3', evt, useKinFit=True)
                    elif kin_bdt >= kin_bdt_cutvals[3]:
                        fill_cat_tree(outTree_dict, dataset, 'untagged_4', evt, useKinFit=True)

            for cat in categories:
                outTree_dict['{0}_{1}'.format(dataset, cat)].Write()
        
        outputFile.Close()
        inputFile.Close()
