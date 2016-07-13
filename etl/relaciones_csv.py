import csv


def read_csv(file):
    with open(file) as f:
        data = list(csv.reader(f, delimiter='|'))
    return data


itks = read_csv('itk.csv')
farmacos = read_csv('farmaco.csv')
inter = read_csv('interacciones.csv')


for n,i in enumerate(inter):
    for it in itks:
        if i[0] == it[1]:
            i[0] = it[0]
    for f in farmacos:
        if i[1] == f[1]:
            i[1] = f[0]

    print('%s|%s|%s|%s|%s|%s|%s' % (str(n+1), i[3], i[5], i[4],
                                    i[6], i[1], i[0]))
