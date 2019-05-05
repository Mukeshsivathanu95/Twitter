import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from mytwitter import MyTwitter
from mytwitter import TweetAll
import os

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class Name(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        mytwitter = None
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            key = users.get_current_user().email()
            mytwitter_key = ndb.Key('MyTwitter', key)
            mytwitter = mytwitter_key.get()
            action=self.request.get('button')
            url = users.create_logout_url(self.request.uri)
            if action == 'Submit':
                name=self.request.get('input')
                profile=self.request.get('input1')
                mytwitter.name=name
                mytwitter.profile=profile
                mytwitter.put()
                self.redirect('/')
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {'url' : url,'ur_string' : url_string,'welcome' : welcome,'user' : user,'mytwitter' : mytwitter}
        template = JINJA_ENVIRONMENT.get_template('name.html')
        self.response.write(template.render(template_values))
