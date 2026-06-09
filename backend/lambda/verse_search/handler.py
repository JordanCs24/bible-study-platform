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
#TO DO: Write the logic for  this function
def parse_verse_reference(query):
    #Parse it to check to see if the
    parts = query.rsplit(' ', 1)
    book = parts[0]
    
    #John 3:16-20 → verse range
    if ':' in parts[1] and '-' in parts[1]:
        chapter_verse = parts[1].split(':')
        chapter = chapter_verse[0]
        verse_range = chapter_verse[1].split('-')
        verse_start = verse_range[0]
        verse_end = verse_range[1]
        return {
            'book': book,
            'chapter': chapter,
            'verse_start': verse_start,
            'verse_end': verse_end,
            'type': 'range'
        }
    elif:
        #John 3:16 → single verse

    else:
        #John 3 → first 5 verses of chapter

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
    print("--- Handler Tests ---")
    tests = [
        {'queryStringParameters': {'q': 'John 3:16'}},
        {'queryStringParameters': {'q': 'love'}},
        {'queryStringParameters': {'q': 'Are we married in heaven'}}
    ]
    for test in tests:
        result = lambda_handler(test, None)
        print(result)
        print('---')

    print("--- Normalization Tests ---")
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