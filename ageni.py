#!/usr/bin/env python3

# AGENI = Acronym GEnerator for Name Ideas
# December 2016
# author: Gary (gary DOT weissman AT uphs DOT upenn DOT edu)
# license: GPL-3

# this script takes some words then generates potential acronyms

import sys, re, argparse
from itertools import permutations

# build parser for arguments
parser = argparse.ArgumentParser(description='Get anagrams of some letter combinations to help think of cool trial name acronyms.')
parser.add_argument('keywords', metavar='K', nargs = '+',
	 help='A list of keywords separated by spaces')
parser.add_argument('-f','--fuzzy',help='Allow up to 1 extra letter between those selected from keywords',
	action='store_true') 
parser.add_argument('-d','--drop', type=int, default = 0,
	help = 'Max number of keywords to drop to find a match.')
parser.add_argument('--dict', help = 'Set a different dictionary path.')

# get the arguments
args = parser.parse_args()
kw = args.keywords
drop = args.drop

# this is the default dictionary: can vary on other machines
default_dict = '/etc/dictionaries-common/words'
my_dict = default_dict if args.dict is None else args.dict

# some error checking
if (drop > len(kw)):
	drop = len(kw) - 1
	print('Warning: Drop cannot be more than all keywords. Reducing drop size to ',drop)
if (drop < 0):
	drop = 0;
	print('Warning: Drop cannot be a negative number. Changing drop to ', drop)

# get the letters of interest
loi = [ x[0] for x in kw]

# get some words
f = open(my_dict,'r')
wraw = f.readlines()
f.close()
# strip line ending for each
wlist = [re.sub('\n','',x) for x in wraw]

# now generate all possible combinations of these letters

p_object = permutations(loi, len(loi))
combos = [x for x in p_object if not None in x]

if (drop > 0):
	for d in list(range(1,drop+1)):
		perms = permutations(loi, len(loi) - d)
		combos.extend([x for x in perms if not None in x])


# check the number of combinations and issue warning if its too big
warn_limit = 1000
if (len(combos) > warn_limit):
	print('Warning: you are matching against over',warn_limit,'letter combinations')
	print('This might take a long time. Are you sure you want to do this?')
	contyn = input('Press any key to continue, or press \'q\' to quit.')
	if (contyn == "q"):
		print('Quitting...')
		sys.exit()
	
# print plan
print('\nNow building anagrams for',len(combos),'letter combinations with fuzzy matching:',
	'ON' if args.fuzzy else 'OFF', 'and dropping up to', drop,'terms')

# use either nothing or some kind of buffer depending on flags
btw = "[a-z\']{0,1}" if args.fuzzy else ""

# now build each regex
regs = []

for c in combos:
	n = "^" + btw.join(c) + "$"
	regs.append(re.compile(n))

results = []

# now check regex against each word
# is there a faster way to do this?
for r in regs:
	for w in wlist:
		m = r.search(w.lower())
		if (m != None): results.append(m.group(0))

# print unique sorted results
for r in set(results):
	print(r)


