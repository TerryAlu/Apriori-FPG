#!/bin/bash

filename="kaggle_breadbasket.csv"
dir="data/kaggle/"
result_file="results.txt"
apriori_output="apriori.output"
fpg_output="fpg.output"

support="0.01"
conf="0.5"

echo "*********************"
echo "****   Apriori   ****"
echo "*********************"
echo ""
time python apriori.py -f ${dir}${filename} -s ${support} -c ${conf} | tee ${apriori_output}
echo ""

echo "*********************"
echo "****     FPG     ****"
echo "*********************"
echo ""
time python fpg.py -f ${dir}${filename} -s ${support} | tee ${fpg_output}
echo ""

python verify.py ${apriori_output} ${fpg_output}
