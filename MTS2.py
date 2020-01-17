import copy
GLOBAL_CONST = "abcdefghijk"
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
    rules_available = []
    for element in sentence:
        if element[len(element) - 1] == 'NOT' or element[len(element) - 1] == '~' or element[len(element) - 1] == '¬':
            operation = exactType(element[0][len(element[0]) - 1])
            if operation == "or" or operation == 'implies' or operation == 'xor':
                rules_available.append('alfa')
            # detect beta
            elif operation == "and" or operation == "iff":
                rules_available.append('beta')
            # detect delta
            elif operation == 'forall':
                rules_available.append('delta')
            # detect gamma
            elif operation == 'exists':
                rules_available.append('gamma')

        else:
            operation = exactType(element[len(element) - 1])
            # detect alfa
            if operation == "and" or operation == 'iff':
                rules_available.append('alfa')
            # detect beta
            elif operation == "or" or operation == "implies" or operation == 'xor':
                rules_available.append('beta')
            # detect gamma
            elif operation == 'forall':
                rules_available.append('gamma')
            # detect delta
            elif operation == 'exists':
                rules_available.append('delta')
    return rules_available

def extractVariable(sentence):
    return sentence[0][0]
#for delta rule
def getLastConst(con):
    return con[len(con) - 1]

def addConst(const_list):
    last_const = const_list[len(const_list) - 1]
    const_index = GLOBAL_CONST.index(last_const)
    const_list.append(GLOBAL_CONST[const_index + 1])

def getConst(itr, const):
    if itr >= len(const):
        return 0
    else:
        return const[itr]

#RULES
def alfa(expression):
    operator = exactType(expression[len(expression) - 1])
    if operator == 'and':
        #print('here')
        return expression[0], expression[1]
    elif operator == 'or':
        #print('here')
        #due to presence of negation
        return [expression[0]] + ['NOT'] , [expression[1]] + ['NOT']
    elif operator == 'implies':
        return expression[0] , [expression[1]] + ['NOT']
    elif operator == 'iff' or operator == 'xor':
        return [expression[0]] + [expression[1]] + ['IMPLIES'] , [expression[1]] + [expression[0]] + ['IMPLIES']

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

def delta(expression, constant, variable):
    for i in range(0,len(expression)):
        if type(expression[i]) == list:
            gamma(expression[i], constant, variable)
        else:
            if expression[i] == variable:
                expression[i] = constant
    return expression[0]


#================================================
def apply(exp, rule, con = None, var = None):
    #to prevent working on the original list
    exp_copy = exp
    if rule == 'alfa':
        return alfa(exp_copy)
    elif rule == 'beta':
        return beta(exp_copy)
    elif rule == 'gamma':
        return gamma(exp_copy, con, var)
    elif rule == 'delta':
        return delta(exp_copy, con, var)
    else:
        return 0

def check(rules):
    if len(rules) == 0:
        return False
    else:
        return True

def whatRule(rules):
    if check(rules) == False:
        return '', 0
    for i in range(len(rules)):
        if rules[i] != 'gamma':
            return rules[i],i
    return 'gamma', 0


def checkAnswer(leafs):
    for i in range(len(leafs)):
        neg = []
        if leafs[i][len(leafs[i]) - 1] == 'NOT':
            neg = leafs[i][0]
            for j in range(0, len(leafs)):
                if neg == leafs[j]:
                    return False
    return True


if __name__ == "__main__":
    #DEFINITIONS
    constants = ['a']
    my_const, my_var = None, None
    i = 0
    leafs = []
    leafs_answer = []
    available_operation = []
    finish = True
    answer = True
    gamma_count = 0
    x = input().split()
    #===========================

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

    # testing leaf
    leafs.append([x])
    leafs_answer.append(True)
    available_operation.append(True)

    while finish:
        operation_cnt = []
        current = 0
        for i in range (len(leafs)):
            z = detect(leafs[i])
            if check(z) == False:
                available_operation[i] = False
            rule, current = whatRule(z)
            operation_cnt.append(rule)
            #extracting variable that will be changed with constant (GAMMA)
            if rule == 'gamma' and gamma_count <= len(constants):
                my_var = extractVariable(leafs[i][0])
                my_const = getConst(gamma_count, constants)
                gamma_count += 1
                print(gamma_count)
            elif rule == 'delta':
                addConst(constants)
                my_var = extractVariable(leafs[i][0])
                my_const = getLastConst(constants)

        #APPLYING THE RULES
            if exactType(leafs[i][current][len(leafs[i][current]) - 1]) == 'not':
                if rule == 'beta':
                    result = apply(leafs[i][current][0], rule, my_const, my_var)
                    leafs[i] = result[0]
                    leafs.append([result[1]])
                    leafs_answer.append(True)
                    available_operation.append(True)
                elif rule == 'gamma'and gamma_count <= len(constants):
                    leafs.append(leafs[i])
                    result = apply(leafs[i][current][0], rule, my_const, my_var)
                    leafs[i] = result[1]
                elif rule == 'delta':
                    result = apply(leafs[i][current], rule, my_const, my_var)
                    leafs[i] = [result[1]]
                elif rule == 'alfa':
                    result1,result2 = apply(leafs[i][current][0], rule, my_const, my_var)
                    leafs[i][current] = result1
                    leafs[i].append(result2)


            else:
                if rule == 'beta':
                    result = apply(leafs[i][current], rule, my_const, my_var)
                    leafs[i] = result[0]
                    leafs.append([result[1]])

                    leafs_answer.append(True)
                    available_operation.append(True)
                elif rule == 'gamma'and gamma_count <= len(constants):
                    #copying the list
                    buf = copy.deepcopy(leafs[i][current])
                    result = apply(leafs[i][current], rule, my_const, my_var)
                    leafs[i] = [buf]
                    leafs[i].append(result[1])
                elif rule == 'delta':
                    result = apply(leafs[i][current], rule, my_const, my_var)
                    leafs[i] = [result[1]]
                elif rule == 'alfa':
                    result1,result2 = apply(leafs[i][current], rule, my_const, my_var)
                    leafs[i][current] = result1
                    leafs[i].append(result2)

            leafs_answer[i] = checkAnswer(leafs[i])
            #print(leafs[i])

        if available_operation.count(False) == len(available_operation) or  gamma_count > len(constants):
            finish = False
    #print(leafs)
    if leafs_answer.count(False) != len(leafs_answer):
        print("SPEŁNIALNA")
    else:
        print("NIESPEŁNIALNA")

