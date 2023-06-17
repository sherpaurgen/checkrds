import concurrent.futures
import time
import yaml
import os
from dbhandler.db import create_diskusage_table
from dbhandler.db import create_cpuusage_table
from dbhandler.db import create_memusage_table
from dbhandler.db import insert_cpuusage_data
from dbhandler.db import insert_memfree_data
from dbhandler.db import create_diskqueuedepth_table
from dbhandler.db import insert_diskqueuedepth_data
from helpers.utility import get_rds_freeable_memory
from helpers.utility import get_cpu_usage
from helpers.utility import list_available_db
from helpers.utility import get_rds_DiskQueueDepth


def main():
    start_time = time.time()
    cwd = os.getcwd()
    rds_conf_path = cwd + '/config/rds.yaml'
    dbfile = cwd + '/rds_stat.db'
    create_diskusage_table(dbfile)
    create_memusage_table(dbfile)
    create_cpuusage_table(dbfile)
    create_diskqueuedepth_table(dbfile)

    with open(rds_conf_path, 'r') as fh:
        data = yaml.safe_load(fh)
    Namespace = data["Namespace"]
    tmp_alldb = []

    for region in data['Regions']:
        tmp_alldb.append(list_available_db(region, Namespace))
    alldb = []

    if len(tmp_alldb) > 0:
        for objlist in tmp_alldb:
            if len(objlist) > 0:
                for db in objlist:
                    alldb.append(db)
    # alldb --
    # [{'DBInstanceIdentifier': 'database-1', 'AllocatedStorage': 20, 'DBInstanceClass': 'db.t3.micro', 'Engine': 'mysql', 'region_name': 'us-east-1', 'Namespace': 'AWS/RDS'}, {'DBInstanceIdentifier': 'pgsql-2', 'AllocatedStorage': 20, 'DBInstanceClass': 'db.t3.micro', 'Engine': 'postgres', 'region_name': 'us-east-1', 'Namespace': 'AWS/RDS'}]
    cpu_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures=[]
        for data in alldb:
            futures.append(executor.submit(get_cpu_usage,data))
        for res in concurrent.futures.as_completed(futures):
            cpu_data.append(res.result())
    #cpu_data= [{'DBInstanceIdentifier': 'pgsql-2', 'AllocatedStorage': 20, 'DBInstanceClass': 'db.t3.micro', 'Engine': 'postgres', 'region_name': 'us-east-1', 'Namespace': 'AWS/RDS', 'cpu_usage': 5.366487783740542}

    for data in cpu_data:
        insert_cpuusage_data(dbfile, data)

    # memory stat fetch starts here
    mem_data=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        memfut=[]
        for d in alldb:
            memfut.append(executor.submit(get_rds_freeable_memory,d))
        for res in concurrent.futures.as_completed(memfut):
            mem_data.append(res.result())

    for d in mem_data:
        insert_memfree_data(dbfile,d)

    diskqueue=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        queueFut=[]
        for d in alldb:
            queueFut.append(executor.submit(get_rds_DiskQueueDepth,d))
        for res in concurrent.futures.as_completed(queueFut):
            diskqueue.append(res.result())
    for d in diskqueue:
        insert_diskqueuedepth_data(dbfile,d)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Elapsed: {execution_time}s")


if __name__ == '__main__':
    main()
