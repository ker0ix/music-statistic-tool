import sqlite3
import customtkinter as ctk
import random
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
            order by "Ø Preis" desc;
            """
            )
        
        spaltennamen = [col[0] for col in cursor.description]
        daten = cursor.fetchall()
        daten.insert(0, spaltennamen)
        self.daten = daten # daten speichern in "rucksack"
        conn.close()
    
class Frame(ctk.CTkScrollableFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        design_paletten = [
            {
                "header_color": "#4c1d95",
                "colors": ["#0f172a", "#1e1b4b"],
                "hover_color": "#3b0764",
                "border_color": "#312e81"
            },
            {
                "header_color": "#1f2937",
                "colors": ["#111827", "#1a2234"],
                "hover_color": "#374151",
                "border_color": "#374151"
            },
            {
                "header_color": "#262626",
                "colors": ["#171717", "#212121"],
                "hover_color": "#2f2f2f",
                "border_color": "#404040"
            }
        ]
        #bei jedem start wird zuffälig ausgewählt welches design benutzt wird
        design = random.choice(design_paletten)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        self.name = ctk.CTkLabel(self, text="Music Statistic tool | By Ilie", padx=10, pady=5)
        self.name.grid(row=0, column=0, sticky="w")

        self.daten = daten_sql()

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
        #TODO: Wenn man ganz oben den Spalten namen anclickt, soll es einen sql befehl ausführen, wie z.b. "ORDER BY ANZAHL VERKÄUFE DESC;"
        
        self.tabelle.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")


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