#!/bin/sh

echo "running full post-BLT python analysis flow"

echo "STEP 1: running scripts/calc_sfs.py"
python scripts/calc_sfs.py
hadd -f data/step1_sfs/output_combined_2016.root data/step1_sfs/output_mmg_2016.root data/step1_sfs/output_eeg_2016.root 

echo "STEP 2: training kinematic BDT"
python scripts/kin_bdt_trainer.py

echo "STEP 3: adding kinematic BDT score with scripts/kin_bdt_reader.py"
python scripts/kin_bdt_reader.py
hadd -f data/step2_kin_bdt/output_combined_2016.root data/step2_kin_bdt/output_mmg_2016.root data/step2_kin_bdt/output_eeg_2016.root 

echo "STEP 4: training VBF BDT"
python scripts/vbf_bdt_trainer.py

echo "STEP 5: adding VBF BDT score with scripts/vbf_bdt_reader.py"
python scripts/vbf_bdt_reader.py

echo "STEP 6: making data/MC plots with scripts/make_data_mc_plots.py"
python scripts/make_data_mc_plots.py

echo "STEP 7: generating categories with scripts/categorizer.py"
python scripts/categorizer.py

echo "STEP 8: creating the lepton tag file"
hadd -f data/step4_cats/output_lepton_2016.root data/step4_cats/output_mmg_2016.root data/step4_cats/output_eeg_2016.root
hadd -f data/step4_cats/output_lepton_2016_yields.root data/step4_cats/output_mmg_2016_yields.root data/step4_cats/output_eeg_2016_yields.root
hadd -f data/step4_cats/output_lepton_2017.root data/step4_cats/output_mmg_2017.root data/step4_cats/output_eeg_2017.root
hadd -f data/step4_cats/output_lepton_2017_yields.root data/step4_cats/output_mmg_2017_yields.root data/step4_cats/output_eeg_2017_yields.root

echo "STEP 9: printing yields with scripts/make_yield_snippets.py"
python scripts/make_yield_snippets.py

echo "STEP 10: copying data files and yields to LPC"
scp data/step4_cats/output_mmg_2016.root jbueghly@cmslpc-sl6.fnal.gov:/uscms/home/jbueghly/nobackup/combine/CMSSW_7_4_7/src/combination_tools/hzg_data
scp data/step4_cats/output_eeg_2016.root jbueghly@cmslpc-sl6.fnal.gov:/uscms/home/jbueghly/nobackup/combine/CMSSW_7_4_7/src/combination_tools/hzg_data
scp data/step4_cats/output_lepton_2016.root jbueghly@cmslpc-sl6.fnal.gov:/uscms/home/jbueghly/nobackup/combine/CMSSW_7_4_7/src/combination_tools/hzg_data
scp data/step4_cats/output_mmg_2017.root jbueghly@cmslpc-sl6.fnal.gov:/uscms/home/jbueghly/nobackup/combine/CMSSW_7_4_7/src/combination_tools/hzg_data
scp data/step4_cats/output_eeg_2017.root jbueghly@cmslpc-sl6.fnal.gov:/uscms/home/jbueghly/nobackup/combine/CMSSW_7_4_7/src/combination_tools/hzg_data
scp data/step4_cats/output_lepton_2017.root jbueghly@cmslpc-sl6.fnal.gov:/uscms/home/jbueghly/nobackup/combine/CMSSW_7_4_7/src/combination_tools/hzg_data
scp yields/rate_snippets/*.txt jbueghly@cmslpc-sl6.fnal.gov:/uscms/home/jbueghly/nobackup/combine/CMSSW_7_4_7/src/combination_tools/signal_yields
