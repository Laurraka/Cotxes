import json

f=open("carretera.json","r")
dades=json.load(f)
f.close()
print(dades['cars'][0]['angle'])
print(dades['sections'][1]['distance'])

for d in dades:
    print(d)
    print(dades[d]) #mostra cada element del diccionari

for section in dades['sections']:
    print(section)

class Cotxe:
    def __init__(self,x,y):
        self.x=x
        self.y=y

cotxes=[]
for c in dades['cars']:
    c1=Cotxe(c['start_position']["x"],c['start_position']["y"],c['width'],c['height']) 
    cotxes.append(c1)