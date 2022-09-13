import boto3

from botocore.waiter import WaiterModel, create_waiter_with_client

from . import waiter_ecs_service_primary_deployment_completed


def get_waiter_ecs_service_primary_deployment_completed():
    return create_waiter_with_client(
        waiter_ecs_service_primary_deployment_completed.ID, 
        WaiterModel(waiter_ecs_service_primary_deployment_completed.CONFIG), 
        boto3.client('ecs')
    )
