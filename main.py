import concurrent.futures
import time
import yaml
import os
from dbhandler.db import create_diskfree_table,insert_diskfree_data
from dbhandler.db import create_cpuusage_table
from dbhandler.db import create_memfree_table
from dbhandler.db import insert_cpuusage_data
from dbhandler.db import insert_memfree_data
from dbhandler.db import create_diskqueuedepth_table,create_elbresponsetime_table
from dbhandler.db import insert_diskqueuedepth_data,insert_elbresponsetime_data
from dbhandler.db import truncate_tables,create_elbtargetgroup_table,insert_elbtargetgroup_data
from helpers.utility import get_rds_freeable_memory
from helpers.utility import get_cpu_usage
from helpers.utility import list_available_db
from helpers.utility import get_rds_DiskQueueDepth,get_rds_diskfree
from helpers.utility import list_elb,getTargetResponseTime,get_target_groups_for_alb,getUnHealthyHostCount


def main():
    start_time = time.time()
    cwd = os.getcwd()
    rds_conf_path = cwd + '/config/rds.yaml'
    dbfile = cwd + '/rds_stat.db'
    create_diskfree_table(dbfile)
    create_memfree_table(dbfile)
    create_cpuusage_table(dbfile)
    create_diskqueuedepth_table(dbfile)
    create_elbresponsetime_table(dbfile)
    create_elbtargetgroup_table(dbfile)
    truncate_tables(dbfile)
    with open(rds_conf_path, 'r') as fh:
        data = yaml.safe_load(fh)
    Namespace = data["Rds_Namespace"]
    tmp_alldb = []

    for region in data['Rds_Regions']:
        tmp_alldb.append(list_available_db(region, Namespace))
    alldb = []

    if len(tmp_alldb) > 0:
        for objlist in tmp_alldb:
            if len(objlist) > 0:
                for db in objlist:
                    alldb.append(db)
    # alldb --
    # [{'DBInstanceIdentifier': 'database-1', 'AllocatedStorage': 20, 'DBInstanceClass': 'db.t3.micro', 'Engine': 'mysql', 'DBInstanceStatus': 'stopped','region_name': 'us-east-1', 'Namespace': 'AWS/RDS'}, {'DBInstanceIdentifier': 'pgsql-2', 'AllocatedStorage': 20, 'DBInstanceClass': 'db.t3.micro', 'Engine': 'postgres', 'region_name': 'us-east-1', 'Namespace': 'AWS/RDS'}]
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
    diskfreequeue=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        diskFut = []
        for d in alldb:
            diskFut.append(executor.submit(get_rds_diskfree, d))
        for res in concurrent.futures.as_completed(diskFut):
            diskfreequeue.append(res.result())

    for d in diskfreequeue:
        insert_diskfree_data(dbfile, d) # free disk space is in MB

    #------------ELB Monitring Start --------#
    with open(rds_conf_path, 'r') as fh:
        data = yaml.safe_load(fh)
    Namespace = data["Elb_Namespace"]
    tmp_allelb = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        elbfut=[]
        for region in data['Elb_Regions']:
            elbfut.append(executor.submit(list_elb,region))
        for item in concurrent.futures.as_completed(elbfut):
            tmp_allelb.append(item.result())
    #
    elbseries=[]
    for regionelblist in tmp_allelb:
        for item in regionelblist:
            elbseries.append(item)
    elbdata=[]
    elbfut=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for elb in elbseries:
            elb['Namespace'] = Namespace
            elbfut.append(executor.submit(getTargetResponseTime,**elb))
        for item in concurrent.futures.as_completed(elbfut):
            elbdata.append(item.result())

    for item in elbdata:
        insert_elbresponsetime_data(dbfile,item)

    tgtdata = []
    fut = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for lb in elbseries:
            fut.append(executor.submit(get_target_groups_for_alb,lb["LoadBalancerArn"], lb["region_name"],lb["LoadBalancerName"],lb['State']))
        for f in concurrent.futures.as_completed(fut):
            tgtdata.append(f.result())

    unhealthycount=[]
    fut = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for item in tgtdata:
            if item['target_groups']:
                for tgt in item['target_groups']:
                    tgtname = 'targetgroup/'+'/'.join(tgt["TargetGroupArn"].split('/')[-2:])
                    load_balancer_name = '/'.join(item["alb_arn"].split('/')[-3:])
                    fut.append(executor.submit(getUnHealthyHostCount,tgtname, load_balancer_name, item["region_name"], item['State'],item["LoadBalancerName"]))
                for f in concurrent.futures.as_completed(fut):
                    unhealthycount.append(f.result())
            else:
                continue

    for x in unhealthycount:
        insert_elbtargetgroup_data(dbfile,x)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Elapsed: {execution_time}s")



if __name__ == '__main__':
    main()
