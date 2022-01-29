
import boto3

from twitter_bot import TwitterBot
from constants import (
    reply_hastags,
    aws_access_key_id,
    aws_secret_access_key,
    bucket_name,
    bucket_object_name,
    temp_file_name)

def main(event, context):
    # INITIALIZE OUR BOT & S3 BUCKET
    bot = TwitterBot()
    s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    bucket = s3.Bucket(bucket_name)
    
    # GET MENTIONS TIMELINE FOR BOT I.E. FIND OUT WHO HAS MENTIONED THE BOT WITH #DhiTimeLineBot IN THEIR TWEET
    tweets = bot.get_user_mention_timeline()  # IF THE RULE ALREADY EXISTS NOTHING HAPPENS, SO WE ARE GOOD
    
    # READ THE MOST RECENT TWEET ID THAT WE REPLIED TO
    bucket.download_file(bucket_object_name, temp_file_name)
    with open(temp_file_name, "r") as f:
        most_recent_tweet_id = int(f.read())
        
    # FILTER ONLY THOSE TWEETS WITH #DhiTimeLineBot & WHOSE ID IS AHEAD OF PROVIDED ID
    filtered_tweets = bot.search_tweets(tweets, reply_hastags[1], threshold_id=most_recent_tweet_id)
    
    # REPLY TO TWEETS
    reply_to_tweets = bot.reply_to_tweets(filtered_tweets)
    filtered_tweets.sort(key=lambda tweet: tweet['tweet_id'])
    
    # IF WE SUCCESSFULLY REPLIED TO TWEETS, USE LATEST TWEET ID ELSE OLDEST TWEET ID
    if len(filtered_tweets):
        old_value = most_recent_tweet_id
        if reply_to_tweets:
            most_recent_tweet_id = filtered_tweets[-1]['tweet_id']
        else:
            most_recent_tweet_id = filtered_tweets[0]['tweet_id']
        print(f"Updating the most recent tweet id from {old_value} TO {most_recent_tweet_id}")
        
    # THEN UPDATE FILE WITH THE ID OF THE TWEET THAT WE MOST RECENTLY REPLIED TO
    with open(temp_file_name, "w") as f:
        f.write(str(most_recent_tweet_id))
    
    # UPLOAD THE FILE
    bucket.upload_file(temp_file_name, bucket_object_name)
