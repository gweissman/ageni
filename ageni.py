#!/usr/bin/env python3

# AGENI = Acronym GEnerator for Name Ideas
# November 2017
# author: Gary (gary DOT weissman AT uphs DOT upenn DOT edu)
# license: GPL-3

# this script takes some words then generates potential acronyms

import sys, re, argparse
from itertools import permutations

# build parser for arguments
parser = argparse.ArgumentParser(description='Get anagrams of some letter combinations to help think of cool trial name acronyms.')
parser.add_argument('keywords', metavar='K', nargs = '+',
	 help='A list of keywords separated by spaces')
parser.add_argument('-f','--fuzzy',help='Allow optional use of the second letter from keywords',
	action='store_true') 
parser.add_argument('-d','--drop', type=int, default = 0,
	help = 'Max number of keywords to drop to find a match.')
parser.add_argument('--dict', help = 'Set a different dictionary path.')
parser.add_argument('-v','--verbose', help = 'Report verbose progress.', 
	action='store_true')
parser.add_argument('-p','--parallel', help = 'Run in parallel with joblib. Requires joblib.',
	action='store_true')
parser.add_argument('-n','--n_cpus', type=int, default = 5, 
	help = 'Number of CPUs to use with parallel jobs.')

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
if (args.fuzzy):
	loi = [ '(' + x[0:2].lower() + '?)' if len(x) > 1 else '('+x[0].lower()+')' for x in kw]
else:
	loi = [ x[0].lower() for x in kw]


# get some words
f = open(my_dict,'r')
wraw = f.readlines()
f.close()
# strip line ending for each
wlist = [re.sub('\n','',x) for x in wraw]
wcombo = " ".join(wlist)

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

# now build each regex
regs = []

if (not args.parallel):
	for c in combos:
		n = "\s" + ''.join(c) + "\s"
		regs.append(re.compile(n))
else:
	from joblib import Parallel, delayed
	def comprgx(c):
		n = "\s" + ''.join(c) + "\s"
		return(re.compile(n))
	regs = Parallel(n_jobs=args.n_cpus,verbose=args.verbose)(delayed(comprgx)(c) for c in combos)	

results = []

# now check regex against each word
print('Now checking letter combinations against dictionary...')
# is there a faster way to do this?
if (not args.parallel):
	for i,r in enumerate(regs):
		results.extend(r.findall(wcombo))
		if (args.verbose and i > 0):
			if (i % (0.1 * len(regs)) == 0):
				print(i, 'combinations checked')
else:
	from joblib import Parallel, delayed
	def helpfind(rgx,txt):
		return(rgx.findall(txt))
	results = Parallel(n_jobs=args.n_cpus,verbose=args.verbose)(delayed(helpfind)(rgx=r,txt=wcombo) for r in regs)

# return acknowledgment of null result if applicable
if len(results) == 0:
	print("Sorry, we didn't find any matches.")
else:
	print("Matching terms:\n")

# unlist the lists if needed
results = sum(results, [])
			
# print unique sorted results
for r in set(results):
	print(''.join(r))


