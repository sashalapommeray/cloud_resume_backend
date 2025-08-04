import boto3
import json

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("visitor_counter_v1")

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

    #  have to initialize in lambda function because you arent able to using sam
    try:
        current = table.get_item(Key={"id": "counter"})
        if "Item" not in current:
            table.put_item(Item={"id": "counter", "visitor_number": 0})
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": f"Initialization error: {str(e)}"})
        }

    if event.get("httpMethod") == "GET":
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
            current = table.get_item(Key={"id": "counter"})
            visitor_count = int(current["Item"]["visitor_number"])

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(visitor_count)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
