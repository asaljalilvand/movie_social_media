import Tkinter as tk
import connection  
from py2neo import Graph,Node,NodeSelector,Relationship

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)
class SettingsPage(tk.Frame):


    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(controller, "Settings")
		
        stvar = tk.StringVar()
        stvar1 = tk.StringVar(self)
        stvar2 = tk.StringVar()
        stvar3 = tk.StringVar(self)
        stvar4 = tk.StringVar()
        
		
        homeButton = tk.Button(self, text="Home",command = lambda:controller.show_page("HomePage"))
        homeButton.grid(row=0,column=3)
		 		
        signoutButton = tk.Button(self, text="Sign Out",command = lambda: controller.show_page("StartPage"))
        signoutButton.grid(row=0,column=4)
		
        L4 = tk.Label(self, text="Username")
        L4.grid(row=1,column=0)
        username1 = tk.Entry(self, textvariable=stvar)
        username1.grid(row=1,column=1)
		
        L5 = tk.Label(self, text="Sexuality")
        L5.grid(row=2,column=0)
        sex = tk.OptionMenu(self,stvar1,"Female","Male")
        sex.grid(row=2,column=1)
		
        L6 = tk.Label(self, text="Age")
        L6.grid(row=3,column=0)
        age = tk.Entry(self, textvariable=stvar2)
        age.grid(row=3,column=1)
		
        L7 = tk.Label(self, text="Education")
        L7.grid(row=2,column=2)
        edu = tk.OptionMenu(self,stvar3,"B.A.","M.A.","PHD")
        edu.grid(row=2,column=3)
		
        L8 = tk.Label(self, text="Password")
        L8.grid(row=4,column=0)
        password1 = tk.Entry(self, textvariable=stvar4,show="*")
        password1.grid(row=4,column=1)
		
      
        button2 = tk.Button(self, text="Save",command = lambda: save(username1.get(), password1.get(),stvar1.get(),age.get(),stvar3.get()))
        button2.grid(row=5,column=2)
		
		
	def save(name,password,sex,age,edu):
		user = connection.g.node(connection.uid)
		if name != '':
			user["name"] = name
			user.push()
		if password != '':
			user["password"] = password
			user.push()
		if sex != '':
			user["sex"] = sex
			user.push()
		if age != '':
			user["age"] = age
			user.push()
		if edu != '':
			user["edu"] = edu
			user.push()	
		
		return None

		
