import json    # read and parse the Bible JSON files from S3
import re      # detect query types using pattern matching
import boto3   # talk to AWS services like S3 and Bedrock

BUCKET_NAME = 'bible-platform-jordan'

KJV_PREFIX = 'bible-data/kjv/'

#Listing of query types
qType1 = None
qType2 = None
qType3 = None #Send it to AWS bedrock 

# Step 1: Receive the event from API Gateway and extract the query string
def lambda_handler(event, context):
    query = event.get('q')
    if( len(query) < 4):
        print("please enter a more specific search")
    elif(query)
    else:
        Type3 = True
        
        
# Step 2 Validation: if the query is empty or less than 3 characters:
#   return a message saying "please enter a more specific search"

# Step 3: Detect the query type and route accordingly

# if the query matches the verse reference pattern (book name + colon + numbers)
#   look up the specific scripture directly from the S3 data file
# elif the query is a single word with no spaces
#   return the most well known verses containing that word via Bedrock
# else
#   send to Bedrock for a warm thoughtful conversational response

# Step 4: Format the result into a clean response
# Step 5: Return the response back to API Gateway


### _TESTING_ ###
if __name__ == '__main__':
    test_event = {
        'queryStringParameters': {
            'q': 'love'
        }
    }
    result = lambda_handler(test_event, None)
    print(result)