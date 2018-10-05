from argparse import ArgumentParser
from itertools import (chain, combinations)

def gen_C(lc_set):
    """
    [
        ((1), (2), (3)),
        ((1,2), (2,3), (1,3)...)
    ];

          |
          V
    
    [
        ((1), (2), (3)),
        ((1,2), (2,3), (1,3)...)
        ((1,2,3), (...)
    ];
    """
    flat_set = list(chain.from_iterable(lc_set))
    nextset = {frozenset(x.union(y)) for x in flat_set for y in flat_set if len(x.union(y))==len(lc_set)+1}
    lc_set.append(nextset)
    return nextset

def count_freq(count_dict, set_list, trans):
    """
    Count itemsets in transctions and update the count_dict
    """
    for x in set_list:
        count_dict[x] = 0
    for x in set_list:
        for y in trans:
            if x.issubset(y):
                count_dict[x] = count_dict[x] + 1

def proper_subset(ori):
    """
    Return a list of proper subsets with size > 0
    """
    ret = list(chain.from_iterable([combinations(ori, i) for i in xrange(1, len(ori))]))
    return [frozenset(x) for x in ret]

def read_data(filepath):
    """
    Return itemsets & trans array from the file
    """
    trans = []
    with open(filepath) as fp:
        for line in fp:
            trans.append(frozenset({x.strip() for x in line.split(',')}))
    itemsets = {frozenset([y]) for x in trans for y in x}

    return itemsets, trans

def set_string(itemset):
    return "(" + ", ".join(x for x in itemset) + ")"

def print_result(lc_set, rules):
    # print freq. itemset
    print ">> Frequent Itemsets <<"
    for set_list in lc_set:
        for x in set_list:
            print set_string(x)

    print ""
    print ">> Rules <<"
    for x in rules:
        for y in rules[x]:
            inference, confidence = y
            print set_string(x), "=>", set_string(inference), "%.3f"%confidence

def cmd():
    # Parse options
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', help='Input csv file path (data separating with comma)', dest='filepath', required=True)
    parser.add_argument('-s', '--minsup', help='minumum support (0~1)', dest='minsup', default=0.5)
    parser.add_argument('-c', '--minconf', help='minimum confidence (0~1)', dest='minconf', default=0.9)
    options = parser.parse_args()

    itemsets, trans = read_data(options.filepath)

    ## Apriori Algorithm

    # init. one set
    count_dict = {}
    lc_set = [itemsets.copy()]
    while True:
        # gen. Lk-1
        count_freq(count_dict, lc_set[-1], trans)
        for x in lc_set[-1].copy():
            sup = 1.0*count_dict[x]/len(itemsets)
            if sup < options.minsup:
                lc_set[-1].remove(x)
        if len(lc_set[-1]) == 0:
            break
        # gen. Ck
        gen_C(lc_set)
    # Remove last empty set
    lc_set.pop(-1)

    # check minimum confidence
    rules = {}
    for kset in lc_set[1:]:
        for y in kset:
            subset = proper_subset(y)
            for x in subset:
                inference = y.difference(x)
                # confidence: ratio of trans. which contains x also contains y
                if count_dict.get(x, 0)>0 and 1.0*count_dict[y]/count_dict[x] >= options.minconf:
                    rules[x] = rules.get(x, None) or []
                    rules[x].append((inference, 1.0*count_dict[y]/count_dict[x]))

    print_result(lc_set, rules)

if __name__ == '__main__':
    cmd();
