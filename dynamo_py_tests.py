import dynamo_api
from unittest.mock import patch, MagicMock
import boto3
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("visitor_counter")

# 1. If the get is options, return options
sample_output_1 = dynamo_api.lambda_handler({"httpMethod": "OPTIONS"}, None)
assert sample_output_1 == {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type', 'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'}, 'body': ''}
print(sample_output_1)


#2. to test the ability to just get the current value
sample_output_2 = dynamo_api.lambda_handler({"httpMethod": "GET"}, None)
# what to put for assert since the number can change?
# assert sample_output_2 == {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': '22'}
assert sample_output_2["statusCode"] == 200
assert sample_output_2["headers"] == {"Access-Control-Allow-Origin": "*"}
assert "body" in sample_output_2
assert sample_output_2["body"].isdigit()
print(sample_output_2)


#3. If the user is new (visited=false/no visited) test the ability to increment by one
fake_get_response = {"Item": {"visitor_number": 0}}
fake_update_response = {"Attributes": {"visitor_number": 1}}
with patch.object(dynamo_api.table, "get_item", return_value=fake_get_response), patch.object(dynamo_api.table, "update_item", return_value=fake_update_response):
    sample_output_3 = dynamo_api.lambda_handler({"httpMethod": "POST","body": json.dumps({"visited": False})}, None)
    assert sample_output_3 == {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': '1'}
    print(sample_output_3)


#4. if the user is not new (visited=true) test the ability to not increment
sample_output_4 = dynamo_api.lambda_handler({"httpMethod": "POST","body": "{\"visited\": true}"}, None)
# what to put for assert since the number can change?
assert sample_output_4["statusCode"] == 200
assert sample_output_4["headers"] == {"Access-Control-Allow-Origin": "*"}
assert "body" in sample_output_4
assert sample_output_4["body"].isdigit()
print(sample_output_4)


#5. if the input is an error, fix this
# sample_output_5 = dynamo_api.lambda_handler({"httpMethod": "POST","body": "{\"visited\": true}"}, None)
sample_output_5 = dynamo_api.lambda_handler({"httpMethod": "POST", "body": "{bad json"}, None)
error_body = json.loads(sample_output_5["body"])
assert sample_output_5["statusCode"] == 500
assert "error" in error_body
print(sample_output_5)
# add in 5th sample output for error