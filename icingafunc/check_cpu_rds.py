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
query = "SELECT CpuUsage FROM cpu_usage WHERE DBInstanceIdentifier = ? and region_name = ?  ORDER BY id DESC LIMIT 1;"
rows=cursor.execute(query, (DBInstanceIdentifier,region_name))
for row in rows:
    cpuusage = row[0]

if cpuusage >= 90:
    print(f"CRITICAL - cpu usage is above threshold {cpuusage}")
    sys.exit(2)
elif cpuusage >= 75:
    print(f"WARNING - cpu usage is approaching threshold {cpuusage}")
    sys.exit(1)
else:
    print(f"OK - cpu usage is within limits {cpuusage}")
    sys.exit(0)
