#!/bin/bash

while /bin/true; do clear; sqlite3 database.db "SELECT * FROM credit;"; sleep 1; done
