#!/usr/bin/env python

import commands
import urllib
import json
import facebook
import os
import shutil

access_token = os.getenv('ACCESS_TOKEN')
graph = facebook.GraphAPI(access_token)
user_id = graph.get_object("me")['id']

download = True
#download = False # so we don't have to re-download photos

def main():
  if download:
    grab_photos()

  print commands.getstatusoutput('./cmd.sh %s' % user_id)

def grab_photos():
  if os.path.exists(user_id):
    shutil.rmtree(user_id)

  # make a directory for user's photos
  os.mkdir(user_id)

  data = graph.get_connections("me", "photos", limit=10000)
  photos = data['data']
  photo_objs = {}
  queries = {}
  for photo_data in photos:
    photo = Photo(photo_data)
    photo_objs[photo.getID()] = photo
    queries[photo.getID()] = 'SELECT object_id from like WHERE object_id in ' + photo.getID()

  like_infos = fql(queries)
  for like_info in like_infos:
    num_likes = len(like_info['fql_result_set'])
    id = str(like_info['name'])
    photo = photo_objs[id]
    photo.setNumLikes(num_likes)

  photo_objs = photo_objs.values()
  photo_objs.sort(compareScores)

  i = 0
  for photo in photo_objs:
    i = i + 1
    print photo.getLink()
    urllib.urlretrieve(photo.getSource(), '%s/%s.jpg' % (user_id, str(i)))

def compareScores(photo_a, photo_b):
  return photo_b.getScore() - photo_a.getScore()

def fql(queries):
  req_url = 'https://api.facebook.com/method/fql.multiquery?format=json&queries=' + urllib.quote(json.dumps(queries)) + '&access_token=' + access_token
  file = urllib.urlopen(req_url)
  return json.load(file)

class Photo:
  def __init__(self, data):
    self.data = data

  def getID(self):
    return self.data['id']

  def getSource(self):
    return self.data['images'][0]['source']

  def getNumComments(self):
    if 'comments' in self.data:
      return len(self.data['comments'])
    else:
      return 0

  def setNumLikes(self, num_likes):
    self.numLikes = num_likes

  def getNumLikes(self):
    return self.numLikes

  def getScore(self):
    return self.getNumComments() + self.getNumLikes()

  def getLink(self):
    return self.data['link']

main()
