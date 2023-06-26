#!/monitoringScripts/VENVT/bin/python
import sys
import sqlite3
import os

script_home = os.path.dirname(os.path.abspath(__file__))
dbpath = script_home+"/../rds_stat.db"
conn = sqlite3.connect(dbpath)
cursor = conn.cursor()

DBInstanceIdentifier=sys.argv[1]
region_name=sys.argv[2]

# Define the query to select the latest record -only1 row
query = "SELECT disk_free FROM disk_free WHERE DBInstanceIdentifier = ? and region_name = ?  ORDER BY id DESC LIMIT 1;"
rows = cursor.execute(query, (DBInstanceIdentifier, region_name))
for row in rows:
    disk_free = row[0]

if disk_free <= 10:
    print(f"CRITICAL - free disk space is less than threshold {disk_free}")
    sys.exit(2)
elif disk_free <= 20:
    print(f"WARNING - free disk space is approaching threshold {disk_free}")
    sys.exit(1)
else:
    print(f"OK - free disk space is within limits {disk_free}")
    sys.exit(0)
