# import boto3
# import json
# from decimal import Decimal

# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('visitor_count')




# class DecimalEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Decimal):
#             return int(obj) if obj % 1 == 0 else float(obj)
#         return super(DecimalEncoder, self).default(obj)



# def lambda_handler(event, context):
#     item_id = event.get('item_id')
    
#     if item_id is None:
#         return {
#             'statusCode': 400,
#             'body': json.dumps({'message': 'Missing item_id'})
#         }

#     try:
#         response = table.get_item(Key={'visitor_number': item_id})
#         item = response.get('Item')

#         if item:
#             # figure out why it prints like this with decimal spelled out Item found: {'visitor_number': Decimal('1')}
#             print(f"old item: {item}")
#             #item.update({'visitor_number': item['visitor_number']+1})
#             print(f"new item: {item}")
#             # for key, value in item.items():
#             #     print(f"Key: {key} (type: {type(key)}), Value: {value} (type: {type(value)})")
#             #item+=1
#             return {
#                 'statusCode': 200,
#                 'body': json.dumps(item, cls=DecimalEncoder)
#             }
#         else:
#             return {
#                 'statusCode': 404,
#                 'body': json.dumps({'message': 'Item not found'})
#             }
#     except Exception as e:
#         return {
#             'statusCode': 500,
#             'body': json.dumps({'error': str(e)})
#         }
#https://binaryguy.tech/aws/dynamodb/update-items-in-dynamodb-using-python/



# import boto3
# from pprint import pprint


# table_name = "visitor_count"                                       
# dynamodb_resource = boto3.resource("dynamodb")
# users_table = dynamodb_resource.Table(table_name)

# def lambda_handler(event,context):
#     response = users_table.update_item(
#         Key={"visitor_number": 1},
#         UpdateExpression="set real_visitor_number = real_visitor_number + :n",
#         ExpressionAttributeValues={
#             ":n": 1,        },
#         ReturnValues="UPDATED_NEW",
#     )
#     pprint(response["Attributes"])
#     return response["Attributes"]



import boto3
from pprint import pprint


table_name = "visitor_counter"                                       
dynamodb_resource = boto3.resource("dynamodb")
users_table = dynamodb_resource.Table(table_name)

def lambda_handler(event,context):
    response = users_table.update_item(
        Key={"id": "counter"},
        UpdateExpression="set visitor_number = visitor_number + :n",
        ExpressionAttributeValues={
            ":n": 1,        },
        ReturnValues="UPDATED_NEW",
    )
    #pprint(response["Attributes"])
    return response["Attributes"]


    # it reruns every time someone reloads. any way to keep track of individual visitors and not just increment per load? cookies?
    # yes, but probably not here. in javascript, only run the api if there is a new user
    # but if someone finds the link and keeps reloading it they could fuck up the visitor count
    # keep it restricted to iam user? would it still work?