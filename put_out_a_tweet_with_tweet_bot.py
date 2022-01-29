
from twitter_bot import TwitterBot
from constants import reply_hastags

def main(event, context):
    bot = TwitterBot()
    bot.add_rule([reply_hastags[0]])  # IF THE RULE ALREADY EXISTS NOTHING HAPPENS, SO WE ARE GOOD
    tweets = bot.stream()
    bot.reply_to_tweets(tweets)