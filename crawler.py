import wikipedia
import time
import re
import boto3
import json
import os

def parsePageContent(content):
  content = re.sub(r'={1,}.+={1,}', '', content)
  content = article.split('\n{1,}')
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

visited_topics = []
topics = {}
content_goal = 25000
checkpoint_treshold = 50
checkpoint_counter = 0

def crawl():
  while len(visited_topics) <= content_goal:
    topic = wikipedia.random(pages=1)

    if topic not in visited_topics:
      try:
        page = wikipedia.page(topic)
        if page is not None or page != '':
          visited_topics.append(topic)
          print(f'Visiting topic: {topic}')
        else:
          continue

        article = page.content
        content = parsePageContent(article)
        content.append(page.summary)
        topics[topic] = content

        if checkpoint_counter >= checkpoint_treshold:
          checkpoint_counter = executeCheckpoint(topics)
          print(f'Checkpoint reached, {len(visited_topics)} visited')
        else:
          checkpoint_counter += 1

        time.sleep(1)
      except:
        continue
    else:
      continue

crawl()