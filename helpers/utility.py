import boto3
from datetime import datetime,timedelta

def list_available_db(region_name,Namespace):
    dblist = []
    client = boto3.client('rds', region_name=region_name)
    response = client.describe_db_instances()
    for db_instance in response['DBInstances']:
        DBInstanceIdentifier = db_instance["DBInstanceIdentifier"]
        DBInstanceClass = db_instance["DBInstanceClass"]
        Engine = db_instance["Engine"]
        AllocatedStorage = db_instance["AllocatedStorage"]
        DBInstanceStatus = db_instance["DBInstanceStatus"]
        region_name = region_name
        dblist.append({"DBInstanceIdentifier": DBInstanceIdentifier, "AllocatedStorage": AllocatedStorage,
                       "DBInstanceClass": DBInstanceClass,"DBInstanceStatus":DBInstanceStatus,
                       "Engine": Engine, "region_name": region_name, "Namespace": Namespace})

    return (dblist)

def get_rds_freeable_memory(dataref):
    data = dataref.copy()
    client = boto3.client('cloudwatch',region_name=data["region_name"])
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    queryparams = {
        'MetricDataQueries': [
            {
                'Id': 'rds_memfreeable',
                'MetricStat': {
                    'Metric': {
                        'Namespace': data['Namespace'],  # AWS/EC2
                        'MetricName': 'FreeableMemory',
                        'Dimensions': [
                            {
                                'Name': 'DBInstanceIdentifier',
                                'Value': data['DBInstanceIdentifier']
                            }
                        ]
                    },
                    'Period': 120,  # Fetch data in 120-second intervals
                    'Stat': 'Average',  # Compute the average CPU usage
                },
            },
        ],
        'StartTime': start_time,
        'EndTime': end_time,
    }
    response = client.get_metric_data(**queryparams)
    if response["MetricDataResults"][0]["Values"]:
        memfreeable = response["MetricDataResults"][0]["Values"][0]
        memfreeable = memfreeable/(1024*1024)    # Bytes to MegaByte
        data["memfreeable"] = memfreeable
    else:
        data["memfreeable"] = -1

    return (data)

def get_cpu_usage(dataref):
    data=dataref.copy() #the dataref is pass by reference ,using copy() to act as pass by reference
    client = boto3.client('cloudwatch', region_name=data["region_name"])
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    queryparams = {
        'MetricDataQueries': [
            {
                'Id': 'rds_cpu_usage',
                'MetricStat': {
                    'Metric': {
                        'Namespace': data['Namespace'],  # AWS/EC2
                        'MetricName': 'CPUUtilization',
                        'Dimensions': [
                            {
                                'Name': 'DBInstanceIdentifier',
                                'Value': data['DBInstanceIdentifier']
                            }
                        ]
                    },
                    'Period': 120,  # Fetch data in 120-second intervals
                    'Stat': 'Average',  # Compute the average CPU usage
                },
            },
        ],
        'StartTime': start_time,
        'EndTime': end_time,
    }
    response = client.get_metric_data(**queryparams)
    if response["MetricDataResults"][0]["Values"]:
        cpuusage = response["MetricDataResults"][0]["Values"][0]
        data["cpu_usage"] = cpuusage
    else:
        data["cpu_usage"] = 0
    return(data)

#DiskQueueDepth
def get_rds_DiskQueueDepth(dataref):
    data=dataref.copy()
    client = boto3.client('cloudwatch',region_name=data["region_name"])
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    queryparams = {
        'MetricDataQueries': [
            {
                'Id': 'rds_DiskQueueDepth',
                'MetricStat': {
                    'Metric': {
                        'Namespace': data['Namespace'],  # AWS/EC2
                        'MetricName': 'DiskQueueDepth',
                        'Dimensions': [
                            {
                                'Name': 'DBInstanceIdentifier',
                                'Value': data['DBInstanceIdentifier']
                            }
                        ]
                    },
                    'Period': 120,  # Fetch data in 120-second intervals
                    'Stat': 'Average',  # Compute the average CPU usage
                },
            },
        ],
        'StartTime': start_time,
        'EndTime': end_time,
    }
    response = client.get_metric_data(**queryparams)
    if not response["MetricDataResults"][0]["Values"]:
        data["DiskQueueDepth"] = -1  # set disk queue/outstanding reques to -1 if this data is not present: this happens if RDS db is stopped
    elif response["MetricDataResults"][0]["Values"]:
        DiskQueueDepth = response["MetricDataResults"][0]["Values"][0]
        data["DiskQueueDepth"] = DiskQueueDepth
        if DiskQueueDepth > 0 and DiskQueueDepth < 1:
            data["DiskQueueDepth"] = 0
    return data

def get_rds_diskfree(dataref):
    data=dataref.copy()
    client = boto3.client('cloudwatch',region_name=data["region_name"])
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    queryparams = {
        'MetricDataQueries': [
            {
                'Id': 'rds_DiskFree',
                'MetricStat': {
                    'Metric': {
                        'Namespace': data['Namespace'],  # AWS/EC2
                        'MetricName': 'FreeStorageSpace',
                        'Dimensions': [
                            {
                                'Name': 'DBInstanceIdentifier',
                                'Value': data['DBInstanceIdentifier']
                            }
                        ]
                    },
                    'Period': 120,  # Fetch data in 120-second intervals
                    'Stat': 'Average',  # Compute the average CPU usage
                },
            },
        ],
        'StartTime': start_time,
        'EndTime': end_time,
    }
    response = client.get_metric_data(**queryparams)
    if response["MetricDataResults"][0]["Values"]:
        FreeStorageSpace = response["MetricDataResults"][0]["Values"][0]
        data["FreeStorageSpace"] = FreeStorageSpace/(1024*1024*1024) # free disk space is Byte hence convert to GB
        # aws CW uses 1000 instead of 1024
    else:
        data["FreeStorageSpace"] = 0
    return data

def list_elb(region_name):
    elblist=[]
    try:
        client = boto3.client('elbv2',region_name=region_name)
        response = client.describe_load_balancers()
        for resp in response['LoadBalancers']:
            LoadBalancerArn=resp['LoadBalancerArn']
            DNSName=resp['DNSName']
            LoadBalancerName=resp['LoadBalancerName']
            VpcId=resp['VpcId']
            State=resp['State']['Code']
            Type=resp['Type']
            AvailabilityZones=resp['AvailabilityZones']
            elblist.append({"LoadBalancerArn":LoadBalancerArn,"LoadBalancerName":LoadBalancerName,"DNSName":DNSName,"AvailabilityZones":AvailabilityZones,"region_name":region_name,
                            "VpcId":VpcId,"Type":Type,"State":State})
            #State can be active | provisioning | active_impaired | failed
    except Exception as e:
        print(e)
    return elblist

def getTargetResponseTime(**kwargsref):
    kwargs = kwargsref.copy()
    cloudwatch = boto3.client('cloudwatch', region_name=kwargs['region_name'])
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    load_balancer_name = '/'.join(kwargs['LoadBalancerArn'].split('/')[-3:])
    dimensions = [
        {
            'Name': 'LoadBalancer',
            'Value': load_balancer_name
        }
    ]
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/ApplicationELB',
        MetricName='TargetResponseTime',
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=120,
        Statistics=['Average']
    )

    if 'Datapoints' in response:
        datapoints = response['Datapoints']
        if len(datapoints) > 0:
            avg_response_time = datapoints[-1]['Average']
            kwargs['avg_response_time'] = avg_response_time
        else:
            kwargs['avg_response_time'] = -1  # if there is no request made to ELB or the targets are unavailable then its value -1
    return kwargs


def get_target_groups_for_alb(alb_arn,region_name,LoadBalancerName,lbState):
    elbv2_client = boto3.client('elbv2',region_name=region_name)
    response = elbv2_client.describe_target_groups(
        LoadBalancerArn=alb_arn
    )
    target_groups = response['TargetGroups']
    data = { "target_groups":target_groups, "region_name":region_name, "LoadBalancerName":LoadBalancerName,"alb_arn":alb_arn,"State":lbState }
    return data

def getUnHealthyHostCount(tgtarn,albname,region_name,state,LoadBalancerName):
    cloudwatch = boto3.client('cloudwatch',region_name=region_name)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=10)
    dimensions = [
        {
            "Name": "TargetGroup",
            "Value": tgtarn
        },
        {
            "Name": "LoadBalancer",
            "Value": albname
        }
    ]
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/ApplicationELB',
        MetricName='UnHealthyHostCount',
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=120,
        Statistics=['Average']
    )

    if response['Datapoints']:
        dp = response['Datapoints'][-1]['Average']
    else:
        dp = -1
    return { "unhealthycount":dp,"State":state,"alb_arn":albname,"region_name":region_name,"tgtarn":tgtarn,"LoadBalancerName":LoadBalancerName }