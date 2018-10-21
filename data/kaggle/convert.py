"""
Convert BreadBasket_DMS.csv to custom csv format
BreadBasket_DMS.csv from kaggle: https://www.kaggle.com/xvivancos/transactions-from-a-bakery
"""

import csv
from collections import defaultdict

trans = defaultdict(set)
with open("BreadBasket_DMS.csv", "r") as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        trans[row['Transaction']].add(row['Item'])

with open("kaggle_breadbasket.csv", "w") as fp:
    for key, tran_set in trans.iteritems():
        tran_str = ",".join(tran_set)
        print key, tran_str
        fp.write(tran_str)
        fp.write("\n")
