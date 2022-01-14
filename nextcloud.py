
"""
Autor: Lizhong Tang
Datum: 08.10.2021
version: Pythhon 3.9.4
Funktionsbeschreibung:

Das Programm stellt einen komfortablen Log-Viewer für das Cloud-System Nextcloud dar.
In dem Programm stehen 3 Methoden zur Verfügung, um die gewünschte Log schnell zu finden. 
Für die Eingabe eines Schlüsselworts darf nicht weniger als 4 Buchstaben sein.
Es wird Dropdown-Menü nur für „user“, „time “ und „method“ erstellt.
Nur wenn Anzahl der Log mehr als 200 ist,wird drittes Dropdown-Menü erstellt und nach 3 Stichwörter gesucht.
Ansonsten bestehen 2 Dropdown-Menüs und wird nach 2 Schlüsselwörter gesucht.
Die Datenbank wird durch das Klicken des Button-Aktualisierungs aktualisiert.
Nach dem Klicken des Buttons wird Log in der Datenbank in Log-List gespeichert
"""




import re                                  
import sys                                      #Module
import pymysql
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from time import *
from tkinter import ttk
import gzip
import multiprocessing


#########################################################  Unterfunktion  ##########################################################

##################################################  Vollbild Menü und Funktion  ###################################################
def vorbereitung():
    global topmenu
    topmenu.add_command(label="Vollbild",command=vollbild)
    frame.destroy()
    fenster.resizable(1,1)           #Fenstergröße veränderbar
    
def vollbild():
    global topmenu
    topmenu.delete(index1="Vollbild",index2="Vollbild")
    fenster.attributes('-fullscreen', True)
    
###############################################################  Exit Menü  ##########################################################
def menue():
    global topmenu
    topmenu = Menu(fenster,bg="lightblue")
    topmenu.add_command(label="Exit",command = verlassen)
    fenster.config(menu=topmenu)
    
#########################################################  zurück auf die Hauptseite  ###########################################
def zurück_menu():
    global topmenu
    menu2 = Menu(topmenu,tearoff=0)
    topmenu.add_cascade(label="Zurück",menu = menu2)
    menu2.add_command(label="Hauptseite",image=foto,compound=LEFT,command=zurück)
    fenster.bind_all("<Control-b>", back)
    
def back(event):
    zurück()
    
def zurück():
    fenster.destroy()    
#####################################################################################################################################    

#####################################################  Vorbereitung für die Suche  #################################################   

def aktualisierung():
    #coupon_pool = multiprocessing.Pool(1)
    #coupon_pool.apply_async(data_pack())
    
    fun_a_process = multiprocessing.Process(target=data_pack)
    fun_a_process.start()
   

        
      
def suchen_aussehen():              #Eingabefeld & Suchfeld 
    global en,bt
    en = Entry(frame,width=73,highlightcolor='blue', highlightthickness=1)
    en.focus()
    en.icursor(0) 
    en.place(x=384,y=80,height=35)
    en.bind("<Return>", enter_suchen)
    en.bind("<Button-1>",ausgabe)            #Funktion der linken Maus
    Button(frame ,width=28,height=28,text="",image=foto_aktualisierung,bg="lightblue",activebackground="green",relief=RAISED,compound=LEFT,command=aktualisierung).place(x=900,y=81)
    Button(frame,text="Verlassen",width=10,height=1,bg="lightgreen",borderwidth=5,activebackground="green",relief=RAISED,command = verlassen).place(x=640,y=160)
    Button(frame ,width=64,height=26,text="Suchen",image=img2,bg="lightblue",activebackground="green",relief=RAISED,compound=LEFT,command=maus_suchen).place(x=828,y=81) 
    Button(frame ,text="Übersicht",bg="lightgreen",width=10,height=1, borderwidth=5,activebackground="green",relief=RAISED,command=button1).place(x=490,y=160)
    menue()
    

    
def func():                             #gewähltes Objekt im Listbox
    global eingabe2,listbox,com_list
    try: 
        first=listbox.curselection()[0]
        eingabe2=listbox.get(first)
        com_list.append(eingabe2)
    except:
        pass
    
 

def ausgabe(event):                                                           #assoziative Eingabe und Listbox
    global en,com,com_list,listbox,item_dict,var_listbox
    
    com_list = []
    log_list = []
    item_dict={"reqid":1,"level":2,"time":3,"remoteaddr":4,"user":5,"app":6,"method":7,"url":8,"message":9,"useragent":10,"version":11}
    for i in items:
        if i != "useragent":
            if en.get() == i[:len(en.get())]:
                en.delete(0, "end")
                en.insert(0, i)
                if var_listbox:
                    if en.get() == "user" or en.get() == "time" or en.get() == "method":
                        var_listbox = False
                        for item in log_data:
                            log_list.append(item[item_dict[en.get()]])
                        log_list=list(set(log_list))
                        listbox = Listbox(frame,width=85,yscrollcommand=sb_v.set,xscrollcommand=sb_h.set)
                        listbox.place(x=385,y=115)
                        sb_v.config(command=listbox.yview)
                        sb_h.config(command=listbox.xview)  
                        for item in log_list:
                            listbox.insert("end",item)
                else:
                    listbox.place_forget()          
                    var_listbox = True
                    
               
        if en.get() == items[-2][:len(en.get())] and len(en.get())>4:
            en.delete(0, "end")
            en.insert(0, items[-2])
        
    

        
def box(event):                                          #listbox
    global user_list,listbox,time_list,method_list,eingabe,drop_anzahl,var_listbox
    try:
        if var_listbox:
            var_listbox = False
            if en.get() != "":
                listbox = Listbox(fenster,width=73,yscrollcommand=sb_v.set,xscrollcommand=sb_h.set)
                listbox.place(x=385,y=115)
                sb_v.config(command=listbox.yview)
                sb_h.config(command=listbox.xview)
                if en.get() == "user" and eingabe == "user" or en.get() == "time" and eingabe == "time" or en.get() == "method"and eingabe == "method":
                    messagebox.showinfo(title="Info",message= "Sie haben sich gerage schon nach dem Schlüsselwort gesucht ")
                else:
                    if en.get() == "user":
                        for i in user_list:
                            listbox.insert("end",i)
                    if en.get() == "time":
                        for i in time_list:
                            listbox.insert("end",i)
                    if en.get() == "method":
                        for i in method_list:
                            listbox.insert("end",i)
            else:
                var_listbox = True
                messagebox.showinfo(title="Info",message= "Bitte geben Sie ein Schlüsselwort ein!!! ")
        
        else:
            listbox.place_forget()
            var_listbox = True
    except:
        pass
        
            
            

def enter_suchen(event):                    #Enter-Event
    maus_suchen()
    
 
def maus_suchen():                             #Link-Button-Event 
    global en,wort,com_list,eingabe2,dropdown,eingabe,dropdown_such_button,drop,var_listbox
    list=[]
    com_list = []
    var_listbox = True
    func()
    eingabe = en.get()
    if eingabe != "":
        if eingabe in items:
            if len(com_list) == 0:
                anzeige(eingabe)
                
            else:
                dropdown = True
                drop = True
                wort = 1
                list.append(eingabe)
                list.append(eingabe2)
                anzeige_inhalt(list)
                en = Entry(fenster,width=61,highlightcolor='blue', highlightthickness=1)     #zweites Dropdown_Menü
                en.focus()
                en.icursor(0) 
                en.place(x=386,y=80,height=35)
                en.bind("<Button-1>", box)
                messagebox.showinfo(title="Info",message= "Sie können nun nach einem Schlüsselwort weitersuchen ")
                dropdown_such_button=Button(fenster ,width=61,height=28,text="Suchen",image=img2,bg="lightblue",activebackground="green",relief=RAISED,compound=LEFT,command=dropdown_sql) 
                dropdown_such_button.place(x=758,y=79)
           
        else:
            if " " in eingabe and len(eingabe.split()) > 1:
                eingabe=eingabe.split()
                if eingabe[0] in items:
                    antwort=messagebox.askyesnocancel('Info','Ja      ------------------   unscharfe Suche\nNein ------------------   scharfe Suche\n')
                    if antwort:
                        wort = 1  #unscharfe Suche
                        anzeige_inhalt(eingabe)
                    elif antwort == False:
                        wort = 2  #scharfe Suche
                        anzeige_inhalt(eingabe)
                    else:
                        pass
                else:
                    wort = 0
                    anzeige_inhalt(eingabe[0]+" "+eingabe[1])
                    
            else:
                if len(eingabe) > 3:
                    wort = 0
                    anzeige_inhalt(eingabe)
                else:
                    messagebox.showinfo(title="Info",message= "mindestens 4 Buchstaben")
    else:  
        messagebox.showinfo(title="Info",message= "Bitte geben Sie Schlüsselwörter ein!!!")
        
####################################################################################################################################
        
######################################################  Suche und Anzeige der gesuchten Inhalte  ################################### 

    

def button1():                                  #Übersicht-Button 
    wahl=messagebox.askokcancel('Info', 'Möchten Sie alle wichtigen Info anschauen?')
    if wahl:
        vorbereitung()
        zurück_menu()
        text = Text(fenster,width=50, height=50,yscrollcommand=sb_v.set,xscrollcommand=sb_h.set,wrap = 'none')
        text.pack(expand = YES,fill = BOTH)
        sb_v.config(command=text.yview)
        sb_h.config(command=text.xview)
        text.insert("end", " "+"Nr"+"\t"+"IP"+"\t"+"\t"+"\t"+"ZEIT"+"\t"+"\t"+"\t"+
                    "USER"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"METHODE"+"\t"+"\t"+"URL"+
                    "\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"INFO"+'\n')
        i = 1
        for item in log_data:
            text.insert("end", " "+str(i)+"."+"\t"+item[4]+"\t"+"\t"+"\t"+item[3]+"\t"+"\t"+"\t"+
                    item[5]+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+item[7]+"\t"+"\t"+item[8]+
                    "\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+item[9]+'\n')
            i += 1
            
      
   
        
def funktion_anzeige():            #item weitersuchen (such_button)
    global wort,text,such_button,win
    
    try:
        button_inhalt_2 = text.get(SEL_FIRST,SEL_LAST)
        antwort=messagebox.askokcancel('Info', 'Möchten Sie unscharfe Suche?')
        if antwort:
            win = True       #unscharfe Suche
        else:
            win = False   
        such_button.pack_forget()
        text.pack_forget()
        wort = 4
        anzeige_inhalt(button_inhalt_2)
    except:
        messagebox.showinfo(title="Info",message= "nicht gewählt")
    
    
    
    
     
def anzeige_inhalt(objekt):                                    #Anzeige der gesuchten Inhalte       
    global wort,button_inhalt,win,drop_anzahl
    if wort != 3 and wort != 4:
        vorbereitung()
        zurück_menu()
        
    if wort == 0:              #ein Wort im volltext suchen
        objekt= '%{}%'.format(objekt)
        sql = "select * from nextcloud where user like '%s' or time like '%s' or method like '%s' or url like '%s' or message like '%s'"\
        %(objekt,objekt,objekt,objekt,objekt)
        
        
    elif wort == 1:   #unscharfe Suche                                           #           1   2   3   
        if (objekt[0] == "time" or objekt[0] == "user") and len(objekt) == 3:    #z.B. 2021-07-05 08:33
            objekt[1]= '%{}%'.format(objekt[1])
            objekt[2]= '%{}%'.format(objekt[2])
            sql = "select * from nextcloud where %s like '%s' and %s like '%s'"%(objekt[0],objekt[1],objekt[0],objekt[2])  
        else:
            objekt[1]= '%{}%'.format(objekt[1])
            sql = "select * from nextcloud where %s like '%s'"%(objekt[0],objekt[1])

        
    elif wort == 2:      #scharfe Suche
        if objekt[0] == "user" and len(objekt) == 3:  #z.B. Lizhong Tang
            sql = "select * from nextcloud where %s = '%s'"%(objekt[0],objekt[1]+" "+objekt[2])
        else:
            sql = "select * from nextcloud where %s = '%s'"%(objekt[0],objekt[1])
       
    elif wort == 3:     #dropdown-Menü
        objekt[1]= '%{}%'.format(objekt[1])
        objekt[3]= '%{}%'.format(objekt[3])
        if drop_anzahl==3:
            objekt[5]= '%{}%'.format(objekt[5])
            sql = "select * from nextcloud where %s like '%s'and %s like '%s'and %s like '%s' "%(objekt[0],objekt[1],objekt[2],objekt[3],objekt[4],objekt[5])
        else:
            sql = "select * from nextcloud where %s like '%s'and %s like '%s' "%(objekt[0],objekt[1],objekt[2],objekt[3])
        #db_text(sql,objekt)
    else:         #wort = 4
        if win:   #Weitersuche unscharfe Suche
            objekt= '%{}%'.format(objekt)
            sql = "select * from nextcloud where %s like '%s'"%(button_inhalt,objekt)
        else:
            sql = "select * from nextcloud where %s = '%s'"%(button_inhalt,objekt)
    db_text(sql,objekt)

def dropdown_sql(): #Annalysieren der Anzahl von Dropdown-Menüs
    global eingabe3,listbox,dropdown_such_button,en,eingabe2,eingabe,wort,dropdown,en,drop_anzahl
    objekt_list = []
    if drop_anzahl != 3:
        eingabe3 = en.get()
    else:
        eingabe5 = en.get()
    try:
        first=listbox.curselection()[0]
        if drop_anzahl != 3:
            eingabe4=listbox.get(first)
        else:
            eingabe6=listbox.get(first)
        listbox.place_forget()
        en.place_forget()
        wort = 3
        if drop_anzahl != 3:
            dropdown_such_button.place_forget()
            objekt_list.append(eingabe)
            objekt_list.append(eingabe2)
            objekt_list.append(eingabe3)
            objekt_list.append(eingabe4)
        else:
            dropdown_such_button.place_forget()
            objekt_list.append(eingabe)
            objekt_list.append(eingabe2)
            objekt_list.append(eingabe3)
            objekt_list.append(eingabe4)
            objekt_list.append(eingabe5)
            objekt_list.append(eingabe6)
        dropdown = False
        anzeige_inhalt(objekt_list)
        
        
    except:
        messagebox.showinfo(title="Info",message= "Wählen Sie bitte")

    
    
        
def db_text(sql,objekt): #Logs werden als Text gezeigt
    global dropdown,dropdown_such_button,listbox,user_list,time_list,method_list,en,drop,drop_anzahl,var_listbox
    db = pymysql.connect(host="localhost",port=3306,user="root",passwd="123456",db="new_schema",charset="utf8")
    cursor = db.cursor()
    drop_anzahl += 1
    try:
        cursor.execute(sql)
        ergebnis = cursor.fetchall()
        i = 1
        user_list = []
        time_list = []
        method_list = []
        for item in ergebnis:
            user_list.append(item[5])
            time_list.append(item[3])
            method_list.append(item[7])
        if len(user_list) > 200 and drop == True and drop_anzahl < 3:
            dropdown = True
        user_list = list(set(user_list))
        time_list = list(set(time_list))
        method_list = list(set(method_list))
        
        if not dropdown:
            text = Text(fenster,width=50, height=50,yscrollcommand=sb_v.set,xscrollcommand=sb_h.set,wrap ='none')  #wrap : kein Zeilenwechsel
            text.pack(expand = YES,fill = BOTH)
            sb_v.config(command=text.yview)
            sb_h.config(command=text.xview)
            text.insert("end", " "+"Nr"+"\t"+"IP"+"\t"+"\t"+"\t"+"ZEIT"+"\t"+"\t"+"\t"+
                    "USER"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"METHODE"+"\t"+"\t"+"URL"+
                    "\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"INFO"+'\n')
            for item in ergebnis:
                text.insert("end", " "+str(i)+"."+"\t"+item[4]+"\t"+"\t"+"\t"+item[3]+"\t"+"\t"+"\t"+
                    item[5]+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+item[7]+"\t"+"\t"+item[8]+
                    "\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+item[9]+'\n')
                i += 1
            messagebox.showinfo(title="Info",message= str(i-1)+" Logs sind für Sie gefunden ")   
        else:         
            if drop_anzahl==2:
                var_listbox = True
                en = Entry(fenster,width=61,highlightcolor='blue', highlightthickness=1)     #zweites Dropdown_Menü
                en.focus()
                en.icursor(0)                                #Cursor fixiert
                en.place(x=386,y=80,height=35)
                en.bind("<Button-1>", box)
                messagebox.showinfo(title="Info",message= "Sie können nun nach einem Schlüsselwort weitersuchen ")
                dropdown_such_button=Button(fenster ,width=61,height=28,text="Suchen",image=img2,bg="lightblue",activebackground="green",relief=RAISED,compound=LEFT,command=dropdown_sql) 
                dropdown_such_button.place(x=758,y=79)
            else:   #drop_anzahl = 1
                pass

    except:
        print("Error")
    db.close()
     

    
def anzeige(objekt):            #Anzeige der alle wichtigen gesuchten Log-Parametern
    global text,button_inhalt,such_button,item_dict
    log_list = []
    such_button=Button(fenster ,width=10,height=1,text="Suchen",bg="lightyellow",command=funktion_anzeige)
    such_button.pack(side=BOTTOM)
    button_inhalt = objekt
    vorbereitung()
    text = Text(fenster,width=50, height=50,yscrollcommand=sb_v.set,xscrollcommand=sb_h.set,wrap = 'none')
    text.pack(expand = YES,fill = BOTH)
    sb_v.config(command=text.yview)
    sb_h.config(command=text.xview)
    item_dict={"reqid":1,"level":2,"time":3,"remoteaddr":4,"user":5,"app":6,"method":7,"url":8,"message":9,"useragent":10,"version":11}
    for item in log_data:
        log_list.append(item[item_dict[objekt]])
    log_list=list(set(log_list))
    i=-1
    for i in range(len(log_list)):
        text.insert("end","  "+str(i+1)+"\t"+log_list[i]+"\n")
    messagebox.showinfo(title="Info",message= str(i+1)+" verschiedenen '{}' sind für Sie gefunden ".format(str(objekt)))
    zurück_menu()
        
    
       
####################################################################################################################################
        
############################################################  Programm verlassen ##################################################   
def verlassen():
    wahl=messagebox.askokcancel('Info', 'Möchten Sie wirklich Nextcloud-Logvierwer verlassen')
    if wahl:
        fenster.destroy()
        sys.exit()
        
def exit(event):            #direkt verlassen
    fenster.destroy()
    sys.exit()
####################################################################################################################################
def data_pack():
    global log_data
    log_data = []
    db = pymysql.connect(host="localhost",port=3306,user="root",passwd="123456",db="new_schema",charset="utf8")
    cursor = db.cursor()
    #sql = "SELECT * FROM nextcloud"
    try:
        cursor.execute("SELECT * FROM nextcloud")
        ergebnis = cursor.fetchall()
        for item in ergebnis:
            log_data.append(item)
    except:
        print("Error")
        
    db.close()

data_pack()
while True:
    items = ["reqid","level","time","remoteaddr","user","app","method","url","message","useragent","version"]
    dropdown_item=["user","time","method"]
    fenster = Tk()
    fenster.iconbitmap('1.ico')                         #tk ico
    fenster.protocol("WM_DELETE_WINDOW",verlassen)      #tk-X einstellen
    fenster.geometry("1200x750+150+40")
    fenster.title("Nextcloud-Logviewer")
    fenster.resizable(0,0)                              #feste Fenstergröße
    drop =False                                         #Voraussetzung der Dropdown-Menüs
    drop_anzahl = 0                                     #Anzahl der Dropdown-Menüs
    dropdown = False                                    #Status der Dropdown_Menüs
    var_listbox = True                                  #Status des Listboxes
    sb_v = Scrollbar(fenster,orient=VERTICAL)
    sb_v.pack(side=RIGHT, fill=Y)
    sb_h = Scrollbar(fenster,orient=HORIZONTAL)
    sb_h.pack(side=BOTTOM, fill=X)
    frame=Frame(fenster,width =1200,height = 750)
    frame.pack()
    canvas = Canvas(frame, width=1200,height=750)
    canvas.pack()
    img1 = Image.open('2.jpg')
    photo = ImageTk.PhotoImage(img1)
    canvas.create_image(600, 375, image=photo)
    img2 = PhotoImage(file="1.png")
    img3 = Image.open("3.jpg")
    foto_aktualisierung = ImageTk.PhotoImage(img3)
    suchen_aussehen()
    image = Image.open("1.jpg")
    foto = ImageTk.PhotoImage(image)
    fenster.bind_all("<Control-q>", exit)
    fenster.focus_set()     
    fenster.mainloop()
######################################################################################################################################    
