#arka gdynia kokaina
x=input().split()

def type(a):
    if ("/" in a):
        return 0                                                                                    #predykat lub funkcja
    if(len(a)==1 and (ord(a)>=ord("a") and ord(a)<=ord("e")) or (len(a)==1 and ord(a)>=ord("A") and ord(a)<=ord("Z"))):
        return 1                                                                                    #stała lub zmienna
    if(a=="FORALL" or a=="EXISTS" or a=="→" or a=="∃"):
        return 2                                                                                    #kwantyfikator
    if(a=="NOT" or a=="¬" or a=="~"):
        return 3                                                                                    #negacja
    return 4                                                                                        #reszta

def operator(index):
    global x
    x=x[:index-2]+  [[x[index-2]] + [x[index-1]] + [x[index]] ]  +x[index+1:]
    #x=x[:index-2]+["("+x[index-2]+" "+x[index]+" "+x[index-1]+")"]+x[index+1:]
    return 2

def negacja(index):
    global x
    x = x[:index-1] + [ x[index-1]+x[index] ] + x[index+1:]
    #x=x[:index-1]+["(" + x[index]+x[index-1]+")"]+x[index+1:]
    return 2

def funkcja_predykat(index):
    global x
    newindeks = int(x[index][2:])
    znakfunkcji = x[index][0]
    newstr=",".join(x[index-newindeks:index])
    x = x[:index-newindeks]+[znakfunkcji+"("+ newstr +")"]+x[index+1:]
    return newindeks

def kwantyfikator(index):
    global x
    x = x[:index-1] + [ x[index-1]+x[index] ] + x[index+1:]
    return 2

if __name__== "__main__":
    i = 0
    while(len(x)>2):
        if(type(x[i])==0):
            i-=funkcja_predykat(i)
        elif(type(x[i])==2):
            i-=kwantyfikator(i)
        elif (type(x[i]) == 3):
            i-=negacja(i)
        elif(type(x[i])==4):
            i-=operator(i)
        i+=1

    print(x)
