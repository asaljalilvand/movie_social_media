import Tkinter as tk
import connection  
from py2neo import Graph,Node,NodeSelector,Relationship

class RecommendationPage(tk.Frame):

    controller = None
    def __init__(self, parent, c):
         
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(c, "Friend Recommendation")
        stvar = tk.StringVar()
        RecommendationPage.controller = c
        searchButton = tk.Button(self, text="Search",command = lambda:RecommendationPage.controller.show_page("SearchPage"))
        searchButton.grid(row=0,column=2)
        homeButton = tk.Button(self, text="Home",command = lambda:RecommendationPage.controller.show_page("HomePage"))
        homeButton.grid(row=0,column=3)
        myProfileButton = tk.Button(self, text="My Profile",command = lambda:RecommendationPage.show_profile(connection.uid))
        myProfileButton.grid(row=0,column=4)
        signoutButton = tk.Button(self, text="Sign Out",command = lambda: RecommendationPage.controller.show_page("StartPage"))
        signoutButton.grid(row=0,column=5)
		
		
        recomlist = {}		
		#at least 3 mutual friends
        query = "match (user1:User)-[r1:FRIEND]-(user2:User)-[r2:FRIEND]-(user3:User) WITH user1,count(user2) as mutual,user3 where id(user1)="+str(connection.uid)+" and id(user3)<>"+str(connection.uid)+" and  mutual>=3 return distinct user3.name as name,id(user3) as id"
        mutual = connection.g.run(query)	
        for m in mutual:
			recomlist[m['id']] = m['name'] 
		#based  on movies/shows liked with same rating
        query = "match (user1:User)-[r1:LIKES]->(m),(user2:User)-[r2:LIKES]->(m) where id(user1)="+str(connection.uid)+" and id(user2)<>"+str(connection.uid)+" and r1.rating = r2.rating return distinct user2.name as name,id(user2) as id"
        similar = connection.g.run(query)
        for s in similar:
			recomlist[s['id']] = s['name'] 
		#remove users who are already friends
        query = "match (user1:User)-[r1:FRIEND]-(user2:User) where id(user1)="+str(connection.uid)+" return distinct id(user2) as id"
        friends = connection.g.run(query)	
        for f in friends:
			recomlist.pop(f['id'], None)		
        r = 1
        for key, value in recomlist.iteritems():	
			b = tk.Button(self, text=value,height=3, width=20, anchor="w",command = lambda key=key:RecommendationPage.show_profile(key))
			b.grid(row=r,column=1)
			r = r+1
        
		
    @staticmethod	
    def show_profile(id):
		connection.pid = id
		RecommendationPage.controller.show_page("ProfilePage")
