#!/bin/bash 

basename="test_"
dir="data/"
result_file="results.txt"
apriori_output="apriori.output"
fpg_output="fpg.output"

i=1
no=10
step=10000

echo "Test ${dir}"
echo "Step: ${step}, Times: ${no}"
echo "Start"

# clear old experiment
echo "" > $result_file

while [ $i -le $no ]
do
    ntrans="$(($i * $step))"
    echo "        $ntrans"

    echo ">> Apriori $ntrans << " >> $result_file
    (time python apriori.py -f data/test_${ntrans}.data > $apriori_output) 2>> $result_file
    echo ">> FPG $ntrans << " >> $result_file
    (time python fpg.py -f data/test_${ntrans}.data > $fpg_output) 2>> $result_file
    python verify.py $apriori_output $fpg_output | tee -a $result_file
    echo "" >> results.txt

    ((i++))
done

echo "Done"


