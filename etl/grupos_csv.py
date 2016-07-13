import csv

with open('grupos.uniq') as f:
    data = list(csv.reader(f, delimiter='|'))

    for num, name in enumerate(data):
        print(str(num+1) + '|' + name[0])
