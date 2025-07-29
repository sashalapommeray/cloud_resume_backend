# import boto3


# table_name = "visitor_counter"                                       
# dynamodb_resource = boto3.resource("dynamodb")
# users_table = dynamodb_resource.Table(table_name)

# def lambda_handler(event,context):
#     response = users_table.update_item(
#         Key={"id": "counter"},
#         UpdateExpression="set visitor_number = visitor_number + :n",
#         ExpressionAttributeValues={":n": 1},
#         ReturnValues="UPDATED_NEW",
#     )
#     return response["Attributes"]["visitor_number"]





# import boto3
# import json

# table_name = "visitor_counter"                                       
# dynamodb_resource = boto3.resource("dynamodb")
# users_table = dynamodb_resource.Table(table_name)
# def lambda_handler(event, context):
#     if event.get("httpMethod") == "OPTIONS":
#         return {
#             "statusCode": 200,
#             "headers": {
#                 "Access-Control-Allow-Origin": "*",
#                 "Access-Control-Allow-Headers": "Content-Type",
#                 "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
#             },
#             "body": ""
#         }
#     response = users_table.update_item(
#         Key={"id": "counter"},
#         UpdateExpression="set visitor_number = visitor_number + :n",
#         ExpressionAttributeValues={":n": 1},
#         ReturnValues="UPDATED_NEW",
#     )
#     visitor_count = int(response["Attributes"]["visitor_number"])
#     return {
#         "statusCode": 200,
#         "headers": {
#             "Access-Control-Allow-Origin": "*",
#         },
#         "body": visitor_count
#     }










# import boto3
# import json

# # DynamoDB setup
# dynamodb = boto3.resource("dynamodb")
# counter_table = dynamodb.Table("visitor_counter")
# log_table = dynamodb.Table("visitor_log")

# def lambda_handler(event, context):
#     try:
#         body = json.loads(event.get("body", "{}"))
#         visitor_id = body.get("visitorId")

#         if not visitor_id:
#             return {
#                 "statusCode": 400,
#                 "body": json.dumps("Missing visitorId")
#             }

#         # Check if visitor is already logged
#         existing = log_table.get_item(Key={"visitor_id": visitor_id})
#         if "Item" in existing:
#             # Already visited, return current count without increment
#             current = counter_table.get_item(Key={"id": "counter"})
#             return {
#                 "statusCode": 200,
#                 "body": json.dumps(current["Item"]["visitor_number"])
#             }

#         # New visitor: increment counter
#         response = counter_table.update_item(
#             Key={"id": "counter"},
#             UpdateExpression="SET visitor_number = visitor_number + :inc",
#             ExpressionAttributeValues={":inc": 1},
#             ReturnValues="UPDATED_NEW"
#         )

#         # Log visitor
#         log_table.put_item(Item={"visitor_id": visitor_id})

#         return {
#             "statusCode": 200,
#             "body": json.dumps(response["Attributes"]["visitor_number"])
#         }

#     except Exception as e:
#         return {
#             "statusCode": 500,
#             "body": json.dumps(f"Error: {str(e)}")
#         }




import boto3
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("visitor_counter")

def lambda_handler(event, context):
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
    if event.get("httpMethod") == "GET":
        # Return current visitor count without incrementing
        current = table.get_item(Key={"id": "counter"})
        visitor_count = int(current["Item"]["visitor_number"])
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(visitor_count)
        }
    try:
        body = json.loads(event.get("body", "{}"))
        visited = body.get("visited", False)

        if not visited:
            response = table.update_item(
                Key={"id": "counter"},
                UpdateExpression="SET visitor_number = visitor_number + :n",
                ExpressionAttributeValues={":n": 1},
                ReturnValues="UPDATED_NEW"
            )
            visitor_count = int(response["Attributes"]["visitor_number"])
        else:
            # Just return current count without incrementing
            current = table.get_item(Key={"id": "counter"})
            visitor_count = int(current["Item"]["visitor_number"])

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(visitor_count)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }






# import boto3


# table_name = "visitor_counter"                                       
# dynamodb_resource = boto3.resource("dynamodb")
# users_table = dynamodb_resource.Table(table_name)

# def lambda_handler(event,context):
#     response = users_table.update_item(
#         Key={"id": "counter"},
#         UpdateExpression="set visitor_number = visitor_number + :n",
#         ExpressionAttributeValues={":n": 1},
#         ReturnValues="UPDATED_NEW",
#     )
#     return response["Attributes"]["visitor_number"]


#     # it reruns every time someone reloads. any way to keep track of individual visitors and not just increment per load? cookies?
#     # yes, but probably not here. in javascript, only run the api if there is a new user
#     # but if someone finds the link and keeps reloading it they could fuck up the visitor count
#     # keep it restricted to iam user? would it still work?
#     # 