import Tkinter as tk
import connection  
import time
from py2neo import Graph,Node,NodeSelector,Relationship


LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

class MediaPage(tk.Frame):

    L2 = None
    window = None
    controller = None
    popup = None
	
    def __init__(self, parent, cntrlr):
         
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(cntrlr, "Movie/Tv Show")
        MediaPage.window = self
        MediaPage.controller = cntrlr
        searchButton = tk.Button(self, text="Search",command = lambda:MediaPage.controller.show_page("SearchPage"))
        searchButton.grid(row=0,column=3)
        homeButton = tk.Button(self, text="Home",command = lambda:MediaPage.controller.show_page("HomePage"))
        homeButton.grid(row=0,column=4)
        myProfileButton = tk.Button(self, text="My Profile",command = lambda:MediaPage.show_profile(connection.uid))
        myProfileButton.grid(row=0,column=5)
        settingButton = tk.Button(self, text="Settings",command =lambda: MediaPage.controller.show_page("SettingsPage"))
        settingButton.grid(row=0,column=6)        
        signoutButton = tk.Button(self, text="Sign Out",command = lambda: MediaPage.controller.show_page("StartPage"))
        signoutButton.grid(row=0,column=7)

        query = "match (n) where id(n)="+str(connection.movie)+" return n.title as title,n.tagline as tagline,n.summary as summary,n.duration as duration,n.year as year,n.rating as rating,n.likes as likes,labels(n) as l"
        media = connection.g.run(query)
        info = ''
        likes = None
        rating = None
        for m in media:
			info = 'type:'+str(m['l'])+'\ntitle: '+m['title']+'\ntagline:'+m['tagline']+'\nsummary:'+m['summary']+'\nduration:'+m['duration']+'\nyear:'+m['year']+'\nrating:'+str(m['rating'])+'\nlikes:'+str(m['likes'])
			likes = int(m['likes'])
			rating = int(m['rating'])
			
        query = "MATCH (m)<-[r:ACTED_IN]-(actor) where id(m)="+str(connection.movie)+" RETURN r.role as role , actor.name as name"
        persons = connection.g.run(query)
        info2 = 'Actors:\n'
        for p in persons:
			info2 = info2+p['name']+' as '+p['role']+'\n'
			
        query = "MATCH (m)<-[:DIRECTED_IN]-(director) where id(m)="+str(connection.movie)+" RETURN director.name as name"
        persons = connection.g.run(query)
        info2 = info2+'\nDirectors:\n'
        for p in persons:
			info2 = info2+p['name']+' '
			
        query = "MATCH (m)<-[:PRODUCED]-(producer) where id(m)="+str(connection.movie)+" RETURN producer.name as name"
        persons = connection.g.run(query)
        info2 = info2+'\n\nProducers:\n'
        for p in persons:
			info2 = info2+p['name']+' '
			
        query = "MATCH (m)<-[:WRITER_OF]-(writer) where id(m)="+str(connection.movie)+" RETURN writer.name as name"
        persons = connection.g.run(query)
        info2 = info2+'\n\nWriters:\n'
        for p in persons:
			info2 = info2+p['name']+' '
			
        query = "MATCH (m)-[:HAS_GENRE]->(genre) where id(m)="+str(connection.movie)+" RETURN genre.name as name"
        genres = connection.g.run(query)
        info2 = info2+'\n\nGeneres:\n'
        for g in genres:
			info2 = info2+g['name']+' '
			
        query = "MATCH (m)-[:HAS_KEYWORD]->(keyword) where id(m)="+str(connection.movie)+" RETURN keyword.name as name"
        keys = connection.g.run(query)
        info2 = info2+'\n\nKeywords:\n'
        for k in keys:
			info2 = info2+k['name']+' '
			
		
        n = tk.Label(self, text = info,anchor='w',font=NORM_FONT,borderwidth=2, relief="groove")
        n.grid(row=1,column=0)
        n2 = tk.Label(self, text = info2,anchor='w',font=NORM_FONT,borderwidth=2, relief="groove")
        n2.grid(row=1,column=1)
		
        query = "MATCH (you)-[r:LIKES]->(movie) where id(you)="+str(connection.uid)+" and id(movie)="+str(connection.movie)+" return r.rating as rating,r.comment as comment"
        relationship = connection.g.run(query)
        relationshipInfo = {}
        for r in relationship:
			relationshipInfo['rating'] = r['rating']
			relationshipInfo['comment'] = r['comment']
		
        l = None
        ltext = None
        if len(relationshipInfo)!=0:
			ltext = 'You have seen this movie! You Voted :'+relationshipInfo['rating']+' Your Comment: '+relationshipInfo['comment']
        else:
			ltext = 'Vote!'
			stvar = tk.StringVar(self)
			stvar1 = tk.StringVar()
			vote = tk.OptionMenu(self,stvar,"1","2","3","4","5")
			vote.grid(row=2,column=1)
			c = tk.Label(self, text ='Comment')
			c.grid(row=2,column=2)
			comment= tk.Entry(self,textvariable=stvar1)
			comment.grid(row=2,column=3)
			add = tk.Button(self, text="vote",command = lambda:MediaPage.add_relation(stvar.get(),comment.get(),likes,rating))
			add.grid(row=2,column=4)		
        l = tk.Label(self, text =ltext)
        l.grid(row=2,column=0)
        			
    @staticmethod   
    def show_profile(id):
		connection.pid = id
		MediaPage.controller.show_page("ProfilePage")	
    @staticmethod
    def add_relation(vote,comment,likes,rating):
		n1 = connection.g.node(connection.uid)
		n2 = connection.g.node(connection.movie)
		new_relationship = Relationship(n1,"LIKES", n2)		
		connection.g.create(new_relationship)
		new_relationship['rating']=vote
		new_relationship['comment']=comment
		n2['likes'] = likes + 1
		n2['rating'] = (rating + int(vote))/(likes + 1)
		new_relationship.push()
		n2.push()
		MediaPage.controller.show_page("MediaPage")
		
		