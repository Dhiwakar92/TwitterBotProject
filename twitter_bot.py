
import json
from requests_oauthlib import OAuth1Session, OAuth2Session
from constants import consumer_key, consumer_secret, access_token, access_token_secret, bearer_token, urls


class TwitterBot:

    def __init__(self):

        self._oauth1_hdrs = {'content-type': 'application/json'}
        self._oauth1_session = OAuth1Session(consumer_key, client_secret=consumer_secret, resource_owner_key=access_token, resource_owner_secret=access_token_secret)

        self._oauth2_hdrs = {'content-type': 'application/json'}
        self._oauth2_session = OAuth2Session(token={'access_token': bearer_token})

    def post_a_tweet(self, tweet):
        "Post a tweet"
        url = urls['post_a_tweet']
        response = self._oauth1_session.post(url=url, headers=self._oauth1_hdrs, data=json.dumps({'text': tweet}))
        return response.status_code

    def reply_to_tweets(self, tweets, reply=None):  # HASHTAGS are in constants.py
        """Replies to tweets, need to provide the username (to reply to) and optionally the tweet."""
        
        if tweets:
            
            for tweet in tweets:
                username, text = tweet['username'], tweet['tweeted'].replace('@', '*')
                reply_tweet = f" Hey @{username}" + (reply if reply else f" thanks for tweeting '{text}', Here's your star \u2605 !")
                status_code = self.post_a_tweet(reply_tweet) # COULD

            return True if status_code == 201 else False

    def get_user_mention_timeline(self, user_name=None):

        if not user_name:
            url = urls['authenticated_user_lookup']
            response = self._oauth1_session.get(url)
            if response.status_code == 200:
                response = response.json()
                user_id = response['data']['id']
        else:
            raise NotImplementedError("We have not implemented this yet.")

        url = urls['user_mention_timeline'].format(user_id=user_id)
        fields = {"tweet.fields": "author_id,id", "expansions": "author_id"}
        response = self._oauth1_session.get(url=url, params=fields, headers=self._oauth1_hdrs)

        output = []
        if response.status_code == 200:
            response = response.json()
            authors = {user['id']: user['username'] for user in response['includes']['users']}
            for tweet in response['data']:
                output.append(
                    {'tweet_id': tweet['id'], 'tweeted': tweet['text'], 'username': authors[tweet['author_id']]}
                )
            return output
        else:
            raise(f"FAILURE, status_code = {response.status_code}, reason = {response.reason}")

    @staticmethod
    def search_tweets(tweets, search_term, threshold_id=None):
        "Return tweets if they contain given search term, AND, optionally if tweet's id > provided threshold_tweet_id."

        if not threshold_id:
            return [tweet for tweet in tweets for term in [search_term, search_term+','] if term in tweet['tweeted'].split()]
        return [tweet for tweet in tweets for term in [search_term, search_term + ','] if term in tweet['tweeted'].split() and int(tweet['tweet_id']) > int(threshold_id)]

    def add_rule(self, rules):
        "Add rules, rules must be of type list."

        # WORTH ASSERTING THAT rules IS A LIST
        url = urls['post_rule']
        data = {'add': []}

        for rule in rules:
            data['add'].append({'value': rule})

        response = self._oauth2_session.post(url=url, json=data)
        return response  # ENHANCE WITH A try...except BLOCK

    def delete_rule(self, rule_id=None, rule_name=None):
        pass  # WE COULD JUST OPTIMIZE BY WRITING SOME COMMON METHOD FOR add_rule && delete_rule SINCE API REMAINS SAME
        raise NotImplementedError

    def retrieve_rules(self):

        url = urls['retrieve_rules']
        response = self._oauth2_session.get(url)
        if response.status_code == 200:
            response = response.json()
            return response.get('data', [])  # IF 'data' IS PRESENT, RETURN IT, ELSE RETURN EMPTY LIST
        else:
            raise(f"FAILURE, status_code = {response.status_code}, reason = {response.reason}")

    def stream(self, fields=None):

        tweets = []

        if not fields:  # THEN JUST CAPTURE THE USERNAME AND THE TEXT OF THE TWEETS
            fields = {"user.fields": "username", "tweet.fields": "text", "expansions": "referenced_tweets.id,entities.mentions.username"}

        url = urls['stream_tweets']
        response = self._oauth2_session.get(url, params=fields, stream=True)

        count = 3
        for line in response.iter_lines():
            if line:
                line = json.loads(line)
                usernames = ','.join((user['username'] for user in line['includes']['users']))
                tweet = line['data']['text']
                tweets.append({'username': usernames, 'tweeted': tweet})

            count -= 1

            if not count:
                return tweets
