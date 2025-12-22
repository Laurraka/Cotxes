import json
from WPoint import *
from LinearEquation import *

#Fer diccionari de ranges de la carretera
f=open("carretera.json","r")
dades=json.load(f)
noms_trams=list(dades['sections_UAB'].keys())
ranges_trams={}
for nom in noms_trams:
    ranges_trams[nom]=range(dades['sections_UAB'][nom]['p1']['y'],dades['sections_UAB'][nom]['p3']['y'])

f.close()

class Joc:

    def construir_carretera(self, wMin, wMax, w, screen):
        primer_tram=1
        ultim_tram=1

        while wMin.y not in ranges_trams['T'+str(primer_tram)]:
            primer_tram=primer_tram+1
        
        while wMax.y not in ranges_trams['T'+str(ultim_tram)]:
            ultim_tram=ultim_tram+1

        L1=LinearEquation(WPoint(dades['sections_UAB']['T'+str(primer_tram)]['p1']['x'],dades['sections_UAB']['T'+str(primer_tram)]['p1']['y']),
                          WPoint(dades['sections_UAB']['T'+str(primer_tram)]['p3']['x'],dades['sections_UAB']['T'+str(primer_tram)]['p3']['y']))
        L2=LinearEquation(WPoint(dades['sections_UAB']['T'+str(primer_tram)]['p2']['x'],dades['sections_UAB']['T'+str(primer_tram)]['p2']['y']),
                          WPoint(dades['sections_UAB']['T'+str(primer_tram)]['p4']['x'],dades['sections_UAB']['T'+str(primer_tram)]['p4']['y']))
        
        p1=screen.WorldToZoomXY(L1.getX(wMin.y),wMin.y)
        p2=screen.WorldToZoomXY(L2.getX(wMin.y),wMin.y)

        L3=LinearEquation(WPoint(dades['sections_UAB']['T'+str(ultim_tram)]['p1']['x'],dades['sections_UAB']['T'+str(ultim_tram)]['p1']['y']),
                          WPoint(dades['sections_UAB']['T'+str(ultim_tram)]['p3']['x'],dades['sections_UAB']['T'+str(ultim_tram)]['p3']['y']))
        L4=LinearEquation(WPoint(dades['sections_UAB']['T'+str(ultim_tram)]['p2']['x'],dades['sections_UAB']['T'+str(ultim_tram)]['p2']['y']),
                          WPoint(dades['sections_UAB']['T'+str(ultim_tram)]['p4']['x'],dades['sections_UAB']['T'+str(ultim_tram)]['p4']['y']))
        
        p3=screen.WorldToZoomXY(L3.getX(wMax.y),wMax.y)
        p4=screen.WorldToZoomXY(L4.getX(wMax.y),wMax.y)

        i=primer_tram

        q1=screen.WorldToZoomXY(dades['sections_UAB']['T'+str(primer_tram)]['p3']['x'],dades['sections_UAB']['T'+str(primer_tram)]['p3']['y'])
        q2=screen.WorldToZoomXY(dades['sections_UAB']['T'+str(primer_tram)]['p4']['x'],dades['sections_UAB']['T'+str(primer_tram)]['p4']['y'])

        w.create_polygon(
            p1.x, p1.y,
            p2.x, p2.y,
            p3.x, p3.y,
            p4.y, p4.y,
            fill="blue",
            outline="black"
        )