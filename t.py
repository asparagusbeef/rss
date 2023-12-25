import json
import os

def extract_tweets_from_json(file_path):
    """
    Extract tweets from a JSON file located at `file_path`.
    """
    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return []

    with open(file_path, 'r') as file:
        data = json.load(file)

    if 'entries' not in data:
        print("No 'entries' key found in the JSON data.")
        return []

    tweets = []
    for entry in data['entries']:
        content = entry.get('content', {})
        item_content = content.get('itemContent', {})
        tweet_result = item_content.get('tweet_results', {}).get('result', {})
        if tweet_result:
            tweets.append(tweet_result)

    return tweets

file_path = 'twitter_entries/entry_2.json'
tweets = extract_tweets_from_json(file_path)
print(f"Extracted {len(tweets)} tweets.")


lst = []

lst = []

for tweet in tweets:
    # Basic tweet info
    full_text: str = tweet.get('legacy', {}).get('full_text')
    full_text = full_text.encode()
    images = tweet.get('legacy', {}).get('extended_entities', {}).get('media', [])
    image_urls = [image['media_url_https'] for image in images]

    # Additional info
    created_at = tweet.get('legacy', {}).get('created_at')
    user_name = tweet.get('legacy', {}).get('user', {}).get('name')
    user_screen_name = tweet.get('legacy', {}).get('user', {}).get('screen_name')
    tweet_id = tweet.get('rest_id')
    tweet_url = f"https://twitter.com/{user_screen_name}/status/{tweet_id}"

    retweet_count = tweet.get('legacy', {}).get('retweet_count')
    favorite_count = tweet.get('legacy', {}).get('favorite_count')

    lst.append({
        'full_text': full_text, 
        'image_urls': image_urls,
        'created_at': created_at,
        'user_name': user_name,
        'user_screen_name': user_screen_name,
        'tweet_url': tweet_url,
        'retweet_count': retweet_count,
        'favorite_count': favorite_count
    })



import openai

prompt = '''
This is a tweet by the user @stopantisemites. They post a lot of tweets. Some of them depict specific NEW antisemitic instances. Others may refer to old antisemitic instances, may refer to antisemitic people, or may be general.

If the tweet depicts a specific NEW antisemitic instance, please type "1". 

If the tweet depicts an old antisemitic instance, a person, or other, please type "0".

TWEET:
{tweet}
'''
openai.api_key = "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"

def is_antisemitic_instance(tweet_text):
    completion = openai.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt.format(tweet=tweet_text)}
        ], 
        model="gpt-3.5-turbo-16k",
        temperature=0.3,
        max_tokens=10,
    )
    return completion.choices[0].message.content

is_antisemtic_instance_lst = []

i=0
for tweet in lst:
    print(f"Tweet {i}")
    is_antisemtic_instance_lst.append(is_antisemitic_instance(tweet['full_text']))
    i+=1

is_antisemtic_instance_lst

antisemitic_instance_tweets = []

for i, val in enumerate(is_antisemtic_instance_lst):
    if val == "1":
        antisemitic_instance_tweets.append(lst[i])

# save to json
with open('antisemitic_instance_tweets.json', 'w', encoding='utf-8') as f:
    json.dump(antisemitic_instance_tweets, f)

