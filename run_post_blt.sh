#!/bin/sh

echo "running full post-BLT analysis flow"

echo "STEP 1: running scripts/mod_bltuples.py"
python scripts/mod_bltuples.py

echo "STEP 2: making data/MC plots with scripts/make_data_mc_plots.py"
python scripts/make_data_mc_plots.py

echo "STEP 3: adding kinematic BDT score with scripts/kin_bdt_reader.py"
python scripts/kin_bdt_reader.py

echo "STEP 4: adding VBF BDT score with scripts/vbf_bdt_reader.py"
python scripts/vbf_bdt_reader.py

echo "STEP 5: generating categories with scripts/categorizer.py"
python scripts/categorizer.py

echo "STEP 6: printing yields with scripts/make_yield_snippets.py"
python scripts/make_yield_snippets.py
