def onp_module():
    def findOperators(operators, sen):
        operators
        for i in range(len(operators)):
            if operators[i] == sen:
                return operators[i]

    def getArguments(function, sen, index):
        numb = int(function[function.find('/') + 1:])
        new_sub_sentence = function[0] + "("
        for i in range(index - numb, index):
            if i != index - 1:
                new_sub_sentence += sen[i] + ", "
            else:
                new_sub_sentence += sen[i]
        new_sub_sentence += ")"

        sen = sen[:index - numb] + [new_sub_sentence] + sentence[index + 1:]
        return sen

    def getOperators(operator, sen, index):
        numb = 2
        if operator == "FORALL" or operator == "∀" or operator == "EXISTS" or operator == "∃":
            new_sub_sentence = '(' + operator + " " + sen[index - 2] + " " + sen[index - 1] + ')'
        elif operator == "NOT" or operator == "~" or operator == "¬":
            numb = 1
            new_sub_sentence = '(' + operator + " " + sen[index - 1] + ')'
        else:
            new_sub_sentence = '(' + sen[index - 2] + " " + operator + " " + sen[index - 1] + ')'

        sen = sen[:index - numb] + [new_sub_sentence] + sentence[index + 1:]
        return sen

    OPERATORS = ["NOT", "¬", "~", "AND", "&", "∧", "OR", "|", "∨", "IMPLIES", "→", "IFF", "↔", "XOR", "⊕", "FORALL",
                 "∀", "EXISTS", "∃"]
    sentence = input().split()
    i = 0
    while i < len(sentence):
        operator = findOperators(OPERATORS, sentence[i])
        if operator != None:
            sentence = getOperators(operator, sentence, i)
            if operator == "NOT" or operator == "~" or operator == "¬":
                i -= 1
            else:
                i -= 2
        elif sentence[i].find('/') != -1:
            numb = int(sentence[i][sentence[i].find('/') + 1:])
            sentence = getArguments(sentence[i], sentence, i)
            i -= numb
        i += 1
    return " ".join(sentence)
'''
def detect(sentence):
    #NOT IMPLEMENTED
def apply(expression):
    #NOT IMPLEMENTED
def alfa(expression):
    #NOT IMPLEMENTED
def beta(expression):
    #NOT IMPLEMENTED
def gamma(expression):
    #NOT IMPLEMENTED
def delta(expression):
    #NOT IMPLEMENTED
'''

if __name__ == "__main__":
    suffix = onp_module()