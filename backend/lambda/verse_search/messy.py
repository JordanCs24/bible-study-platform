import re      # detect query types using pattern matching

def normalize_query(query):
    print("Before: " + query)
    query = query.strip()
    print(query)
    query = re.sub(r'(\d+)\s*:\s*(\d+)', r'\1:\2', query)
    query = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', query)
    print(query)
    query = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', query)
    print("After: " + query + "\n\n")

normalize_query("John 3 : 16")
normalize_query("john3:16")
normalize_query("1john4:8")
normalize_query("John 3:16Love") 