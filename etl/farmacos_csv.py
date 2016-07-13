import csv


def read_csv(file):
    with open(file) as f:
        data = list(csv.reader(f, delimiter='|'))
    return data


grupos = read_csv('Grupo.csv')
farmacos = read_csv('farmacos.uniq')


for n,f in enumerate(farmacos):
    for g in grupos:
        if g[1] == f[1]:
            f[1] = g[0]
    print('%s|%s|%s' % (str(n+1),f[0],f[1]))



