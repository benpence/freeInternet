#!/bin/bash
sqlite3 ../database.db "UPDATE credit SET credit = $2 WHERE client = '128.164.160.198'"
sqlite3 ../database.db "UPDATE credit SET credit = $1 WHERE client = '128.164.160.199'"


