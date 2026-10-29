import sqlite3
import customtkinter as ctk
import time
from CTkTable import CTkTable as ctkT

class daten_sql():

    def __init__(self):

        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()
        cursor.execute(
            """
            select 
            g.name as "Genre", 
            count(distinct t.AlbumId) as "Anzahl Alben", 
            count(distinct ar.ArtistId) as "Anzahl Künstler",
            count(il.invoicelineid) as "Anzahl Verkäufe",
            concat(coalesce(round(avg(il.UnitPrice),2),0),"$") as "Ø Preis"
            from Genre g
            left join Track t on t.GenreId = g.GenreId
            left join Album a on a.AlbumId = t.AlbumId
            left join Artist ar on ar.ArtistId = a.ArtistId
            left join InvoiceLine il on il.TrackId = t.TrackId
            group by g.Name
            order by "Anzahl Alben" desc;
            """
            )
        
        spaltennamen = [col[0] for col in cursor.description]
        daten = cursor.fetchall()
        daten.insert(0, spaltennamen)
        self.daten = daten

        conn.close()
    
class Frame(ctk.CTkScrollableFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        self.name = ctk.CTkLabel(self, text="Music Statistic tool | By Ilie", padx=10, pady=5)
        self.name.grid(row=0, column=0, sticky="w")

        self.daten = daten_sql()
        self.tabelle = ctkT(master=self, row=len(self.daten.daten), column=5, values=self.daten.daten)
        self.tabelle.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
    
        self.geometry("600x800")
        self.title("Music statistic tool")
        
        self.frame = Frame(master=self, width=600, height=800, corner_radius=0)
        self.frame.grid(row=0,column=0, sticky="nsew")
        self.grid_columnconfigure(0,weight=1)
        
        

app = App()
app.mainloop()
