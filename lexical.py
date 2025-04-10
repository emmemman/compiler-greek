IDs = []
token = ('','',0) 
line = 1
counter = 0
keywords = {'πρόγραμμα','δήλωση', 'εάν', 'τότε', 'αλλιώς', 'εάν_τέλος','επανάλαβε','μέχρι','όσο','όσο_τέλος','για','έως','με_βήμα',' για_τέλος','διάβασε','γράψε','συνάρτηση','διαδικασία','διαπροσωπεία',' είσοδος','έξοδος','αρχή_συνάρτησης','τέλος_συνάρτησης',' αρχή_διαδικασίας','τέλος_διαδικασίαs',' αρχή_προγράμματος',' τέλος_προγράμματος',' ή','και','όχι','εκτέλεσε'}

f = open('test.greek', 'r', encoding='utf-8')

#####################################
########  Lexical Analyzer  #########
#####################################

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
            token = lexical_analyzer()
            programblock()
        else:
            print('Error incorrect ID name for program at line: ',token[2])
            exit()
    else:
        print('Error program doesnt start with "πρόγραμμα" at line: ',token[2])
        exit()

def programblock():
    global token
    declarations()
    subprograms()
    if(token[0] == 'αρχή_προγράμματος'):
        token = lexical_analyzer()
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
        varlist()

def varlist():
    global token
    if(token[0] in IDs):
        token = lexical_analyzer()
        while(token[0] == ','):
            token = lexical_analyzer()
            if(token[0] in IDs):
                token = lexical_analyzer()
            else:
                print('Invalid ID name at line: ',token[2])
                exit()
    else:
        print('Invalid ID name at line: ',token[2])
        exit()

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
    if(token[0] in IDs):
        token = lexical_analyzer()
        if(token[0] == '('):
            token = lexical_analyzer()
            formalparlist()
            if(token[0]==')'):
                token = lexical_analyzer()
                funcblock()
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
        token = lexical_analyzer()
        if(token[0] == '('):
            token = lexical_analyzer()
            formalparlist()
            if(token[0]==')'):
                token = lexical_analyzer()
                procblock()
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
        varlist()

def funcblock():
    global token
    if(token[0]=='διαπροσωπεία'):
        token = lexical_analyzer()
        funcinput()
        funcoutput()
        declarations()
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
        varlist()
    
def funcoutput():
    global token
    if(token[0]=='έξοδος'):
        token = lexical_analyzer()
        varlist()

def sequence():
    global token
    statement()
    while(token[0]==';'):
        token = lexical_analyzer()
        statement()

def statement():
    global token
    if(token[0] in IDs):
        token = lexical_analyzer()
        assignment_stat()
    elif(token[0]=='εάν'):
        token = lexical_analyzer()
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
    if(token[0]==':='):
        token = lexical_analyzer()
        expression()
    else:
        print('Error expected ":=" at line: ',token[2])
        exit()

def if_stat():
    global token
    condition()
    if(token[0]=='τότε'):
        token = lexical_analyzer()
        sequence()
        elsepart()
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
    condition()
    if(token[0]=='επανάλαβε'):
        token = lexical_analyzer()
        sequence()
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
    sequence()
    if(token[0]=='μέχρι'):
        token = lexical_analyzer()
        condition()
    else:
        print('Error expected "μέχρι" at line: ',token[2])
        exit()

def for_stat():
    global token
    if(token[0] in IDs):
        token = lexical_analyzer()
        if(token[0]==':='):
            token = lexical_analyzer()
            expression()
            if(token[0]=='έως'):
                token = lexical_analyzer()
                expression()
                step()
                if(token[0]=='επανάλαβε'):
                    token = lexical_analyzer()
                    sequence()
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
        expression()

def print_stat():
    global token
    expression()

def input_stat():
    global token
    if(token[0] in IDs):
        token = lexical_analyzer()
    else:
        print('Error expected ID at line: ',token[2])
        exit()

def call_stat():
    global token
    if(token[0] in IDs):
        token = lexical_analyzer()
        idtail()
    else:
        print('Error expected ID at line: ',token[2])
        exit()

def idtail():
    global token
    if(token[0] == '('):
        token = lexical_analyzer()
        actualpars()

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
            token = lexical_analyzer()
        else:
            print('Error expected ID at line: ',token[2])
            exit()
    else:
        expression()

def condition():
    global token
    boolterm()
    while(token[0]=='ή'):
        token = lexical_analyzer()
        boolterm()

def boolterm():
    global token
    boolfactor()
    while(token[0]=='και'):
        token = lexical_analyzer()
        boolfactor()

def boolfactor():
    global token
    if(token[0]=='όχι'):
        token = lexical_analyzer()
        if(token[0]=='['):
            token = lexical_analyzer()
            condition()
            if(token[0]==']'):
                token = lexical_analyzer()
            else:
                print('Error expected "]" at line: ',token[2])
                exit()
        else:
            print('Error expected "[" at line: ',token[2])
            exit()
    elif(token[0]=='['):
        token = lexical_analyzer()
        condition()
        if(token[0]==']'):
                token = lexical_analyzer()
        else:
            print('Error expected "]" at line: ',token[2])
            exit()
    else:
        expression()
        relational_oper()
        expression()

def expression():
    global token
    optional_sign()
    term()
    while(token[0] in '+-'):
        token = lexical_analyzer()
        term()

def term():
    global token
    factor()
    while(token[0] in '*/'):
        token = lexical_analyzer()
        factor()

def factor():
    global token
    if(token[0].isdigit()):
        token = lexical_analyzer()
    elif(token[0] == '('):
        token = lexical_analyzer()
        expression()
        if(token[0] == ')'):
            token = lexical_analyzer()
        else:
            print('Error expected ")" at line: ',token[2])
            exit()
    elif(token[0] in IDs):
        token = lexical_analyzer()
        idtail()
    else:
        print('Error , wrong factor type at line: ',token[2], 'with token:',token[0])
        exit()

def relational_oper():
    global token
    if(token[1] == 'LOGICAL'):
        token = lexical_analyzer()
    else:
        print("Error! Missing 'relational operator' in line ", token[2])
        exit()

def add_oper():
    global token
    if(token[1] == 'ADD_OP'):
        token = lexical_analyzer()

def mul_oper():
    global tokens
    if(token[1] == 'MUL_OP'):
        token = lexical_analyzer()

def optional_sign():
    global tokens
    add_oper()

token = lexical_analyzer()

startRule()