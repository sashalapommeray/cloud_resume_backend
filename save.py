# import boto3
# from pprint import pprint


# table_name = "visitor_counter"                                       
# dynamodb_resource = boto3.resource("dynamodb")
# users_table = dynamodb_resource.Table(table_name)

# def lambda_handler(event,context):
#     response = users_table.update_item(
#         Key={"id": "counter"},
#         UpdateExpression="set visitor_number = visitor_number + :n",
#         ExpressionAttributeValues={
#             ":n": 1,        },
#         ReturnValues="UPDATED_NEW",
#     )
#     #pprint(response["Attributes"])
#     return response["Attributes"]["visitor_number"]




import boto3
import json

table_name = "visitor_counter"                                       
dynamodb_resource = boto3.resource("dynamodb")
users_table = dynamodb_resource.Table(table_name)

def lambda_handler(event, context):
    # Handle preflight OPTIONS request
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
            },
            "body": ""
        }

    # Update DynamoDB counter
    response = users_table.update_item(
        Key={"id": "counter"},
        UpdateExpression="set visitor_number = visitor_number + :n",
        ExpressionAttributeValues={":n": 1},
        ReturnValues="UPDATED_NEW",
    )

    # Convert Decimal to int for JSON serialization
    visitor_count = int(response["Attributes"]["visitor_number"])

    # Return JSON response with CORS headers
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "visitor_number": visitor_count
        })
    }



    # it reruns every time someone reloads. any way to keep track of individual visitors and not just increment per load? cookies?
    # yes, but probably not here. in javascript, only run the api if there is a new user
    # but if someone finds the link and keeps reloading it they could fuck up the visitor count
    # keep it restricted to iam user? would it still work?