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
tk.bind("<Escape>", lambda e: tk.destroy())

ample_window = tk.winfo_screenwidth()
alt_window = tk.winfo_screenheight()

#-----Variables globals-----
joc=None
partida_executant = False
pantalla_inici = True
botons_actius = []

#-----Funcions de gestió de interface-----
def crear_boto(text, comanda, x, y, ample=200, alt=60, color="#4CAF50"):
    """Crea un botó i el guarda a una llista"""
    boto = Button(tk, text=text, font=("Arial", 20, "bold"),
                   bg=color, fg="white", command=comanda)
    boto.place(relx=x, rely=y, anchor=CENTER, width=ample, height=alt)
    botons_actius.append(boto)
    return boto

def netejar_interface():
    """Neteja el canvas i elimina els botons"""
    w.delete("all")
    for boto in botons_actius:
        boto.destroy()
    botons_actius.clear()

def mostrar_text_centrat(text, y_rel, tamany_font=40, color="black"):
    """Mostra un text centrat a la pantalla"""
    w.create_text(ample_window/2, alt_window * y_rel, 
                  text=text, 
                  font=("Arial", tamany_font, "bold"), 
                  fill=color)

def iniciar_partida(nom_ciutat):
    """Inicia una partida amb l'escenari seleccionat"""
    global joc, partida_executant, pantalla_inici
    
    netejar_interface()
    pantalla_inici = False
    partida_executant = True
    
    # Crear cotxe i pantalla
    screen = Pantalla(WPoint(0,0), WPoint(500,281),
                     ZPoint(0,0), ZPoint(ample_window, alt_window))
    
    # TO-DO: Canviar inicialització cotxes per fitxer .json
    c1 = Cotxe(250,100,15,23,v=1)
    cotxes = [c1]
    
    joc = Joc(nom_ciutat, cotxes, screen)
    
    # Iniciar bucle del joc
    bucle_joc(screen)

def mostrar_menu_escenari():
    """Mostra el menú per a seleccionar un escenari"""
    global pantalla_inici
    
    netejar_interface()
    pantalla_inici = False
    
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
        "1. Utilitza les tecles de fletxa per moure el cotxe",
        "2. Evita els obstacles",
        "3. Recull les recompenses per sumar punts",
        "4. Té en compte que perds vides en xocar amb obstacles",
        "",
        "Prem ESC per sortir del joc en qualsevol moment"
    ]
    
    for i, text in enumerate(instruccions):
        w.create_text(ample_window/2, alt_window * 0.3 + i * 40, 
                     text=text, 
                     font=("Arial", 16), 
                     fill="black")
    
    crear_boto("Tornar", mostrar_pantalla_inici, 0.5, 0.85, color="#9E9E9E")

def mostrar_pantalla_inici():
    global pantalla_inici, partida_executant
    
    netejar_interface()
    w.config(bg="white")
    
    pantalla_inici = True
    partida_executant = False
    
    # Títol del joc
    mostrar_text_centrat("JOC DE COTXES", 0.2)
    
    # Crear botons del menú principal
    crear_boto("Jugar", mostrar_menu_escenari, 0.25, 0.8, color="#2196F3")
    crear_boto("Instruccions", mostrar_instruccions, 0.5, 0.8, color="#2196F3")
    crear_boto("Sortir", tk.destroy, 0.75, 0.8, color="#2196F3")

def bucle_joc(screen):
    global joc

    w.delete("all")
    w.config(bg="#78CC54")
    
    # Dibuixem escenari
    for i in range(0, len(joc.parets)-1, 2):
        joc.parets[i].show(joc.parets[i+1], w, screen)

    for i in range(0, len(joc.recompenses)):
        joc.recompenses[i].show(w, screen)

    for i in range(0, len(joc.obstacles)):
        joc.obstacles[i].show(w, screen)
    
    #Pintem la línia de meta
    joc.meta.show(w, screen)
    
    # Controls del cotxe
    # if joc and joc.cotxes and len(joc.cotxes) > 0:
    #     c1 = joc.cotxes[0]
    #     c1.reset()  
    #     c1.controls()
    #     c1.mou()
    #     c1.xoc_paret(joc)
    #     c1.recompensa_agafada(joc)
    #     c1.xoc_obstacle(joc)
    #     c1.show(w, joc.screen)
    #     c1.mostra_puntuacio(w, ample_window-150, 40)
    #     c1.mostra_vides(w, 40, 40)
    
    w.update()
    screen.TranslateWorld(1)
    time.sleep(10/1000)
    
    # Seguim amb el bucle
    if partida_executant:
       tk.after(10, bucle_joc(screen))

# Iniciar amb la pantalla d'inici
mostrar_pantalla_inici()

# Iniciar el bucle principal de tkinter
tk.mainloop()