from tkinter import *
import time
from Cotxe import *
from ZPoint import *
from WPoint import *
from pantalla import *
from joc import *
import json

tk = Tk()
tk.attributes("-fullscreen", True)
w = Canvas(tk)
w.pack(fill=BOTH, expand=True)
tk.bind("<Escape>", lambda e: tk.destroy()) #Podem prémer ESC per sortir del joc en qualsevol moment

ample_window = tk.winfo_screenwidth() 
alt_window = tk.winfo_screenheight()

#-----Variables globals-----
joc=None
partida_executant = False
botons_actius = []

#Guardem referència de les imatges per a les instruccions
img_porc=carrega_imatge("imatges/Porc_senglar_1.png", 90, 70)
img_platan=carrega_imatge("imatges/plàtan.png", 50, 45)
img_container=carrega_imatge("imatges/contenidor.png", 80, 70)
img_iaia=carrega_imatge("imatges/Iaia_1.png", 75, 97)
img_con=carrega_imatge("imatges/con.png", 60, 75)
img_guiri=carrega_imatge("imatges/Guiri_1.png", 90, 135)
img_car=carrega_imatge("imatges/car_Q.png", 50, 100)
img_coin_10=carrega_imatge("imatges/moneda_10.png", 60, 60)
img_coin_20=carrega_imatge("imatges/moneda_20.png", 60, 60)
img_coin_50=carrega_imatge("imatges/moneda_50.png", 60, 60)

#-----Funcions de gestió de interfície-----
def crear_boto(text, comanda, x, y, ample=200, alt=60, color="#4CAF50"):
    """Crea un botó i el guarda a una llista"""
    boto = Button(tk, text=text, font=("Arial", 20, "bold"),
                   bg=color, fg="white", command=comanda)
    boto.place(relx=x, rely=y, anchor=CENTER, width=ample, height=alt)
    botons_actius.append(boto)
    return boto

def netejar_interface():
    #Neteja el canvas i elimina els botons
    w.delete("all")
    for boto in botons_actius:
        boto.destroy()
    botons_actius.clear()

def mostrar_text_centrat(text, y_rel, tamany_font=40, color="black"):
    #Mostra un text centrat a la pantalla
    w.create_text(ample_window/2, alt_window * y_rel, 
                  text=text, 
                  font=("Arial", tamany_font, "bold"), 
                  fill=color)

def iniciar_partida(nom_ciutat):
    #Inicia una partida amb l'escenari seleccionat
    global joc, partida_executant
    
    netejar_interface()
    partida_executant = True
    
    # Crear cotxe i pantalla
    screen = Pantalla(WPoint(0,0), WPoint(500,281),
                     ZPoint(0,0), ZPoint(ample_window, alt_window))
    
    w=screen.LongXZoomToWorld(60)
    h=screen.LongYZoomToWorld(120)
    cotxe = Cotxe(250,100,w,h,v=1)
    
    joc = Joc(nom_ciutat, cotxe, screen)
    
    # Iniciar bucle del joc
    bucle_joc(screen)

def game_over(escenari):
    mostrar_text_centrat("HAS PERDUT", 0.2)
    
    # Crear botons per seleccionar escenari
    crear_boto("Torna-hi", lambda: iniciar_partida(escenari), 0.33, 0.5, color="#F44336")
    crear_boto("Inici", mostrar_pantalla_inici, 0.66, 0.5, color="#9E9E9E")

def guanyat(escenari, cotxe):
    mostrar_text_centrat("HAS COMPLETAT EL CIRCUIT", 0.2)

    w.create_text(ample_window/2, alt_window*0.55, 
                     text=f"Has obtingut {cotxe.puntuacio} punts.", 
                     font=("Arial", 16), 
                     fill="black")
    
    # Botons per a tornar a jugar o anar al menú principal
    crear_boto("Tornar a jugar", lambda: iniciar_partida(escenari), 0.33, 0.75, color="#F44336")
    crear_boto("Inici", mostrar_pantalla_inici, 0.66, 0.75, color="#9E9E9E")

def mostrar_menu_escenari():
    #Mostra el menú per a seleccionar un escenari
    
    netejar_interface()
    
    mostrar_text_centrat("SELECCIONA ESCENARI", 0.2)
    
    # Crear botons per seleccionar escenari
    crear_boto("UAB", lambda: iniciar_partida("UAB"), 0.25, 0.5, color="#4CAF50")
    crear_boto("Cerdanyola", lambda: iniciar_partida("Cerdanyola"), 0.5, 0.5, color="#2196F3")
    crear_boto("Barcelona", lambda: iniciar_partida("Barcelona"), 0.75, 0.5, color="#F44336")
    crear_boto("Tornar", mostrar_pantalla_inici, 0.5, 0.8, color="#9E9E9E")

def mostrar_instruccions():
    netejar_interface()
    w.config(bg="white")
    
    mostrar_text_centrat("INSTRUCCIONS", 0.15)
    
    instruccions = [
        "1. Utilitza les fletxes del teclat per moure el cotxe",
        "2. Perds la partida si xoques contra una paret o et quedes sense vides",
        "3. Tens 3 vides. Evita els següents obstacles per no perdre una vida:"
    ]

    for i, text in enumerate(instruccions):
        w.create_text(ample_window/4, (alt_window * 0.3 + i * 40)-70, 
                     text=text, 
                     font=("Arial", 16), 
                     fill="black", anchor="nw")

    #Imatges dels obstacles
    w.create_image(ample_window/4-50, alt_window/8*3, image=img_porc, anchor="nw")
    w.create_image(ample_window/4-50, alt_window/8*4, image=img_platan, anchor="nw")
    w.create_image(ample_window/4-50, alt_window/8*5, image=img_container, anchor="nw")
    w.create_image(ample_window/4-50, alt_window/8*6, image=img_iaia, anchor="nw")
    w.create_image(ample_window/2+70, alt_window/8*3, image=img_con, anchor="nw")
    w.create_image(ample_window/2+70, alt_window/8*4, image=img_guiri, anchor="nw")
    w.create_image(ample_window/2+70, alt_window/8*6-30, image=img_car, anchor="nw")

    #Descripció dels obstacles
    w.create_text(ample_window/4+70, alt_window/8*3+30, 
                     text="Un porc senglar amb pesta porcina", 
                     font=("Arial", 16), 
                     fill="black", anchor="w")
    
    w.create_text(ample_window/4+70, alt_window/8*4+25, 
                     text="Una pela de plàtan", 
                     font=("Arial", 16), 
                     fill="black", anchor="w")
    
    w.create_text(ample_window/4+70, alt_window/8*5+30, 
                     text="Un container", 
                     font=("Arial", 16), 
                     fill="black", anchor="w")
    
    w.create_text(ample_window/4+70, alt_window/8*6+50, 
                     text="Una iaia", 
                     font=("Arial", 16), 
                     fill="black", anchor="w")
    
    w.create_text(ample_window/2+180, alt_window/8*3+35, 
                     text="Un con de trànsit", 
                     font=("Arial", 16), 
                     fill="black", anchor="w")
    
    w.create_text(ample_window/2+180, alt_window/8*4+60, 
                     text="Un guiri despistat", 
                     font=("Arial", 16), 
                     fill="black", anchor="w")
    
    w.create_text(ample_window/2+180, alt_window/8*6+20, 
                     text="Altres cotxes circulant", 
                     font=("Arial", 16), 
                     fill="black", anchor="w")
    
    crear_boto("Següent", mostrar_instruccions2, 0.90, 0.80, color="#9E9E9E")
    crear_boto("Tornar", mostrar_pantalla_inici, 0.90, 0.90, color="#9E9E9E")

def mostrar_instruccions2():
    netejar_interface()
    w.config(bg="white")
    
    mostrar_text_centrat("INSTRUCCIONS", 0.15)   

    w.create_text(ample_window/4, alt_window * 0.3 -70, 
                    text="4. Guanya punts recol·lectant monedes. La puntuació per a cada tipus de moneda és:", 
                    font=("Arial", 16), 
                    fill="black", anchor="nw")

    #Imatges de les recompenses
    w.create_image(ample_window/4-100, alt_window/4+50, image=img_coin_10, anchor="nw")
    w.create_image(ample_window/2-100, alt_window/4+50, image=img_coin_20, anchor="nw")
    w.create_image(ample_window/4*3-100, alt_window/4+50, image=img_coin_50, anchor="nw")

    #Descripció de les monedes
    w.create_text(ample_window/4, alt_window/4+80, 
                     text="10 punts", 
                     font=("Arial", 16), 
                     fill="black", anchor="w")
    
    w.create_text(ample_window/2, alt_window/4+80, 
                     text="20 punts", 
                     font=("Arial", 16), 
                     fill="black", anchor="w")
    
    w.create_text(ample_window/4*3, alt_window/4+80, 
                     text="50 punts", 
                     font=("Arial", 16), 
                     fill="black", anchor="w")
    
    w.create_text(ample_window/4, alt_window * 0.6 -70, 
                    text="5. Si xoques contra un obstacle perds 50 punts.", 
                    font=("Arial", 16), 
                    fill="black", anchor="nw")
    
    w.create_text(ample_window/4, alt_window * 0.6, 
                    text="Prem ESC en qualsevol moment per sortir del joc.", 
                    font=("Arial", 16), 
                    fill="black", anchor="nw")
    
    crear_boto("Anterior", mostrar_instruccions, 0.90, 0.80, color="#9E9E9E")
    crear_boto("Tornar", mostrar_pantalla_inici, 0.90, 0.90, color="#9E9E9E")

def mostrar_pantalla_inici():
    global partida_executant
    
    netejar_interface()
    w.config(bg="white")
 
    partida_executant = False
    
    # Títol del joc
    mostrar_text_centrat("JOC DE COTXES (PITÓN)", 0.2)
    
    # Crear botons del menú principal
    crear_boto("Jugar", mostrar_menu_escenari, 0.25, 0.8, color="#2196F3")
    crear_boto("Instruccions", mostrar_instruccions, 0.5, 0.8, color="#2196F3")
    crear_boto("Sortir", tk.destroy, 0.75, 0.8, color="#2196F3")

def bucle_joc(screen):
    global joc, partida_executant

    if not partida_executant:
        return

    w.delete("all")

    #Colors de fons segons escenari
    if joc.escenari=="UAB":
        w.config(bg="#78CC54")
    if joc.escenari=="Cerdanyola":
        w.config(bg="#D0D4CF")
    if joc.escenari=="Barcelona":
        w.config(bg="#F4E786")
    
    for i in range(0, len(joc.parets)-1, 2): #Dibuixem carretera
        joc.parets[i].show(joc.parets[i+1], w, screen)

    for i in range(0, len(joc.recompenses)): #Dibuixem recompenses
        joc.recompenses[i].show(w, screen)

    for i in range(0, len(joc.obstacles)): #Dibuixem obstacles
        joc.obstacles[i].show(w, screen)
    
    joc.meta.show(w, screen) #Pintem la línia de meta
    
    # Controls del cotxe
    c = joc.cotxe 
    c.controls()
    c.mou()
    c.xoc_paret(joc)
    c.recompensa_agafada(joc)
    c.xoc_obstacle(joc)
    c.show(w, screen)
    c.mostra_puntuacio(w, ample_window-150, 40)
    c.mostra_vides(w, 40, 40)
    
    w.update()
    screen.TranslateWorld(1)

    if joc.game_over(c):
        partida_executant=False
        game_over(joc.escenari)

    if joc.guanyar(c):
        partida_executant=False
        guanyat(joc.escenari, c)
    
    # Seguim amb el bucle
    if partida_executant:
       tk.after(2, lambda: bucle_joc(screen)) #El segon argument ha de ser una referència a una funció

# Iniciar amb la pantalla d'inici
mostrar_pantalla_inici()

# Iniciar el bucle principal de tkinter
tk.mainloop()