import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def parseBF():
    response = requests.get("https://www.buzzfeed.com/news")
    html = BeautifulSoup(response.text, "html.parser")

    topics = defaultdict(list)
    for link in html.findAll(lambda tag: tag.name=='a' and 'data-bfa' in tag.attrs):
        attr = link['data-bfa']
        if not 'post_category' in attr: continue
        values = attr.split(',')
        topic = [v.split(':')[1] for v in values if v.startswith('post_category')]
        topic = topic[0]
        # print topic, link['href']
        topics[topic].append(link['href'])
    return topics

topics = parseBF()
for t in topics:
    print t
    print '\t'+'\n\t'.join(topics[t])
