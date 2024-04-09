import time
import pymysql

choice = int(input("Enter number 1 for user search and 2 for Hashtag search"))


if choice == 1:
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Search query for finding users >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Plum@08901',
                             database='twitterUser',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()

    with connection.cursor() as cursor:
        # Replace 'username_column', 'user_id_column', 'full_name_column' with actual column names
        # Replace 'your_search_criteria' with the actual search term
        search_criteria = input("Enter search criteria (username, user ID, or full name): ")
        
        start_time_user = time.time()
        sql_query = """
        SELECT * FROM users
        WHERE screen_name = %s OR id = %s OR name = %s
        """
        cursor.execute(sql_query, (search_criteria, search_criteria, search_criteria))
        
        # Fetch all matching user records
        result = cursor.fetchall()
        
        for user in result:
            print(user)  # Each 'user' is a dictionary of user data
        end_time_user = time.time()

        print("--------------------------->>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<------------------------------")
        print(f"{end_time_user-start_time_user}")

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Search query for finding users end >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  


#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Search query for finding hastags start >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
elif choice == 2:
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client['twitterDataMDB']
    collection = db['tweets']
    hashtag = input("Enter your desired hashtag --> ")
    start_time_hashtag = time.time()
    tweets_with_specific_hashtag = collection.find({
        'hashtags_for_tweets': {
        '$elemMatch': {
            'text': hashtag
        }
        }
    }, {'text': 1, 'hashtags_for_tweets': 1})  # Including only the 'text' and 'hashtags_for_tweets' fields in the results

# Iterate over the results and print the tweet text and hashtags
    for tweet in tweets_with_specific_hashtag:
        print("Tweet Text:", tweet.get('text'))
        hashtags = tweet.get('hashtags_for_tweets', [])
        print("Hashtags:")
        for hashtag in hashtags:
            print(hashtag.get('text'))
    print("---")
    end_time_hashtag = time.time()
    print("--------------------------->>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<------------------------------")
    print(f"{end_time_hashtag-start_time_hashtag}")

else:
    print("Galt Chocie sorry !!!!")


