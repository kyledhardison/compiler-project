from Definitions import Tokens
from Definitions import Token
from Errors import ErrorHandler
from Scanner import Scanner
import copy

#Each function represents a non-terminal from the project documents.
#This logic can be used to construct the AST

class Parser:
    #Constructor
    def __init__(self, scanner):
        self.e = ErrorHandler()
        self.s = scanner
        self.Do_Code_Gen = True #Whether or not to continue with code gen
        self.Token_Accepted = True
        
        #debug variables
        self.Scanner_Debug = False
        self.Parser_Debug = False

        self.token = Token()
        self.Previous_Token = Token()

    def Next_Token(self):
        if(self.Token_Accepted):
            self.token = self.s.Get_Next_Token()
            self.Token_Accepted = False

            #debug statements for the scanner, prints every token passed to the parser
            if(self.Scanner_Debug):
                print("Token: ", end='')
                print(Tokens(self.token.Type).name, end = '')
                print(" Line: ", end='')
                print(self.token.Line_Num, end='')
                print(" Value: ", end='')
                print(self.token.Value)

    def Accept_Token(self):
        self.Token_Accepted = True


    #Root Node, call to begin parse
    def Parse(self):
        self.program_header()

        self.program_body()

        #Period should end program
        self.Next_Token()
        if(self.token.Type != Tokens.PERIOD.value):
            self.e.Warning_Tokenless("End of file: '.' Expected.")
            #self.Do_Code_Gen = False


    def program_header(self):
        if(self.Parser_Debug): #Debug Statement
            print("<program-header>")
        #Confirm first 3 tokens are correct, header should always be the same
        self.Next_Token()
        if(self.token.Type != Tokens.PROGRAM.value):
            self.e.Error_Expected(self.token, "program")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.IDENTIFIER.value):
            self.e.Error_Expected(self.token,"identifier")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.IS.value):
            self.e.Error_Expected(self.token,"is")
            self.Do_Code_Gen = False
        self.Accept_Token()


    def program_body(self):
        if(self.Parser_Debug): #Debug Statement
            print("<program-body>")
        self.Next_Token()
        while(self.token.Type != Tokens.BEGIN.value): #Declarations before BEGIN
            self.declaration()

            self.Next_Token()
            if(self.token.Type != Tokens.SEMICOLON.value):
                self.e.Error_Expected(self.token,";")
                self.Do_Code_Gen = False
            self.Accept_Token()
            self.Next_Token()
        self.Accept_Token()

        while(self.token.Type != Tokens.END.value): #Statements between BEGIN and END
            self.statement()

            self.Next_Token()
            if(self.token.Type != Tokens.SEMICOLON.value):
                self.e.Error_Expected(self.token,";")
                self.Do_Code_Gen = False
            self.Accept_Token()
            self.Next_Token()
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.PROGRAM.value): #PROGRAM should follow END
            self.e.Error_Expected(self.token, "program")
            self.Do_Code_Gen = False
        self.Accept_Token()


    def declaration(self):
        if(self.Parser_Debug): #Debug Statement
            print("<declaration>")
        self.Next_Token()
        if(self.token.Type == Tokens.GLOBAL.value):#GLOBAL 
            self.Accept_Token()

        self.Next_Token()
        if(self.token.Type == Tokens.PROCEDURE.value): #PROCEDURE
            self.procedure_declaration()
        elif(self.token.Type == Tokens.VARIABLE.value): #VARIABLE
            self.variable_declaration()
        elif(self.token.Type == Tokens.TYPE.value): #TYPE
            self.type_declaration()
        else:
            self.e.Error_Expected(self.token, "global, procedure, variable, or type")
            self.Do_Code_Gen = False
            self.Accept_Token()


    def procedure_declaration(self):
        if(self.Parser_Debug): #Debug Statement
            print("<procedure-declaration>")
        self.procedure_header()
        self.procedure_body()


    def procedure_header(self):
        if(self.Parser_Debug): #Debug Statement
            print("<procedure-header>")
        if(self.token.Type != Tokens.PROCEDURE.value): #PROCEDURE
            self.e.Error_Expected(self.token, "procedure")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.IDENTIFIER.value): #IDENTIFIER
            self.e.Error_Expected(self.token, "procedure")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.COLON.value): # :
            self.e.Error_Expected(self.token, ":")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.type_mark()

        self.Next_Token()
        if(self.token.Type != Tokens.LPAREN.value): # (
            self.e.Error_Expected(self.token, "(")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.RPAREN.value):
            self.parameter_list()

        self.Next_Token()
        if(self.token.Type != Tokens.RPAREN.value): # )
            self.e.Error_Expected(self.token, ")")
            self.Do_Code_Gen = False
        self.Accept_Token()


    def parameter_list(self):
        if(self.Parser_Debug): #Debug Statement
            print("<parameter-list>")
        self.parameter()

        self.Next_Token()
        if(self.token.Type == Tokens.COMMA.value): # ,
            self.Accept_Token()
            self.parameter_list()


    def parameter(self):
        if(self.Parser_Debug): #Debug Statement
            print("<parameter>")
        self.variable_declaration()
    

    def procedure_body(self):
        if(self.Parser_Debug): #Debug Statement
            print("<procedure-body>")
        self.Next_Token()
        while(self.token.Type != Tokens.BEGIN.value): #Declarations come before BEGIN
            self.declaration()
            self.Next_Token()
            if(self.token.Type != Tokens.SEMICOLON.value):
                self.e.Error_Expected(self.token,";")
                self.Do_Code_Gen = False
            self.Accept_Token()
            self.Next_Token()
        self.Accept_Token()

        self.Next_Token()
        while(self.token.Type != Tokens.END.value): #Statements come between BEGIN and END
            self.statement()
            self.Next_Token() #Might break everything
            if(self.token.Type != Tokens.SEMICOLON.value):
                self.e.Error_Expected(self.token,";")
                self.Do_Code_Gen = False
            self.Accept_Token()
            self.Next_Token()
        self.Accept_Token()
        
        self.Next_Token()
        if(self.token.Type != Tokens.PROCEDURE.value):
            self.e.Error_Expected(self.token,"procedure")
            self.Do_Code_Gen = False
        self.Accept_Token()


    
    def variable_declaration(self):
        if(self.Parser_Debug): #Debug Statement
            print("<variable-declaration>")
        self.Next_Token()
        if(self.token.Type != Tokens.VARIABLE.value):
            self.e.Error_Expected(self.token,"variable")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.IDENTIFIER.value):
            self.e.Error_Expected(self.token,"identifier")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.COLON.value):
            self.e.Error_Expected(self.token,":")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.type_mark()

        self.Next_Token()
        if(self.token.Type == Tokens.LBRACK.value): # [
            self.Accept_Token()

            self.bound()

            self.Next_Token()
            if(self.token.Type != Tokens.RBRACK.value): # ]
                self.e.Error_Expected(self.token,"]")
                self.Do_Code_Gen = False
            self.Accept_Token()


    def type_declaration(self):
        if(self.Parser_Debug): #Debug Statement
            print("<type-declaration>")
        self.Next_Token()
        if(self.token.Type != Tokens.TYPE.value):
            self.e.Error_Expected(self.token,"type")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.IDENTIFIER.value):
            self.e.Error_Expected(self.token,"identifier")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.IS.value):
            self.e.Error_Expected(self.token,"is")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.type_mark()


    def type_mark(self):
        if(self.Parser_Debug): #Debug Statement
            print("<type-mark>")
        self.Next_Token()
        if(self.token.Type != Tokens.INTEGER.value and self.token.Type != Tokens.FLOAT.value and self.token.Type != Tokens.STRING.value and\
            self.token.Type != Tokens.BOOL.value and self.token.Type != Tokens.IDENTIFIER.value and self.token.Type != Tokens.ENUM.value):
            self.e.Error_Expected(self.token,"integer, float, string, bool, identifier, or enum")
            self.Do_Code_Gen = False
        self.Accept_Token()

        if(self.token.Type == Tokens.ENUM.value): #ENUM
            self.Next_Token()
            if(self.token.Type != Tokens.LBRACE.value): # {
                self.e.Error_Expected(self.token,"{")
                self.Do_Code_Gen = False
            self.Accept_Token()

            self.Next_Token()
            if(self.token.Type != Tokens.IDENTIFIER.value): # IDENTIFIER
                self.e.Error_Expected(self.token,"identifier")
                self.Do_Code_Gen = False
            self.Accept_Token()

            self.Next_Token()
            if(self.token.Type == Tokens.COMMA.value): # ,
                while(self.token.Type != Tokens.RBRACE.value): #TODO: Possible case where unclosed brackets cause infinite loop
                    self.Next_Token()
                    if(self.token.Type != Tokens.COMMA.value): # COMMA
                        self.e.Error_Expected(self.token,",")
                        self.Do_Code_Gen = False
                    self.Accept_Token

                    self.Next_Token()
                    if(self.token.Type != Tokens.IDENTIFIER.value): # IDENTIFIER
                        self.e.Error_Expected(self.token,"identifier")
                        self.Do_Code_Gen = False
                    self.Accept_Token()

            self.Next_Token()
            if(self.token.Type != Tokens.RBRACE.value): # }
                self.e.Error_Expected(self.token,"}")
                self.Do_Code_Gen = False
            self.Accept_Token()
            

    def bound(self):
        if(self.Parser_Debug): #Debug Statement
            print("<bound>")
        self.number()


    def statement(self):
        if(self.Parser_Debug): #Debug Statement
            print("<statement>")
        self.Next_Token()

        if(self.token.Type == Tokens.IDENTIFIER.value):
            #self.Previous_Token = copy.deepcopy(self.token)
            #self.Accept_Token()

            #self.Next_Token()
            #if(self.token.Type == Tokens.ASSIGN.value):
            self.assignment_statement()
            #else:
            #    self.e.Error_Expected(self.token,":=")
            #    self.Do_Code_Gen = False

        elif(self.token.Type == Tokens.IF.value):
            self.if_statement()

        elif(self.token.Type == Tokens.FOR.value):
            self.loop_statement()

        elif(self.token.Type == Tokens.RETURN.value):
            self.return_statement()

        else:
            self.e.Error_Expected(self.token,"assignment, if, for, or return")
            self.Do_Code_Gen = False
            
    
    def procedure_call(self, Last_Token = None):
        if(self.Parser_Debug): #Debug Statement
            print("<procedure-call>")
        if(Last_Token):
            if(Last_Token.Type != Tokens.IDENTIFIER.value): # IDENTIFIER
                self.e.Error_Expected(Last_Token,"identifier")
                self.Do_Code_Gen = False
            #self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.LPAREN.value): # (
            self.e.Error_Expected(self.token,"(")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.RPAREN.value):
            self.argument_list()

        self.Next_Token()
        if(self.token.Type != Tokens.RPAREN.value): # (
            self.e.Error_Expected(self.token,")")
            self.Do_Code_Gen = False
        self.Accept_Token()
    

    def assignment_statement(self):
        if(self.Parser_Debug): #Debug Statement
            print("<assignment-statement>")
        self.destination()

        self.Next_Token()
        if(self.token.Type != Tokens.ASSIGN.value): # :=
            self.e.Error_Expected(self.token,":=")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.expression()
        

    def destination(self):
        if(self.Parser_Debug): #Debug Statement
            print("<destination>")
        self.Next_Token()
        if(self.token.Type != Tokens.IDENTIFIER.value): # IDENTIFIER
            self.e.Error_Expected(self.token,"identifier")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type == Tokens.LBRACK.value): #[
            self.Accept_Token()
            self.expression()

            self.Next_Token()
            if(self.token.Type != Tokens.RBRACK.value): # ]
                self.e.Error_Expected(self.token,"]")
                self.Do_Code_Gen = False
            self.Accept_Token()


    def if_statement(self):
        if(self.Parser_Debug): #Debug Statement
            print("<if-statement>")
        self.Next_Token()
        if(self.token.Type != Tokens.IF.value): # IF
            self.e.Error_Expected(self.token,"if")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.LPAREN.value): # (
            self.e.Error_Expected(self.token,"(")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.expression()

        self.Next_Token()
        if(self.token.Type != Tokens.RPAREN.value): # )
            self.e.Error_Expected(self.token,")")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.THEN.value): # THEN
            self.e.Error_Expected(self.token,"then")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type == Tokens.ELSE.value or self.token.Type == Tokens.ELSE.END): # not ELSE or END
            self.e.Error_Expected(self.token,"statement")
            self.Do_Code_Gen = False
        
        else:
            while(self.token.Type != Tokens.ELSE.value and self.token.Type != Tokens.END.value):
                self.statement()

                self.Next_Token()
                if(self.token.Type != Tokens.SEMICOLON.value): # ;
                    self.e.Error_Expected(self.token,";")
                    self.Do_Code_Gen = False
                self.Accept_Token()
                self.Next_Token()
            self.Accept_Token()
        
        #self.Next_Token()
        if(self.token.Type == Tokens.ELSE.value): # ELSE
            self.Accept_Token()

            self.Next_Token()
            if(self.token.Type == Tokens.END.value): # not END
                self.e.Error_Expected(self.token,"statement")
                self.Do_Code_Gen = False
            else:
                while(self.token.Type != Tokens.END.value):
                    self.statement()

                    self.Next_Token()
                    if(self.token.Type != Tokens.SEMICOLON.value): # ;
                        self.e.Error_Expected(self.token,";")
                        self.Do_Code_Gen = False
                    self.Accept_Token()
                    self.Next_Token()
                self.Accept_Token()
        
        #self.Next_Token()
        if(self.token.Type != Tokens.END.value): # END
            self.e.Error_Expected(self.token,"end")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.IF.value): # IF
            self.e.Error_Expected(self.token,"if")
            self.Do_Code_Gen = False
        self.Accept_Token()


    def loop_statement(self):
        if(self.Parser_Debug): #Debug Statement
            print("<loop-statement>")
        self.Next_Token()
        if(self.token.Type != Tokens.FOR.value): # FOR
            self.e.Error_Expected(self.token,"for")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.LPAREN.value): # (
            self.e.Error_Expected(self.token,"(")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.assignment_statement()

        self.Next_Token()
        if(self.token.Type != Tokens.SEMICOLON.value): # ;
            self.e.Error_Expected(self.token,";")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.expression()

        self.Next_Token()
        if(self.token.Type != Tokens.RPAREN.value): # )
            self.e.Error_Expected(self.token,")")
            self.Do_Code_Gen = False
        self.Accept_Token()

        if(self.token.Type == Tokens.END.value):
            self.e.Error_Expected(self.token,"statement")
            self.Do_Code_Gen = False
        else:
            while(self.token.Type != Tokens.END.value):
                self.statement()

                self.Next_Token()
                if(self.token.Type != Tokens.SEMICOLON.value): # ;
                    self.e.Error_Expected(self.token,";")
                    self.Do_Code_Gen = False
                self.Accept_Token()
                self.Next_Token()
            #self.Accept_Token()
        
        self.Next_Token()
        if(self.token.Type != Tokens.END.value): # END
            self.e.Error_Expected(self.token,"end")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.Next_Token()
        if(self.token.Type != Tokens.FOR.value): # FOR
            self.e.Error_Expected(self.token,"for")
            self.Do_Code_Gen = False
        self.Accept_Token()


    def return_statement(self):
        if(self.Parser_Debug): #Debug Statement
            print("<return-statement>")
        self.Next_Token()
        if(self.token.Type != Tokens.RETURN.value): # RETURN
            self.e.Error_Expected(self.token,"return")
            self.Do_Code_Gen = False
        self.Accept_Token()

        self.expression()


    #Probably not needed, since identifier is already an enumerated type
    #def identifier(self):
    #    pass


    def expression(self):
        if(self.Parser_Debug): #Debug Statement
            print("<expression>")
        self.ArithOp()
        self.expression_prime()


    #'Prime' function to alter grammar and avoid left recursion
    def expression_prime(self):
        if(self.Parser_Debug): #Debug Statement
            print("<expression-prime>")
        self.Next_Token()
        if(self.token.Type == Tokens.AMPERSAND.value or self.token.Type == Tokens.PIPE.value): # & or |
            self.Accept_Token()

            self.Next_Token()
            if(self.token.Type == Tokens.NOT.value): # NOT
                self.Accept_Token()
            
            self.ArithOp()
            self.expression_prime()


    def ArithOp(self):
        if(self.Parser_Debug): #Debug Statement
            print("<ArithOp>")
        self.relation()
        self.ArithOp_prime()


    #'Prime' function to alter grammar and avoid left recursion
    def ArithOp_prime(self):
        if(self.Parser_Debug): #Debug Statement
            print("<ArithOp-prime>")
        self.Next_Token()
        if(self.token.Type == Tokens.PLUS.value or self.token.Type == Tokens.MINUS.value): # + or -
            self.Accept_Token()

            self.relation()
            self.ArithOp_prime()


    def relation(self):
        if(self.Parser_Debug): #Debug Statement
            print("<relation>")
        self.term()
        self.relation_prime()


    #'Prime' function to alter grammar and avoid left recursion
    def relation_prime(self):
        if(self.Parser_Debug): #Debug Statement
            print("<relation-prime>")
        self.Next_Token() 
        if(self.token.Type == Tokens.LESS.value or self.token.Type == Tokens.GRTEQUAL.value or self.token.Type == Tokens.LTEQUAL.value \
            or self.token.Type == Tokens.GREATER.value or self.token.Type == Tokens.EQUAL.value or self.token.Type == Tokens.NOTEQUAL.value): # < >= <= > == !=
                self.Accept_Token()

                self.term()
                self.relation_prime()


    def term(self):
        if(self.Parser_Debug): #Debug Statement
            print("<term>")
        self.factor()
        self.term_prime()


    #'Prime' function to alter grammar and avoid left recursion
    def term_prime(self):
        if(self.Parser_Debug): #Debug Statement
            print("<term-prime>")
        self.Next_Token()
        if(self.token.Type == Tokens.MULTIPLY.value or self.token.Type == Tokens.FSLASH.value): # * /
            self.Accept_Token()

            self.factor()
            self.term_prime()


    def factor(self):
        if(self.Parser_Debug): #Debug Statement
            print("<factor>")
        self.Next_Token()
        if(self.token.Type == Tokens.LPAREN.value): # (
            self.Accept_Token()
            self.expression()

            self.Next_Token()
            if(self.token.Type != Tokens.RPAREN.value): # )
                self.e.Error_Expected(self.token,")")
                self.Do_Code_Gen = False
            self.Accept_Token()

        elif(self.token.Type == Tokens.MINUS.value): # -
            self.Accept_Token()

            self.Next_Token()
            if(self.token.Type == Tokens.IDENTIFIER.value): # - IDENTIFIER
                self.name()
            elif(self.token.Type == Tokens.INTEGER.value or self.token.Type == Tokens.FLOAT.value): # - INTEGER or FLOAT
                self.number()
            else:
                self.e.Error_Expected(self.token,"identifier, integer, or float")
                self.Do_Code_Gen = False
                self.Accept_Token()

        elif(self.token.Type == Tokens.IDENTIFIER.value): # IDENTIFIER
                self.Accept_Token()
                Last_Token = copy.deepcopy(self.token)
                #Placeholder code
                self.Next_Token()
                if(self.token.Type == Tokens.LPAREN.value): #Procedure call
                    self.procedure_call(Last_Token)
                else:
                    self.name(Last_Token)

                #self.name() => id then maybe [ ]
                #self.procedure_call => id then definitely ()
                #TODO: Need to reference symbol table to tell if identifier is name or procedure
                #might not need this, I think I worked it out

        elif(self.token.Type == Tokens.INTEGER.value or self.token.Type == Tokens.FLOAT.value): #INTEGER or FLOAT
                self.number()

        elif(self.token.Type == Tokens.STRING.value): # STRING
                self.string()

        elif(self.token.Type == Tokens.TRUE.value): # TRUE
                self.Accept_Token()

        elif(self.token.Type == Tokens.FALSE.value): # FALSE
                self.Accept_Token()

        elif(self.token.Type == Tokens.BUILTIN.value): #BUILTIN functions
            #TODO: Make sure this is the right way to handle this
            self.Accept_Token()
            self.procedure_call()

        
        else:
            self.e.Error_Expected(self.token,"factor")
            self.Accept_Token()


    def name(self, Last_Token = None):
        if(self.Parser_Debug): #Debug Statement
            print("<name>")
        if(Last_Token):
            if(Last_Token.Type != Tokens.IDENTIFIER.value): # IDENTIFIER
                self.e.Error_Expected(Last_Token,"identifier")
                self.Do_Code_Gen = False

        
        self.Next_Token()
        if(self.token.Type == Tokens.LBRACK.value): # [
            self.Accept_Token()

            self.expression()

            self.Next_Token()
            if(self.token.Type != Tokens.RBRACK.value): # ]
                self.e.Error_Expected(self.token,"]")
                self.Do_Code_Gen = False
            self.Accept_Token()


    def argument_list(self):
        if(self.Parser_Debug): #Debug Statement
            print("<argument-list>")
        self.expression()

        self.Next_Token()
        if(self.token.Type == Tokens.COMMA.value):
            self.Accept_Token()
            self.argument_list()


    def number(self): 
        if(self.Parser_Debug): #Debug Statement
            print("<number>")
        self.Next_Token()
        if(self.token.Type != Tokens.INTEGER.value and self.token.Type != Tokens.FLOAT.value): # INTEGER and FLOAT
            self.e.Error_Expected(self.token,"integer or float")
            self.Do_Code_Gen = False
        self.Accept_Token()


    def string(self):
        if(self.Parser_Debug): #Debug Statement
            print("<string>")
        self.Next_Token()
        if(self.token.Type != Tokens.STRING.value): # STRING
            self.e.Error_Expected(self.token,"string")
            self.Do_Code_Gen = False
        self.Accept_Token()

    