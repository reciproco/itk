#!/bin/bash
sqlite3 ./db.sqlite3 <<!
.headers on
.mode csv
.separator "|"
.import ./etl/$1.csv interacciones_$1
!
