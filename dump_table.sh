#!/bin/bash
sqlite3 ./db.sqlite3 <<!
.headers on
.mode csv
.separator "|"
.output $1.csv
select * from interacciones_$1;
!
