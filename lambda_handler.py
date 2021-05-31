def lambda_handler(event, context):
    #get location from the GET call
    
     location = int(event['queryStringParameters']['location'])
     return { 'status' : 200, 'body' : 'Lambda executed successfully! Got the location : ' + location }