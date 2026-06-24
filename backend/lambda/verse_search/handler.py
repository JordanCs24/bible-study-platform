import json    # read and parse the Bible JSON files from S3
import re      # detect query types using pattern matching
import boto3   # talk to AWS services like S3 and Bedrock

verse_pattern = re.compile(r'^[\d\s]*[a-zA-Z]+[\s\w]*\d+(:\d+(-\d+)?)?$') #Type 1 check

s3 = boto3.client('s3')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')

BUCKET_NAME = 'bible-platform-jordan'

SYSTEM_PROMPT = """You are a compassionate and knowledgeable Bible study companion. 
You respond with warmth and genuine care. You never lecture, moralize, or make anyone feel judged. 
You offer scripture as a gift, not a correction. When someone asks a deep or difficult question, 
you engage with it honestly and thoughtfully. Always directly answer the question being asked first, 
then support your answer with the most relevant and specific scripture verses you can find.
Do not give generic or surface level answers. Go deep. Be specific to what the person is actually asking.
You are not a preacher. You are a friend who knows the Bible well.
When given a single keyword, return the 3 most well known verses related to that word. 
Format them cleanly with the reference first, then the verse text.
Do not use em dashes or dashes of any kind in your responses. Use periods or commas instead."""

SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:646177707976:Bible-Study-Platform'

KJV_PREFIX = 'bible-data/kjv/'
# Function to handle all edge cases 
# Ex: 1Chronicals3:12
def normalize_query(query):
    query = query.strip()
    query = re.sub(r'(\d+)\s*:\s*(\d+)', r'\1:\2', query)
    query = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', query)
    query = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', query)
    return query.title()


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
    elif ':' in parts[1]:
        #John 3:16 → single verse
        chapter_verse = parts[1].split(':')
        chapter = chapter_verse[0]
        verse_start = chapter_verse[1]
        return {
            'book': book,
            'chapter': chapter,
            'verse_start': verse_start,
            'type': 'single_verse'
        }
    else:
        #John 3 → first 5 verses of chapter
        chapter = parts[1]
        return {
            'book': book,
            'chapter': chapter,
            'type': 'chapter'
        }
                            
def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, OPTIONS'
        },
        'body': json.dumps(body)
    }


def get_verse_from_s3(parsed_reference):
    book = parsed_reference['book']
    try:
        file_path = KJV_PREFIX + book + ".json"
        response = s3.get_object(Bucket=BUCKET_NAME, Key=file_path)
        file_content = response['Body'].read().decode('utf-8')
        data = json.loads(file_content)
    except Exception as e:
        return build_response(404, {'error': "That book could not be found try again. You may have misspelled it."})
    
    for chapter_obj in data['chapters']:
        if (chapter_obj['chapter'] == parsed_reference['chapter']):
            if (parsed_reference['type'] == 'single_verse'):
                for verse_obj in chapter_obj['verses']:
                    if(verse_obj['verse'] == parsed_reference['verse_start']):
                        return build_response(200, {
                            'reference': book + ' ' + parsed_reference['chapter'] + ':' + verse_obj['verse'],
                            'text': verse_obj['text']})
            #Write the code for the other types        
            if (parsed_reference['type'] == 'range'):
                matched_verses = []
                verse_start = int(parsed_reference['verse_start'])
                verse_end = int (parsed_reference['verse_end'])
                for verse_obj in chapter_obj['verses']:
                    if verse_start <= int(verse_obj['verse']) <= verse_end:
                        matched_verses.append(verse_obj)
                return build_response(200, {
                    'reference': book + ' ' + parsed_reference['chapter'] + ':' + parsed_reference['verse_start'] + '-' + parsed_reference['verse_end'],
                    'verses': matched_verses
                })
            if (parsed_reference['type'] == 'chapter'):
                first_five = chapter_obj['verses'][0:5]
                return build_response(200, {
                    'reference': book + ' ' + parsed_reference['chapter'] + ':1-5',# what goes here for "John 3"? 
                    'verses': first_five,
                    'message': 'Showing the first 5 verses. Full chapter reading coming soon.'
                })
    return build_response(404, {
                'error': "That verse does not exist, try again are you looking for a different text if so say what you are trying to find."
    })
    
def call_bedrock(user_message, max_tokens):
    try: 
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "system": SYSTEM_PROMPT,
            "messages": [
                    {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
    
        response = bedrock.invoke_model(
            modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0",
            body=json.dumps(body)
        )
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
    except Exception as e:
        print(f"Bedrock Error: {str(e)}")
        send_alert(str(e))
        try:
            fallback_body = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": user_message
                            }
                        ]
                    }
                ]
            }
            fallback_response = bedrock.invoke_model(
                modelId="us.amazon.nova-lite-v1:0",
                body=json.dumps(fallback_body)
            )
            fallback_result = json.loads(fallback_response['body'].read())
            return fallback_result['output']['message']['content'][0]['text']

        except Exception as fallback_error:
            print(f"Fallback model error: {str(fallback_error)}")
            return None

def send_alert(error_message):
    try: 
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='Bible Platform Alert - AI Service Down',
            Message=f'Bedrock is unavailable. Your users cannot get AI responses.\n\nError details: {error_message}'
        )
    except Exception as e:
        print(f"SNS alert failed: {str(e)}")
                        
# Step 1: Receive the event from API Gateway and extract the query string
def lambda_handler(event, context):
    query = event["queryStringParameters"].get('q')
    # Step 2 Validation: if the query is empty or less than 3 characters:
    #   return a message saying "please enter a more specific search"
    if(query is None):
            return build_response(400, {'error': 'Your search field is empty'})
        
    query = normalize_query(query) #Handles the edgecases
    if(len(query) < 3):
        return build_response(400, {'error': 'Please enter a more specific search'})
    # Step 3: Detect the query type and route accordingl
    # if the query matches the verse reference pattern (book name + colon + numbers)
    elif (re.match(verse_pattern, query)):
        print("Type 1: Direct verse reference")
        parsed_reference = parse_verse_reference(query)
        return get_verse_from_s3(parsed_reference)
    #   look up the specific scripture directly from the S3 data file
    # elif the query is a single word with no spaces
    #   return the most well known verses containing that word via Bedrock
    elif ' ' not in query:
        print("Type 2: Single keyword")
        ai_response = call_bedrock(f"Find the 3 most well known Bible verses for: {query}", 300)
        if ai_response is None:
            return build_response(503, {'error': 'Our AI is currently unavailable. Please try again shortly.'})
        return build_response(200, {'verse': ai_response})
     #   send to Bedrock for a warm thoughtful conversational response
    else:
        print("Type 3: Conversational question")
        ai_response = call_bedrock(query, 600)
        if ai_response is None:
            return build_response(503, {'error': 'Our AI is currently unavailable. Please try again shortly.'})
        return build_response(200, {'verse': ai_response})
# Step 4: Format the result into a clean response
# Step 5: Return the response back to API Gateway