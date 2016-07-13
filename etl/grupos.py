import csv

with open('interacciones.csv') as f:
    data = list(csv.reader(f, delimiter='|'))

    for i in data:
        print(i[2])
