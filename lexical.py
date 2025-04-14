IDs = []
token = ('','',0) 
line = 1
varIDs = []
functionIDs = []

quadList = []
tempList = []

quadCounter = 1
tempCounter = 0

scopes = []
scope = []

keywords = {'πρόγραμμα','δήλωση', 'εάν', 'τότε', 'αλλιώς', 'εάν_τέλος','επανάλαβε','μέχρι','όσο','όσο_τέλος','για','έως','με_βήμα',' για_τέλος','διάβασε','γράψε','συνάρτηση','διαδικασία','διαπροσωπεία',' είσοδος','έξοδος','αρχή_συνάρτησης','τέλος_συνάρτησης',' αρχή_διαδικασίας','τέλος_διαδικασίαs',' αρχή_προγράμματος',' τέλος_προγράμματος',' ή','και','όχι','εκτέλεσε'}

f = open('test.greek', 'r', encoding='utf-8')

######################
#  Lexical Analyzer  #
######################

def lexical_analyzer():
    global line
    global token
    state = 0
    lexeme = ''

    while state != 9:
        backtrack = f.tell()
        c = f.read(1)

        if(state == 0):
            #keno h allagh grammhs paramenw
            if(c == '\n'):
                
                line+=1
                state = 0
            elif(c.isspace()):
                state = 0
            
            #gramma
            elif(c.isalpha()):
                lexeme+=c
                state=1

            #arithmos
            elif(c.isdigit()):
                lexeme+=c
                state = 2

            #elegxos gia :
            elif(c == ":"):
                lexeme+=c
                state = 3

            #elegxos gia <
            elif(c == "<"):
                lexeme+=c
                state = 4

            #elegxos gia >
            elif(c=='>'):
                lexeme+=c
                state = 5

            #sxolia
            elif(c=='{'):
                lexeme+=c
                state = 6
            
            #perasma me anafora
            elif(c=='%'):
                lexeme+=c
                token = (lexeme,'DECL_REF',line)
                state = 9

            #sygkrish oxi anathesh
            elif(c=='='):
                lexeme+=c
                token = (lexeme,'LOGICAL',line)
                state = 9
           
            #prosthesh afairesh
            elif(c in "+-"):
                lexeme+=c
                token = (lexeme,'ADD_OP',line)
                state = 9

            #pollaplasiasmos diairesh
            elif(c in "*/"):
                lexeme+=c
                token = (lexeme,'MUL_OP',line)
                state = 9

            #grouping
            elif(c in '()[]"'):
                lexeme+=c
                token = (lexeme,'GROUPING',line)
                state = 9

            #separator
            elif(c in ',;'):
                lexeme+=c
                token = (lexeme,'SEPERATOR',line)
                state = 9
        
        elif(state == 1):
            
            if(c.isalpha() or c.isdigit() or c=='_'):
                lexeme+=c
                state = 1
            elif(c.isspace()):
                if(lexeme not in keywords):
                    if(lexeme not in IDs):
                        IDs.append(lexeme)
                    token = (lexeme,'IDENTIFIER',line)
                elif(lexeme in keywords):
                    token = (lexeme,'KEYWORD',line)
                if(c == '\n'):
                    line+=1
                state = 9
            
            else:
                if(lexeme not in keywords):
                    if(lexeme not in IDs):
                        IDs.append(lexeme)
                    token = (lexeme,'IDENTIFIER',line)
                elif(lexeme in keywords):
                    token = (lexeme,'KEYWORD',line)

                f.seek(backtrack)
                state = 9
        
        elif(state == 2):
            if(c.isdigit()):
                lexeme+=c
                state = 2

            elif(c.isalpha()):
                print("Error! Letter after digit in line "+str(line))
                exit()

            elif(c.isspace()):
                num =int(lexeme)
                if(num < - (2**32)-1 or num > (2**32)-1):
                    print("Error! Number out of range in line "+str(line))
                    exit()
                token = (lexeme,'LITERAL_INT',line)
                if(c=='\n'):
                    line+=1
                state = 9

            else:
                num = int(lexeme)

                if(num < - (2**32)-1 or num > (2**32)-1):
                    print("Error! Number out of range in line "+str(line))
                    exit()
                token = (lexeme,'LITERAL_INT',line)
                f.seek(backtrack)
                state = 9

        elif(state == 3):
            if(c == '='):
                lexeme+=c
                token = (lexeme,'ASSIGNMENT',line)
                state = 9
            else:
                token = (lexeme,'SEPERATOR',line)
                f.seek(f.tell()-1)
                state = 9

        elif(state == 4):
            if(c=='='):
                lexeme+=c
                token = (lexeme,'LOGICAL',line)
                state = 9
            elif(c=='>'):
                lexeme+=c
                token = (lexeme,'LOGICAL',line)
                state = 9
            elif(c.isspace()):
                token = (lexeme,'LOGICAL',line)
                if(c=='\n'):
                    line+=1
                state = 9
            else:
                token = (lexeme,'LOGICAL',line)
                f.seek(f.tell()-1)
                state = 9
        
        elif(state == 5):
            if(c=='='):
                lexeme+=c
                token = (lexeme,'LOGICAL',line)
                state = 9
            elif(c=='<'):
                lexeme+=c
                token = (lexeme,'LOGICAL',line)
                state = 9
            elif(c.isspace()):
                token = (lexeme,'LOGICAL',line)
                if(c=='\n'):
                    line+=1
                state = 9
            else:
                token = (lexeme,'LOGICAL',line)
                f.seek(f.tell()-1)
                state = 9

        elif(state == 6):
            lexeme = ''
            while c:
                c = f.read(1)
                if(c=='\n'):
                    
                    line+=1
                if c == '}':
                    state = 0
                    break

    return token

##################
#  Symbol Table  #
##################

class Entity:

    def __init__(self, id, state):
        self.id = id
        self.state = state
        self.scope = -1

    @classmethod

    def Var(wrap, id, state, offset):

        variable = wrap(id, state)
        variable.offset = offset

        return variable

    @classmethod

    def Sub(wrap, id, state):
        
        sub = wrap(id, state)
        sub.squad = 0
        sub.args = []
        sub.length = 0

        return sub

    @classmethod

    def Par(wrap, id, state, mode, offset):

        parameter = wrap(id, state)
        parameter.mode = mode
        parameter.offset = offset

        return parameter

    @classmethod

    def Temp(wrap, id, state, offset):

        temp = wrap(id, state)
        temp.offset = offset

        return temp

def newEntity(entity):

    global scopes

    if scopes:
            print('evala afto '+str(entity.id))
            scopes[-1][2].append(entity)

def newScope(identifier):
    global scopes
    print('evala new scope '+str(identifier))

    scopes.append([identifier,len(scopes),[]])
        
def remScope():

    global scopes

    if scopes: 
        del scopes[-1]
            
def newArg(argument):

    global scopes

    if scopes:
        if scopes[-1][2]:
            print('evala afto ARGUMENT'+argument[0])
            target = scopes[-1][2][-1]
            print(target.id)
            target.args.append(argument)

def newParams():

    global scopes

    if len(scopes) > 1:
        print('prwto if sto params me len'+str(len(scopes)))
        what = scopes[-2][2][-1]
        print(str(what.id))
        if scopes[-2][2]:
            print('mphka if')
            for arg in scopes[-1][2][-1].args:
                parameter = Entity.Par(arg[0], 'prm', arg[2], getOffset())
                print('evala afto PARAMETER'+parameter.id)
                newEntity(parameter)
        
def getOffset():

    global scopes

    offset = 12

    if scopes:
        if scopes[-1][2]:
            for ent in scopes[-1][2]: 
                if ent.state == 'var' or ent.state == 'tmp' or ent.state == 'prm':
                    offset += 4

        return offset

def getLength():

    global scopes

    if len(scopes) > 1:
        if scopes[-2][2]:
            scopes[-2][2][-1].length = getOffset()

def getSQuad():

    global scopes

    if len(scopes) > 1:
        if scopes[-2][2]:
            scopes[-2][2][-1].squad = nextquad()

def outputSymbFile(file):

    global scopes, buffer

    buffer = ''
    F = open(file + '.symb', 'a', encoding='utf-8')
    for scope in reversed(scopes):
        buffer += '\nScope ' + str(scope[1]) +'\n'
   
        for ent in scope[2]:
                
            if ent.state == 'var':
                buffer += '  Variable entity: ' + ent.id +', offset: ' + str(ent.offset) + '\n'

            elif ent.state == 'tmp':
                buffer += '  Temporary variable entity: ' + ent.id +', offset: ' + str(ent.offset) + '\n'

            elif ent.state == 'prm':
                buffer += '  Parameter entity: ' + ent.id + ', mode: ' + str(ent.mode) + ', offset: ' + str(ent.offset) + '\n'

            elif ent.state == 'func':
                buffer += '  Function entity: ' + ent.id + ', starting quad: ' + str(ent.squad) + ', length: ' + str(ent.length) + '\n'

            elif ent.state == 'proc':
                buffer += '  Procedure entity: ' + ent.id + ', starting quad: ' + str(ent.squad) + ', length: ' + str(ent.length) + '\n'

    F.write(buffer + '\n')
    F.close()

def search_id(id):

    global scopes

    if scopes:

        for scope in scopes[::-1]:

            for ent in scope[2]:
                if ent.id == id:
                    ent.scope = scope
                    return ent

#######################
#  Intermediate Code  #
#######################

def nextquad():
    global quadCounter
    return quadCounter

def genquad(op,x,y,z):
    global quadList, quadCounter
    count = nextquad()

    newquad = [count,op,x,y,z]
    quadList.append(newquad)

    quadCounter+=1
    return newquad

def newtemp():
    global tempCounter
    global tempList

    temp = 'T_'
    tempCounter +=1 
    temp += str(tempCounter)

    tempList += [temp]

    ent = Entity.Temp(temp, 'tmp', getOffset())
    newEntity(ent)

    return temp

def emptyList():
    emptyLst = []

    return emptyLst

def makeList(x):
    makeLst = [x]

    return makeLst

def merge(list1,list2):
    mergeLst = []
    mergeLst += list1 + list2

    return mergeLst

def backpatch(lists,z):
    global quadList

    for i in range(len(lists)):
        for j in range(len(quadList)):
            if lists[i] == quadList[j][0] and quadList[j][4] == '_':
                quadList[j][4] = z
                break

def intFile(file):
    global quadList,buffer

    buffer = ''
    F = open(file + '.int','w', encoding='utf-8')
    for i in range(len(quadList)):
        buffer += str(quadList[i][0]) + ' ' + str(quadList[i][1]) + ' ' + str(quadList[i][2]) + ' ' + str(quadList[i][3]) + ' ' + str(quadList[i][4]) + '\n'

    F.write(buffer + '\n')
    F.close()

#####################################
########   Syntax Analyzer  #########
#####################################

def startRule():
    program()
    print('Syntax analysis succesful!')

def program():
    global token
    if(token[0] == 'πρόγραμμα'):
        token = lexical_analyzer()
        if(token[0] in IDs):

            program_name = token[0]
            genquad('begin_block', program_name,'_','_')

            newScope(program_name)

            token = lexical_analyzer()
            programblock()

            genquad('halt','_','_','_')
            genquad('end_block', program_name,'_','_')
        else:
            print('Error incorrect ID name for program at line: ',token[2])
            exit()
    else:
        print('Error program doesnt start with "πρόγραμμα" at line: ',token[2])
        exit()

def programblock():
    global token
    global scopes
    declarations()
    subprograms()
    if(token[0] == 'αρχή_προγράμματος'):
        token = lexical_analyzer()

        outputSymbFile('symbtest')
        
        while(len(scopes)>=2):
            remScope()

        sequence()
        if(token[0] == 'τέλος_προγράμματος'):
            token = lexical_analyzer()
        else:
            
            print('Error programblock doesnt end with "τέλος_προγράμματος" at line: ',token[2])
            exit()
    else:
        print('Error programblock doesnt start with "αρχή_προγράμματος" at line: ',token[2])
        exit()
    
def declarations():
    global token
    while(token[0]=='δήλωση'):
        token = lexical_analyzer()
        varlist(False)

def varlist(isArgs):
    global token
    varlst = []

    if(token[0] in IDs):
 
        varlst.append(token[0])
        
        if(not isArgs):
            ent = Entity.Var(token[0], 'var',getOffset())
            newEntity(ent)

        token = lexical_analyzer()

        while(token[0] == ','):

            token = lexical_analyzer()

            if(token[0] in IDs):

                varlst.append(token[0])

                if(not isArgs):
                    ent = Entity.Var(token[0], 'var',getOffset())
                    newEntity(ent)

                token = lexical_analyzer()
            else:
                print('Invalid ID name at line: ',token[2])
                exit()
    else:
        print('Invalid ID name at line: ',token[2])
        exit()
    
    return varlst

def subprograms():
    global token
    while(token[0] == 'συνάρτηση' or token[0] == 'διαδικασία'):
        if(token[0] == 'συνάρτηση'):
            token = lexical_analyzer()
            func()
        elif(token[0] == 'διαδικασία'):
            token = lexical_analyzer()
            proc()

def func():
    global token
    global functionIDs
    
    if(token[0] in IDs):

        func_name = token[0]
        functionIDs.append(func_name)

        genquad('begin_block', func_name,'_','_')

        newScope(func_name)

        ent = Entity.Sub(func_name, 'func')
        newEntity(ent)

        token = lexical_analyzer()
        

        if(token[0] == '('):
            token = lexical_analyzer()
            formalparlist()
            if(token[0]==')'):
                token = lexical_analyzer()
                funcblock()
                genquad('end_block', func_name,'_','_')
            else:
                print('Error, expected ")" at line: ', token[2])
                exit()
        else:
            print('Error expected "(" at line: ',token[2])
            exit()
    else:
        print('Error, not an ID at line: ',token[2])
        exit()

def proc():
    global token
    if(token[0] in IDs):

        proc_name = token[0]
        genquad('begin_block', proc_name,'_','_')

        newScope(proc_name)
        
        ent = Entity.Sub(proc_name, 'proc')
        newEntity(ent)

        token = lexical_analyzer()

        

        if(token[0] == '('):
            token = lexical_analyzer()
            formalparlist()
            if(token[0]==')'):
                token = lexical_analyzer()
                procblock()
                genquad('end_block', proc_name,'_','_')
            else:
                print('Error, expected ")" at line: ', token[2])
                exit()
        else:
            print('Error expected "(" at line: ',token[2])
            exit()
    else:
        print('Error, not an ID at line: ',token[2])
        exit()

def formalparlist():
    global token
    if(token[0]!=')'):
        varlist(True)

def funcblock():
    global token
    
    if(token[0]=='διαπροσωπεία'):
        token = lexical_analyzer()
        funcinput()
        funcoutput()
        declarations()

        newParams()

        subprograms()
        if(token[0]=='αρχή_συνάρτησης'):
            token = lexical_analyzer()
            sequence()
            if(token[0]=='τέλος_συνάρτησης'):
                token = lexical_analyzer()
            else:
                print('Error, function not closed at line:', token[2])
                exit()
        else:
            print('Error, function not opened at line:', token[2])
            exit()
    else:
        print('Error, function not diaprosopeia at line:', token[2])
        exit()

def procblock():
    global token
    if(token[0]=='διαπροσωπεία'):
        token = lexical_analyzer()
        funcinput()
        funcoutput()
        declarations()

        newParams()

        subprograms()
        if(token[0]=='αρχή_διαδικασίας'):
            token = lexical_analyzer()
            sequence()
            if(token[0]=='τέλος_διαδικασίας'):
                token = lexical_analyzer()
            else:
                print('Error, proc not closed at line:', token[2])
                exit()
        else:
            print('Error, proc not opened at line:', token[2])
            exit()
    else:
        print('Error, proc not diaprosopeia at line:', token[2])
        exit()

def funcinput():
    global token
    if(token[0]=='είσοδος'):
        token = lexical_analyzer()
        varlst = varlist(True)
        for v in varlst:
            arg = [v,'cv','in']
            newArg(arg)

            genquad('par', v, 'cv', '_')
 
def funcoutput():
    global token
    if(token[0]=='έξοδος'):
        token = lexical_analyzer()
        varlst = varlist(True)
        for v in varlst:
            arg = [v,'ref','inout']
            newArg(arg)

            genquad('par', v, 'ref', '_')

def sequence():
    global token
    statement()
    while(token[0]==';'):
        token = lexical_analyzer()
        statement()

def statement():
    global token
    if(token[0] in IDs):
        assignment_stat()
    elif(token[0]=='εάν'):
        if_stat()
    elif(token[0]=='όσο'):
        token = lexical_analyzer()
        while_stat()
    elif(token[0]=='επανάλαβε'):
        token = lexical_analyzer()
        do_stat()
    elif(token[0]=='για'):
        token = lexical_analyzer()
        for_stat()
    elif(token[0]=='διάβασε'):
        token = lexical_analyzer()
        input_stat()
    elif(token[0]=='γράψε'):
        token = lexical_analyzer()
        print_stat()
    elif(token[0]=='εκτέλεσε'):
        token = lexical_analyzer()
        call_stat()
    else:
        print('Error wrong statement at line: ',token[2])
        exit()

def assignment_stat():
    global token

    target = token[0]
    token = lexical_analyzer()

    if(token[0]==':='):
        token = lexical_analyzer()
        E = expression()

        genquad(':=', E,'_',target)
    else:
        print('Error expected ":=" at line: ',token[2])
        exit()

def if_stat():
    global token

    token = lexical_analyzer()
    B = condition()

    if(token[0]=='τότε'):
        token = lexical_analyzer()
        backpatch(B[0], nextquad())
        sequence()

        iflst = makeList(nextquad())
        genquad('jump','_','_','_')
        backpatch(B[1],nextquad())

        elsepart()

        backpatch(iflst,nextquad())

        if(token[0]=='εάν_τέλος'):
            token = lexical_analyzer()
        else:
            print('Error if not closed properly at line: ',token[2])
            exit()
    else:  
        print('Error expected "τότε" at line: ',token[2])
        exit()

def elsepart():
    global token
    if(token[0]=='αλλιώς'):
        token = lexical_analyzer()
        sequence()

def while_stat():
    global token

    Bq = nextquad()
    B = condition()

    if(token[0]=='επανάλαβε'):
        token = lexical_analyzer()
        backpatch(B[0],nextquad())

        sequence()

        genquad('jump','_','_',Bq)
        backpatch(B[1],nextquad())

        if(token[0]=='όσο_τέλος'):
            token = lexical_analyzer()
        else:
            print('Error expected "όσο_τέλος" at line: ',token[2])
            exit()
    else:
        print('Error expected "επανάλαβε" at line: ',token[2])
        exit()

def do_stat():
    global token

    Bq = nextquad()
    sequence()

    if(token[0]=='μέχρι'):
        token = lexical_analyzer()
        B = condition()

        backpatch(B[1],Bq)
    else:
        print('Error expected "μέχρι" at line: ',token[2])
        exit()

def for_stat():
    global token

    if(token[0] in IDs):
        i = token[0]
        token = lexical_analyzer()

        if(token[0]==':='):
            token = lexical_analyzer()
            start_val = expression()
            genquad(':=', start_val, '_', i)

            if(token[0]=='έως'):
                token = lexical_analyzer()
                end_val = expression()
                step_val = step()

                L1 = nextquad()
                B = genquad('<=', i, end_val, '_')  # αν ισχυει συνεχιζει

                if(token[0]=='επανάλαβε'):


                    token = lexical_analyzer()
                    sequence()

                    #προσθετω step στο i
                    temp = newtemp()
                    genquad('+', i, step_val, temp)
                    genquad(':=', temp, '_', i)

                    #παω παλι στον ελεγχο
                    genquad('jump', '_', '_', L1)

                    backpatch(B,nextquad())

                    if(token[0]=='για_τέλος'):
                        token = lexical_analyzer()
                    else:
                        print('Error expected "για_τέλος" at line: ',token[2])
                        exit()
                else:
                    print('Error expected "επανάλαβε" at line: ',token[2])
                    exit()
            else:
                print('Error expected "έως" at line: ',token[2])
                exit()
        else:
            print('Error expected ":=" at line: ',token[2])
            exit()
    else:
        print('Error expected ID at line: ',token[2])
        exit()

def step():
    global token

    if(token[0]=='με_βήμα'):
        token = lexical_analyzer()
        E = expression()
        return E
    
    return 1

def print_stat():
    global token
    E = expression()
    genquad('out',E,'_','_')

def input_stat():
    global token
    if(token[0] in IDs):
        genquad('inp',token[0],'_','_')
        token = lexical_analyzer()
    else:
        print('Error expected ID at line: ',token[2])
        exit()

def call_stat():
    global token
    if(token[0] in IDs):
        temp = token[0]
        token = lexical_analyzer()
        idtail(temp)
    else:
        print('Error expected ID at line: ',token[2])
        exit()

def idtail(f_id):
    global token
    global functionIDs

    if(token[0] == '('):
        token = lexical_analyzer()
        actualpars()

        w = newtemp()

        if f_id in functionIDs:
            genquad('par', w, 'RET', '_')

        genquad('call', f_id, '_', '_')

        return w
    
    return f_id

def actualpars():
    global token
    actualparlist()
    if(token[0] == ')'):
        token = lexical_analyzer()
    else:
        print('Error expected ")" at line: ',token[2])
        exit()

def actualparlist():
    global token
    if(token[0] != ')'):
        actualparitem()
        while(token[0]==','):
            token = lexical_analyzer()
            actualparitem()

def actualparitem():
    global token

    if(token[0]=='%'):
        token = lexical_analyzer()
        if(token[0] in IDs):

            genquad('par', token[0], 'REF', '_')  
            token = lexical_analyzer()

        else:
            print('Error expected ID at line: ',token[2])
            exit()
    else:
        E = expression()
        genquad('par', E, 'CV', '_')

def condition():
    global token

    Q1 = boolterm()

    conditionT = Q1[0]
    conditionF = Q1[1]

    while(token[0]=='ή'):
        backpatch(conditionF,nextquad())
        token = lexical_analyzer()

        Q2 = boolterm()

        conditionT = merge(conditionT,Q2[0])
        conditionF = Q2[1]

    return conditionT, conditionF

def boolterm():
    global token

    R1 = boolfactor()
    booltermT = R1[0]
    booltermF = R1[1]

    while(token[0]=='και'):
        backpatch(booltermF,nextquad())

        token = lexical_analyzer()

        R2 = boolfactor()

        booltermT = R2[0]
        booltermF = merge(booltermF,R2[1])

    return booltermT,booltermF

def boolfactor():
    global token

    if(token[0]=='όχι'):
        token = lexical_analyzer()

        if(token[0]=='['):
            token = lexical_analyzer()
            B = condition()
            boolfactorT = B[1]
            boolfactorF = B[0]

            if(token[0]==']'):
                token = lexical_analyzer()
                return boolfactorF,boolfactorT
            
            else:
                print('Error expected "]" at line: ',token[2])
                exit()
        else:
            print('Error expected "[" at line: ',token[2])
            exit()

    elif(token[0]=='['):
        token = lexical_analyzer()

        B = condition()

        boolfactorT = B[0]
        boolfactorF = B[1]

        if(token[0]==']'):
                token = lexical_analyzer()
                return boolfactorT,boolfactorF
        else:
            print('Error expected "]" at line: ',token[2])
            exit()
    else:
        E1 = expression()
        rel_op = relational_oper()
        E2 = expression()

        Rtrue = makeList(nextquad())
        genquad(rel_op,E1,E2,'_')
        Rfalse = makeList(nextquad())
        genquad('jump','_','_','_')
    
    return Rtrue,Rfalse

def expression():
    global token

    op_s = optional_sign()
    T1 = term()
    if(op_s == '-'):
        temp = newtemp()
        genquad('-',0,T1,temp)
        T1 = temp

    while(token[0] in '+-'):
        addOp = add_oper()
        T2 = term()

        w = newtemp()
        genquad(addOp,T1,T2,w)
        T1 = w
    
    return T1

def term():
    global token

    F1 = factor()

    while(token[0] in '*/'):
        mulOp = mul_oper()
        F2 = factor()

        w = newtemp()
        genquad(mulOp,F1,F2,w) 
        F1 = w
    return F1

def factor():
    global token

    if(token[0].isdigit()):
        F = token[0]
        token = lexical_analyzer()
        return F
    
    elif(token[0] == '('):
        token = lexical_analyzer()
        E = expression()

        if(token[0] == ')'):
            token = lexical_analyzer()
            return E
        
        else:
            print('Error expected ")" at line: ',token[2])
            exit()

    elif(token[0] in IDs):
        temp = token[0]
        token = lexical_analyzer()
        F = idtail(temp)
        return F
    
    else:
        print('Error , wrong factor type at line: ',token[2], 'with token:',token[0])
        exit()

def relational_oper():
    global token

    if token[0] == '=':
        relop = token[0]
        token = lexical_analyzer()

    elif token[0] == '<=':
        relop = token[0]
        token = lexical_analyzer()

    elif token[0] ==  '>=':
        relop = token[0]
        token = lexical_analyzer()

    elif token[0] == '>':
        relop = token[0]
        token = lexical_analyzer()

    elif token[0] == '<':
        relop = token[0]
        token = lexical_analyzer()

    elif token[0] == '<>':
        relop = token[0]
        token = lexical_analyzer()  

    else:
        print("Error! Missing 'relational operator' in line "+token[1])
        exit()
    
    return relop

def add_oper():
    global token

    if(token[0] == '+'):
        token = lexical_analyzer()
        return '+'
    
    elif(token[0] == '-'):
        token = lexical_analyzer()
        return '-'

def mul_oper():
    global token

    if(token[0] == '*'):
        mulop = '*'
        token = lexical_analyzer()
    
    elif(token[0] == '/'):
        mulop = '/'
        token = lexical_analyzer()
    
    return mulop

def optional_sign():
    global token
    add_oper()

token = lexical_analyzer()


startRule()

outputSymbFile('symbtest')
print("Outputed .symb file in dir, with name symbtest.symb \n")
for s in scopes:
    print('YO '+ s[0]+str(s[1]))
    for wh in s[2]:
        print('YOYO'+wh.id)

remScope()

intFile('test')
print("Outputed .int file in dir, with name test.int \n")