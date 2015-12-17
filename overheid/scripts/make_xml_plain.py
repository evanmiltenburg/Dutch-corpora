from bs4 import BeautifulSoup
import nltk.data
from nltk.tokenize import word_tokenize
import glob
import gzip
import sys

tokenizer = nltk.data.load('tokenizers/punkt/dutch.pickle')

def good_sentence(s):
    if len(s) < 4 or s.count(',') > 4:
        return False
    else:
        digits = filter(lambda x:x.isdigit(),s)
        
        if len(digits) > (float(len(s))/2):
            return False
        else:
            return True

def sentences_for_file(filename):
    with open(filename) as f:
        soup = BeautifulSoup(f)
        pars = filter(lambda p: not p == None,
                      map(lambda x:x.get_text(), soup.find_all('al')))
        sentences = [word_tokenize(sentence) for x in pars
                     for sentence in tokenizer.tokenize(x)]
        return [' '.join(s).encode('utf-8') for s in filter(good_sentence, sentences)]

def main(ftype):
    with gzip.open('../corpus/' + ftype + '_plain.txt.gz','w') as f:
        for filename in glob.glob('../data/' + ftype + '/*/*.xml'):
            f.write('\n'.join(sentences_for_file(filename)))

if __name__ == "__main__":
    ftypes  = {'kst', 'trb', 'stb', 'ag', 'ah', 'stcrt', 'kv', 'h', 'blg', 'nds'}
    ftype   = sys.argv[1]
    if ftype in ftypes:
        main(ftype)
    else:
        raise KeyError('No known folder of that type. (You entered: '+ftype + ')')
