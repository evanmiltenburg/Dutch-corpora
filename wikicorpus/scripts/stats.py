import gzip

with gzip.open('../corpus/wikicorpus.txt.gz') as f:
    print sum(len(line.split()) for line in f)
