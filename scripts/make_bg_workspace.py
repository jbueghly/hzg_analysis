#!/usr/bin/env python

import ROOT as r
from rootpy.tree import Tree
from rootpy.io import root_open

if __name__ == '__main__':

    period = 2017
    channel = 'mmg'
    cat = 'untagged_1'

    inputFile = root_open('data/step4_cats/output_{0}_{1}.root'.format(channel, period))
    data_tree = inputFile['data_{0}'.format(cat)]

    w = r.RooWorkspace('cms_hgg_workspace')

    # variables
    IntLumi = r.RooRealVar('IntLumi', 'IntLumi', 0, 359000)
    CMS_hgg_mass = r.RooRealVar('CMS_hgg_mass', 'CMS_hgg_mass', 100, 180)
    # weight?

    data = r.RooDataSet('Data_13TeV_{0}'.format(cat), 'Data_13TeV_{0}'.format(cat), data_tree, r.RooArgSet(CMS_hgg_mass))
    
    getattr(w, 'import')(CMS_hgg_mass)
    getattr(w, 'import')(IntLumi)
    getattr(w, 'import')(data)

    w.Print()
    w.SaveAs('test_workspace.root')
