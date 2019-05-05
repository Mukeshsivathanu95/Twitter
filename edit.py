import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from mytwitter import MyTwitter
from mytwitter import TweetAll
import os
from name import Name

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class Edit(webapp2.RequestHandler):
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
            self.response.out.write("<html><head></head><body>")
            self.response.out.write("Edit your information below:<br/>")
            self.response.out.write("""<form method='get' action='/edit'>""")
            first=mytwitter.profile
            self.response.out.write("""PROFILE INFO:<br/><input style="height:200px;width:1000px;font-size:14pt;" type='text' name='input1' required='True' maxlength="280" placeholder="%s"/><br/>"""%(first))
            self.response.out.write("""<input type='submit' name='button' value='Submit'/>""")
            self.response.out.write("""</form>""")
            self.response.out.write("<a href='/'>Home</a>")

            action=self.request.get('button')
            if action == 'Submit':
                profile=self.request.get('input1')
                mytwitter.profile=profile
                mytwitter.put()
                self.redirect('/')
            self.response.out.write("</body></html>")

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {'url' : url,'url_string' : url_string,'user' : user,'mytwitter' : mytwitter,'first':first}
        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_values))

    def post(self):
        key = users.get_current_user().email()
        mytwitter_key = ndb.Key('MyTwitter', key)
        mytwitter = mytwitter_key.get()
        overall=ndb.Key('TweetAll','master')
        m=overall.get()
        name=mytwitter.name
        action=self.request.get('button')
        if action == 'Submit':
            tweets=self.request.get('tweets')
            mytwitter.tweets.append(tweets)
            m.alltweets.append(tweets)
            m.uname.append(name)
            m.put()
            mytwitter.put()
            self.redirect('/')
