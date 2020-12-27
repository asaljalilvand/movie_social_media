import Tkinter as tk
import connection  
from py2neo import Graph,Node,NodeSelector,Relationship

class MovieRecommendationPage(tk.Frame):

    controller = None
    def __init__(self, parent, c):
         
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(c, "Movie Recommendation")
        stvar = tk.StringVar()
        MovieRecommendationPage.controller = c
        searchButton = tk.Button(self, text="Search",command = lambda:MovieRecommendationPage.controller.show_page("SearchPage"))
        searchButton.grid(row=0,column=2)
        homeButton = tk.Button(self, text="Home",command = lambda:MovieRecommendationPage.controller.show_page("HomePage"))
        homeButton.grid(row=0,column=3)
        myProfileButton = tk.Button(self, text="My Profile",command = lambda:MovieRecommendationPage.show_profile(connection.uid))
        myProfileButton.grid(row=0,column=4)
        signoutButton = tk.Button(self, text="Sign Out",command = lambda: MovieRecommendationPage.controller.show_page("StartPage"))
        signoutButton.grid(row=0,column=5)
		
		
        recomlist = {}		
		#movies with genres similar to user's taste
        query = "match (user:User)-[:LIKES]->(m),(m)-[:HAS_GENRE]->(g:Genre),(rm)-[:HAS_GENRE]->(g:Genre) where id(user) = "+str(connection.uid)+" return distinct id(rm) as id,rm.title as name"
        movies = connection.g.run(query)	
        for m in movies:
			recomlist[m['id']] = m['name'] 
		#based  on movies/shows liked with same rating
        query = "match (user1:User)-[r1:LIKES]->(m)<-[r2:LIKES]-(user2:User),(user2:User)-[r3:LIKES]->(rm) where id(user1)="+str(connection.uid)+" and id(user2)<>"+str(connection.uid)+" and r1.rating = r2.rating and r3.rating='5' return distinct id(rm) as id,rm.title as name"
        similar = connection.g.run(query)
        for s in similar:
			recomlist[s['id']] = s['name'] 
		#based on personal information
        query = "match (user1:User),(user2:User)-[:LIKES]->(m) where id(user1) = "+str(connection.uid)+" and user1.sex = user2.sex and user1.edu = user2.edu and user1.age = user2.age return distinct id(m) as id,m.title as name"
        movies = connection.g.run(query)	
        for m in movies:
			recomlist[m['id']] = m['name']				
		#remove movies which are already seen
        query = "match (user1:User)-[:LIKES]-(m) where id(user1)="+str(connection.uid)+" return distinct id(m) as id"
        seen = connection.g.run(query)	
        for s in seen:
			recomlist.pop(s['id'], None)
		
        r = 1
        for key, value in recomlist.iteritems():	
			b = tk.Button(self, text=value,height=3, width=20, anchor="w",command = lambda key=key:MovieRecommendationPage.show_movie(key))
			b.grid(row=r,column=1)
			r = r+1
        
		
    @staticmethod   
    def show_movie(id):
		connection.movie = id
		MovieRecommendationPage.controller.show_page("MediaPage")
