import Tkinter as tk
import connection  

class ResultPage(tk.Frame):

    controller = None
    def __init__(self, parent, c):
         
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(c, "Results")
        ResultPage.controller = c
        searchButton = tk.Button(self, text="Back",command = lambda:ResultPage.controller.show_page("SearchPage"))
        searchButton.grid(row=0,column=2)
					
        rw = 1
        flag = True
        for r in connection.searchRes:						
			b = tk.Button(self, text=r['name'],height=3, width=20, anchor="w",command = lambda r=r:ResultPage.show_movie(r['id']))
			b.grid(row=rw,column=1)
			rw = rw+1
			flag = False
        if flag==True:
			l = tk.Label(self, text ="No results found")
			l.grid(row=2,column=0)
        
		
    @staticmethod   
    def show_movie(id):
		connection.movie = id
		ResultPage.controller.show_page("MediaPage")
