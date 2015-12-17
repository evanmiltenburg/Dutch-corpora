# Standard library:
import glob
import gzip
from itertools import imap

# Additional modules:
import nltk.data
from nltk.tokenize import word_tokenize
from lxml import etree,html

class wikipedia_text(object):
    def __init__(self, dirname='text'):
        self.dirname = dirname
        self.sent_tokenizer = nltk.data.load('tokenizers/punkt/dutch.pickle')
    
    def sent_tokenize(self,text):
        return self.sent_tokenizer.tokenize(text)
    
    def lower_word_tokenize(self,sentence):
        return word_tokenize(sentence.lower())
    
    def __iter__(self):
        for fname in glob.glob(self.dirname+'/*/*'):
            with open(fname) as f:
                contents = '<contents>'+f.read()+'</contents>'
                root = html.fromstring(contents)
                for doc in root.iterfind('doc'):
                    for sentence in imap(self.lower_word_tokenize, self.sent_tokenize(doc.text)):
                        if len(sentence) > 4:
                            yield sentence

text = wikipedia_text()
with gzip.open('nlwiki-20150429-plain.txt.gz','w') as f:
    batch = []
    for line in text:
        batch.append(' '.join(line).encode('utf-8'))
        if len(batch) > 500:
            f.write('\n'.join(batch))
            f.write('\n')
            batch = []
    f.write('\n'.join(batch))
