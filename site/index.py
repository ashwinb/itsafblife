from mod_python import apache, util
import commands
import datetime
import facebook
import feed.date.rfc3339
import json
import math
import os
import pickle
import random
import shutil
import smtplib
import string
import sys
import urllib

def index(req):
  redirect_uri = 'http://localhost/hackathon/site/app.py'
  util.redirect(req, 'https://graph.facebook.com/oauth/authorize?client_id=156562204392783&type=user_agent&redirect_uri=%s&scope=offline_access%%2Cuser_photo_video_tags' % redirect_uri)

def app(req, access_token=None):
  if access_token == None:
    return """\
  <html>
    <head>
      <script src="/hackathon/site/resources/code.js"></script>
    </head>
    <body onload="loaded()">
    <form action='/hackathon/site/app.py'>
      <input name='access_token' style='display:none' value=''/>
    </form>
    </body>
  </html>"""

  os.chdir('/var/www/hackathon')
  f = FBMontage(access_token)
  s = f.grab_photos()
  f.create_slideshow()
  return '<html>%s</html>' % s

class FBMontage:
  def __init__(self, access_token):
    self.accessToken = access_token
    self.graph = facebook.GraphAPI(self.accessToken)
    self.userID = self.graph.get_object("me")['id']

  def create_slideshow(self):
    print commands.getstatusoutput('./cmd.sh %s' % self.userID)

  def grab_photos(self):
    data = self.graph.get_connections("me", "photos", limit=10000)
    songlength = commands.getoutput('mp3info -p "%%S" %s' % 'green_day.mp3')
    num_photos = int(math.floor(string.atoi(songlength) / 3.5))

    download = False # so we don't have to re-download photos
    download = True

    cached_buckets = True
    cached_buckets = False
    if download and os.path.exists(self.userID):
      shutil.rmtree(self.userID)

    # make a directory for user's photos
    if download:
      os.umask(0)
      os.mkdir(self.userID)

    if cached_buckets:
      buckets = pickle.load(open('buckets.p', 'rb'))
    else:
      buckets = self.get_bucketed_photos()

    #pickle.dump(buckets, open('buckets.p', 'wb'))
    photo_objs = self.get_top_photos(buckets, num_photos)

    i = 1
    # dvd-slideshow can't do a numeric sort so name the files in the
    # form: 001.jpg, 002.jpg...
    max_digits = int(math.floor(math.log10(len(photo_objs))))
    for photo in photo_objs:
      digits = int(math.floor(math.log10(i)))
      filename = '0' * (max_digits - digits) + str(i)
      i = i + 1
      print photo.getLink()
      urllib.urlretrieve(photo.getSource(), '%s/%s.jpg' % (self.userID, filename))

  def bucket(self, photos):
    num_buckets = 10

    photos.sort(compareTimes)
    first_time = photos[0].getTime()
    last_time = photos[len(photos) - 1].getTime()
    bucket_size = ((last_time - first_time) + 1) / float(num_buckets)
    photos.sort(compareScores)

    buckets = dict([(x,[]) for x in range(num_buckets)])

    for photo in photos:
      bucket = int(math.floor((photo.getTime() - first_time)/bucket_size))
      buckets[bucket].append(photo)
    # for bucket_num, photos in buckets.items():
    #  print 'bucket num %d' % bucket_num
    #  for photo in photos:
    #    print datetime.date.strftime(datetime.date.fromtimestamp(photo.getTime()), '%d/%m/%Y')

    return buckets

  def get_top_photos(self, buckets, num_photos):
    top_photos = []
    i = 0
    done = False
    while len(top_photos) < num_photos and not done:
      done = True
      for bucket_num, photos in buckets.items():
        if len(top_photos) == num_photos:
          break
        if i < len(photos):
          done = False
          top_photos.append(photos[i])
      i = i + 1
    top_photos.sort(compareTimes)
    return top_photos

  def get_bucketed_photos(self):
    data = self.graph.get_connections("me", "photos", limit=10000)
    photos = data['data']
    photo_objs = {}
    queries = {}
    for photo_data in photos:
      photo = Photo(photo_data)
      photo_objs[photo.getID()] = photo
      queries[photo.getID()] = 'SELECT object_id from like WHERE object_id in ' + photo.getID()

    like_infos = self.fql(queries)
    for like_info in like_infos:
      num_likes = len(like_info['fql_result_set'])
      id = str(like_info['name'])
      photo = photo_objs[id]
      photo.setNumLikes(num_likes)

    return self.bucket(photo_objs.values())

  def fql(self, queries):
    req_url = 'https://api.facebook.com/method/fql.multiquery'
    params = {'format' : 'json', 'queries' : json.dumps(queries), 'access_token' : self.accessToken}
    file = urllib.urlopen(req_url, urllib.urlencode(params))
    return json.loads(file.read())

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

  def getTime(self):
    return int(feed.date.rfc3339.tf_from_timestamp(self.data['created_time']))


def compareScores(photo_a, photo_b):
  score_a = photo_a.getScore()
  score_b = photo_b.getScore()

  # old pictures don't have comments nor likes, do this to pick photos
  # from same album less often
  if score_a == score_b:
    random.randint(-1,1)
  return score_b - score_a

def compareTimes(photo_a, photo_b):
  return photo_a.getTime() - photo_b.getTime()

