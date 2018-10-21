from argparse import ArgumentParser
from itertools import (chain, combinations)
from collections import defaultdict

def read_data(filepath):
    """
    Return itemsets & trans array from the file
    trans: [(set(), <count>)]
    """
    trans = []
    with open(filepath) as fp:
        for line in fp:
            trans.append(({x.strip() for x in line.split(',')}, 1))

    return trans

def count_freq(count_dict, set_list, trans):
    """
    Count itemsets in transctions and update the count_dict
    """
    for x in set_list:
        count_dict[x] = 0
    for x in set_list:
        for tran in trans:
            if x in tran[0]:
                count_dict[x] = count_dict[x] + tran[1]


def sorted_mincount_trans(trans, mincount, subtree=False):
    """
    Remove items from transactions if they do not satisfy minimum count condition.
    Rearrange item order for each transaction accroding to the frequence of one-item set.
    If this function is called by subtree, then there is no need to rearrange item order.
    """

    # trans to itemset
    itemsets = {y for x in trans for y in x[0]}

    ## Create sorted one-item list
    count_dict = {}
    # one item count
    count_freq(count_dict, itemsets, trans)
    # check mincount
    freq_items = {k: v for k, v in count_dict.iteritems() if v >= mincount}
    # sort one-item by count
    sorted_freq_list = sorted(freq_items.iteritems(), key=lambda x: x[1], reverse=True)
    # assign index of elements in freq_list
    freq_list_index_map = {}
    for i, x in enumerate(sorted_freq_list):
        freq_list_index_map[x[0]] = i

    ## Modify and reorder all trans. according to sorted one-item list
    # create set of freq. one item
    freq_one_item_set = {x for x, y in sorted_freq_list}
    # delete unfreq, items and represent sorted trans. by 2d list
    sorted_trans = [(list(tran[0] & freq_one_item_set), tran[1]) for tran in trans]
    # rearrange trans. by sorted_freq_list
    if not subtree:
        for idx, tup in enumerate(sorted_trans):
            sorted_trans[idx] = (sorted(tup[0], key=lambda x: freq_list_index_map[x]), tup[1])

    return sorted_freq_list, sorted_trans

class Node(dict):
    """
    Node is identified and hashed by the name. Therefore, nodes in the same tree must with different names.
    Root node does not has name.
    """

    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent # Node
        self.child = {} # str => Node
        self.count = 0

    def is_root(self):
        return self.name is None

    def __str__(self):
        # Root
        if self.name is None:
            return "Node<_Root_>"
        elif self.parent is None:
            return "Node<"+ self.name + ": ?>"
        else:
            return "Node<"+ self.name + ": %s>" % (self.parent.name if self.parent.name else "_Root_")

    def __repr__(self):
        return self.__str__()

    def is_root(self):
        return self.name == None

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.count < other.count

class Tree(dict):
    """
    FP Grwoth tree.
    """

    def __init__(self, trans, threshold, subtree_item=None):
        """
        If the subtree_item is not None, then the tree is a conditional tree,
        and the threshold will be minimum count as opposed to minimum support.
        Otherwise, the tree is not a conditional tree, the threshold = minsup.
        """
        self.trans = trans
        if subtree_item is not None:
            self.mincount = threshold
        else:
            self.mincount = threshold * len(trans)
        self.subtree_item = subtree_item # type = Node

        self.horizon_access = defaultdict(list) # {name: [node...]}
        self.root = None
        self.sf_items, self.sm_trans = sorted_mincount_trans(self.trans, self.mincount, self.subtree_item is not None)
        self.build()

    def build(self):
        """
        Create fp tree accroding to trans. and record horizontal access order (i.e header list).
        """
        self.root = Node()
        for tran in self.sm_trans:
            cur_node = self.root
            for x in tran[0]:
                # try to get old node
                next_node = cur_node.child.get(x, None)
                # if new node is created
                if next_node is None:
                    next_node = Node(x)
                    self.horizon_access[x].append(next_node)
                # connect and count
                self.connect(cur_node, next_node, tran[1])
                # move to next node
                cur_node = next_node

    def print_tree(self, root):
        print root
        for x in root.child.values():
            self.print_tree(x)

    def find_patterns(self):
        """
        Find all patterns satisfy the minimum support and return them as a list of tuple.
        For each 1 freqent item, if this tree has branch, then it will construct conditional subtree recusively
        until trivial enough to find trivial patterns.
        """
        ret = []
        if self.has_branch():
            for item, _ in reversed(self.sf_items):
                item_linkedlist = self.horizon_access[item]
                subtree_trans = []
                for item_node in item_linkedlist:
                    count = item_node.count
                    item_node = item_node.parent
                    traceback = set() # list of traceback node name (exclude the btn item)
                    while not item_node.is_root():
                        traceback.add(item_node.name)
                        item_node = item_node.parent
                    # create traceback with btn item count
                    subtree_trans.append((traceback, count))
                subtree = Tree(subtree_trans, self.mincount, item)
                ret.extend(subtree.find_patterns())

        else:
            ret = self.trivial_patterns()

        # add subtree condition item
        if self.subtree_item is not None:
            for i, t in enumerate(ret):
                ret[i] = t + (self.subtree_item,)
            ret.append((self.subtree_item,))
        return ret


    def subset(self, ori):
        ret = list(chain.from_iterable(combinations(ori, i) for i in xrange(1, len(ori)+1)))
        return ret

    def trivial_patterns(self):
        """
        Return a list of patterns (tuple) if the tree does not have branch
        """
        trace = []
        assert self.root is not None
        current_node = self.root
        while len(current_node.child)>0:
            current_node = current_node.child.values()[0]
            trace.append(current_node.name)
        ret = self.subset(trace)
        return ret

    def has_branch(self):
        assert self.root is not None
        current_node = self.root
        while len(current_node.child)==1:
            current_node = current_node.child.values()[0]
        return len(current_node.child)>1 

    def connect(self, parent, child, count=1):
        """
        Connect parent and child nodes by setting attr. of nodes
        """
        parent.child[child.name] = child
        child.parent = parent
        child.count = child.count + count

def set_string(itemset):
    return "(" + ", ".join(x for x in itemset) + ")"

def print_result(patterns):
    # print freq. itemset
    print ">> Frequent Itemsets <<"
    patterns = [x for x in sorted(patterns, key=lambda x: len(x))]
    for pattern in patterns:
        print set_string(pattern)


def cmd():
    # Parse options
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', help='Input csv file path (data separating with comma)', dest='filepath', required=True)
    parser.add_argument('-s', '--minsup', help='minumum support (0~1)', dest='minsup', default=0.5, type=float)
    options = parser.parse_args()

    trans = read_data(options.filepath)

    ## FP-Growth Algorithm
    
    fp = Tree(trans, options.minsup)
    pats = fp.find_patterns()
    print_result(pats)

if __name__ == '__main__':
    cmd();
