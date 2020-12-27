import Tkinter as tk
import connection  
import time
from py2neo import Graph,Node,NodeSelector,Relationship


LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

class EditMovie(tk.Frame):

    L2 = None
    window = None
    controller = None
    popup = None
	
    def __init__(self, parent, cntrlr):
         
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(cntrlr, "Edit")
        EditMovie.window = self
        EditMovie.controller = cntrlr

        button = tk.Button(self, text="Home",command = lambda: EditMovie.show_home())
        button.grid(row=0,column=4)	
		
        addButton = tk.Button(self, text="Add New Person",command = lambda: EditMovie.new_person_window())
        addButton.grid(row=6,column=4)
		
        addButton1 = tk.Button(self, text="Add New Genre",command = lambda: EditMovie.new_window('Genre'))
        addButton1.grid(row=6,column=5)
		
        addButton2 = tk.Button(self, text="Add New Keyword",command = lambda: EditMovie.new_window('Keyword'))
        addButton2.grid(row=6,column=6)
		
        signoutButton = tk.Button(self, text="Sign Out",command = lambda: EditMovie.controller.show_page("StartPage"))
        signoutButton.grid(row=0,column=5)
		
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
		
        query = "Match (node:Person) Return node.name as name,ID(node) as id"
        persons = connection.g.run(query)
        personDict = {}
        for p in persons:
			personDict[p['name']]=p['id']
		
        query = "Match (node:Genre) Return node.name as name,ID(node) as id"
        genres = connection.g.run(query)
        genreDict= {}
        for g in genres:
			genreDict[g['name']]=g['id']
			
        query = "Match (node:Keyword) Return node.name as name,ID(node) as id"
        keys = connection.g.run(query)
        keyDict = {}
        for k in keys:
			keyDict[k['name']]=k['id']
			
        stvar = tk.StringVar(self)
        stvar1 = tk.StringVar()
        stvar2 = tk.StringVar(self)
        stvar3 = tk.StringVar(self)
        stvar4 = tk.StringVar(self)
        stvar5 = tk.StringVar(self)
		
        l = tk.Label(self, text ="Actor")
        l.grid(row=2,column=0)
        actor = tk.OptionMenu(self,stvar, *personDict.keys())
        actor.grid(row=2,column=1)
        role= tk.Entry(self,textvariable=stvar1)
        role.grid(row=2,column=2)
        actoradd = tk.Button(self, text="add",command = lambda:EditMovie.add_relation(connection.movie,personDict[stvar.get()],'ACTED_IN',3,role.get()))
        actoradd.grid(row=2,column=3)	
		
        l1 = tk.Label(self, text ="Crew")
        l1.grid(row=3,column=0)
        crew = tk.OptionMenu(self,stvar2, *personDict.keys())
        crew.grid(row=3,column=1)
        crole= tk.OptionMenu(self,stvar3,"WRITER_OF","PRODUCED","DIRECTED_IN")
        crole.grid(row=3,column=2)
        crewadd = tk.Button(self, text="add",command = lambda:EditMovie.add_relation(connection.movie,personDict[stvar2.get()],stvar3.get(),2,''))
        crewadd.grid(row=3,column=3)
		
        l2 = tk.Label(self, text ="Genre")
        l2.grid(row=4,column=0)
        genre = tk.OptionMenu(self,stvar4, *genreDict)
        genre.grid(row=4,column=1)
        genreadd = tk.Button(self, text="add",command = lambda:EditMovie.add_relation(connection.movie,genreDict[stvar4.get()],'HAS_GENRE',1,''))
        genreadd.grid(row=4,column=3)
		
        l3 = tk.Label(self, text ="Keyword")
        l3.grid(row=5,column=0)
        keyword = tk.OptionMenu(self,stvar5, *keyDict)
        keyword.grid(row=5,column=1)
        keyadd = tk.Button(self, text="add",command = lambda:EditMovie.add_relation(connection.movie,keyDict[stvar5.get()],'HAS_KEYWORD',1,''))
        keyadd.grid(row=5,column=3)

    @staticmethod	
    def show_home():
		if connection.userType=='admin':
			EditMovie.controller.show_page("AdminPage")
		else :
			EditMovie.controller.show_page("HomePage")

	
 
    @staticmethod	
    def new_window(type):
	    EditMovie.popup = tk.Tk()
	    EditMovie.popup.wm_title("Add New Genre/Keyword")
	    stvar = tk.StringVar()
		
	    l = tk.Label(EditMovie.popup, text ="Name")
	    l.grid(row=0,column=0)
	    name = tk.Entry(EditMovie.popup, textvariable=stvar)
	    name.grid(row=0,column=1)		
		
	    add = tk.Button(EditMovie.popup, text="Add",command = lambda : EditMovie.new_gk(name.get(),type))
	    add.grid(row = 4,column = 1)			
	    EditMovie.popup.mainloop()
		
    @staticmethod	
    def new_gk(n,type):
		selector = NodeSelector(connection.g)
		node = selector.select(type,name=n)
		nodelist=list(node)
		if len(nodelist) >1:
			EditMovie.popupmsg("Input already exists!")
		else:
			query = "CREATE (a:"+type+"{name:'"+str(n)+"'})"
			connection.g.run(query)
			#EditMovie.popupmsg("done!")
			time.sleep(5)
			EditMovie.controller.show_page("EditMovie")
			
    @staticmethod	
    def new_person_window():
	    EditMovie.popup = tk.Tk()
	    EditMovie.popup.wm_title("Add New Person")
	    stvar = tk.StringVar()
	    stvar1 = tk.StringVar()
		
	    l = tk.Label(EditMovie.popup, text ="Name")
	    l.grid(row=0,column=0)
	    name = tk.Entry(EditMovie.popup, textvariable=stvar)
	    name.grid(row=0,column=1)
		
	    l1 = tk.Label(EditMovie.popup, text ="Birth Year")
	    l1.grid(row=1,column=0)
	    year = tk.Entry(EditMovie.popup, textvariable=stvar1)
	    year.grid(row=1,column=1)		
		
	    add = tk.Button(EditMovie.popup, text="Add",command = lambda : EditMovie.new_person(name.get(),year.get()))
	    add.grid(row = 4,column = 1)			
	    EditMovie.popup.mainloop()
		
    @staticmethod	
    def new_person(n,y):
		selector = NodeSelector(connection.g)
		node = selector.select("Person",name=n,born=y)
		nodelist=list(node)
		if len(nodelist) >1:
			EditMovie.popupmsg("Person exists!")
		else:
			query = "CREATE (a:Person{name:'"+str(n)+"', born:'"+str(y)+"'})"
			connection.g.run(query)
			time.sleep(5)
			EditMovie.controller.show_page("EditMovie")
		
		
    @staticmethod
    def add_relation(mid,fid,rname,rtype,role):#genre/keyword = 1  actor=3  other = 2
		n1 = connection.g.node(mid)
		n2 = connection.g.node(fid)
		if rtype==1:
			new_relationship = Relationship(n1,rname, n2)
		else:
			new_relationship = Relationship(n2,rname, n1)			
		connection.g.create(new_relationship)
		if rtype==3:
			new_relationship['role']=role
			new_relationship.push()
		EditMovie.controller.show_page("EditMovie")
		
    @staticmethod
    def popupmsg(msg):
		popup = tk.Tk()
		popup.wm_title("!")
		label = tk.Label(popup, text=msg, font=LARGE_FONT)
		label.pack()
		B1 = tk.Button(popup, text="Okay", command = popup.destroy)
		B1.pack()
		popup.mainloop()
		