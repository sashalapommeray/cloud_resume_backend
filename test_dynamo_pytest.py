import pytest
from unittest.mock import patch
import json
import dynamo_api

def test_options_method():
    event = {"httpMethod": "OPTIONS"}
    expected = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': ''
    }
    response = dynamo_api.lambda_handler(event, None)
    assert response == expected

@patch.object(dynamo_api.table, "get_item", return_value={"Item": {"visitor_number": 10}})
def test_get_method(mock_get):
    event = {"httpMethod": "GET"}
    response = dynamo_api.lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert response["headers"] == {"Access-Control-Allow-Origin": "*"}
    assert json.loads(response["body"]) == 10

@patch.object(dynamo_api.table, "get_item", return_value={"Item": {"visitor_number": 0}})
@patch.object(dynamo_api.table, "update_item", return_value={"Attributes": {"visitor_number": 1}})
def test_post_new_visitor(mock_update, mock_get):
    event = {"httpMethod": "POST", "body": json.dumps({"visited": False})}
    response = dynamo_api.lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert response["headers"] == {"Access-Control-Allow-Origin": "*"}
    assert json.loads(response["body"]) == 1

@patch.object(dynamo_api.table, "get_item", return_value={"Item": {"visitor_number": 5}})
def test_post_existing_visitor(mock_get):
    event = {"httpMethod": "POST", "body": json.dumps({"visited": True})}
    response = dynamo_api.lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert response["headers"] == {"Access-Control-Allow-Origin": "*"}
    assert json.loads(response["body"]) == 5

def test_post_bad_json():
    event = {"httpMethod": "POST", "body": "{bad json"}
    response = dynamo_api.lambda_handler(event, None)
    assert response["statusCode"] == 500
    error_body = json.loads(response["body"])
    assert "error" in error_body
