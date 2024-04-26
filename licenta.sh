#!/bin/bash

mkdir -p output 
cd output
mkdir -p amr
cd amr
mkdir -p truths
mkdir -p myths
mkdir -p tweets
cd ..
mkdir -p sentences
cd sentences
mkdir -p truths
mkdir -p myths
mkdir -p tweets
cd ../..
python3 create_dataset.py
python3 sentences.py
source activate ./licenta
python3 amr.py
conda deactivate 
conda activate ./amr_logic
cd output
mkdir -p logic
cd logic
mkdir -p truths
mkdir -p myths
mkdir -p tweets
cd ../..
python3 amr_to_logic.py
cd output
mkdir -p logic_fix
cd logic_fix
mkdir -p truths
mkdir -p myths
mkdir -p tweets
cd ../..
python3 logic_fix.py
conda deactivate 
cd output
mkdir -p cnf
cd cnf
mkdir -p truths
mkdir -p myths
mkdir -p tweets
cd ../..
python3 logic_to_cnf.py
conda activate ./logic_solver
cd output
mkdir -p final_output
cd ..
python3 resolution.py
conda deactivate
