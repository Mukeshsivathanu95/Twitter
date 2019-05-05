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
from update import Update

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
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
            overall=ndb.Key('TweetAll','master')
            m=overall.get()
            if m==None:
                m=TweetAll(id='master')
                m.put()
            if mytwitter == None:
                welcome = 'This is a Twitter model'
                mytwitter = MyTwitter(id=key)
                mytwitter.put()
            if mytwitter.name==None:
                self.redirect('/name')
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
        query= MyTwitter.query().fetch()
        name=self.request.get('search')
        lastman=None
        first=0
        findtweet=self.request.get('findtweet')
        list3=[]
        second=0
        action=self.request.get('button')
        if action=='Search':
            for i in query:
                if i.name==name:
                    first=first+1
                    lastman=name
        z=[]
        if action=='FindTweet':
            for i in query:
                for j in i.tweets:
                    if findtweet in j:
                        z.append(i.name)
                        second=second+1
                        list3.append(j)
        list1=0
        list2=0
        if mytwitter!=None:
            for i in mytwitter.followers:
                    list1=list1+1
            for j in mytwitter.following:
                    list2=list2+1

        module_part = ndb.Key('TweetAll', 'master')
        module = module_part.get()
        tweetlist=[]
        tweetname=[]
        if module!=None:
            for i in reversed(module.alltweets):
                tweetlist.append(i)
            tweetlist = tweetlist[:50]
            for j in reversed(module.uname):
                tweetname.append(j)
            tweetname=tweetname[:50]
        tweetz=zip(tweetname,tweetlist)
        www=zip(z,list3)
        template_values = {'url' : url,'url_string' : url_string,'user' : user,'welcome' : welcome,'mytwitter' : mytwitter,'first':first,'lastman':lastman,'second':second,'list3':list3,'list1':list1,'list2':list2,'tweetz':tweetz,"www":www}
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))






app = webapp2.WSGIApplication([('/', MainPage),('/name', Name),('/edit',Edit),('/userprofile/(.*)',UserProfile),('/update/(.*)',Update)], debug=True)
