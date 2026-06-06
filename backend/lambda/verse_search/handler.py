import json    # read and parse the Bible JSON files from S3
import re      # detect query types using pattern matching
import boto3   # talk to AWS services like S3 and Bedrock

verse_pattern = re.compile(r'^[\d\s]*[a-zA-Z]+[\s\w]*\d+:\d+$') #Type 1 check

BUCKET_NAME = 'bible-platform-jordan'

KJV_PREFIX = 'bible-data/kjv/'
# Function to handle all edge cases 
# Ex: 1Chronicals3:12
def normalize_query(query):
    query = query.strip()
    query = re.sub(r'(\d+)\s*:\s*(\d+)', r'\1:\2', query)
    query = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', query)
    query = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', query)
    return query.title()
#TO DO: Write the logic for the this function
def parse_verse_reference(query):
    # your comment outline here
    #Parse it to check to see if the
    #John 3:16          → single verse
    #John 3:16-20       → verse range
    #John 3             → first 5 verses of chapter
    #1 John 3:16        → books with number prefix
    #john3:16           → no space, handled by normalization
    #JOHN 3:16          → caps, handled by normalization

# Step 1: Receive the event from API Gateway and extract the query string
def lambda_handler(event, context):
    query = event["queryStringParameters"].get('q')
    # Step 2 Validation: if the query is empty or less than 3 characters:
    #   return a message saying "please enter a more specific search"
    if(query is None):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Your search field is empty'})
        }
        
    query = normalize_query(query) #Handles the edgecases
    if(len(query) < 3):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Please enter a more specific search'})
        }
    # Step 3: Detect the query type and route accordingl
    # if the query matches the verse reference pattern (book name + colon + numbers)
    elif (re.match(verse_pattern, query)):
        print("Type 1: Direct verse reference")
        return {
        'statusCode': 200,
        'body': json.dumps({'type': 'verse', 'query': query})
        }
    #   look up the specific scripture directly from the S3 data file
    # elif the query is a single word with no spaces
    #   return the most well known verses containing that word via Bedrock
    elif ' ' not in query:
        print("Type 2: Single keyword")
        return {
            'statusCode': 200,
            'body': json.dumps({'type': 'keyword', 'query': query})
        }   
     #   send to Bedrock for a warm thoughtful conversational response
    else:
        print("Type 3: Conversational question")
        return {
            'statusCode': 200,
            'body': json.dumps({'type': 'conversational', 'query': query})
        }
# Step 4: Format the result into a clean response
# Step 5: Return the response back to API Gateway


### _TESTING_ ###
if __name__ == '__main__':
    tests = [
        {'queryStringParameters': {'q': 'John 3:16'}},
        {'queryStringParameters': {'q': 'love'}},
        {'queryStringParameters': {'q': 'Are we married in heaven'}}
    ]
    for test in tests:
        result = lambda_handler(test, None)
        print(result)
        print('---')
        
#Testing Normalization function
if __name__ == '__main__':
    test_queries = [
        "john3:16",
        "JOHN 3 : 16",
        "1chronicles 3:5",
        "1Chronicals3:12",
        "love",
        "Are we married in heaven"
    ]
    for q in test_queries:
        print(f"Input: {q} → Output: {normalize_query(q)}")