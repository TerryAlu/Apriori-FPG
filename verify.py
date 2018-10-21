import sys
from ast import literal_eval

if len(sys.argv) != 3:
    print "./%s <apriori_output> <fpg_output>" % __file__
    print sys.exit(1)

def make_set(setstr):
    outset = literal_eval(setstr)
    if type(outset) is int:
        outset = (outset,)
    return frozenset(outset)

def verify(s1, s2):
    if len(s1) != len(s2):
        return False
    for x in s1:
        if x not in s2:
            return False
    return True

def read_data(filename):
    res = set()
    with open(filename, "r") as fp:
        _ = fp.readline()
        for line in fp:
            if "Rules" in line:
                break
            try:
                res.add(make_set(line))
            except:
                pass
    return res


apriori_output = read_data(sys.argv[1])
fpg_output = read_data(sys.argv[2])

##  DEBUG: show results
# for x in sorted(apriori_output, key=lambda x: len(x)):
    # print x
# print "---"
# for x in sorted(fpg_output, key=lambda x: len(x)):
    # print x

result = verify(apriori_output, fpg_output)
print "Verify Result: %s" % ("OK" if result else "Fail")
if result:
    sys.exit(0)
else:
    sys.exit(1)
