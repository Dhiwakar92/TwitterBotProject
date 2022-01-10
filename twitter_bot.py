
import json
from requests_oauthlib import OAuth1Session, OAuth2Session
from constants import consumer_key, consumer_secret, access_token, access_token_secret, bearer_token, urls, reply_hastag


class TwitterBot:

    def __init__(self):
        self._oauth1_hdrs = {'content-type': 'application/json'}
        self._oauth1_session = OAuth1Session(consumer_key, client_secret=consumer_secret, resource_owner_key=access_token, resource_owner_secret=access_token_secret)
        self._oauth2_hdrs = {'content-type': 'application/json'}
        self._oauth2_session = OAuth2Session(token={'access_token': bearer_token})

    def post_a_tweet(self, tweet):

        url = urls['post_a_tweet']
        response = self._oauth1_session.post(url=url, headers=self._oauth1_hdrs, data=json.dumps({'text': tweet}))
        return response

    def add_rule(self, rules):  # PASS IN A LIST OF RULES

        url = urls['post_rule']
        data = {'add': []}

        for rule in rules:
            data['add'].append({'value': rule})

        response = self._oauth2_session.post(url=url, json=data)
        return response  # ENHANCE WITH A try...except BLOCK

    def delete_rule(self, rule_id=None, rule_name=None):
        pass  # WE COULD JUST OPTIMIZE BY WRITING SOME COMMON METHOD FOR add_rule && delete_rule SINCE API REMAINS SAME
        raise NotImplementedError

    def stream(self, fields=None):

        tweets = []

        if not fields: # THEN JUST CAPTURE THE USERNAME AND THE TEXT OF THE TWEETS
            fields = {"user.fields": "username", "tweet.fields": "text", "expansions": "referenced_tweets.id,entities.mentions.username"}

        url = urls['stream_tweets']
        response = self._oauth2_session.get(url, params=fields, stream=True)
        count = 10
        for line in response.iter_lines():
            if line:
                line = json.loads(line)
                usernames = ','.join((user['username'] for user in line['includes']['users']))
                tweet = line['data']['text']
                tweets.append({'username': usernames, 'tweeted': tweet})

            count -= 1

            if not count:
                return tweets

    def reply_to_tweets(self, tweets):  # HASHTAG is in constants.py
        for tweet in tweets:
            username, text = tweet['username'], tweet['tweeted']
            reply = f" Hey @{username}, thanks for tweeting '{text}', Here's your star !"
            self.post_a_tweet(reply)