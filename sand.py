import boto3
from datetime import datetime,timedelta

def getTargetResponseTime():
    cloudwatch = boto3.client('cloudwatch',region_name='us-east-1')
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    dimensions = [
        {
            "Name": "LoadBalancer",
            #"Value":"app/myLoadbalancer1/c0389851c55b8fa4"
            "Value": "app/lb2ush/0d3d3448fc2f51cc"
        },
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
    print(f"{response}\n\n")

getTargetResponseTime()