import sqlite3
import customtkinter as ctk
import random
from CTkTable import CTkTable as ctkT

class daten_sql():
    def __init__(self, sortierung):

        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()
        
        query = f"""
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
                order by "{sortierung}" desc;
                """

        cursor.execute(query)
        
        spaltennamen = [col[0] for col in cursor.description]
        daten = cursor.fetchall()

        self.spalten = spaltennamen # spaltennamen speichern
        self.daten = daten # daten speichern in "rucksack"
        conn.close()

class Frame(ctk.CTkScrollableFrame): 
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        design_paletten = [
            {"header_color": "#4c1d95","colors": ["#0f172a", "#1e1b4b"],"hover_color": "#3b0764","border_color": "#312e81"},
            {"header_color": "#1f2937","colors": ["#111827", "#1a2234"],"hover_color": "#374151","border_color": "#374151"},
            {"header_color": "#262626","colors": ["#171717", "#212121"],"hover_color": "#2f2f2f","border_color": "#404040"}
        ]

        #bei jedem start wird zuffälig ausgewählt welche Farbpalette benutzt wird
        design = random.choice(design_paletten)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure((0,1,2),weight=1)

        self.name = ctk.CTkLabel(self, text="Music Statistic tool | By Ilie", padx=10, pady=5)
        self.name.grid(row=0, column=0, sticky="w")

        self.daten = daten_sql("Anzahl Verkäufe")

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(column=0, row=1, sticky="ew", padx=5)
        

        self.spalten = daten_sql("Anzahl Verkäufe")

        for i, spalte in enumerate(self.spalten.spalten):
            self.header_frame.grid_columnconfigure(i, weight=1)
            btn = ctk.CTkButton(
                self.header_frame,
                text=spalte,
                fg_color=design["header_color"],
                hover_color=design["hover_color"],
                corner_radius=4,
                command= lambda s=spalte: self.sortierung(s)
            )
            btn.grid(column=i,row=1)
        
        self.tabelle = ctkT(master=self, 
        row=len(self.daten.daten), 
        column=5, 
        values=self.daten.daten, 
        border_width=3,
        corner_radius=6, 
        font=("Arial", 12), 
        padx=0,
        pady=0,
        **design
        )
        self.tabelle.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

    def sortierung(self, spaltenname):
        neue_daten = daten_sql(sortierung=spaltenname)
        self.daten = neue_daten.daten
        self.tabelle.update_values(self.daten)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
    
        self.geometry("600x500")
        self.title("Music statistic tool")
        
        #Vergrößern in x & y richtung
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.frame = Frame(master=self, width=600, height=800, corner_radius=0)
        self.frame.grid(row=0,column=0, sticky="nsew")

app = App()
app.mainloop()