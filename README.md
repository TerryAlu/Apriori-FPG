## Apriori & FPGrowth

This project implemtns Apriori and FPGrowth algorithm.
Both `apriori.py` and `fpg.py` generate freqent itemsets, but only `apriori.py`  generates rules.

## Environment

* OS: Ubuntu 16.04
* Pyhton version: 2.7.12
* WEKA version: 3.9.3

## Prerequisites (Optional)

1. Download latest weka from [here](https://www.cs.waikato.ac.nz/ml/weka/downloading.html) and extract files.
2. Enter `ibm_datagen` and  `make`

## Usage

###  Input Format

    # Each row represents a transaction
    # Each column represent an item
    
    <item1>,<item2>.....
    <item1>,<item3>,<item5>...
    ..
    ..
    
###  Command

Apriori with input file `test.csv`, minimum support=`0.5`, minimum confidence=`0.9`

    python apriori.py -f test.csv -s 0.5 -c 0.9

Apriori with input file `test.csv`, minimum support=`0.5`

    python fpg.py -f test.csv
