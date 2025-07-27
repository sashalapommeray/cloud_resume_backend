import boto3
import json

table_name = "visitor_counter"                                       
dynamodb_resource = boto3.resource("dynamodb")
users_table = dynamodb_resource.Table(table_name)

def lambda_handler(event, context):

    response = users_table.update_item(
        Key={"id": "counter"},
        UpdateExpression="set visitor_number = visitor_number + :n",
        ExpressionAttributeValues={":n": 1},
        ReturnValues="UPDATED_NEW",
    )

    # Convert Decimal to int for JSON serialization
    visitor_count = response["Attributes"]["visitor_number"]

    return visitor_count
