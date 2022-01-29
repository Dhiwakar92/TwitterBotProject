
# AUTHORIZATION & AUTHENTICATION RELATED CONSTANTS
with open('secrets.txt', 'r') as f:
        lines = f.readlines()
        lines = iter(lines)

consumer_key = next(lines).strip()
consumer_secret = next(lines).strip()
access_token = next(lines).strip()
access_token_secret = next(lines).strip()
bearer_token = next(lines).strip()
aws_access_key_id = next(lines).strip()
aws_secret_access_key = next(lines).strip()

# URLS
base_url = 'https://api.twitter.com'
urls = {
        'authenticated_user_lookup': base_url+'/2/users/me',
        'post_a_tweet': base_url+'/2/tweets',
        'stream_tweets': base_url+'/2/tweets/search/stream',
        'post_rule': base_url+'/2/tweets/search/stream/rules',
        'retrieve_rules': base_url+'/2/tweets/search/stream/rules',
        'user_mention_timeline': base_url+'/2/users/{user_id}/mentions'
}

# S3 BUCKET CONSTANTS
bucket_name = 'mostrecenttweetid'
bucket_object_name = 'most_recent_tweet_id.txt'
temp_file_name = '/tmp/most_recent_tweet_id.txt'  # THIS WOULD BE THE ONLY WRITEABLE PATH ON AWS

reply_hastags = ["#DhiSimpleBot", "#mention"]

