# chwdp
x = input().split()
def exactType(a):
    const = "abcde"
    var = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    typedict = {
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
        return 0  # predykat lub funkcja
    if (len(a) == 1 and (ord(a) >= ord("a") and ord(a) <= ord("e")) or (
            len(a) == 1 and ord(a) >= ord("A") and ord(a) <= ord("Z"))):
        return 1  # stała lub zmienna
    if (a == "FORALL" or a == "EXISTS" or a == "→" or a == "∃"):
        return 2  # kwantyfikator
    if (a == "NOT" or a == "¬" or a == "~"):
        return 3  # negacja
    return 4  # reszta


def operator(index):
    global x
    x = x[:index - 2] + [[x[index - 2]] + [x[index - 1]] + [x[index]]] + x[index + 1:]
    # x=x[:index-2]+["("+x[index-2]+" "+x[index]+" "+x[index-1]+")"]+x[index+1:]
    return 2


def negacja(index):
    global x
    x = x[:index-1]+ [[x[index-1]] + [x[index]]] + x[index+1:]
    return 1

def kwantyfikator(index):
    global x
    if len(x) - 1 == index:
        x = [x[:index - 1] + [x[index - 1]]] + x[index:]
    else:
        x = x[:index - 2] + [[[x[index - 2]] + [x[index - 1]]] + [x[index]]] + x[index + 1:]
    return 2

def done():
    global x

    if(type(x[len(x)-1])==3):
        if(len(x)==2):
            return 1
        return 0
    elif(type(x[len(x)-1])==0):
        funkcja_predykat(len(x)-1)
        x=x[0]
        return 1
    elif(type(x[len(x)-1])==2):
        if (len(x) < 3):
            return 1
        return 0
    else:
        if (len(x) == 3):
            return 1
        return 0

def funkcja_predykat(index):
    global x
    newindeks = int(x[index][2:])
    znakfunkcji = x[index][0]
    newstr="".join(x[index-newindeks:index])
    stala=[]
    for i in range(newindeks):
        stala.append(newstr[i])
    x=x[:index-newindeks] + [stala + [znakfunkcji]] + x[index+1:]
    #x = x[:index-newindeks]+[znakfunkcji+"("+ newstr +")"]+x[index+1:]
    return newindeks

def detect(sentence):
    operation = ''
    for element in sentence:
        if element[len(element) - 1] == 'NOT' or element[len(element) - 1] == '~' or element[len(element) - 1] == '¬':
            print(element[0][len(element[0]) - 1])
            operation = exactType(element[0][len(element[0]) - 1])
            print(operation)
            if operation == "or" or operation == 'implies' or operation == 'xor':
                return 'alfa'
            # detect beta
            elif operation == "and" or operation == "iff":
                return 'beta'
            # detect delta
            elif operation == 'forall':
                return 'delta'
            # detect gamma
            elif operation == 'exists':
                return 'gamma'
            else:
                return 'Nothing'
        else:
            print(element[len(element) - 1])
            operation = exactType(element[len(element) - 1])
            # detect alfa
            if operation == "and" or operation == 'iff':
                return 'alfa'
            # detect beta
            elif operation == "or" or operation == "implies" or operation == 'xor':
                return 'beta'
            # detect gamma
            elif operation == 'forall':
                return 'gamma'
            # detect delta
            elif operation == 'exists':
                return 'delta'
            else:
                return 'Nothing'


if __name__ == "__main__":
    i = 0
    leaf = []
    print(x)
    while(not done()):
        if (type(x[i]) == 0):
            i -= funkcja_predykat(i)
        elif (type(x[i]) == 2):
            i -= kwantyfikator(i)
        elif (type(x[i]) == 3):
            i -= negacja(i)
        elif (type(x[i]) == 4):
            i -= operator(i)
        i += 1
    # testing leaf
    leaf.append(x)
    z = detect(leaf)
    #print rule
    print(z)
