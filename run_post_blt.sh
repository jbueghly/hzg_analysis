#!/bin/sh

echo "running full post-BLT analysis flow"

echo "STEP 1: running scripts/mod_bltuples.py"
python scripts/calc_sfs.py
hadd -f data/step1_phores/output_combined_2016_flat.root data/step1_phores/output_mumug_2016_flat.root data/step1_phores/output_elelg_2016_flat.root 

echo "STEP 2: making data/MC plots with scripts/make_data_mc_plots.py"
python scripts/make_data_mc_plots.py

echo "STEP 3: training kinematic BDT"
python scripts/bdt_trainer.py

echo "STEP 4: adding kinematic BDT score with scripts/kin_bdt_reader.py"
python scripts/kin_bdt_reader.py

echo "STEP 5: adding VBF BDT score with scripts/vbf_bdt_reader.py"
python scripts/vbf_bdt_reader.py

echo "STEP 6: generating categories with scripts/categorizer.py"
python scripts/categorizer.py
#python scripts/categorizer_bdt_fit.py

echo "STEP 7: creating the lepton tag file"
hadd -f data/step4_cats/output_lepton_2016.root data/step4_cats/output_mmg_2016.root data/step4_cats/output_eeg_2016.root
hadd -f data/step4_cats/output_lepton_2016_yields.root data/step4_cats/output_mmg_2016_yields.root data/step4_cats/output_eeg_2016_yields.root

echo "STEP 8: printing yields with scripts/make_yield_snippets.py"
python scripts/make_yield_snippets.py
#python scripts/make_yield_snippets_bdt_fit.py

echo "copying data files and yields to LPC"
scp data/step4_cats/output_mmg_2016.root jbueghly@cmslpc-sl6.fnal.gov:/uscms/home/jbueghly/nobackup/combine/CMSSW_7_4_7/src/combination_tools/hzg_data
scp data/step4_cats/output_eeg_2016.root jbueghly@cmslpc-sl6.fnal.gov:/uscms/home/jbueghly/nobackup/combine/CMSSW_7_4_7/src/combination_tools/hzg_data
scp data/step4_cats/output_lepton_2016.root jbueghly@cmslpc-sl6.fnal.gov:/uscms/home/jbueghly/nobackup/combine/CMSSW_7_4_7/src/combination_tools/hzg_data
scp yields/rate_snippets/*.txt jbueghly@cmslpc-sl6.fnal.gov:/uscms/home/jbueghly/nobackup/combine/CMSSW_7_4_7/src/combination_tools/signal_yields
