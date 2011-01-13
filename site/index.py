from mod_python import apache
import commands
import json
import smtplib

def index(req):
  redirect_uri = 'http://localhost/hackathon/site/index.py'
  s = """\
<html>
  <script src="resources/code.js"></script>
  <body onload="loaded()">
  <a href='https://graph.facebook.com/oauth/authorize?client_id=156562204392783&type=user_agent&redirect_uri=%s&scope=offline_access%%2Cuser_photo_video_tags'>Install app!</a>
  <form action='index.py/go'>
    <input name='access_token' style='display:none'/>
  </form>
  </body>
</html>"""

  return s % (redirect_uri)

def go(req, access_token):
  #commands.getstatusoutput('python ../grab_photos.py %s' % access_token)
  return '<html>%s</html>' % access_token
