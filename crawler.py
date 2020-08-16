import wikipedia
import time
import re
import sys
import boto3
import json
import os
import logging


def parsePageContent(article):
    content = re.sub(r'={1,}.+={1,}', '', article)
    content = content.split('\n{1,}')
    return content


def executeCheckpoint(topics):
    s3 = boto3.client('s3')
    file = 'wikipedia-content-dataset.json'
    bucket = 'wikipedia-crawler-s3'

    with open(file, 'w') as outfile:
        json.dump(topics, outfile)

    s3.upload_file(file, bucket, file)
    os.remove(file)
    return 0

def setupLogger():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def crawl():
    visited_topics = []
    topics = {}
    content_goal = 25000
    checkpoint_treshold = 25
    checkpoint_counter = 0

    while len(visited_topics) <= content_goal:
        topic = wikipedia.random(pages=1)
        if topic not in visited_topics:
            try:
                page = wikipedia.page(topic)
                if page is not None or page != '':
                    visited_topics.append(topic)
                    logging.info(f'Visiting topic: {topic}')
                else:
                    continue

                article = page.content
                content = parsePageContent(article)
                content.append(page.summary)
                topics[topic] = content

                if checkpoint_counter >= checkpoint_treshold:
                    checkpoint_counter = executeCheckpoint(topics)
                    logging.info(f'Checkpoint reached, {len(visited_topics)} visited')
                else:
                    checkpoint_counter += 1

                time.sleep(1)
            except Exception as ex:
                logging.error(ex)
                continue
        else:
            continue

setupLogger()
crawl()
