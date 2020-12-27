# -*- coding: utf-8 -*-
import Tkinter as tk
import connection  
from py2neo import Graph,Node,NodeSelector,Relationship
LARGE_FONT= ("Verdana", 10,"bold")
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)
class HomePage(tk.Frame):

    L2 = None
    window = None
    controller = None
    popup = None
    def __init__(self, parent, cntrlr):
         
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(cntrlr, "Home")
        HomePage.window = self
        HomePage.controller = cntrlr
        stvar = tk.StringVar()
        stvar1 = tk.StringVar()
        
        searchButton = tk.Button(self, text="Search",command = lambda:HomePage.controller.show_page("SearchPage"))
        searchButton.grid(row=0,column=0)
        homeButton = tk.Button(self, text="Home",command = lambda:HomePage.controller.show_page("HomePage"))
        homeButton.grid(row=0,column=1)
        myProfileButton = tk.Button(self, text="My Profile",command = lambda:HomePage.show_profile(connection.uid))
        myProfileButton.grid(row=0,column=2)
        rButton = tk.Button(self, text="Friend Recom.",command = lambda:HomePage.controller.show_page("RecommendationPage"))
        rButton.grid(row=0,column=4)
        r2Button = tk.Button(self, text="Movie Recom.",command = lambda:HomePage.controller.show_page("MovieRecommendationPage"))
        r2Button.grid(row=1,column=4)
        addButton2 = tk.Button(self, text="Add New Movie/Tv Show",command = lambda: HomePage.controller.show_page("NewMovie"))
        addButton2.grid(row=2,column=4)
        settingButton = tk.Button(self, text="Settings",command =lambda: HomePage.controller.show_page("SettingsPage"))
        settingButton.grid(row=0,column=3)        
        signoutButton = tk.Button(self, text="Sign Out",command = lambda: HomePage.controller.show_page("StartPage"))
        signoutButton.grid(row=0,column=6)
		
        r=2
        c=0
        query = "Match (node:News) Return node.title as title,node.content as content Order by node.date DESC limit 5"
        news = connection.g.run(query)
        n = tk.Label(self, text = 'Top News:',anchor='center',font=LARGE_FONT,borderwidth=2, relief="groove",height=3, width=25)
        n.grid(row=1,column=0)
        for n in news:
			txt = str(n['title']) + '\n' + str(n['content'])
			l = tk.Label(self, text = txt,borderwidth=2, relief="groove",height=3, width=25)
			l.grid(row=r,column=c)
			r = r+1
			
        r=2
        c=1
        query = "Match (node:Movie) Return node.title as title,node.rating as rating,id(node) as id Order by node.rating DESC"
        media = connection.g.run(query)
        l2 = tk.Label(self, text = 'Top 5 Highest Rated Movies:',anchor='center',font=LARGE_FONT,borderwidth=2, relief="groove",height=3, width=25)
        l2.grid(row=1,column=1)
        for m in media:
			txt = str(m['title']) + ' Rating =' + str(m['rating'])
			b =  tk.Button(self, text = txt,height=3, width=25,command = lambda m=m:HomePage.show_movie(m['id']))
			b.grid(row=r,column=c)
			r = r+1
			
        r=2
        c=2
        query = "Match (node:Tv_Show) Return node.title as title,node.rating as rating,id(node) as id Order by node.rating DESC"
        media = connection.g.run(query)
        l3 = tk.Label(self, text = 'Top 5 Highest Rated Tv Shows:',anchor='center',font=LARGE_FONT,borderwidth=2, relief="groove",height=3, width=25)
        l3.grid(row=1,column=2)
        for m in media:
			txt = str(m['title']) + ' Rating =' + str(m['rating'])
			b =  tk.Button(self, text = txt,height=3, width=25,command = lambda m=m:HomePage.show_movie(m['id']))
			b.grid(row=r,column=c)
			r = r+1
			
        r=2
        c=3
        query = "Match (node:Movie) Return node.title as title,node.year as year,id(node) as id Order by node.year DESC"
        media = connection.g.run(query)
        l4 = tk.Label(self, text = 'Top 5 Newest Movies:',anchor='center',font=LARGE_FONT,borderwidth=2, relief="groove",height=3, width=25)
        l4.grid(row=1,column=3)
        for m in media:
			txt = str(m['title']) + ' Year =' + str(m['year'])
			b =  tk.Button(self, text = txt,height=3, width=25,command = lambda m=m:HomePage.show_movie(m['id']))
			b.grid(row=r,column=c)
			r = r+1
		
    @staticmethod   
    def show_profile(id):
		connection.pid = id
		HomePage.controller.show_page("ProfilePage")
		
    @staticmethod   
    def show_movie(id):
		connection.movie = id
		HomePage.controller.show_page("MediaPage")
		