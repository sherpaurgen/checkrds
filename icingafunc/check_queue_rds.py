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
query = "SELECT diskqueuedepth FROM diskqueuedepth WHERE DBInstanceIdentifier = ? and region_name = ?  ORDER BY id DESC LIMIT 1;"
rows = cursor.execute(query, (DBInstanceIdentifier,region_name))
for row in rows:
    diskqueuedepth = row[0]

if diskqueuedepth >= 10:
    print(f"CRITICAL - db queue is above threshold {diskqueuedepth}")
    sys.exit(2)
elif diskqueuedepth >= 5:
    print(f"WARNING - db queue is approaching threshold {diskqueuedepth}")
    sys.exit(1)
else:
    print(f"OK - db queue is within limits {diskqueuedepth}")
    sys.exit(0)
