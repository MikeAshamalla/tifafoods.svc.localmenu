import json
from decimal import Decimal
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
            'body': json.dumps(str(main(location)))
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


def fetch_default_web_menu_items_from_db():
    query_string = \
   'SELECT ' + \
        'item_uuid, ' + \
        'item_name, ' + \
        'item_price, ' + \
        'modifier_group_uuid, ' + \
        'modifier_group_name, ' + \
        'default_is_web_menu_item, ' + \
        'item_category_name ' + \
    'FROM ' + \
        '"view_default_web_menu_items"'
    try:
        # Create a cursor to perform database operations
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query_string)
        return cursor.fetchall()
    except:
        raise
    finally:
        try: cursor.close()
        finally: connection.close()


def fetch_default_web_menu_modifiers_from_db():
    query_string = \
   'SELECT ' + \
        'modifier_group_uuid, ' + \
        'modifier_group_name, ' + \
        'modifier_uuid, ' + \
        'modifier_name, ' + \
        'modifier_price, ' + \
        'default_is_web_menu_modifier ' + \
    'FROM ' + \
        '"view_default_web_menu_modifiers"'
    try:
        # Create a cursor to perform database operations
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query_string)
        return cursor.fetchall()
    except:
        raise
    finally:
        try: cursor.close()
        finally: connection.close()


def fetch_web_menu_item_overrides_from_db(tfi_location_id):
    query_string = \
   'SELECT ' + \
        'item_uuid, ' + \
        'item_name, ' + \
        'item_price, ' + \
        'modifier_group_uuid, ' + \
        'modifier_group_name, ' + \
        'default_is_web_menu_item, ' + \
        'item_local_price, ' + \
        'local_is_web_menu_item, ' + \
        'tfi_location_id ' + \
    'FROM ' + \
        '"view_web_menu_item_overrides"  ' + \
    'WHERE ' + \
        'tfi_location_id = %s '
    try:
        # Create a cursor to perform database operations
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query_string, (tfi_location_id, ))
        return cursor.fetchall()
    except:
        raise
    finally:
        try: cursor.close()
        finally: connection.close()


def fetch_web_menu_modifier_overrides_from_db(tfi_location_id):
    query_string = \
   'SELECT ' + \
        'modifier_group_uuid, ' + \
        'modifier_group_name, ' + \
        'modifier_uuid, ' + \
        'modifier_name, ' + \
        'modifier_price, ' + \
        'tfi_location_id, ' + \
        'modifier_local_price, ' + \
        'default_is_web_menu_modifier, ' + \
        'local_is_web_menu_modifier ' + \
    'FROM ' + \
        '"view_web_menu_modifier_overrides"  ' + \
    'WHERE ' + \
        'tfi_location_id = %s '
    try:
        # Create a cursor to perform database operations
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query_string, (tfi_location_id, ))
        return cursor.fetchall()
    except:
        raise
    finally:
        try: cursor.close()
        finally: connection.close()


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


def get_item_override_priceList(item_override, modifiers):
    modifier_group_uuid = item_override[3]
    if not modifier_group_uuid:   #No modifiers
        # Return the default price unless the item has a local price
        if not item_override[6]:
            return [{'size': '', 'price': str(item_override[2])}]
        else:
            return [{'size': '', 'price': str(item_override[6])}]
    else:
        return modifiers[modifier_group_uuid]


def add_priced_item(priced_items, item, item_category):
    category = None
    for entry in priced_items['pricedItems']:
        if entry['category'] == item_category:
            category = entry
    if category:
        category['items'].append(item)
    else:
        priced_items['pricedItems'].append({'category': item_category, 'subCategory': '', 'items': [item]})


def process_items(tfi_location_id):
    default_items = fetch_default_web_menu_items_from_db()
    item_overrides, modifier_overrides = {}, {}
    modifiers = {}
    priced_items = {'pricedItems': []}

    for item_row in fetch_web_menu_item_overrides_from_db(tfi_location_id):
        item_overrides[item_row[0]] = item_row
    for mod_row in fetch_web_menu_modifier_overrides_from_db(tfi_location_id):
        modifier_overrides[mod_row[2]] = mod_row
    for mod in fetch_default_web_menu_modifiers_from_db():
        final_mod = None
        modifier_id = mod[2]
        if modifier_id in modifier_overrides:   #There's a modifier override
            mod_override = modifier_overrides[modifier_id]
            if mod_override[8]:   #local_is_web_modifier == True
                final_mod = {'size': mod_override[3], 'price':str(mod_override[6])}
        else:
            if mod[5]:   #default_is_web_menu_modifier == True
                final_mod = {'size': mod[3], 'price':str(mod[4])}
        mod_group_id = mod[0]
        if final_mod:
            if mod_group_id in modifiers:
                modifiers[mod_group_id].append(final_mod)
            else:
                modifiers[mod_group_id] = [final_mod, ] 

    for item in default_items:
        item_id, is_web_menu, item_category = item[0], item[5], item[6]
        #Determine whether or not this item is shown in the web menu
        if item_id not in item_overrides and is_web_menu:
            modifier_group_uuid = item[3]
            #No item override
            if not modifier_group_uuid:   #No modifier
                add_priced_item(priced_items, {'name': item[1], 'priceList': [{'size': '', 'price': str(item[2])}]}, item_category)
            else:
                if modifier_group_uuid in modifiers:
                    add_priced_item(priced_items, {'name': item[1], 'priceList': modifiers[modifier_group_uuid]}, item_category)
        elif item_id in item_overrides and item_overrides[item_id][6]:
            #There is an item override
            add_priced_item(priced_items, {'name': item[1], 'priceList': get_item_override_priceList(item_overrides[item_id], modifiers)}, item_category)
    return priced_items


def main(location):
    # TEST_LOCATION = 'F00000-1'
    # print(get_gelato_sorbetto_flavors(TEST_LOCATION))
    # print('\n', fetch_default_web_menu_modifiers_from_db())
    # print('\n', fetch_web_menu_modifier_overrides_from_db(TEST_LOCATION))
    # print(json.dumps(process_items(TEST_LOCATION), indent=4))

    fetch_default_web_menu_modifiers_from_db()
    fetch_web_menu_modifier_overrides_from_db(location)
    return process_items(location)


if __name__ == "__main__":
    main()
