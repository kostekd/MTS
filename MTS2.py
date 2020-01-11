#chwdp
x=input().split()

def exactType(a):
	const="abcde"
	var="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	typedict= {
		"NOT": "not",
		"~": "not",
		"¬": "not",
		"AND": "and",
		"&": "and",
		"∧": "and",
		"OR": "or",
		"|": "or",
		"∨": "or",
		"IMPLIES": "implies",
		"→": "implies",
		"IFF": "iff",
		"↔": "iff",
		"XOR": "xor",
		"⊕": "xor",
		"FORALL": "forall",
		"∀": "forall",
		"EXISTS": "exists",
		"∃": "exists"
	}
	if a in const:
		return "CONST"
	elif a in var:
		return "VAR"
	else:
		return typedict.get(a)

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
    newstr="".join(x[index-newindeks:index])
    stala=[]
    for i in range(newindeks):
        stala.append(newstr[i])
    x=x[:index-newindeks]+[stala + [znakfunkcji]]+x[index+1:]
    #x = x[:index-newindeks]+[znakfunkcji+"("+ newstr +")"]+x[index+1:]
    return newindeks

def kwantyfikator(index):
    global x
    x = x[:index-1] + [ x[index-1]+x[index] ] + x[index+1:]
    return 2

def detect(sentence):
    operation = ''
    for element in sentence:
        if element == element[len(element) - 1] == 'NOT' or element == element[len(element) - 1] == '~' or element == element[len(element) - 1] == '¬':
            operation = exactType(element[0][len(element) - 1])
            if operation == "or" and operation == 'implies' and operation == 'xor':
                return 'alfa'
            # detect beta
            elif operation == "and" and operation == "iff":
                return 'beta'
            # detect delta
            elif operation == 'forall' :
                return 'delta'
            # detect gamma
            elif operation == 'exists':
                return 'gamma'
            else:
                return 0
        else:
            operation = exactType(element[len(element) - 1])
            # detect alfa
            if operation == "and" and operation == 'iff':
                return 'alfa'
            # detect beta
            elif operation == "or" and operation == "implies" and operation == 'xor':
                return 'beta'
            #detect gamma
            elif operation == 'forall' :
                return 'gamma'
            #detect delta
            elif operation == 'exists':
                return 'delta'
            else:
                return 0

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
