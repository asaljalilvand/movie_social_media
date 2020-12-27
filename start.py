from py2neo import Graph,Node,NodeSelector
import Tkinter as tk
import connection  
from administrator import *
from new_movie import *
from edit_movie import *
from userhome import *
from setting import *
from profile import *
from friendlist import *
from media import *
from recommendation import *
from mr import *
from search import *
from searchlist import *

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

class PagePool(tk.Tk):

    container = None
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        PagePool.container = tk.Frame(self)

        PagePool.container.pack(side="top", fill="both", expand = True)

        PagePool.container.grid_rowconfigure(0, weight=1)
        PagePool.container.grid_columnconfigure(0, weight=1)
        self.show_page("StartPage")


    def show_page(self, page_name):
        frame = None
        if page_name == 'StartPage':
        	frame = StartPage(PagePool.container, self)  
        if page_name == 'AdminPage':
			frame = AdminPage(PagePool.container, self)
        if page_name == 'NewMovie':
			frame = NewMovie(PagePool.container, self)	
        if page_name == 'EditMovie':
			frame = EditMovie(PagePool.container, self)	
        if page_name == 'HomePage':
			frame = HomePage(PagePool.container, self)	
        if page_name == 'SettingsPage':
			frame = SettingsPage(PagePool.container, self)
        if page_name == 'ProfilePage':
			frame = ProfilePage(PagePool.container, self)	
        if page_name == 'FollowPage':
			frame = FollowPage(PagePool.container, self)	
        if page_name == 'MediaPage':
			frame = MediaPage(PagePool.container, self)	
        if page_name == 'SearchPage':
			frame = SearchPage(PagePool.container, self)		
        if page_name == 'ResultPage':
			frame = ResultPage(PagePool.container, self)				
        if page_name == 'RecommendationPage':
			frame = RecommendationPage(PagePool.container, self)
        if page_name == 'MovieRecommendationPage':
			frame = MovieRecommendationPage(PagePool.container, self)			
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        return
        
class StartPage(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(controller, "Movies")
        
        stvar = tk.StringVar()
        stvar1 = tk.StringVar()
        stvar2 = tk.StringVar()
        stvar3= tk.StringVar(self)
        stvar4 = tk.StringVar()
        stvar5= tk.StringVar(self)
        stvar6= tk.StringVar()
		
        v = tk.StringVar()
        v.set("L") # initialize
		
        admin = tk.Radiobutton(self, text='Adminstrator',variable=v, value='Admin')
        admin.grid(row=0,column=1)
        user = tk.Radiobutton(self, text='User',variable=v, value='User')
        user.grid(row=0,column=2)
	
        L1 = tk.Label(self, text="Username")
        L1.grid(row=1,column=0)
        username = tk.Entry(self, textvariable=stvar)
        username.grid(row=1,column=1)
		
        L2 = tk.Label(self, text="Password")
        L2.grid(row=2,column=0)
        password = tk.Entry(self, textvariable=stvar1,show="*")
        password.grid(row=2,column=1)
		
        button = tk.Button(self, text="Log In",command = lambda:login(v.get(),username.get(),password.get()))
        button.grid(row=3,column=2)
		
        L3 = tk.Label(self, text="Sign Up")
        L3.grid(row=4,column=1)
		
        L4 = tk.Label(self, text="Username")
        L4.grid(row=5,column=0)
        username1 = tk.Entry(self, textvariable=stvar2)
        username1.grid(row=5,column=1)
		
        L5 = tk.Label(self, text="Sexuality")
        L5.grid(row=6,column=0)
        sex = tk.OptionMenu(self,stvar3,"Female","Male")
        sex.grid(row=6,column=1)
		
        L6 = tk.Label(self, text="Age")
        L6.grid(row=7,column=0)
        age = tk.Entry(self, textvariable=stvar6)
        age.grid(row=7,column=1)
		
        L7 = tk.Label(self, text="Education")
        L7.grid(row=6,column=2)
        edu = tk.OptionMenu(self,stvar5,"B.A.","M.A.","PHD")
        edu.grid(row=6,column=3)
		
        L8 = tk.Label(self, text="Password")
        L8.grid(row=8,column=0)
        password1 = tk.Entry(self, textvariable=stvar4,show="*")
        password1.grid(row=8,column=1)
      
        button2 = tk.Button(self, text="Sign Up",command = lambda: singup(username1.get(), password1.get(),stvar3.get(),age.get(),stvar5.get()))
        button2.grid(row=9,column=2)
		
	def popupmsg(msg):
		popup = tk.Tk()
		popup.wm_title("!")
		label = tk.Label(popup, text=msg, font=NORM_FONT)
		label.pack()
		B1 = tk.Button(popup, text="Okay", command = popup.destroy)
		B1.pack()
		popup.mainloop()

		
	def singup(username,password,sex,age,edu):
		selector = NodeSelector(connection.g)
		node = selector.select("User",name=username,password=password)
		nodelist=list(node)
		if len(nodelist) !=0:
			popupmsg("username already used ")
		else:
			query = "CREATE (a:User{name:'"+str(username)+"',sex:'"+str(sex)+"',edu:'"+str(edu)+"',age:'"+str(age)+"', password:'"+str(password)+"'}) return id(a) as id"
			result = connection.g.run(query)
			for r in result:					
				connection.uid = r['id']
			connection.userType = 'user'
			controller.show_page("HomePage")
	
				
	def login(lable,username,password):				
		query = "match (n:"+str(lable)+") where n.name='"+str(username)+"' and n.password='"+str(password)+"' return id(n) as id,n.name as name ,n.password as password"
		result = connection.g.run(query)		
		for r in result:	
			if r['name'] == username and r['password'] == password:				
				connection.uid = r['id']
				if lable=='Admin':
					connection.userType = 'admin'
					controller.show_page("AdminPage")
				else:
					connection.userType = 'user'
					controller.show_page("HomePage")
				return			
		popupmsg("username/password incorrect")
			


        


app = PagePool()
app.mainloop()