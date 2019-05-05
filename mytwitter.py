from google.appengine.ext import ndb

class MyTwitter(ndb.Model):
      name = ndb.StringProperty()
      profile = ndb.StringProperty()
      tweets = ndb.StringProperty(repeated=True)
      followers= ndb.StringProperty(repeated=True)
      following = ndb.StringProperty(repeated=True)

class TweetAll(ndb.Model):
    alltweets=ndb.StringProperty(repeated=True)
    uname=ndb.StringProperty(repeated=True)
