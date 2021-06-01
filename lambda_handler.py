import json
import psycopg2
import boto3
import base64
from botocore.exceptions import ClientError

DATABASE = 'tfiweb'
PORT = '5432'
SECRET_NAME = 'tifafoods.tfimain.db'
REGION_NAME = 'us-west-2'

def lambda_handler(event, context):
    if event['queryStringParameters']:
        location = event['queryStringParameters']['location']
    if location:
        return {
            'statusCode': 200,
            'body': json.dumps(str(get_gelato_sorbetto_flavors(location)))
        }
    else:
        return {
            'statusCode': 404,
            'body': ''
        }


# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:   
# https://aws.amazon.com/developers/getting-started/python/
def get_db_credentials():
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=REGION_NAME
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=SECRET_NAME
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            
    return json.loads(secret if len(secret) > 0 else decoded_binary_secret)
    
def connect_to_db():
    secret = get_db_credentials()
    try:
        connection = psycopg2.connect(user=secret['username'],
                                        password=secret['password'],
                                        host=secret['host'],
                                        port=PORT,
                                        database=DATABASE
                                    )
        return connection
    except:
        raise


def test_db_connection():
    connection, cursor = None, None
    try:
        # Create a cursor to perform database operations
        connection = connect_to_db()
        cursor = connection.cursor()
        # Return PostgreSQL details
        return 'PostgreSQL server information ' + str(connection.get_dsn_parameters())
    except:
        raise
    finally:
        try:
            if cursor:
                cursor.close()
        finally:
            if connection:
                connection.close()


def fetch_local_flavors_from_db(tfi_location_id):
    query_string = \
   'SELECT ' + \
        'flavor_name, ' + \
        'flavor_group_name, ' + \
        'tfi_location_id ' + \
    'FROM ' + \
        '"view_local_flavors"  ' + \
    'WHERE ' + \
        'tfi_location_id = %s AND flavor_group_name = %s ' + \
    'ORDER BY flavor_name'

    try:
        # Create a cursor to perform database operations
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query_string, (tfi_location_id, 'Gelato & Sorbetto', ))
        return cursor.fetchall()
    except:
        raise
    finally:
        try: cursor.close()
        finally: connection.close()


def get_gelato_sorbetto_flavors(tfi_location_id):
    flavors = fetch_local_flavors_from_db(tfi_location_id)
    output = {'category': 'Gelato & Sorbetto', 'subCategory': 'Current Flavors', 'itemList': []}
    for item in flavors:
        output['itemList'].append(item[0])
    return output


def main():
    TEST_LOCATION = 'F00000-1'
    print(get_gelato_sorbetto_flavors(TEST_LOCATION))

if __name__ == "__main__":
    main()