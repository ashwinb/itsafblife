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

download = True # so we don't have to re-download photos

def main():
  if download:
    grab_photos()

  print commands.getstatusoutput('./cmd.sh %s' % user_id)

def grab_photos():
  if os.path.exists(user_id):
    shutil.rmtree(user_id)

  # make a directory for user's photos
  os.mkdir(user_id)

  data = graph.get_connections("me", "photos")
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

  for id in photo_objs:
    print 'Saving %s.jpg...' % id
    urllib.urlretrieve(photo_objs[id].getSource(), '%s/%s.jpg' % (user_id, id))

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

main()
