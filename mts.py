# chwdp
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


def typ(a):
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

    if(typ(x[len(x)-1])==3):
        if(len(x)==2):
            return 1
        return 0
    elif(typ(x[len(x)-1])==0):
        funkcja_predykat(len(x)-1)
        x=x[0]
        return 1
    elif(typ(x[len(x)-1])==2):
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
            operation = exactType(element[0][len(element[0]) - 1])
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

def extractVariable(sentence):
    return sentence[0][0]
def getConst(con):
    #NOT IMPLEMENTED, FOR NOW RETURNING ELEMENT 0
    return con[0]
#RULES
def alfa(expression):
    operator = exactType(expression[len(expression) - 1])
    if operator == 'and':
        return [expression[0]] + [expression[1]]
    elif operator == 'or':
        #due to presence of negation
        return [[expression[0]] + ['NOT']] + [[expression[1]] + ['NOT']]
    elif operator == 'implies':
        return [expression[0]] + [[expression[1]] + ['NOT']]
    elif operator == 'iff' or operator == 'xor':
        return [[expression[0]] + [expression[1]] + ['IMPLIES']] + [[expression[1]] + [expression[0]] + ['IMPLIES']]

def beta(expression):
    operator = exactType(expression[len(expression) - 1])
    if operator == 'and':
        return [[expression[0]] + ['NOT']] + [[expression[1]] + ['NOT']]
    elif operator == 'or':
        return [expression[0]] + [expression[1]]
    elif operator == 'implies':
        return [expression[0] + ['NOT']] + [expression[1]]
    elif operator == 'iff' or expression == 'xor':
        return[[[expression[0]] + [expression[1]] + ['IMPLIES']] + ['NOT']] + [[[expression[1]] + [expression[0]] + ['IMPLIES']] + ['NOT']]

def gamma(a, const, var):
    for i in range(0,len(a)):
        if type(a[i]) == list:
            gamma(a[i], const, var)
        else:
            if a[i] == var:
                a[i] = const

    return a[0]

#================================================
def apply(exp, rule, con = None, var = None):
    if rule == 'alfa':
        return alfa(exp)
    elif rule == 'beta':
        return beta(exp)
    elif rule == 'gamma':
        return gamma(exp, con, var)
    else:
        return 0
if __name__ == "__main__":
    constants = ['a']
    my_const, my_var = None, None
    i = 0
    leafs = []
    x = input().split()

    while(not done()):
        if (typ(x[i]) == 0):
            i -= funkcja_predykat(i)
        elif (typ(x[i]) == 2):
            i -= kwantyfikator(i)
        elif (typ(x[i]) == 3):
            i -= negacja(i)
        elif (typ(x[i]) == 4):
            i -= operator(i)
        i += 1
    print(x)
    # testing leaf
    leafs.append([x])
    current = 0
    for i in range (len(leafs)):
        z = detect(leafs[i])

        #extracting variable that will be changed with constant (GAMMA)
        if z == 'gamma':
            my_var = extractVariable(leafs[i][0])
            my_const = getConst(constants)
            

        if exactType(leafs[i][current][len(leafs[i][current]) - 1]) == 'not':
            result = apply(leafs[i][current][0], z, my_const, my_var)
            if z == 'beta':
                leafs[i] = result[0]
                leafs.append([result[1]])
            else:
                leafs[i] = result

        else:
            result = apply(leafs[i][current], z, my_const, my_var)
            print(result)
            if z == 'beta':
                leafs[i] = result[0]
                leafs.append([result[1]])
            else:
                leafs[i] = result
print(leafs)
