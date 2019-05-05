import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from mytwitter import MyTwitter
from mytwitter import TweetAll
import os
from name import Name
from edit import Edit

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)


class UserProfile(webapp2.RequestHandler):
    def get(self,id):
        self.response.headers['Content-Type'] = 'text/html'
        click=id
        query = MyTwitter.query(MyTwitter.name == click)
        third=[]
        for i in query:
            for j in reversed(i.tweets):
                third.append(j)
        third = third[:50]
        template_values={'query':query,'third':third}
        template=JINJA_ENVIRONMENT.get_template('userprofile.html')
        self.response.write(template.render(template_values))
    def post(self,id):
        key = users.get_current_user().email()
        mytwitter_key = ndb.Key('MyTwitter', key)
        mytwitter = mytwitter_key.get()
        name=mytwitter.name
        click=id
        keys=None
        profilename=None
        query = MyTwitter.query(MyTwitter.name == click)
        for i in query:
            keys=i.key.id()
        action=self.request.get('button')
        if action == 'FOLLOW':
                mytwitter_key = ndb.Key('MyTwitter', keys)
                mytwitter = mytwitter_key.get()
                profilename=mytwitter.name
                if name==mytwitter.name:
                        self.redirect('/userprofile/%s'%(click))
                else:
                    if name in mytwitter.followers:
                            self.redirect('/userprofile/%s'%(click))
                    else:
                            mytwitter.followers.append(name)
                            mytwitter.following.append(profilename)
                            mytwitter.put()
                            mytwitter.put()
                            self.redirect('/userprofile/%s'%(click))
        if action == 'UNFOLLOW':
            mytwitter_key = ndb.Key('MyTwitter', keys)
            mytwitter = mytwitter_key.get()
            profilename=mytwitter.name
            if name in mytwitter.followers:
                mytwitter.followers.remove(name)
                mytwitter.put()
                if profilename in mytwitter.following:
                    mytwitter.following.remove(profilename)
                    mytwitter.put()
            self.redirect('/userprofile/%s'%(click))
