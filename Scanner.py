from pathlib import Path
from Definitions import Tokens
from Definitions import Token
from Errors import ErrorHandler

class Scanner:
    #Constructor
    def __init__(self, fileName):
        self.Errors = False
        self.Line_Num = 1
        self.e = ErrorHandler()

        #Open file in what SHOULD be an OS-neutral way
        folder = Path("./")
        self.Source_File = folder / fileName
        self.f = open(self.Source_File)

        self.Reserved_Dict = {}

        Reserved_Words = ["PROGRAM", "IS", "BEGIN", "END", "GLOBAL", "PROCEDURE", "VARIABLE",\
            "TYPE", "INTEGER", "FLOAT", "STRING", "BOOL", "ENUM", "IF", "THEN", "ELSE", "FOR",\
                "RETURN", "NOT", "TRUE", "FALSE"]

        #Seeding reserved words table
        for w in Reserved_Words:
            self.Reserved_Dict[w] = Tokens[w].value

        #Seeding built in functions
        self.Reserved_Dict["GETBOOL"] = Tokens.BUILTIN.value
        self.Reserved_Dict["GETINTEGER"] = Tokens.BUILTIN.value
        self.Reserved_Dict["GETFLOAT"] = Tokens.BUILTIN.value
        self.Reserved_Dict["GETSTRING"] = Tokens.BUILTIN.value
        self.Reserved_Dict["PUTBOOL"] = Tokens.BUILTIN.value
        self.Reserved_Dict["PUTINTEGER"] = Tokens.BUILTIN.value
        self.Reserved_Dict["PUTFLOAT"] = Tokens.BUILTIN.value
        self.Reserved_Dict["PUTSTRING"] = Tokens.BUILTIN.value
        self.Reserved_Dict["SQRT"] = Tokens.BUILTIN.value


    #Deconstructor
    def __del__(self):
        self.f.close()
    


    #Check if character is alphabetic
    def is_alpha(self, char):
        return char.isalpha()
        
    def is_digit(self, char):
        return char.isdigit()

    #Check if character is to be ignored
    def is_space(self, char):
        return ord(char) == '9' or char == ' ' or char =='\n' or char == '' or char == '\t'
    def is_period(self, char):
        return char == '.'
    def is_comma(self, char):
        return char == ','
    def is_semicolon(self, char):
        return char == ';'
    def is_lbracket(self, char):
        return char == '['
    def is_rbracket(self, char):
        return char == ']'
    def is_leftbrace(self, char):
        return char == '{'
    def is_rightbrace(self, char):
        return char == '}'
    def is_lparen(self, char):
        return char == '('
    def is_rparen(self, char):
        return char == ')'
    def is_colon(self, char):
        return char == ':'
    def is_equals(self, char):
        return char == '='
    def is_amp(self, char):
        return char == '&'
    def is_pipe(self, char):
        return char == '|'
    def is_plus(self, char):
        return char == '+'
    def is_minus(self, char):
        return char == '-' 
    def is_langle(self, char):
        return char == '<'
    def is_rangle(self, char):
        return char == '>'
    def is_exclamation(self, char):
        return char == '!'
    def is_star(self, char):
        return char == '*'
    def is_fslash(self, char):
        return char == '/'
    def is_bslash(self, char):
        return char == '\\'
    def is_newline(self, char):
        return char == '\n'
    def is_apostraphe(self, char):
        return char == '"'
    def is_underscore(self, char):
        return char == '_'

    #Skips spaces and comments
    def Skip_Spaces(self):
        #Skipping spaces 
        if(not self.c):
            return
        
        while(self.is_space(self.c) or self.is_fslash(self.c)):
            #Iterate line number if newline is found
            if(self.is_newline(self.c)):
                self.Line_Num += 1
            
            #If forward slash, check if it's a single or block comment
            if(self.is_fslash(self.c)):
                pos = self.f.tell()
                self.c = self.f.read(1)

                #If // (single line comment), jump to the end of the line
                if(self.is_fslash(self.c)):
                    while True:
                        self.c = self.f.read(1)
                        if(self.is_newline(self.c)):
                            break
                        if(not self.c):
                            return
                
                #If /* (multiline comment): skip to */ (end), including any nested comments
                elif(self.is_star(self.c)):
                    comments = 1
                    self.c = self.f.read(1)
                    while(comments > 0):

                        if(self.is_fslash(self.c)):
                            self.c = self.f.read(1)
                            if(self.is_star(self.c)): #Extra nested multiline
                                comments +=1
                            elif(self.is_newline(self.c)):
                                self.Line_Num += 1

                        elif(self.is_star(self.c)):
                            self.c = self.f.read(1)
                            if(self.is_fslash(self.c)): #Terminated line
                                comments -= 1
                            elif(self.is_newline(self.c)):
                                self.Line_Num += 1

                        elif(self.is_newline(self.c)):
                            self.Line_Num += 1
                        self.c = self.f.read(1)
                else:
                    self.f.seek(pos-1)
                    self.c = self.f.read(1)
                    break
            else:
                self.c = self.f.read(1)

            if(not self.c):
                return


    def Get_Next_Token(self):
        self.c = ''
        token = Token()
        self.c = self.f.read(1)

        self.Skip_Spaces()

        if(not self.c):
            token.Type = Tokens.EOF.value
            return token

        token.Line_Num = int(self.Line_Num)
        

        if(self.is_fslash(self.c)): # /
            token.Type = Tokens.FSLASH.value
            return token
        

        elif(self.is_colon(self.c)):
            pos = self.f.tell()
            self.c = self.f.read(1)
            if(self.is_equals(self.c)): # :=
                token.Type = Tokens.ASSIGN.value
            else: # :
                token.Type = Tokens.COLON.value
                self.f.seek(pos-1)
                self.c = self.f.read(1)
            return token


        elif(self.is_apostraphe(self.c)): # STRING
            token.Type = Tokens.STRING.value
            buffer = ''
            self.c = self.f.read(1)
            while(self.c != '"'):
                buffer = buffer + self.c
                self.c = self.f.read(1)
                
                if(not self.c):
                    self.Errors = True
                    self.e.Error(token, "Unterminated string") 
                    token.Type = Tokens.UNKNOWN.value
                    break

            pos = self.f.tell()
            self.f.seek(pos-1)
            self.c = self.f.read(1)
            
            token.Value = str(buffer)
            return token


        elif(self.is_equals(self.c)):
            pos = self.f.tell()
            self.c = self.f.read(1)

            if(self.is_equals(self.c)): # ==
                token.Type = Tokens.EQUAL.value
            else:
                token.Type = Tokens.UNKNOWN.value
                self.f.seek(pos-1)
                self.c = self.f.read(1)
            return token


        elif(self.is_exclamation(self.c)):
            pos = self.f.tell()
            self.c = self.f.read(1)

            if(self.is_equals(self.c)): # !=
                token.Type = Tokens.NOTEQUAL.value
            else:
                token.Type = Tokens.UNKNOWN.value
                self.f.seek(pos-1)
                self.c = self.f.read(1)
            return token


        elif(self.is_langle(self.c)):
            pos = self.f.tell()
            self.c = self.f.read(1)
            if(self.is_equals(self.c)): # <=
                token.Type = Tokens.LTEQUAL.value
            else: # <
                token.Type = Tokens.LESS.value
                self.f.seek(pos-1)
                self.c = self.f.read(1)
            return token


        elif(self.is_rangle(self.c)):
            pos = self.f.tell()
            self.c = self.f.read(1)
            if(self.is_equals(self.c)): # >=
                token.Type = Tokens.GRTEQUAL.value
            else: # >
                token.Type = Tokens.GREATER.value
                self.f.seek(pos-1)
                self.c = self.f.read(1)
            return token


        #All other single character tokens
        elif(self.is_period(self.c) or self.is_comma(self.c) or self.is_semicolon(self.c) or \
            self.is_lparen(self.c) or self.is_rparen(self.c) or self.is_plus(self.c) or \
                self.is_minus(self.c) or self.is_amp(self.c) or self.is_pipe(self.c) or\
                    self.is_lbracket(self.c) or self.is_rbracket(self.c) or \
                        self.is_leftbrace(self.c) or self.is_rightbrace(self.c)):
                        token.Type = ord(self.c)
                        return token
        

        #INT or FLOAT
        elif(self.is_digit(self.c)):
            buffer = ''
            while(self.is_digit(self.c)):
                buffer = buffer + self.c
                self.c = self.f.read(1)

            if(self.is_period(self.c)): # FLOAT
                token.Type = Tokens.FLOAT.value
                buffer += self.c
                self.c = self.f.read(1)
                while(self.is_digit(self.c)):
                    buffer = buffer + self.c
                    self.c = self.f.read(1)

                token.Value = float(buffer)

            else:
                token.Type = Tokens.INTEGER.value
                token.Value = int(buffer)
            
            pos = self.f.tell()
            if(self.c):
                self.f.seek(pos-1)
            return token

        
        #Anything else, either unknown, an identifier, or a reserved word
        else:
            token.Type = Tokens.UNKNOWN.value

            if(not self.is_alpha(self.c)):
                #TODO: Probably an error here for an illegal character
                self.e.Error(token, "Illegal character") 
                self.Errors = True
                
                return token

            buffer = ''

            while (self.is_alpha(self.c) or self.is_digit(self.c) or self.is_underscore(self.c)):
                buffer = buffer + self.c
                self.c = self.f.read(1)
            
            pos = self.f.tell()
            if(self.c):
                self.f.seek(pos-1)
            
            buffer = buffer.upper()
            token.Type = Tokens.IDENTIFIER.value
            token.Value = str(buffer)

            if(token.Value in self.Reserved_Dict):
                token.Type = self.Reserved_Dict[token.Value]

            return token