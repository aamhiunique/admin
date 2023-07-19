import json
import os
import boto3
import uuid

TAG="Register Aamhi unique Admin"
dynamodb = boto3.client('dynamodb')
table = os.environ.get("AAMHI_UNIQUE_ADMIN_REGISTER_TABLE")
def execute(event, context):
    try:
        if "body" in event.keys():
            data = event["body"]
            admin = json.loads(data)
            adminId = get_random_id()
            adminFname = admin["adminFname"]
            adminLname = admin["adminLname"]
            adminEmail = admin["adminEmail"]
            adminContact = admin["adminContact"]
            adminPassword = admin["adminPassword"]

            adminExistsByEmail = get_admin_by_email(adminEmail)
            adminExistsByContact = get_admin_by_contact(adminContact)
            

            if adminExistsByEmail:
                return{
                    "statusCode":"409",
                    "body": f'Admin with email {adminEmail} already exists'
                }
            elif adminExistsByContact:
                return {
                    "statusCode": "409",
                    "body": f'Admin with contact {adminContact} already exists'
                }
            
            
            else:
                res = put_data_to_dynamo(adminId, adminFname, adminLname, adminEmail, adminContact, adminPassword)
                return {
                        "statusCode": "201",
                        "body": "Admin Register Successfully"
                        }
    except Exception as ex:
        
        return {
            "statusCode":"503",
            "body":"Error"
        }
    
def get_random_id():
    id=str(uuid.uuid4())
    return id


def put_data_to_dynamo(adminId, adminFname, adminLname, adminEmail, adminContact, adminPassword):
    adminUsername = adminFname[0:3] + adminLname[0:3]
    table = os.environ.get("AAMHI_UNIQUE_ADMIN_REGISTER_TABLE")
    dynamo = boto3.resource("dynamodb")
    dynamoTable = dynamo.Table(table)
    dynamoTable.put_item(
        Item={
            "adminId":adminId,
            "adminFname":adminFname,
            "adminLname":adminLname,
            "adminUsername": adminUsername,
            "adminEmail": adminEmail,
            "adminPassword":adminPassword,
            "active": 0,
            "adminContact": adminContact
        }
    )
    return "Success"

def get_admin_by_email(email): 
    try:
        response = dynamodb.scan(
            TableName=table,
            FilterExpression='email= :email',
            ExpressionAttributeValues={
                ':email':{'S':email}
            }
        )
        print(response)
        return len(response['Items']) > 0
    except Exception as e:
        print(f'Error searching DynamoDB table: {e}')
        return False



def get_admin_by_contact(contact):
    try:
        response = dynamodb.scan(
            TableName=table,
            FilterExpression='contact= :contact',
            ExpressionAttributeValues={
                ':contact':{'S':contact}
            }
        )
        print(response)
        return len(response['Items']) > 0
    except Exception as e:
        print(f'Error searching DynamoDB table: {e}')
        return False
    
