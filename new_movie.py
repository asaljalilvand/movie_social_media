import Tkinter as tk
import connection  

class NewMovie(tk.Frame):

    L2 = None
    window = None
    controller = None
    popup = None
    def __init__(self, parent, cntrlr):
        
        tk.Frame.__init__(self,parent)
        tk.Tk.wm_title(cntrlr, "New Movie/Tv Show")
        NewMovie.controller = cntrlr
        stvar = tk.StringVar(self)
        stvar1 = tk.StringVar()
        stvar2 = tk.StringVar()
        stvar3 = tk.StringVar()
        stvar4 = tk.StringVar()
        stvar5 = tk.StringVar()		
		
        l = tk.Label(self, text ="Type")
        l.grid(row=0,column=0)
        type = tk.OptionMenu(self,stvar,"Movie","Tv_Show")
        type.grid(row=0,column=1)
		
        l1 = tk.Label(self, text ="title")
        l1.grid(row=1,column=0)
        title = tk.Entry(self,textvariable=stvar1)
        title.grid(row=1,column=1)
		
        l2 = tk.Label(self, text ="tagline")
        l2.grid(row=2,column=0)
        tagline = tk.Entry(self,textvariable=stvar2)
        tagline.grid(row=2,column=1)
		
        l3 = tk.Label(self, text ="summary")
        l3.grid(row=3,column=0)
        summary = tk.Entry(self,textvariable=stvar3)
        summary.grid(row=3,column=1)
		
        l4 = tk.Label(self, text ="duration")
        l4.grid(row=4,column=0)
        duration = tk.Entry(self,textvariable=stvar4)
        duration.grid(row=4,column=1)		
		
        l6 = tk.Label(self, text ="Year")
        l6.grid(row=5,column=0)
        year = tk.Entry(self,textvariable=stvar5)
        year.grid(row=5,column=1)		
		
        add = tk.Button(self, text="Next",command = lambda : NewMovie.new(stvar.get(),title.get(),tagline.get(),summary.get(),duration.get(),year.get()))
        add.grid(row = 7,column = 1)
        

    @staticmethod	
    def new(type,title,tagline,summary,duration,year):
		query = "CREATE (a:"+str(type)+"{title:'"+str(title)+"', tagline:'"+str(tagline)+"', summary:'"+str(summary)+"', duration:'"+str(duration)+"', year:'"+str(year)+"',rating:0,likes:0}) return ID(a) as id"
		result  = connection.g.run(query)
		for r in result:
			connection.movie = r['id']
		connection.mediaType = type
		NewMovie.controller.show_page("EditMovie")

		