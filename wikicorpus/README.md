# Wikipedia corpus for Dutch (version 1, June 2015)
This folder contains the scripts I used to create the Wikipedia plaintext corpus
hosted [here](http://kyoto.let.vu.nl/~miltenburg/public_data/wikicorpus/). This
is a corpus based on the Dutch Wikipedia. It consists of 192,830,802 tokens
(words + interpunction).

# Source
This corpus is based on the backup dump of April 29, 2015. That file can be found [here](http://dumps.wikimedia.org/nlwiki/20150429/nlwiki-20150429-pages-meta-current1.xml.bz2).

# Processing
To process the data, I made use of the following scripts:

- [WikiExtractor.py](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor) is a script that parses Wikipedia dumps and extracts all text from them, while ignoring boilerplate data.
- `plainwiki.py` processes the output of WikiExtractor and writes all the text to a single file. In this file, every sentence is on a new line, and all tokens are space-separated.
    Sentences with 4 or less tokens (words or punctuation) were ignored. This way we can remove headers (titles etc.) from the data.

For the tokenization, I used the Dutch sentence tokenizer from the NLTK, and the standard word tokenizer from the same package.
