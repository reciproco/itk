#!/bin/bash

cat IMATINIB.csv NILOTINIB.csv DASATINIB.csv BOSUTINIB.csv PONATINIB.csv > interacciones.csv
sed -i.bak '/GRUPO TERA/d' interacciones.csv
sed -i.bak s/Acido/Ácido/g interacciones.csv
sed -i.bak s/Imunomoduladores/Inmunomoduladores/g interacciones.csv
sed -i.bak s/Tretinoina/Tretinoína/g interacciones.csv
sed -i.bak s/Topotecan/Topotecán/g interacciones.csv
sed -i.bak s/Tolvaptan/Tolvaptán/g interacciones.csv
sed -i.bak 's/H. Preparados Hormonales Sistémicos, excl Hormonas Sexuales/H. Preparados Hormonales Sistémicos, excl. Hormonas Sexuales/g' interacciones.csv
sed -i.bak 's/Sodio, Bicarbonato /Sodio, Bicarbonato/g' interacciones.csv
sed -i.bak 's/l. Agentes Antineoplásicos/L. Agentes Antineoplásicos/g' interacciones.csv
sed -i.bak 's/Magnesio Hidróxido/Magnesio, Hidróxido/g' interacciones.csv
sed -i.bak 's/Ketoconazol /Ketoconazol/g' interacciones.csv
sed -i.bak 's/Dabigatran/Dabigatrán/g' interacciones.csv
sed -i.bak 's/Arsenico, Trióxido/Arsénico, Trióxido/g' interacciones.csv

python grupos.py > grupos.raw
sort grupos.raw | uniq > grupos.uniq
python grupos_csv.py > grupo.csv

python farmaco_y_grupo.py > farmacos.raw
sort farmacos.raw | uniq > farmacos.uniq
python farmacos_csv.py > farmaco.csv

python relaciones_csv.py > rel_itk_far.csv


