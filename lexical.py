IDs = []
tokens = []
token = '' 
line = 1
counter = 0
keywords = {'πρόγραμμα','δήλωση', 'εάν', 'τότε', 'αλλιώς', 'εάν_τέλος','επανάλαβε','μέχρι','όσο','όσο_τέλος','για','έως','με_βήμα',' για_τέλος','διάβασε','γράψε','συνάρτηση','διαδικασία','διαπροσωπεία',' είσοδος','έξοδος','αρχή_συνάρτησης','τέλος_συνάρτησης',' αρχή_διαδικασίας','τέλος_διαδικασίαs',' αρχή_προγράμματος',' τέλος_προγράμματος',' ή','και','εκτέλεσε'}


#####################################
########  Lexical Analyzer  #########
#####################################

def lexical_analyzer():
    global line
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
                tokens.append((lexeme,'DECL_REF',line))
                state = 9

            #sygkrish oxi anathesh
            elif(c=='='):
                lexeme+=c
                tokens.append((lexeme,'LOGICAL',line))
                state = 9
           
            #prosthesh afairesh
            elif(c in "+-"):
                lexeme+=c
                tokens.append((lexeme,'ADD_OP',line))
                state = 9

            #pollaplasiasmos diairesh
            elif(c in "*/"):
                lexeme+=c
                tokens.append((lexeme,'MUL_OP',line))
                state = 9

            #grouping
            elif(c in '()[]"'):
                lexeme+=c
                tokens.append((lexeme,'GROUPING',line))
                state = 9

            #separator
            elif(c in ',;'):
                lexeme+=c
                tokens.append((lexeme,'SEPERATOR',line))
                state = 9
        
        elif(state == 1):
            
            if(c.isalpha() or c.isdigit() or c=='_'):
                lexeme+=c
                state = 1
            elif(c.isspace()):
                if(lexeme not in keywords):
                    if(lexeme not in IDs):
                        IDs.append(lexeme)
                    tokens.append((lexeme,'IDENTIFIER',line))
                elif(lexeme in keywords):
                    tokens.append((lexeme,'KEYWORD',line))
                if(c == '\n'):
                    line+=1
                state = 9
            
            else:
                if(lexeme not in keywords):
                    if(lexeme not in IDs):
                        IDs.append(lexeme)
                    tokens.append((lexeme,'IDENTIFIER',line))
                elif(lexeme in keywords):
                    tokens.append((lexeme,'KEYWORD',line))

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
                tokens.append((lexeme,'LITERAL_INT',line))
                if(c=='\n'):
                    line+=1
                state = 9

            else:
                num = int(lexeme)

                if(num < - (2**32)-1 or num > (2**32)-1):
                    print("Error! Number out of range in line "+str(line))
                    exit()
                tokens.append((lexeme,'LITERAL_INT',line))
                f.seek(backtrack)
                state = 9

        elif(state == 3):
            if(c == '='):
                lexeme+=c
                tokens.append((lexeme,'ASSIGNMENT',line))
                state = 9
            else:
                tokens.append((lexeme,'SEPERATOR',line))
                f.seek(f.tell()-1)
                state = 9

        elif(state == 4):
            if(c=='='):
                lexeme+=c
                tokens.append((lexeme,'LOGICAL',line))
                state = 9
            elif(c=='>'):
                lexeme+=c
                tokens.append((lexeme,'LOGICAL',line))
                state = 9
            elif(c.isspace()):
                tokens.append((lexeme,'LOGICAL',line))
                if(c=='\n'):
                    line+=1
                state = 9
            else:
                tokens.append((lexeme,'LOGICAL',line))
                f.seek(f.tell()-1)
                state = 9
        
        elif(state == 5):
            if(c=='='):
                lexeme+=c
                tokens.append((lexeme,'LOGICAL',line))
                state = 9
            elif(c=='<'):
                lexeme+=c
                tokens.append((lexeme,'LOGICAL',line))
                state = 9
            elif(c.isspace()):
                tokens.append((lexeme,'LOGICAL',line))
                if(c=='\n'):
                    line+=1
                state = 9
            else:
                tokens.append((lexeme,'LOGICAL',line))
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
    
    return lexeme

#####################################
########   Syntax Analyzer  #########
#####################################

def startRule():
    program()
    print('Syntax analysis succesful!')

def program():
    global tokens
    global counter
    if(tokens[counter][0] == 'πρόγραμμα'):
        counter+=1
        if(tokens[counter][0] in IDs):
            counter+=1
            programblock()
        else:
            print('Error incorrect ID name for program at line: ',tokens[counter][2])
            exit()
    else:
        print('Error program doesnt start with "πρόγραμμα" at line: ',tokens[counter][2])
        exit()

def programblock():
    global tokens
    global counter
    declarations()
    subprograms()
    if(tokens[counter][0] == 'αρχή_προγράμματος'):
        counter+=1
        sequence()
        if(tokens[counter][0] == 'τέλος_προγράμματος'):
            counter+=1
        else:
            print('Error programblock doesnt end with "τέλος_προγράμματος" at line: ',tokens[counter][2])
            exit()
    else:
        print('Error programblock doesnt start with "αρχή_προγράμματος" at line: ',tokens[counter][2])
        exit()
    
def declarations():
    global counter
    global tokens
    while(tokens[counter][0]=='δήλωση'):
        counter+=1
        varlist()

def varlist():
    global tokens
    global counter
    if(tokens[counter][0] in IDs):
        counter+=1
        while(tokens[counter][0] == ','):
            counter+=1
            if(tokens[counter][0] in IDs):
                counter+=1
            else:
                print('Invalid ID name at line: ',tokens[counter][2])
                exit()
    else:
        print('Invalid ID name at line: ',tokens[counter][2])
        exit()

def subprograms():
    global counter
    global tokens
    while(tokens[counter][0] == 'συνάρτηση' or tokens[counter][0] == 'διαδικασία'):
        if(tokens[counter][0] == 'συνάρτηση'):
            counter+=1
            func()
        elif(tokens[counter][0] == 'διαδικασία'):
            counter+=1
            proc()

def func():
    global counter
    global tokens
    if(tokens[counter][0] in IDs):
        counter+=1
        if(tokens[counter][0] == '('):
            counter+=1
            formalparlist()
            if(tokens[counter][0]==')'):
                counter+=1
                funcblock()
            else:
                print('Error, expected ")" at line: ', tokens[counter][2])
                exit()
        else:
            print('Error expected "(" at line: ',tokens[counter][2])
            exit()
    else:
        print('Error, not an ID at line: ',tokens[counter][2])
        exit()

def proc():
    global counter
    global tokens
    if(tokens[counter][0] in IDs):
        counter+=1
        if(tokens[counter][0] == '('):
            counter+=1
            formalparlist()
            if(tokens[counter][0]==')'):
                counter+=1
                procblock()
            else:
                print('Error, expected ")" at line: ', tokens[counter][2])
                exit()
        else:
            print('Error expected "(" at line: ',tokens[counter][2])
            exit()
    else:
        print('Error, not an ID at line: ',tokens[counter][2])
        exit()

def formalparlist():
    global tokens
    global counter
    if(tokens[counter][0]!=')'):
        varlist()

def funcblock():
    global tokens
    global counter
    if(tokens[counter][0]=='διαπροσωπεία'):
        counter+=1
        funcinput()
        funcoutput()
        declarations()
        if(tokens[counter][0]=='αρχή_συνάρτησης'):
            counter+=1
            sequence()
            if(tokens[counter][0]=='τέλος_συνάρτησης'):
                counter+=1
            else:
                print('Error, function not closed at line:', tokens[counter][2])
                exit()
        else:
            print('Error, function not opened at line:', tokens[counter][2])
            exit()
    else:
        print('Error, function not diaprosopeia at line:', tokens[counter][2])
        exit()

def procblock():
    global tokens
    global counter
    if(tokens[counter][0]=='διαπροσωπεία'):
        counter+=1
        funcinput()
        funcoutput()
        declarations()
        if(tokens[counter][0]=='αρχή_διαδικασίας'):
            counter+=1
            sequence()
            if(tokens[counter][0]=='τέλος_διαδικασίας'):
                counter+=1
            else:
                print('Error, proc not closed at line:', tokens[counter][2])
                exit()
        else:
            print('Error, proc not opened at line:', tokens[counter][2])
            exit()
    else:
        print('Error, proc not diaprosopeia at line:', tokens[counter][2])
        exit()

def funcinput():
    global tokens
    global counter
    if(tokens[counter][0]=='είσοδος'):
        counter+=1
        varlist()
    
def funcoutput():
    global tokens
    global counter
    if(tokens[counter][0]=='έξοδος'):
        counter+=1
        varlist()

def sequence():
    global tokens
    global counter
    statement()
    while(tokens[counter][0]==';'):
        counter+=1
        statement()

def statement():
    global counter
    global tokens
    if(tokens[counter][0] in IDs):
        counter+=1
        assignment_stat()
    elif(tokens[counter][0]=='εάν'):
        counter+=1
        if_stat()
    elif(tokens[counter][0]=='όσο'):
        counter+=1
        while_stat()
    elif(tokens[counter][0]=='επανάλαβε'):
        counter+=1
        do_stat()
    elif(tokens[counter][0]=='για'):
        counter+=1
        for_stat()
    elif(tokens[counter][0]=='διάβασε'):
        counter+=1
        input_stat()
    elif(tokens[counter][0]=='γράψε'):
        counter+=1
        print_stat()
    elif(tokens[counter][0]=='εκτέλεσε'):
        counter+=1
        call_stat()
    else:
        print('Error wrong statement at line: ',tokens[counter][2])
        exit()

def assignment_stat():
    global tokens
    global counter
    if(tokens[counter][0]==':='):
        counter+=1
        expression()
    else:
        print('Error expected ":=" at line: ',tokens[counter][2])
        exit()

def if_stat():
    global tokens
    global counter
    condition()
    if(tokens[counter][0]=='τότε'):
        counter+=1
        sequence()
        elsepart()
        if(tokens[counter][0]=='εάν_τέλος'):
            counter+=1
        else:
            print('Error if not closed properly at line: ',tokens[counter][2])
            exit()
    else:  
        print('Error expected "τότε" at line: ',tokens[counter][2])
        exit()

def elsepart():
    global tokens
    global counter
    if(tokens[counter][0]=='αλλιώς'):
        counter+=1
        sequence()

def while_stat():
    global tokens
    global counter
    condition()
    if(tokens[counter][0]=='επανάλαβε'):
        counter+=1
        sequence()
        if(tokens[counter][0]=='όσο_τέλος'):
            counter+=1
        else:
            print('Error expected "όσο_τέλος" at line: ',tokens[counter][2])
            exit()
    else:
        print('Error expected "επανάλαβε" at line: ',tokens[counter][2])
        exit()

def do_stat():
    global tokens
    global counter
    sequence()
    if(tokens[counter][0]=='μέχρι'):
        counter+=1
        condition()
    else:
        print('Error expected "μέχρι" at line: ',tokens[counter][2])
        exit()

def for_stat():
    global tokens
    global counter
    if(tokens[counter][0] in IDs):
        counter+=1
        if(tokens[counter][0]==':='):
            counter+=1
            expression()
            if(tokens[counter][0]=='έως'):
                counter+=1
                expression()
                step()
                if(tokens[counter][0]=='επανάλαβε'):
                    counter+=1
                    sequence()
                    if(tokens[counter][0]=='για_τέλος'):
                        counter+=1
                    else:
                        print('Error expected "για_τέλος" at line: ',tokens[counter][2])
                        exit()
                else:
                    print('Error expected "επανάλαβε" at line: ',tokens[counter][2])
                    exit()
            else:
                print('Error expected "έως" at line: ',tokens[counter][2])
                exit()
        else:
            print('Error expected ":=" at line: ',tokens[counter][2])
            exit()
    else:
        print('Error expected ID at line: ',tokens[counter][2])
        exit()

def step():
    global tokens
    global counter
    if(tokens[counter][0]=='με_βήμα'):
        counter+=1
        expression()

def print_stat():
    global tokens
    global counter
    expression()

def input_stat():
    global tokens
    global counter
    if(tokens[counter][0] in IDs):
        counter+=1
    else:
        print('Error expected ID at line: ',tokens[counter][2])
        exit()

def call_stat():
    global tokens
    global counter
    if(tokens[counter][0] in IDs):
        counter+=1
        idtail()
    else:
        print('Error expected ID at line: ',tokens[counter][2])
        exit()

def idtail():
    global tokens
    global counter
    if(tokens[counter][0] == '('):
        counter+=1
        actualpars()

def actualpars():
    global tokens
    global counter
    actualparlist()
    if(tokens[counter][0] == ')'):
        counter+=1
    else:
        print('Error expected ")" at line: ',tokens[counter][2])
        exit()

def actualparlist():
    global tokens
    global counter
    if(tokens[counter][0] != ')'):
        actualparitem()
        while(tokens[counter][0]==','):
            counter+=1
            actualparitem()

def actualparitem():
    global tokens
    global counter
    if(tokens[counter][0]=='%'):
        counter+=1
        if(tokens[counter][0] in IDs):
            counter+=1
        else:
            print('Error expected ID at line: ',tokens[counter][2])
            exit()
    else:
        expression()

def condition():
    global tokens
    global counter
    boolterm()
    while(tokens[counter][0]=='ή'):
        counter+=1
        boolterm()

def boolterm():
    global tokens
    global counter
    boolfactor()
    while(tokens[counter][0]=='και'):
        counter+=1
        boolfactor()

def boolfactor():
    global tokens
    global counter
    if(tokens[counter][0]=='όχι'):
        counter+=1
        if(tokens[counter][0]=='['):
            counter+=1
            condition()
            if(tokens[counter][0]==']'):
                counter+=1
            else:
                print('Error expected "]" at line: ',tokens[counter][2])
                exit()
        else:
            print('Error expected "[" at line: ',tokens[counter][2])
            exit()
    elif(tokens[counter][0]=='['):
        counter+=1
        condition()
        if(tokens[counter][0]==']'):
                counter+=1
        else:
            print('Error expected "]" at line: ',tokens[counter][2])
            exit()
    else:
        expression()
        relational_oper()
        expression()

def expression():
    global tokens
    global counter
    optional_sign()
    term()
    while(tokens[counter][0] in '+-'):
        counter+=1
        term()

def term():
    global tokens
    global counter
    factor()
    while(tokens[counter][0] in '*/'):
        counter+=1
        factor()

def factor():
    global tokens
    global counter
    if(tokens[counter][0].isdigit()):
        counter+=1
    elif(tokens[counter][0] == '('):
        counter+=1
        expression()
        if(tokens[counter][0] == ')'):
            counter+=1
        else:
            print('Error expected ")" at line: ',tokens[counter][2])
            exit()
    elif(tokens[counter][0] in IDs):
        counter+=1
        idtail()
    else:
        print('Error , wrong factor type at line: ',tokens[counter][2], 'with token:',tokens[counter][0])
        exit()

def relational_oper():
    global tokens
    global counter
    if(tokens[counter][1] == 'LOGICAL'):
        counter+=1
    else:
        print("Error! Missing 'relational operator' in line ", tokens[counter][2])
        exit()

def add_oper():
    global tokens
    global counter
    if(tokens[counter][1] == 'ADD_OP'):
        counter+=1

def mul_oper():
    global tokens
    global counter
    if(tokens[counter][1] == 'MUL_OP'):
        counter+=1

def optional_sign():
    global tokens
    global counter
    add_oper()





f = open('test.greek', 'r', encoding='utf-8')


while(token!='τέλος_προγράμματος'):
    token = lexical_analyzer()

startRule()