from enum import Enum

#Enumerated token class because python doesn't just have regular enums
#Access by name: Tokens.NAME.value
#Access by value: Tokens(VALUE).name
class Tokens(Enum):
    #Single character tokens
    #Enumerated based on their ASCII values
    PERIOD = ord('.')
    COMMA = ord(',')
    SEMICOLON = ord(';')
    LBRACK = ord('[')
    RBRACK = ord(']')
    LBRACE = ord('{')
    RBRACE = ord('}')
    LPAREN = ord('(')
    RPAREN = ord(')')
    AMPERSAND = ord('&')
    PIPE = ord('|')
    PLUS = ord('+')
    MINUS = ord('-')
    LESS = ord('<')
    GREATER = ord('>')
    MULTIPLY = ord('*')
    FSLASH = ord('/')
    BSLASH = ord('\\')
    APOSTRAPHE = ord('"')
    COLON = ord(":")

    #Multi character tokens
    #Arbitrarily enumerated
    PROGRAM = 300
    IS = 301
    BEGIN = 302
    END = 303
    GLOBAL = 304
    PROCEDURE = 305
    VARIABLE = 306
    TYPE = 307
    INTEGER = 308
    FLOAT = 309
    STRING = 310
    BOOL = 311
    ENUM = 312
    IF = 313
    THEN = 314
    ELSE = 315
    FOR = 316
    RETURN = 317
    NOT = 318
    TRUE = 319
    FALSE = 320
    ASSIGN = 321
    GRTEQUAL = 322
    LTEQUAL = 323
    EQUAL = 324
    NOTEQUAL = 325
    IDENTIFIER = 326
    BUILTIN = 327
    EOF = 328
    UNKNOWN = 329


class Token:
    def __init__(self):
        self.Type = -1
        self.Line_Num = -1
        self.Value = None
