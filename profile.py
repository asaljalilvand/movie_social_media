# -*- coding: utf-8 -*-
import Tkinter as tk
import connection  
from py2neo import Graph,Node,NodeSelector,Relationship
LARGE_FONT= ("Verdana", 10,"bold")
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)
class ProfilePage(tk.Frame):

    window = None
    controller = None
    popup = None
    def __init__(self, parent, cntrlr):
         
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(cntrlr, "Profile")
        ProfilePage.window = self
        ProfilePage.controller = cntrlr
        stvar = tk.StringVar()
        stvar1 = tk.StringVar()
        
        self.logo = tk.PhotoImage(file='user.gif')
        query = "match (n:User) where id(n)="+str(connection.pid)+" return n.name as name,n.age as age,n.edu as edu,n.sex as sex"
        result = connection.g.run(query)
        info = ''
        for m in result:
			info = 'name:'+m['name']+'\nage: '+m['age']+'\nsex:'+m['sex']+'\neducation:'+m['edu']
			if m['sex']=='Male':
				self.logo = tk.PhotoImage(file='male.gif')
        L1 = tk.Label(self, image=self.logo)
        L1.grid(row=0,column=0)
        l = tk.Label(self, text = info,anchor='center', relief="groove")
        l.grid(row=0,column=1)	
        searchButton = tk.Button(self, text="Search",command = lambda:ProfilePage.controller.show_page("SearchPage"))
        searchButton.grid(row=0,column=2)
        homeButton = tk.Button(self, text="Home",command = lambda:ProfilePage.controller.show_page("HomePage"))
        homeButton.grid(row=0,column=3)
        myProfileButton = tk.Button(self, text="My Profile",command = lambda:ProfilePage.show_profile(connection.uid))
        myProfileButton.grid(row=0,column=4)
        settingButton = tk.Button(self, text="Settings",command =lambda: ProfilePage.controller.show_page("SettingsPage"))
        settingButton.grid(row=0,column=5)
        signoutButton = tk.Button(self, text="Sign Out",command = lambda: ProfilePage.controller.show_page("StartPage"))
        signoutButton.grid(row=0,column=6)
		
		
        friends = True
        if(int(connection.uid) != int(connection.pid)):
			query = "MATCH (you)-[:FRIEND]-(yourFriends) where id(you)="+str(connection.uid)+" RETURN id(yourFriends) as id"
			result=connection.g.run(query)		
			friends = []	
			btn = None			
			for r in result:
				friends.append(r['id'])
			if connection.pid not in friends:	
				friends = False				
				btn = tk.Button(self, text="Add Friend",command = lambda:ProfilePage.add_friend())					
			else:
				friends = True
				btn = tk.Button(self, text="Unfriend",command = lambda:ProfilePage.remove_friend())
					
			btn.grid(row=5,column=0)
			
        f1 = tk.Button(self, text="Friends",command = lambda:ProfilePage.controller.show_page("FollowPage"))
        f1.grid(row=2,column=0)
 
        r=2
        c=1
        query = "MATCH (you)-[r:LIKES]->(movie:Movie) where id(you)="+str(connection.pid)+" return id(movie) as id,movie.title as title,r.rating as rating,r.comment as comment"
        media = connection.g.run(query)
        l2 = tk.Label(self, text = 'My Movies:',anchor='center',font=LARGE_FONT,borderwidth=2, relief="groove",height=3, width=30)
        l2.grid(row=1,column=1)
        for m in media:
			txt = str(m['title']) + '\nmy vote =' + str(m['rating']) + ' my comment =' + str(m['comment'])
			b =  tk.Button(self, text = txt,height=3, width=30,command = lambda m=m:ProfilePage.show_movie(m['id']))
			b.grid(row=r,column=c)
			r = r+1
			
        r=2
        c=2
        query = "MATCH (you)-[r:LIKES]->(movie:Tv_Show) where id(you)="+str(connection.pid)+" return id(movie) as id,movie.title as title,r.rating as rating,r.comment as comment"
        media = connection.g.run(query)
        l3 = tk.Label(self, text = 'My Tv Shows:',anchor='center',font=LARGE_FONT,borderwidth=2, relief="groove",height=3, width=30)
        l3.grid(row=1,column=2)
        for m in media:
			txt = str(m['title']) + '\nmy vote =' + str(m['rating']) + ' my comment =' + str(m['comment'])
			b =  tk.Button(self, text = txt,height=3, width=30,command = lambda m=m:ProfilePage.show_movie(m['id']))
			b.grid(row=r,column=c)
			r = r+1
			
			
		
    @staticmethod   
    def show_profile(id):
		connection.pid = id
		HomePage.controller.show_page("ProfilePage")
		
    @staticmethod   
    def show_movie(id):
		connection.movie = id
		ProfilePage.controller.show_page("MediaPage")
		
		
    @staticmethod
    def add_friend():
		n1 = connection.g.node(connection.uid)
		n2 = connection.g.node(connection.pid)
		new_relationship = Relationship(n1,"FRIEND", n2)		
		connection.g.create(new_relationship)
		ProfilePage.controller.show_page("ProfilePage")
   
    @staticmethod
    def remove_friend():
		query = "MATCH (you)-[r:FRIEND]-(yourFriend) where id(you)="+str(connection.uid)+" and id(yourFriend)="+str(connection.pid)+" delete r"
		connection.g.run(query)			
		ProfilePage.controller.show_page("ProfilePage")






















	
		
		
		
		
		
		
		
		