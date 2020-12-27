import Tkinter as tk
import connection  


LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

class SearchPage(tk.Frame):

    L2 = None
    window = None
    controller = None
    popup = None
    def __init__(self, parent, cntrlr):
         
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(cntrlr, "Search")
        SearchPage.window = self
        SearchPage.controller = cntrlr

        homeButton = tk.Button(self, text="Home",command = lambda:SearchPage.controller.show_page("HomePage"))
        homeButton.grid(row=0,column=3)
        myProfileButton = tk.Button(self, text="My Profile",command = lambda:SearchPage.show_profile(connection.uid))
        myProfileButton.grid(row=0,column=4)
        settingButton = tk.Button(self, text="Settings",command =lambda: SearchPage.controller.show_page("SettingsPage"))
        settingButton.grid(row=0,column=5)
        signoutButton = tk.Button(self, text="Sign Out",command = lambda: SearchPage.controller.show_page("StartPage"))
        signoutButton.grid(row=0,column=6)
		
        stvar = tk.StringVar()
        stvar1 = tk.StringVar()
        stvar2 = tk.StringVar()
        stvar3 = tk.StringVar()
        stvar4 = tk.StringVar()
        stvar5 = tk.StringVar()		
		
        l = tk.Label(self, text ="title")
        l.grid(row=1,column=0)
        title = tk.Entry(self,textvariable=stvar)
        title.grid(row=1,column=1)
		
        l1 = tk.Label(self, text ="year")
        l1.grid(row=1,column=3)
        year = tk.Entry(self,textvariable=stvar1)
        year.grid(row=1,column=4)
		
        l2 = tk.Label(self, text ="genre")
        l2.grid(row=2,column=0)
        genre = tk.Entry(self,textvariable=stvar2)
        genre.grid(row=2,column=1)
		
        l3 = tk.Label(self, text ="actor")
        l3.grid(row=2,column=3)
        actor = tk.Entry(self,textvariable=stvar3)
        actor.grid(row=2,column=4)
		
        l4 = tk.Label(self, text ="director")
        l4.grid(row=3,column=0)
        director = tk.Entry(self,textvariable=stvar4)
        director.grid(row=3,column=1)		
		
        l6 = tk.Label(self, text ="writer")
        l6.grid(row=3,column=3)
        writer = tk.Entry(self,textvariable=stvar5)
        writer.grid(row=3,column=4)		
		
        add = tk.Button(self, text="Search",command = lambda : SearchPage.search(title.get(),year.get(),genre.get(),actor.get(),director.get(),writer.get()))
        add.grid(row = 7,column = 1)
		

    @staticmethod   
    def show_profile(id):
		connection.pid = id
		SearchPage.controller.show_page("ProfilePage")
		
    @staticmethod
    def search(title,year,genre,actor,director,writer):
		properties = '{'
		query='MATCH (m'
		relationships=[]
		where=[]
		if title!='':
			properties=properties+'title:"'+title+'"'
		if year!='':
			if title!='':
				properties=properties+','
			properties=properties+'year:"'+year+'"'
			
		if properties!='{':
			query=query+properties+'}'
		query=query+")"
						
		if genre!='':
			relationships.append('(m)-[:HAS_GENRE]->(genre:Genre)')
			where.append("genre.name='"+genre+"'")
			
		if actor!='':
			relationships.append('(m)<-[:ACTED_IN]-(actor:Person)')
			where.append("actor.name='"+actor+"'")
			
		if director!='':
			relationships.append('(m)<-[:DIRECTED_IN]-(director:Person)')
			where.append("director.name='"+director+"'")
			
		if writer!='':
			relationships.append('(m)<-[:WRITER_OF]-(writer:Person)')
			where.append("writer.name='"+writer+"'")
			
		if len(relationships)!=0:
			query=query+','
		last = len(relationships)-1
		for idx, val in enumerate(relationships):
			query=query+val
			if idx != last:
				query=query+','
			else :
				query=query+' where '
				
		for idx, val in enumerate(where):
			query=query+val
			if idx != last:
				query=query+' and '

		query=query+' return m.title as name,id(m) as id'
		connection.searchRes = connection.g.run(query)
		SearchPage.controller.show_page("ResultPage")




















	
		
		
		
		
		
		
		
		