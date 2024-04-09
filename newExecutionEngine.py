import json

def understandingJson(filepath):
    with open(filepath, "r") as f:
        json_data = f.read()

    json_objects = []
    brace_count = 0
    start_index = None

    for i, c in enumerate(json_data):
        if c == "{":
            brace_count += 1
            if brace_count == 1:
                start_index = i
        elif c == "}":
            brace_count -= 1
            if brace_count == 0:
                json_objects.append(json_data[start_index:i + 1])

    data = json.loads("[" + ",".join(json_objects) + "]")
    output_filename = "twitterData.json"
    with open(output_filename, "w") as f:
        json.dump(data, f)
    # return data

results = understandingJson(filepath="corona-out-2")

import pymysql
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Plum@08901',
                             database='twitterUser',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    screen_name VARCHAR(255),
    verified BOOLEAN,
    location VARCHAR(255),
    url VARCHAR(255),
    description TEXT,
    followers_count INT,
    following_count INT,
    friends_count INT,
    listed_count INT,
    favourites_count INT,
    statuses_count INT,
    created_at TIMESTAMP,
    time_zone VARCHAR(255),
    lang VARCHAR(255),
    default_profile BOOLEAN,
    default_profile_image BOOLEAN
)
"""
cursor.execute(create_table_query)

#########Abhi mongodb ka scene 

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['twitterDataMDB']
collection_tweets = db['tweets']
collection_retweets = db['retweets']
collection_quotedStatus = db['quotedStatus']

# collection_retweets.insert_one({"sample_key": "sample_value"})
# collection_quotedStatus.insert_one({"sample_key": "sample_value"})


#Now insertion wala part
key_list = [
    'id' 
    'name' ,
    'screen_name' ,
    'verified',
    'location' ,
    'url',
    'description' ,
    'followers_count' ,
    'following_count' ,
    'friends_count' ,
    'listed_count' ,
    'favourites_count' ,
    'statuses_count' ,
    'created_at' ,
    'time_zone' ,
    'lang' ,
    'default_profile' ,
    'default_profile_image' 
]

# SQL query for inserting data into user_data table

import json
import pymysql
from datetime import datetime
import pandas as pd

with open('twitterData.json', 'r') as file:
    data = json.load(file)

def parse_datetime(datetime_str):
    try:
        return datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

conn = pymysql.connect(host='localhost', user='root', password='Plum@08901', database='twitterUser')
cur = conn.cursor()


column_names = [  # Ensure these match your database schema
    'id', 'name', 'screen_name', 'verified', 'location', 'url', 'description', 'followers_count', 'following_count', 'friends_count',
    'listed_count', 'favourites_count', 'statuses_count', 'created_at', 'time_zone', 'lang', 'default_profile', 
    'default_profile_image'
]

query_insert = """
INSERT INTO users (id, name, screen_name, verified, location, url, description, followers_count, following_count, 
friends_count, listed_count, favourites_count, statuses_count, created_at, time_zone, lang, default_profile, 
default_profile_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""
key_list = [  # Ensure these match your database schema
    'id', 'name', 'screen_name', 'verified', 'location', 'url', 'description', 'followers_count', 'following_count', 'friends_count',
    'listed_count', 'favourites_count', 'statuses_count', 'created_at', 'time_zone', 'lang', 'default_profile', 
    'default_profile_image'
]
#naya method

def process_and_insert_user_data(user_data):
    val_list = [user_data.get(key, None) if key != "created_at" else parse_datetime(user_data.get(key, None)) for key in key_list]
    
    # Check if the user already exists
    cur.execute("SELECT 1 FROM users WHERE id = %s", (user_data.get("id"),))
    if cur.fetchone():
        print(f"User {user_data.get('id')} already exists. Skipping insertion for this user...")
    else:
        try:
            cur.execute(query_insert, val_list)
            conn.commit()
        except Exception as e:
            print(f"Error inserting user data: {e}")

for item in data:
    # Process primary user
    primary_user_data = item.get("user", {})
    process_and_insert_user_data(primary_user_data)
    
    # Process retweeted user, if present
    if "retweeted_status" in item:
        retweeted_user_data = item["retweeted_status"].get("user", {})
        process_and_insert_user_data(retweeted_user_data)

# Close cursor and connection
cur.close()
conn.close()





# <<<<<<<<<<<<<<<<<<<<<<<<Mongo ka tweets collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.




from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['twitterDataMDB']
tweets_collection = db['tweets']



# Path to your JSON file containing the list of tweets
# file_path = 'twitterData.json'

# # Open and read the JSON file
# with open(file_path, 'r') as file:
#     tweet_data = json.load(file)  # This assumes the file is structured as a JSON list

# # Process each tweet to simplify user data
# for tweet in tweet_data:
#     # Extract and include only the user_id, exclude the rest of the user data
#     tweet['user_id'] = tweet['user']['id']
#     del tweet['user']  # Remove the original user object

#     # You can also remove or process other fields as necessary here

# # Insert the processed tweets into the MongoDB collection
# result = tweets_collection.insert_many(tweet_data)

# # Print the IDs of the newly inserted documents
# print(f"Inserted {len(result.inserted_ids)} tweets")

import json
import re #used to find all the source of the tweets published... for further analysis source is an important parameter

file_path = '/Users/manasmaskar/Rutgers/Spring24/DBMS/twitterProject/twitterData.json'

# Open and read the JSON file
with open(file_path, 'r') as file:
    tweet_data = json.load(file)

regex = re.compile(r'>\s*([^<]+)\s*<')

extracted_tweets = []

for tweet in tweet_data:
    # Extract the required information from each tweet
    extracted_tweet = {
        "created_at": tweet.get("created_at"),
        "id": tweet.get("id"),
        "id_str": tweet.get("id_str"),
        "text": tweet.get("text"),
        "source": tweet.get("source"),
        "user_id": tweet['user']['id'] if 'user' in tweet else None,  # Safely extracting user ID from the user object
        "truncated": tweet.get("truncated"),
        "in_reply_to_status_id": tweet.get("in_reply_to_status_id"),
        "in_reply_to_status_id_str": tweet.get("in_reply_to_status_id_str"),
        "in_reply_to_user_id": tweet.get("in_reply_to_user_id"),
        "in_reply_to_user_id_str": tweet.get("in_reply_to_user_id_str"),
        "in_reply_to_screen_name": tweet.get("in_reply_to_screen_name"),
        "retweet_status_id": tweet['retweeted_status']['id'] if 'retweeted_status' in tweet else None,  # Original tweet's ID if this is a retweet
        "retweet_status_id_str": tweet['retweeted_status']['id_str'] if 'retweeted_status' in tweet else None,  # Original tweet's ID string if this is a retweet
        "retweet_count": tweet.get("retweet_count"),  # Number of times this tweet has been retweeted
        "quoted_count": tweet.get("quote_count"),
        "reply_count": tweet.get("reply_count"),
        "favorite_count": tweet.get("favorite_count"),
        "retweeted_status": tweet.get('retweeted'),
        "hashtags_for_tweets": tweet.get('entities', {}).get('hashtags', []),
        "filter_level": tweet.get("filter_level"),
        "timestamp_ms": tweet.get("timestamp_ms"),

    }

    # Add the extracted tweet to the list
    match = regex.search(tweet['source'])
    extracted_tweet['tweet_source'] = match.group(1) if match else None

    # Add the extracted tweet to the list
    extracted_tweets.append(extracted_tweet)

# if extracted_tweets:  # Ensure the list is not empty
#     print(json.dumps(extracted_tweets[0], indent=4))
# else:
#     print("No tweets were extracted.")

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['twitterDataMDB']
collectionfor_tweets = db['tweets']
insertManytweets = collectionfor_tweets.insert_many(extracted_tweets)
print("Insertion all the tweets")


# <<<<<<<<<<<<<<<<<<Inserting the retweets in mongodb from tweets collection >>>>>>>>>>>>>>>>>>>
retweets_collection = db['retweets']
file_path = 'twitterData.json'
with open(file_path, 'r') as file:
    tweet_data = json.load(file)

for tweet in tweet_data:
    # Check if tweet is a retweet based on the 'text' attribute
    if tweet['text'].startswith("RT") and 'retweeted_status' in tweet:
        retweeted_status = tweet['retweeted_status']
        
        # Extract retweet information
        retweet_info = {
            'retweet_id': tweet['id'],
            'retweet_id_str': tweet['id_str'],
            'retweet_user_id': tweet['user']['id'],
            'retweet_user_id_str': tweet['user']['id_str'],
            'retweet_text': tweet['text'],
            'original_tweet_id': retweeted_status.get('id'),
            'original_tweet_id_str': retweeted_status.get('id_str'),
            'original_user_id': retweeted_status['user']['id'] if 'user' in retweeted_status else None,
            'original_user_id_str': retweeted_status['user']['id_str'] if 'user' in retweeted_status else None,
        }

        # Insert retweet information into the 'retweets' collection
        retweets_collection.insert_one(retweet_info)

print("Retweet information has been inserted into the 'retweets' collection.")


#<<<<<<<<<<Quoted Status isnertion queries for mongodb >>>>>>>>>>>>>>>>>>

with open('twitterData.json', 'r') as file:
    tweet_data = json.load(file)
quoted_tweets_data = []
for tweet in tweet_data:
    if 'quoted_status' in tweet:
        quoted_tweet_info = {
            'quoted_status_id': tweet['quoted_status']['id'],
            'quoted_status_id_str': tweet['quoted_status']['id_str'],
            'quoted_status_user_id': tweet['quoted_status']['id'],
            'quoted_status_user_id': tweet['quoted_status']['id_str'],
            'text': tweet['quoted_status']['text'],
            'original_tweet_id': tweet['id'],
            'original_tweet_user_id': tweet['user']['id']
        }
        quoted_tweets_data.append(quoted_tweet_info)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['twitterDataMDB']

# Insert quoted tweets into the quoted_status collection
quoted_status_collection = db['quotedStatus']
quoted_result = quoted_status_collection.insert_many(quoted_tweets_data)

# Print the IDs of the inserted documents
print("Inserted quoted tweet document")







