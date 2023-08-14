#import os
import json

def handler(event, context):
  """Vercel serverless function handler."""

  # Get the event data from the request body.
  event_data = json.loads(event['body'])

  # Do something with the event data.
  print(event_data)

  # Return a response to the client.
  response = {
    'statusCode': 200,
    'body': json.dumps({'message': 'Hello, world!'})
  }

  return response
