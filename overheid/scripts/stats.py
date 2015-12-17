import gzip, glob
import tabulate

def filename_to_name(filename):
    return filename.split('/')[-1].split('.txt')[0]

table = []
for filename in glob.glob('../corpus/*'):
    with gzip.open(filename) as f:
        tokens = sum(len(line.split()) for line in f)
    table.append([filename_to_name(filename), tokens])
table.append(['total', sum(b for a,b in table)])

print tabulate.tabulate(table, headers=['Type', 'Count'])
