import Tkinter as tk
import connection  
import time
from py2neo import Graph,Node,NodeSelector,Relationship


LARGE_FONT= ("Verdana", 10,"bold")
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

class AdminPage(tk.Frame):

    L2 = None
    window = None
    controller = None
    popup = None
	
    def __init__(self, parent, cntrlr):
         
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(cntrlr, "Home")
        AdminPage.window = self
        AdminPage.controller = cntrlr

        addButton2 = tk.Button(self, text="Add New Movie/Tv Show",command = lambda: AdminPage.controller.show_page("NewMovie"))
        addButton2.grid(row=0,column=0)
		
        addButton4 = tk.Button(self, text="Add News",command = lambda: AdminPage.news_window())
        addButton4.grid(row=0,column=1)
 
        signoutButton = tk.Button(self, text="Sign Out",command = lambda: AdminPage.controller.show_page("StartPage"))
        signoutButton.grid(row=0,column=3)
		
        r=2
        c=0
        query = "Match (node:News) Return node.title as title,node.content as content Order by node.date DESC"
        news = connection.g.run(query)
        n = tk.Label(self, text = 'Top News:',anchor='center',font=LARGE_FONT,borderwidth=2, relief="groove",height=3, width=30)
        n.grid(row=1,column=0)
        for n in news:
			txt = str(n['title']) + '\n' + str(n['content'])
			l = tk.Label(self, text = txt,borderwidth=2, relief="groove",height=3, width=30)
			l.grid(row=r,column=c)
			r = r+1
        r=2
        c=1
        query = "Match (node:Movie) Return node.title as name limit 5"
        media = connection.g.run(query)
        l2 = tk.Label(self, text = 'Movies:',anchor='center',font=LARGE_FONT,borderwidth=2, relief="groove",height=3, width=25)
        l2.grid(row=1,column=1)
        for m in media:
			l = tk.Label(self, text = m['name'],borderwidth=2, relief="groove",height=3, width=30)
			l.grid(row=r,column=c)
			r = r+1
			
        r=2
        c=2
        query = "Match (node:Tv_Show) Return node.title as name limit 5"
        media = connection.g.run(query)
        l3 = tk.Label(self, text = 'Tv Shows:',anchor='center',font=LARGE_FONT,borderwidth=2, relief="groove",height=3, width=25)
        l3.grid(row=1,column=2)
        for m in media:
			l = tk.Label(self, text = m['name'],borderwidth=2, relief="groove",height=3, width=30)
			l.grid(row=r,column=c)
			r = r+1
			  
	
    @staticmethod
    def news_window():
		AdminPage.popup = tk.Tk()
		AdminPage.popup.wm_title("Add News")
		stvar = tk.StringVar()
		stvar1 = tk.StringVar()
		l = tk.Label(AdminPage.popup, text ="Title")
		l.grid(row=0,column=0)
		title = tk.Entry(AdminPage.popup, textvariable=stvar)
		title.grid(row=0,column=1)
		
		l2 = tk.Label(AdminPage.popup, text ="Content")
		l2.grid(row=0,column=2)
		content = tk.Entry(AdminPage.popup, textvariable=stvar1)
		content.grid(row=0,column=3)
		
		add = tk.Button(AdminPage.popup, text="Add" ,command = lambda :AdminPage.add_news(title.get(),content.get()))
		add.grid(row = 1,column = 2)			
		
		AdminPage.popup.mainloop()
		
		
    @staticmethod
    def add_news(t,c):
		news = Node("News",title=t)
		admin = connection.g.node(connection.uid)
		admin_add_news = Relationship(admin, "ADDS", news)
		connection.g.create(admin_add_news)
		news["content"] = c
		news["date"] = time.time()
		news.push()
		AdminPage.controller.show_page("AdminPage")
		
    @staticmethod
    def popupmsg(msg):
		popup = tk.Tk()
		popup.wm_title("!")
		label = tk.Label(popup, text=msg, font=LARGE_FONT)
		label.pack()
		B1 = tk.Button(popup, text="Okay", command = popup.destroy)
		B1.pack()
		popup.mainloop()
		