import Tkinter as tk
import connection  
from py2neo import Graph,Node,NodeSelector,Relationship
class FollowPage(tk.Frame):

    controller = None
    def __init__(self, parent, c):
         
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(c, "Friends")
        stvar = tk.StringVar()
        FollowPage.controller = c
        searchButton = tk.Button(self, text="Search",command = lambda:FollowPage.controller.show_page("SearchPage"))
        searchButton.grid(row=0,column=2)
        homeButton = tk.Button(self, text="Home",command = lambda:FollowPage.controller.show_page("HomePage"))
        homeButton.grid(row=0,column=3)
        myProfileButton = tk.Button(self, text="My Profile",command = lambda:FollowPage.show_profile(connection.uid))
        myProfileButton.grid(row=0,column=4)
        signoutButton = tk.Button(self, text="Sign Out",command = lambda: FollowPage.controller.show_page("StartPage"))
        signoutButton.grid(row=0,column=5)
		
        query = "MATCH (you)-[:FRIEND]-(yourFriends) where id(you)="+str(connection.pid)+" RETURN id(yourFriends) as id, yourFriends.name as name"
        friends = connection.g.run(query)			
        r = 1
        for f in friends:						
			b = tk.Button(self, text=f['name'],height=3, width=20, anchor="w",command = lambda f=f:FollowPage.show_profile(f['id']))
			b.grid(row=r,column=1)
			r = r+1
        
		
    @staticmethod	
    def show_profile(id):
		connection.pid = id
		FollowPage.controller.show_page("ProfilePage")
