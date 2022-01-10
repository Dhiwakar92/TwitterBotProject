
# AUTHORIZATION & AUTHENTICATION RELATED CONSTANTS
with open('secrets.txt', 'r') as f:
        lines = f.readlines()

lines = iter(lines)
consumer_key = next(lines)
consumer_secret = next(lines)
access_token = next(lines)
access_token_secret = next(lines)
bearer_token = next(lines)

# URLS
base_url = 'https://api.twitter.com/2'
urls = {
        'post_a_tweet': base_url+'/tweets',
        'stream_tweets': base_url+'/tweets/search/stream',
        'post_rule': base_url+'/tweets/search/stream/rules'
}

reply_hastag = "#DhiSwiggyBotPleaseReply"