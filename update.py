import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from mytwitter import MyTwitter
from mytwitter import TweetAll
import os
from name import Name
from edit import Edit
from userprofile import UserProfile

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class Update(webapp2.RequestHandler):
    def get(self,id):
        self.response.headers['Content-Type'] = 'text/html'
        click=id
        key = users.get_current_user().email()
        mytwitter_key = ndb.Key('MyTwitter', key)
        mytwitter = mytwitter_key.get()
        third=mytwitter.tweets
        third=third[::-1]
        template_values={'mytwitter':mytwitter,'third':third}
        template=JINJA_ENVIRONMENT.get_template('update.html')
        self.response.write(template.render(template_values))
    def post(self,id):
        action = self.request.get('button')
        key = users.get_current_user().email()
        mytwitter_key = ndb.Key('MyTwitter', key)
        mytwitter = mytwitter_key.get()
        master_key = ndb.Key('TweetAll', 'master')
        master = master_key.get()
        click=id
        tweetword=None
        if action == 'delete':
            third=mytwitter.tweets
            third=third[::-1]
            del third[int(self.request.get('index')) - 1]
            third=third[::-1]
            mytwitter.tweets=third
            mytwitter.put()
            tweetword=self.request.get('users_name')
            master.alltweets.remove(tweetword)
            master.put()
            self.redirect('/')
        if action=='Edit':
            tweetword=self.request.get('users_name')
            fourth=mytwitter.tweets
            fourth=fourth[::-1]
            tweetword1=fourth[int(self.request.get('index'))-1]
            third=mytwitter.tweets
            third=third[::-1]
            third[int(self.request.get('index'))-1]=self.request.get('users_name')
            third=third[::-1]
            mytwitter.tweets=third
            mytwitter.put()
            master.alltweets[master.alltweets.index(tweetword1)]=tweetword
            master.put()
            self.redirect('/')
