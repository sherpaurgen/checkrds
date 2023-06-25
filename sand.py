import boto3
from datetime import datetime,timedelta

aa={'LoadBalancerArn': 'arn:aws:elasticloadbalancing:us-east-1:031847382033:loadbalancer/app/myLoadbalancer1/c0389851c55b8fa4', 'LoadBalancerName': 'myLoadbalancer1', 'DNSName': 'myLoadbalancer1-1015332893.us-east-1.elb.amazonaws.com', 'AvailabilityZones': [{'ZoneName': 'us-east-1c', 'SubnetId': 'subnet-058e275a933ad6ade', 'LoadBalancerAddresses': []}, {'ZoneName': 'us-east-1b', 'SubnetId': 'subnet-0872dfc8bb388574e', 'LoadBalancerAddresses': []}], 'region_name': 'us-east-1', 'VpcId': 'vpc-017ea2e23ec62b435', 'Type': 'application', 'State': 'active', 'Namespace': 'AWS/ApplicationELB'}

def getUnHealthyHostCount(data):
    cloudwatch = boto3.client('cloudwatch',region_name='us-east-1')
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=10)
    dimensions =  [
        {
            "Name": "TargetGroup",
            "Value": "targetgroup/tgtgrp1/6a64ef61972848aa"
        },
        {
            "Name": "LoadBalancer",
            "Value": "app/myLoadbalancer1/c0389851c55b8fa4"
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
    print(f"{response}\n\n")

def list_elb():
    region_name = 'us-east-1'
    elblist=[]
    try:
        client = boto3.client('elbv2',region_name='us-east-1')
        response = client.describe_load_balancers()
        print(response)
        print("------------------\n\n")
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

def get_target_groups_for_alb(alb_arn):
    elbv2_client = boto3.client('elbv2',region_name='us-east-1')
    response = elbv2_client.describe_target_groups(
        LoadBalancerArn=alb_arn
    )
    target_groups = response['TargetGroups']
    return target_groups

alb_arn = 'arn:aws:elasticloadbalancing:us-east-1:031847382033:loadbalancer/app/myLoadbalancer1/c0389851c55b8fa4'

get_target_groups_for_alb(alb_arn)
print("\n\n")


