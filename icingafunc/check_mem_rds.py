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
query = "SELECT MemUsage FROM mem_free WHERE DBInstanceIdentifier = ? and region_name = ?  ORDER BY id DESC LIMIT 1;"
rows=cursor.execute(query, (DBInstanceIdentifier,region_name))
for row in rows:
    MemUsage = row[0]

if MemUsage <= 100:
    print(f"CRITICAL - memory free is below threshold {MemUsage} MB")
    sys.exit(2)
elif MemUsage <= 300:
    print(f"WARNING - memory free is below threshold {MemUsage} MB")
    sys.exit(1)
else:
    print(f"OK - memory free is within limits {MemUsage} MB")
    sys.exit(0)
