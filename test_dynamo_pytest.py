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
@patch.object(dynamo_api.table, "put_item")
def test_get_method(mock_put, mock_get):
    event = {"httpMethod": "GET"}
    response = dynamo_api.lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert response["headers"] == {"Access-Control-Allow-Origin": "*"}
    assert json.loads(response["body"]) == 10
    mock_put.assert_not_called()  

@patch.object(dynamo_api.table, "get_item", return_value={"Item": {"visitor_number": 0}})
@patch.object(dynamo_api.table, "update_item", return_value={"Attributes": {"visitor_number": 1}})
@patch.object(dynamo_api.table, "put_item")
def test_post_new_visitor(mock_put, mock_update, mock_get):
    event = {"httpMethod": "POST", "body": json.dumps({"visited": False})}
    response = dynamo_api.lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert response["headers"] == {"Access-Control-Allow-Origin": "*"}
    assert json.loads(response["body"]) == 1
    mock_put.assert_not_called()  

@patch.object(dynamo_api.table, "get_item", return_value={"Item": {"visitor_number": 5}})
@patch.object(dynamo_api.table, "put_item")
def test_post_existing_visitor(mock_put, mock_get):
    event = {"httpMethod": "POST", "body": json.dumps({"visited": True})}
    response = dynamo_api.lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert response["headers"] == {"Access-Control-Allow-Origin": "*"}
    assert json.loads(response["body"]) == 5
    mock_put.assert_not_called()

@patch.object(dynamo_api.table, "put_item")
@patch.object(dynamo_api.table, "get_item", side_effect=[{}, {"Item": {"visitor_number": 0}}])
def test_initializes_counter(mock_get, mock_put):
    event = {"httpMethod": "GET"}
    response = dynamo_api.lambda_handler(event, None)
    mock_put.assert_called_once_with(Item={"id": "counter", "visitor_number": 0})
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == 0

@patch.object(dynamo_api.table, "get_item", return_value={"Item": {"visitor_number": 99}})
@patch.object(dynamo_api.table, "put_item")
def test_post_bad_json(mock_put, mock_get):
    event = {"httpMethod": "POST", "body": "{bad json"}
    response = dynamo_api.lambda_handler(event, None)
    assert response["statusCode"] == 500
    error_body = json.loads(response["body"])
    assert "error" in error_body
