import sys
from argparse import ArgumentParser
from itertools import (chain, combinations)

def read_data(filepath):
    """
    Return itemsets & trans array from the file
    """
    trans = []
    with open(filepath) as fp:
        for line in fp:
            trans.append(frozenset({x.strip() for x in line.split(',')}))
    itemsets = {y for x in trans for y in x}

    return list(itemsets), trans

def output(filepath, itemsets, trans):
    """
    Write data to filepath in weka format
    """
    with open(filepath, "w") as fp:
        # first row lists all items
        attr = ",".join(itemsets)
        fp.write(attr)
        fp.write("\n")

        # write "true" if item is in the trans. else write "false", and seperate items by comma
        for tran in trans:
            tran_str = ""
            for item in itemsets:
                if item in tran:
                    tran_str = tran_str + "true,"
                else:
                    tran_str = tran_str + "false,"
            # remove the end comma
            tran_str = tran_str[:-1]
            fp.write(tran_str)
            fp.write("\n")

def filter_result(in_filepath):
    """
    Remove all lines containing "false" and write the result to <in_filepath>_filter.<ext>
    """
    try:
        ext_index = in_filepath.index(".")
        out_filepath = in_filepath[:ext_index] + "_filter" + in_filepath[ext_index:]
    except:
        # in_filepath without extension
        out_filepath = in_filepath + "_filter"

    with open(in_filepath, "r") as rfp:
        with open(out_filepath, "w") as wfp:
            for line in rfp:
                if not "false" in line:
                    wfp.write(line)

def cmd():
    # Parse options
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', help='Input csv file path (data separating with comma)', dest='in_file')
    parser.add_argument('-o', '--output', help='output file path', dest='out_file')
    parser.add_argument('-f', '--filter', help='filter file path', dest='filter_file')
    options = parser.parse_args()

    used = False
    # Convert input csv file to weka csv format
    if options.in_file and options.out_file:
        itemsets, trans = read_data(options.in_file)
        output(options.out_file, itemsets, trans)
        used = True
    # Remove all line contain "false"
    if options.filter_file:
        filter_result(options.filter_file)
        used = True

    if not used:
        parser.print_help()

if __name__ == '__main__':
    cmd();
