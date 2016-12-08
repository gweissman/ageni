AGENI is the Acrononym GEnerator for Name Ideas

It helps when thinking of fun names for randomized controlled trials based on some keywords.

Standard usage:

```
./ageni.py heartburn gerd treatment awesome best ever
```

Use the `--help` flag for help:

```
usage: ageni.py [-h] [-f] [-d DROP] [--dict DICT] [-v] K [K ...]

Get anagrams of some letter combinations to help think of cool trial name
acronyms.

positional arguments:
  K                     A list of keywords separated by spaces

optional arguments:
  -h, --help            show this help message and exit
  -f, --fuzzy           Allow up to 1 extra letter between those selected from
                        keywords
  -d DROP, --drop DROP  Max number of keywords to drop to find a match.
  --dict DICT           Set a different dictionary path.
  -v, --verbose         Report verbose progress.
```
