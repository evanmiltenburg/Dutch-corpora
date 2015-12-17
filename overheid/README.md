# Overheid.nl Corpus (version 1, June 2015)

This folder contains scripts to create a corpus of Dutch government-related texts.
That corpus is hosted [here](http://kyoto.let.vu.nl/~miltenburg/public_data/overheid/).

This corpus is based on open XML data from the Dutch government, obtained through
[Overheid.nl](www.overheid.nl). This data consists of text from four types of sources
(codes between parentheses are those used by Overheid.nl, which I kept for consistency):

* Kamervragen met antwoorden (ah)
* Handelingen (h)
* Kamerstukken (kst)
* Staatscourant (stcrt)

# Size

The following table was generated using `python stats.py > stats.txt`. You can find this script in the
`scripts` folder. This script doubles as the simplest example of how to loop over all the text in the
different files.

Type        |     Count
:---------- | --------:
ah_plain    |  33552672
kst_plain   | 470323325
stcrt_plain | 193701516
h_plain     | 173886809
total       | 871464322

# Creation

Overheid.nl has an sftp server [bestanden.officielebekendmakingen.nl](bestanden.officielebekendmakingen.nl),
that is described in [this pdf file](http://www.koop.overheid.nl/sites/koop.wmrijk.nl/files/Handleiding%20uitvragen%20Offici%C3%ABle%20Publicaties_0.pdf).

I used this server to retrieve XML files from 1995-2014 (i.e. 20 years). For this purpose, I wrote two standalone scripts:

* `overheid_sftp.py` to collect files of a given type for a specific year.
* `overheid_range_sftp.py` to collect files of a given type for a range of years. (This is the one I used)

While the latter is very useful to retrieve everything at once, one might choose to use the former to add or update files for a particular year.
For example, one might want to get all the data for 2015 (currently not part of the corpus) as well. `overheid_sftp.py` is well-suited for this.
To get the 'kamervragen met antwoorden', simply use `python overheid_sftp.py 2015 ah`.

Both scripts download all the xml data to the ah, h, kst and stcrt folders. I used `make_all_plain.py` to create files containing tokenized
plain text for each source type. During this conversion, the files were immediately compressed (in gzip format)
in order to save space.

# Processing details

* In the XML files, every paragraph of text is contained in `<al>`-tags (presumably 'alinea').
* For each paragraph, I used the Dutch sentence splitter from the NLTK package to get sentences.
* For each sentence, I used the generic `word_tokenize` function from the NLTK package to get words.
* All sentences were filtered using the following conditions:
    * Length: Sentences have to contain more than 4 tokens.
    * Lists: Sentences cannot contain lists (these are typically attendance lists, which aren't of interest to me).
        List heuristic: a sentence contains a list if it contains more than 4 commas.
    * Digits: Sentences cannot contain too many digits (>50% of the tokens).
* I wrote all 'approved' sentences to a file, one sentence per line, and
 joined the tokens of each sentence using spaces.

# Use

The corpus is very straightforward to use. In Python, import the `gzip` module to be able to open the files.
You can then use `with gzip.open('ah_plain.txt.gz') as f: ...` instead of the usual
`with open('ah_plain.txt.gz') as f: ...`, and proceed as normal. Tokenize sentences using `str.split()`.
