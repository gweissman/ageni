AGENI is the Acrononym GEnerator for Name Ideas

It helps when thinking of fun names for randomized controlled trials based on some keywords.

Standard usage:

```
./ageni.py heartburn gerd treatment awesome best ever
```

Use the `--help` flag for help:

```
usage: ageni.py [-h] [-f] [-d DROP] [--dict DICT] [-v] [-p] [-n N_CPUS]
                K [K ...]

Get anagrams of some letter combinations to help think of cool trial name
acronyms.

positional arguments:
  K                     A list of keywords separated by spaces

optional arguments:
  -h, --help            show this help message and exit
  -f, --fuzzy           Allow optional use of the second letter from keywords
  -d DROP, --drop DROP  Max number of keywords to drop to find a match.
  --dict DICT           Set a different dictionary path.
  -v, --verbose         Report verbose progress.
  -p, --parallel        Run in parallel with joblib. Requires joblib.
  -n N_CPUS, --n_cpus N_CPUS
                        Number of CPUs to use with parallel jobs.
```

For example, on MacOS the Unix word file is found at `/usr/share/dict/words`
