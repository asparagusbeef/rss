import json
import datetime
import lxml.etree as ET
from xml.sax.saxutils import escape

def create_rss_feed(tweets, rss_file_name):
    rss_root = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss_root, 'channel')

    ET.SubElement(channel, 'title').text = "My Twitter Feed"
    ET.SubElement(channel, 'link').text = "https://asparagusbeef.github.io/rss/feed.xml"
    ET.SubElement(channel, 'description').text = "A feed of tweets"

    for tweet in tweets:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = escape(tweet['full_text'][:90] + "...")
        ET.SubElement(item, 'link').text = tweet['tweet_url']

        description = ""
        if tweet['image_urls']:
            description += "<img src='{}'/>".format(escape(tweet['image_urls'][0])) 
        description += "<p>{}</p>".format(escape(tweet['full_text']))

        description_element = ET.SubElement(item, 'description')
        description_element.text = ET.CDATA(description)

        pub_date = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        ET.SubElement(item, 'pubDate').text = pub_date.strftime('%a, %d %b %Y %H:%M:%S +0000')

    tree = ET.ElementTree(rss_root)
    with open(rss_file_name, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)

# Load your tweets JSON here
with open("antisemitic_instance_tweets.json", "r") as f:
    tweets = json.load(f)

rss_file_name = 'my_feed.xml'
create_rss_feed(tweets, rss_file_name)
