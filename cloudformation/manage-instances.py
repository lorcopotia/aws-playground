import boto3

ec2 = boto3.client('ec2')

def manage_instances(action):
    filters = [
        {
            'Name': 'tag:workstation',
            'Values': ['*']
        }
    ]
    instances = ec2.describe_instances(Filters=filters)
    instance_ids = [
        instance['InstanceId']
        for reservation in instances['Reservations']
        for instance in reservation['Instances']
    ]

    if instance_ids:
        if action == 'start':
            ec2.start_instances(InstanceIds=instance_ids)
            print(f'Iniciando instancias: {instance_ids}')
        elif action == 'stop':
            ec2.stop_instances(InstanceIds=instance_ids)
            print(f'Deteniendo instancias: {instance_ids}')
    else:
        print("No se encontraron instancias con la etiqueta 'workstation'.")

def lambda_handler(event, context):
    action = event['action']
    manage_instances(action)
