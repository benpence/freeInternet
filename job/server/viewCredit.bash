#!/bin/bash

while /bin/true; do 
    clear;
    sqlite3 -column -header ../../database.db "SELECT * FROM credit;";
    echo ;
    sqlite3 -column -header ../../database.db "SELECT * FROM translation;";
    sleep 5;
done
