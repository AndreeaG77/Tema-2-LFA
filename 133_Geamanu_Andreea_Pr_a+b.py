# Tema 2 (L-NFA) + (NFA to DFA) + (Minimizare DFA)
# Citirea datelor
f = open("intrare")
n = int(f.readline())
# Codul functioneaza si cu stari care nu sunt consecutive
stari = [int(x) for x in f.readline().split()]
m = int(f.readline())
tranzitii = []
for i in range(m):
    tranzitii.append([x for x in f.readline().split()])
s = int(f.readline())
nrf = int(f.readline())
stari_finale = [int(x) for x in f.readline().split()]
nrCuv = int(f.readline())
cuvinte = []
for i in range(nrCuv):
    cuvinte.append(f.readline().strip())
f.close()
g = open("egale.txt", "w")

# Creez un dictionar cu liste de adiacenta pentru fiecare nod
dict_tranzitii = {}
for lista in tranzitii:
    if lista[0] not in dict_tranzitii:
        dict_tranzitii[lista[0]] = [(lista[1], lista[2])]
    else:
        dict_tranzitii[lista[0]].append((lista[1], lista[2]))
for stare in stari:
    if str(stare) not in dict_tranzitii:
        dict_tranzitii[str(stare)] = []


# NFA to DFA
# Starea de eroare (dead state) o consider valoarea 0

def NFA_to_DFA(stari, dict_tranzitii,stare_initiala):
    # Creez o lista cu literele folosite la tranzitii
    lista_tranzitii = []
    for lista in tranzitii:
        if lista[2] not in lista_tranzitii:
            lista_tranzitii.append(lista[2])
    #print(dict_tranzitii)
    dead_state = "0"
    # Creez un nou dictionar care sa contina listele de adiacenta pentru DFA
    dict_nou = {}
    stari_aux = []
    coada = []
    coada.append(stari[0])
    stari_aux.append(str(stari[0]))
    while coada != []:
        stare = coada[0]
        coada.pop(0)
        # Pentru fiecare stare ma uit in ce stari se duce cu fiecare litera din lista_tranzitii
        for tranz in lista_tranzitii:
            l = []
            if str(stare) in dict_tranzitii:
                for tuplu in dict_tranzitii[str(stare)]:
                    if tuplu[1] == tranz:
                        l.append(tuplu[0])
                # Daca nu se duce in nicio stare cu litera curenta, o trimit catre starea de eroare
                if l == []:
                    if stare not in dict_nou:
                        dict_nou[str(stare)] = [(dead_state, tranz)]
                    else:
                        dict_nou[str(stare)].append((dead_state, tranz))
                # Daca se duce intr-o singura stare, se pastreaza aceasta valoare
                elif len(l) == 1:
                    if str(stare) not in dict_nou:
                        dict_nou[str(stare)] = [(l[0], tranz)]
                    else:
                        dict_nou[str(stare)].append((l[0], tranz))
                # Daca se duce in mai multe stari trebuie sa creez o noua stare compusa din aceste stari
                else:
                    l.sort()
                    stare_noua = ""
                    for nod in l:
                        stare_noua = stare_noua + str(nod) + "/"
                    stare_noua = stare_noua[:-1]
                    if str(stare) not in dict_nou:
                        dict_nou[str(stare)] = [(stare_noua, tranz)]
                    else:
                        dict_nou[str(stare)].append((stare_noua, tranz))
            elif stare != dead_state:
                lista_stari_curente = []
                index1 = 0
                index2 = str(stare).find("/")
                while index2 != -1:
                    lista_stari_curente.append(str(stare)[index1:index2])
                    index1 = index2 + 1
                    index2 = str(stare).find("/", index1)
                lista_stari_curente.append(str(stare)[index1:])
                ls = []
                for st in lista_stari_curente:
                    for tuplu in dict_tranzitii[st]:
                        if tuplu[1] == tranz:
                            ls.append(tuplu[0])
                ls2 = set(ls)
                ls2 = sorted(ls2)
                stare_noua = ""
                for nod in ls2:
                    stare_noua = stare_noua + str(nod) + "/"
                stare_noua = stare_noua[:-1]
                if stare not in dict_nou:
                    dict_nou[stare] = [(stare_noua, tranz)]
                else:
                    dict_nou[stare].append((stare_noua, tranz))
            else:
                if stare not in dict_nou:
                    dict_nou[stare] = [(stare, tranz)]
                else:
                    dict_nou[stare].append((stare, tranz))

        for tuplu in dict_nou[str(stare)]:
            if tuplu[0] not in stari_aux:
                coada.append(tuplu[0])
                stari_aux.append(tuplu[0])

    #for stare in dict_nou:
        #print(stare, dict_nou[stare], sep=" ")

    # Creez o lista cu noile stari finale
    stari_finale2=[]
    for stare in stari_finale:
        for stare2 in stari_aux:
            indx=stare2.find(str(stare))
            if indx!=-1:
                if indx+len(str(stare))==len(stare2):
                    stari_finale2.append(stare2)
                elif stare2[indx+len(str(stare))]=="/":
                    stari_finale2.append(stare2)
    if stari_finale2==[]:
        for stare in stari_finale:
            stari_finale2.append(str(stare))

    print("Dictionarul cu toate tranzitiile NFA to DFA: ",dict_nou, sep="\n")
    print("Stare initiala NFA to DFA: ", stare_initiala, sep="\n")
    print("Starile finale NFA to DFA: ",stari_finale2,sep="\n")
    return dict_nou,stari_aux,stari_finale2

import copy

def next_state(st,litera,d):
    for tuplu in d[st]:
        if tuplu[1]==litera:
            return tuplu[0]

def find_states(s1,s2,e):
    for i in range(0,len(e)):
        if s1 in e[i]:
            break
    if s2 in e[i]:
        return 1
    return 0

#Minimizare DFA

def minDFA(stare_initiala):
    # Creez o lista cu literele folosite la tranzitii
    lista_tranzitii = []
    for lista in tranzitii:
        if lista[2] not in lista_tranzitii:
            lista_tranzitii.append(lista[2])
    n=len(lista_tranzitii)
    d={}
    ls=[]
    lsf=[]
    d,ls,lsf=NFA_to_DFA(stari, dict_tranzitii,stare_initiala)
    lsnf=[]
    for stare in ls:
        if stare not in lsf:
            lsnf.append(stare)
    e2=[lsnf,lsf]
    e1=[]
    while e1 != e2:
        e1=copy.deepcopy(e2)
        eaux=[]
        for element in e2:
            if len(element)==1:
                eaux.append(element)
            else:
                nr = 0
                for litera in lista_tranzitii:
                    s1 = next_state(element[0], litera,d)
                    s2 = next_state(element[1], litera,d)
                    ok = find_states(s1, s2, e2)
                    if ok == 1:
                        nr += 1
                if nr==n:
                    eaux.append([element[0],element[1]])
                else:
                    eaux.append([element[0]])
                    eaux.append([element[1]])
                for i in range(2,len(element)):
                    for el in eaux:
                        if el[0] in element:
                            nr=0
                            x=0
                            for litera in lista_tranzitii:
                                s1=next_state(el[0],litera,d)
                                s2=next_state(element[i],litera,d)
                                ok=find_states(s1,s2,e2)
                                if ok==1:
                                    nr+=1
                            if nr==n:
                                el.append(element[i])
                                x=1
                                break
                    if x==0:
                        eaux.append([element[i]])
        e2=copy.deepcopy(eaux)
    stari_finale_echiv=[]
    stari_echiv=[]
    for el in e2:
        if len(el)==1:
            stari_echiv.append(el[0])
            if el[0] in lsf:
                stari_finale_echiv.append(el[0])
        else:
            sn=""
            el=sorted(el)
            ok=0
            for st in el:
                sn=sn + st + "/"
                if st in lsf:
                    ok=1
            sn=sn[:-1]
            if ok==1:
                stari_finale_echiv.append(sn)
            stari_echiv.append(sn)
    dict_echiv={}
    for stare in ls:
        if stare in stari_echiv:
            dict_echiv[stare]=d[stare]
    for stare in stari_echiv:
        if stare not in dict_echiv:
            dict_echiv[stare]=[]
            stpartial=stare[0:stare.find("/")]
            for litera in lista_tranzitii:
                s1=next_state(stpartial,litera,d)
                if s1 in stari_echiv:
                    dict_echiv[stare].append((s1,litera))
                else:
                    mst=[]
                    indxstart=0
                    indx2=stare.find("/")
                    while indx2 != -1:
                        mst.append(stare[indxstart:indx2])
                        indxstart=indx2+1
                        indx2=stare.find("/", indx2+1)
                    mst.append(stare[indxstart:])
                    mst=sorted(mst)
                    mst2=[]
                    for saux in mst:
                        ss=next_state(saux,litera,d)
                        mst2.append(ss)
                    mst2=set(mst2)
                    mst2=sorted(mst2)
                    if len(mst2)==1:
                        dict_echiv[stare].append((mst2[0],litera))
                    else:
                        ss=""
                        for saux in mst2:
                            ss=ss+saux+"/"
                        ss=ss[:-1]
                        dict_echiv[stare].append((ss,litera))
    stare_initiala_echiv=""
    if str(stare_initiala) not in stari_echiv:
        for saux in stari_echiv:
            if saux not in ls:
                mst = []
                indxstart = 0
                indx2 = saux.find("/")
                while indx2 != -1:
                    mst.append(saux[indxstart:indx2])
                    indxstart = indx2 + 1
                    indx2 = saux.find("/", indx2 + 1)
                mst.append(saux[indxstart:])
                if str(stare_initiala) in mst:
                    stare_initiala_echiv=stare_initiala_echiv+saux
                    break
    else:
        stare_initiala_echiv = stare_initiala_echiv + str(stare_initiala)

    print("Dictionarul cu toate tranzitiile Minimizare DFA: ",dict_echiv,"Stare initiala Minimizare DFA",stare_initiala_echiv, sep="\n")
    print("Stari finale Minimizare DFA: ",stari_finale_echiv ,sep="\n")


# L-NFA

def BFS(stare_initiala, cuvant):
    i = 0
    coada = []
    sir=stare_initiala
    sir=str(sir)
    sir=sir + " "
    coada.append((stare_initiala,i,sir))
    while coada != []:
        (nod_crt, i, sir) = coada[0]
        coada.pop(0)
        if dict_tranzitii[str(nod_crt)] != []:
            for (vecin_nod_crt, litera_tranz) in dict_tranzitii[str(nod_crt)]:
                if i<len(cuvant) and cuvant[i]==litera_tranz:
                    if i == len(cuvant)-1 and int(vecin_nod_crt) in stari_finale:
                        return "DA" + " " + sir + vecin_nod_crt
                    else:
                        sir=sir + vecin_nod_crt + " "
                        coada.append((vecin_nod_crt, i+1, sir))
                elif litera_tranz=="L":
                    if int(vecin_nod_crt) in stari_finale and i==len(cuvant):
                        return "DA" + " " + sir + vecin_nod_crt
                    else:
                        sir=sir + vecin_nod_crt + " "
                        coada.append((vecin_nod_crt, i, sir))

    return "NU"

for cuv in cuvinte:
    g.write(BFS(s,cuv) + "\n")

#NFA_to_DFA(stari, dict_tranzitii)
minDFA(s)
g.close()